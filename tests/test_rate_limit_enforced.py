"""Rate limiting must be enforced, or production must refuse to start.

Two halves that only work together:

* ``RateLimitHeadersMiddleware`` injects ``X-RateLimit-*`` on **every**
  response and, by its own docstring, defers enforcement elsewhere.
* ``api.security.rate_limit:setup_rate_limit`` installs ``SlowAPIMiddleware``
  — and used to ``return`` silently when slowapi was missing.

A deployment without slowapi therefore served rate-limit headers that nothing
honoured. That matters most at ``/api/v1/auth/login``: it sits behind
``PUBLIC_PREFIXES``, so it skips the API key middleware entirely, and it has
no per-route throttle of its own. An unthrottled login endpoint that announces
a throttle is worse than one that announces nothing.

slowapi is pinned in ``requirements.txt``, so this should be unreachable in
production. ``setup_rate_limit`` now raises there rather than no-op, matching
``api/main.py:_validate_production_secrets``, which also refuses to start
rather than run insecure.

``/api/v1/compliance/status`` reported this control as
``_module_present("slowapi")`` — importability, which is precisely the thing
that differs from enforcement in the failure case. It now reads the running
middleware stack.

Note on this environment: slowapi is **not installed** here, so the enforced
probe is expected to be False locally and True in CI and production. The tests
below assert the *mechanism*, not a fixed answer, so they hold either way.
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from api.security import rate_limit


def test_production_refuses_to_start_without_slowapi(monkeypatch):
    """The regression: this used to return quietly and leave login open."""
    from fastapi import FastAPI

    monkeypatch.setattr(rate_limit, "_HAS_SLOWAPI", False)
    monkeypatch.setattr(
        rate_limit, "get_settings", lambda: SimpleNamespace(is_production=True)
    )

    with pytest.raises(RuntimeError) as raised:
        rate_limit.setup_rate_limit(FastAPI())

    message = str(raised.value)
    assert "slowapi" in message
    assert "rate limiting" in message.lower()


@pytest.mark.parametrize("env", ["development", "test", ""])
def test_dev_and_test_tolerate_a_missing_slowapi(monkeypatch, env):
    """Local runs without the optional dependency must still boot."""
    from fastapi import FastAPI

    monkeypatch.setattr(rate_limit, "_HAS_SLOWAPI", False)
    monkeypatch.setattr(
        rate_limit, "get_settings", lambda: SimpleNamespace(is_production=False)
    )
    monkeypatch.setenv("APP_ENV", env)

    rate_limit.setup_rate_limit(FastAPI())  # must not raise


def test_a_missing_limiter_is_treated_as_missing_slowapi(monkeypatch):
    """`_HAS_SLOWAPI` true with no limiter is the same hole."""
    from fastapi import FastAPI

    monkeypatch.setattr(rate_limit, "_HAS_SLOWAPI", True)
    monkeypatch.setattr(rate_limit, "limiter", None)
    monkeypatch.setattr(
        rate_limit, "get_settings", lambda: SimpleNamespace(is_production=True)
    )

    with pytest.raises(RuntimeError):
        rate_limit.setup_rate_limit(FastAPI())


@pytest.mark.parametrize("alias", ["APP_ENV", "ENVIRONMENT", "VERCEL_ENV"])
def test_every_supported_production_alias_fails_closed(monkeypatch, alias):
    """Platform-standard env aliases must not silently disable the guard."""
    from fastapi import FastAPI

    from core.config.settings import Settings

    for name in ("APP_ENV", "ENVIRONMENT", "VERCEL_ENV"):
        monkeypatch.delenv(name, raising=False)
    monkeypatch.setenv(alias, "production")
    monkeypatch.setattr(rate_limit, "_HAS_SLOWAPI", False)
    monkeypatch.setattr(rate_limit, "get_settings", Settings)

    with pytest.raises(RuntimeError):
        rate_limit.setup_rate_limit(FastAPI())



# ── The compliance surface ────────────────────────────────────────────────


def test_the_probe_reads_the_middleware_stack_not_the_import():
    """It must agree with the app, whichever way that falls in this env."""
    import api.main
    from api.routers.compliance_status import _rate_limiting_enforced

    installed = any(
        middleware.cls.__name__ == "SlowAPIMiddleware"
        for middleware in api.main.app.user_middleware
    )

    assert _rate_limiting_enforced(api.main.app) is installed


def test_importability_alone_no_longer_counts_as_the_control():
    import api.main
    from api.routers import compliance_status

    payload = compliance_status._security_status(api.main.app)

    assert "implemented" not in payload["rate_limiting"], (
        "module presence is back as evidence of rate limiting"
    )
    assert "enforced" in payload["rate_limiting"]


def test_the_probe_is_false_when_the_middleware_is_absent():
    """Proves it measures the stack rather than always answering True."""
    from api.routers.compliance_status import _rate_limiting_enforced

    class _Stub:
        user_middleware: list = []

    assert _rate_limiting_enforced(_Stub()) is False


def test_the_endpoint_does_not_import_api_main():
    """`api.main` imports this router; importing it back closes a cycle.

    CodeQL flagged it even as a lazy in-function import. `request.app` is the
    same object with no cycle.

    Asserted over the AST rather than the file text: the docstrings in that
    module name ``api.main`` to explain why it is not imported, and a
    substring check would match those.
    """
    import ast
    from pathlib import Path

    tree = ast.parse(
        (
            Path(__file__).resolve().parents[1] / "api/routers/compliance_status.py"
        ).read_text(encoding="utf-8")
    )

    imported = {
        alias.name
        for node in ast.walk(tree)
        if isinstance(node, ast.Import)
        for alias in node.names
    } | {
        node.module
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom) and node.module
    }

    assert "api.main" not in imported, "the import cycle is back"


@pytest.mark.asyncio
async def test_enforced_control_counts_as_active_in_endpoint(monkeypatch):
    """The public posture must count enforcement, not under-report it."""
    from api.routers import compliance_status

    monkeypatch.setattr(compliance_status, "_pdpl_status", lambda: {})
    monkeypatch.setattr(compliance_status, "_zatca_status", lambda: {})
    monkeypatch.setattr(
        compliance_status,
        "_security_status",
        lambda app: {"rate_limiting": {"enforced": True}},
    )

    payload = await compliance_status.compliance_status(
        SimpleNamespace(app=object())
    )

    assert payload["overall_posture"]["security_controls"] == "1/1 active"



# ── The header half of the pair ───────────────────────────────────────────


def test_headers_are_advertised_on_an_ordinary_response():
    """Pins the claim these tests exist to keep honest.

    If this ever stops being true, the enforcement guard above is no longer
    load-bearing and can be reconsidered — but while the header is sent, it
    must not be a lie.
    """
    from fastapi.testclient import TestClient

    import api.main

    resp = TestClient(api.main.app).get("/healthz")

    assert "X-RateLimit-Limit" in resp.headers
