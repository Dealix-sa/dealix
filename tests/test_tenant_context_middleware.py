"""Tenant resolution must actually run, and must not silently claim to isolate.

``resolve_tenant_context`` and ``assert_tenant_match`` were written, tested in
isolation, and never wired in. ``request.state.tenant_context`` was therefore
never populated, so every per-object guard that reads it had nothing to compare
against. Separately, ``db/rls_policies.py`` defines row-level security for 30+
tables and ``apply_rls()`` has zero callers.

That combination is worse than having neither: the code reads as though tenant
isolation exists. This wires the resolver in, and pins the parts that are still
*not* enforced so the gap stays visible instead of being assumed closed.

Enforcement defaults to shadow. The resolver has never run against real traffic;
turning it straight to enforce would risk 403-ing valid requests whose tenant
cannot yet be derived. Shadow mode generates the evidence to make that call.
"""

from __future__ import annotations

import pytest
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from httpx import ASGITransport, AsyncClient

from api.middleware.tenant_isolation import (
    ENFORCE,
    OFF,
    SHADOW,
    TenantContextMiddleware,
    get_enforcement_mode,
)


def _app(mode: str | None = None) -> FastAPI:
    app = FastAPI()
    app.add_middleware(TenantContextMiddleware, mode=mode)

    @app.get("/probe")
    async def probe(request: Request) -> JSONResponse:
        context = getattr(request.state, "tenant_context", None)
        return JSONResponse(
            {
                "tenant_id": getattr(request.state, "tenant_id", None),
                "source": context.source if context else None,
            }
        )

    return app


async def _get(app: FastAPI, headers: dict[str, str] | None = None):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        return await client.get("/probe", headers=headers or {})


# ── Mode resolution ─────────────────────────────────────────────────────────


def test_default_mode_is_shadow():
    """Not 'enforce' — the resolver is unproven against real traffic."""
    assert get_enforcement_mode({}) == SHADOW


@pytest.mark.parametrize(
    ("value", "expected"),
    [("shadow", SHADOW), ("enforce", ENFORCE), ("off", OFF), ("ENFORCE", ENFORCE)],
)
def test_mode_is_read_from_environment(value, expected):
    assert get_enforcement_mode({"TENANT_ENFORCEMENT": value}) == expected


def test_unrecognised_mode_falls_back_to_shadow():
    """An unknown value must not accidentally mean 'off' or 'enforce'."""
    assert get_enforcement_mode({"TENANT_ENFORCEMENT": "yes-please"}) == SHADOW


# ── Shadow mode: observe, never alter ───────────────────────────────────────


@pytest.mark.asyncio
async def test_shadow_mode_allows_a_request_with_no_resolvable_tenant():
    response = await _get(_app(mode=SHADOW))

    assert response.status_code == 200
    assert response.json()["tenant_id"] is None


@pytest.mark.asyncio
async def test_shadow_mode_resolves_and_records_a_tenant_header():
    response = await _get(_app(mode=SHADOW), {"X-Tenant-ID": "acme"})

    assert response.status_code == 200
    body = response.json()
    assert body["tenant_id"] == "acme"
    assert body["source"] == "header"


@pytest.mark.asyncio
async def test_shadow_mode_resolves_a_tenant_from_an_api_key_prefix():
    response = await _get(_app(mode=SHADOW), {"X-API-Key": "apikey_acme_secret123"})

    assert response.json()["tenant_id"] == "acme"


# ── Enforce mode: the opt-in behaviour ──────────────────────────────────────


@pytest.mark.asyncio
async def test_enforce_mode_rejects_an_unresolvable_tenant():
    response = await _get(_app(mode=ENFORCE))

    assert response.status_code == 403
    assert response.json()["detail"] == "tenant_could_not_be_resolved"


@pytest.mark.asyncio
async def test_enforce_mode_allows_a_resolvable_tenant():
    response = await _get(_app(mode=ENFORCE), {"X-Tenant-ID": "acme"})

    assert response.status_code == 200
    assert response.json()["tenant_id"] == "acme"


@pytest.mark.asyncio
async def test_off_mode_skips_resolution_entirely():
    response = await _get(_app(mode=OFF), {"X-Tenant-ID": "acme"})

    assert response.status_code == 200
    assert response.json()["tenant_id"] is None


# ── The middleware is actually installed ────────────────────────────────────


def test_middleware_is_registered_on_the_real_app():
    """Being importable is not the same as being wired in — that was the bug."""
    from api.main import app

    names = {m.cls.__name__ for m in app.user_middleware}

    assert "TenantContextMiddleware" in names, sorted(names)


# ── What is still NOT enforced ──────────────────────────────────────────────


def test_row_level_security_is_defined_but_not_applied():
    """Pin the remaining gap rather than let the code imply it is closed.

    ``apply_rls()`` issues DDL against production tables. Running it is a
    schema and security change that belongs in a reviewed migration with
    founder approval, not an app-startup side effect. Until then, RLS is
    written but inert, and this test says so out loud.
    """
    import ast
    import pathlib

    repo_root = pathlib.Path(__file__).resolve().parents[1]
    callers: list[str] = []
    for path in (repo_root / "api").rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8", errors="ignore"))
        for node in ast.walk(tree):
            if (
                isinstance(node, ast.Call)
                and getattr(node.func, "id", getattr(node.func, "attr", None)) == "apply_rls"
            ):
                callers.append(path.relative_to(repo_root).as_posix())

    assert callers == [], (
        "apply_rls() is now called from the application: "
        f"{callers}. Applying row-level security is a production schema "
        "change — it belongs in a reviewed migration, and this test should be "
        "replaced with one that verifies the policies actually take effect."
    )


# ── Enforce mode must not break public surfaces ─────────────────────────────


def test_public_paths_are_exempt_from_tenant_enforcement():
    """Health probes, webhooks and the public funnel carry no tenant by design."""
    from api.middleware.tenant_isolation import is_tenant_exempt_path

    for path in ("/healthz", "/health", "/ready", "/livez", "/version", "/api/v1/meta"):
        assert is_tenant_exempt_path(path), path
    for path in ("/api/v1/public/custom-ai-request", "/api/v1/webhooks/whatsapp"):
        assert is_tenant_exempt_path(path), path


def test_tenant_scoped_paths_are_not_exempt():
    """The exemption must stay narrow, or enforcement means nothing."""
    from api.middleware.tenant_isolation import is_tenant_exempt_path

    for path in ("/api/v1/leads", "/api/v1/founder/dashboard", "/api/v1/approvals/pending"):
        assert not is_tenant_exempt_path(path), path


def test_exemption_reuses_the_api_key_public_lists():
    """One definition of 'public'. Two would drift, and drift is a security bug."""
    from api.middleware.tenant_isolation import is_tenant_exempt_path
    from api.security.api_key import PUBLIC_PATHS

    for path in PUBLIC_PATHS:
        assert is_tenant_exempt_path(path), path


@pytest.mark.asyncio
async def test_enforce_mode_still_serves_a_health_probe():
    """The regression that would have failed every Railway deploy.

    Without the exemption, TENANT_ENFORCEMENT=enforce returns 403 to the
    healthcheck — the container never goes healthy and the deploy rolls back.
    """
    app = FastAPI()
    app.add_middleware(TenantContextMiddleware, mode=ENFORCE)

    @app.get("/healthz")
    async def healthz() -> JSONResponse:
        return JSONResponse({"status": "ok"})

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/healthz")

    assert response.status_code == 200, (
        "enforce mode 403'd the health probe — deploys would fail"
    )


@pytest.mark.asyncio
async def test_enforce_mode_still_rejects_a_tenant_scoped_path():
    """Positive control: the exemption must not disable enforcement."""
    app = FastAPI()
    app.add_middleware(TenantContextMiddleware, mode=ENFORCE)

    @app.get("/api/v1/leads")
    async def leads() -> JSONResponse:
        return JSONResponse({"leads": []})

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/v1/leads")

    assert response.status_code == 403
