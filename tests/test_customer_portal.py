"""Customer Portal Backend MVP — endpoint tests (Track B.4).

Covers:
  - 401 unauthenticated for every endpoint.
  - 403 cross-tenant access for sprint detail + proof-pack download.
  - 200 happy paths for /me, /sprints, /sprints/{id}, /proof-packs,
    /proof-packs/{id}/download, /feedback, /invoices.
  - PDPL log sanitiser correctness.

All tests use FastAPI dependency overrides — no live DB / no live JWT
signing — so they run in any environment.
"""

from __future__ import annotations

from collections.abc import AsyncGenerator
from datetime import datetime, timezone
from typing import Any
from unittest.mock import MagicMock

import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from api.routers.customer_portal import (
    _log_safe_summary,
    _safe_id,
    get_current_customer,
    router as customer_portal_router,
)
from api.security.auth_deps import get_current_user
from db.session import get_db


# ── Helpers ────────────────────────────────────────────────────────


def _make_user(
    *,
    user_id: str = "usr_test_001",
    tenant_id: str | None = "ten_test_alpha",
    email: str = "owner@alpha.sa",
    name: str = "Test Owner",
    system_role: str | None = None,
) -> MagicMock:
    """Return a stand-in UserRecord that satisfies get_current_user."""
    u = MagicMock()
    u.id = user_id
    u.tenant_id = tenant_id
    u.email = email
    u.name = name
    u.system_role = system_role
    u.is_active = True
    u.deleted_at = None
    u.role_id = None
    return u


class _FakeAsyncSession:
    """Minimal AsyncSession stand-in that records added rows + serves
    canned query results."""

    def __init__(self) -> None:
        self.added: list[Any] = []
        self.flushed = False
        self.invoices: list[Any] = []

    def add(self, row: Any) -> None:
        self.added.append(row)

    async def flush(self) -> None:
        self.flushed = True

    async def execute(self, _stmt: Any) -> Any:
        rows = list(self.invoices)

        class _Result:
            def scalars(self_inner) -> Any:
                class _Scalars:
                    def all(self_in2) -> list[Any]:
                        return rows

                return _Scalars()

        return _Result()

    async def commit(self) -> None:
        return None

    async def rollback(self) -> None:
        return None


@pytest_asyncio.fixture
async def portal_app() -> AsyncGenerator[FastAPI, None]:
    app = FastAPI()
    app.include_router(customer_portal_router)
    try:
        yield app
    finally:
        app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def portal_client(
    portal_app: FastAPI,
) -> AsyncGenerator[AsyncClient, None]:
    transport = ASGITransport(app=portal_app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c


def _install_auth(app: FastAPI, user: MagicMock) -> None:
    """Override the two auth dependencies so endpoints see `user`."""
    app.dependency_overrides[get_current_user] = lambda: user

    async def _principal() -> Any:
        # Use the real dependency so its 403-no-tenant branch keeps
        # being exercised in tests that don't install an override.
        return await get_current_customer(user)

    app.dependency_overrides[get_current_customer] = _principal


def _install_db(app: FastAPI, session: _FakeAsyncSession) -> None:
    async def _get_db() -> AsyncGenerator[_FakeAsyncSession, None]:
        yield session

    app.dependency_overrides[get_db] = _get_db


def _fake_session(**overrides: Any) -> MagicMock:
    defaults: dict[str, Any] = {
        "id": "spr_alpha_001",
        "customer_handle": "ten_test_alpha",
        "title": "Sector Sprint",
        "status": "in_delivery",
        "day": 4,
        "total_days": 7,
        "started_at": datetime(2026, 5, 20, tzinfo=timezone.utc),
        "ends_at": datetime(2026, 5, 27, tzinfo=timezone.utc),
        "timeline": [
            {"step": "kickoff", "status": "done", "completed_at": "2026-05-20"},
            {"step": "delivery", "status": "active", "completed_at": None},
        ],
        "pending_approvals": 1,
    }
    defaults.update(overrides)
    m = MagicMock()
    for k, v in defaults.items():
        setattr(m, k, v)
    return m


def _fake_proof_event(
    *,
    event_id: str = "pk_alpha_001",
    customer_handle: str = "ten_test_alpha",
) -> MagicMock:
    e = MagicMock()
    e.id = event_id
    e.customer_handle = customer_handle
    e.event_type = "proof_pack_v1"
    e.title = "Sprint Proof Pack"
    e.tier = "L3"
    e.score = 0.82
    e.created_at = datetime(2026, 5, 24, tzinfo=timezone.utc)
    e.model_dump = lambda: {
        "id": event_id,
        "customer_handle": customer_handle,
        "event_type": "proof_pack_v1",
    }
    return e


# ── 401 unauthenticated ────────────────────────────────────────────


@pytest.mark.asyncio
async def test_me_requires_auth(portal_client: AsyncClient) -> None:
    res = await portal_client.get("/api/v1/portal/me")
    assert res.status_code == 401


@pytest.mark.asyncio
async def test_sprints_requires_auth(portal_client: AsyncClient) -> None:
    res = await portal_client.get("/api/v1/portal/sprints")
    assert res.status_code == 401

    res2 = await portal_client.get("/api/v1/portal/sprints/spr_xyz")
    assert res2.status_code == 401


@pytest.mark.asyncio
async def test_proof_packs_requires_auth(portal_client: AsyncClient) -> None:
    res = await portal_client.get("/api/v1/portal/proof-packs")
    assert res.status_code == 401

    res2 = await portal_client.get("/api/v1/portal/proof-packs/pk_xyz/download")
    assert res2.status_code == 401


@pytest.mark.asyncio
async def test_feedback_requires_auth(portal_client: AsyncClient) -> None:
    res = await portal_client.post(
        "/api/v1/portal/feedback",
        json={"rating": 5, "comment": "great"},
    )
    assert res.status_code == 401


@pytest.mark.asyncio
async def test_invoices_requires_auth(portal_client: AsyncClient) -> None:
    res = await portal_client.get("/api/v1/portal/invoices")
    assert res.status_code == 401


# ── /me happy path ─────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_me_returns_profile(
    portal_app: FastAPI, portal_client: AsyncClient
) -> None:
    _install_auth(portal_app, _make_user())
    res = await portal_client.get("/api/v1/portal/me")
    assert res.status_code == 200
    body = res.json()
    assert body["user_id"] == "usr_test_001"
    assert body["tenant_id"] == "ten_test_alpha"
    assert body["email"] == "owner@alpha.sa"
    assert body["portal_version"] == "b4_mvp"


# ── /sprints happy path + 403 cross-tenant ─────────────────────────


@pytest.mark.asyncio
async def test_list_sprints_returns_filtered_results(
    portal_app: FastAPI,
    portal_client: AsyncClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _install_auth(portal_app, _make_user())

    mine = _fake_session()
    other = _fake_session(id="spr_beta_001", customer_handle="ten_other_beta")

    monkeypatch.setattr(
        "api.routers.customer_portal._list_sprint_sessions",
        lambda *, customer_id: [mine, other],
    )

    res = await portal_client.get("/api/v1/portal/sprints")
    assert res.status_code == 200
    body = res.json()
    # Cross-tenant row filtered out defensively.
    assert body["count"] == 1
    assert body["sprints"][0]["sprint_id"] == "spr_alpha_001"
    assert body["sprints"][0]["status"] == "in_delivery"


@pytest.mark.asyncio
async def test_get_sprint_404_when_unknown(
    portal_app: FastAPI,
    portal_client: AsyncClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _install_auth(portal_app, _make_user())
    monkeypatch.setattr(
        "api.routers.customer_portal._list_sprint_sessions",
        lambda *, customer_id: [],
    )
    res = await portal_client.get("/api/v1/portal/sprints/spr_does_not_exist")
    assert res.status_code == 404
    assert res.json()["detail"] == "sprint_not_found"


@pytest.mark.asyncio
async def test_get_sprint_403_cross_tenant(
    portal_app: FastAPI,
    portal_client: AsyncClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _install_auth(portal_app, _make_user(tenant_id="ten_test_alpha"))
    cross = _fake_session(id="spr_beta_001", customer_handle="ten_other_beta")

    # Simulate a leaky upstream that returns rows from other tenants —
    # the router must reject with 403, not leak the data.
    monkeypatch.setattr(
        "api.routers.customer_portal._list_sprint_sessions",
        lambda *, customer_id: [cross],
    )

    res = await portal_client.get("/api/v1/portal/sprints/spr_beta_001")
    assert res.status_code == 403
    assert res.json()["detail"] == "cross_tenant_access_denied"


@pytest.mark.asyncio
async def test_get_sprint_happy_path(
    portal_app: FastAPI,
    portal_client: AsyncClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _install_auth(portal_app, _make_user())
    monkeypatch.setattr(
        "api.routers.customer_portal._list_sprint_sessions",
        lambda *, customer_id: [_fake_session()],
    )
    res = await portal_client.get("/api/v1/portal/sprints/spr_alpha_001")
    assert res.status_code == 200
    body = res.json()
    assert body["sprint"]["sprint_id"] == "spr_alpha_001"
    assert body["pending_approvals"] == 1
    assert len(body["timeline"]) == 2
    assert body["next_action_ar"]
    assert body["next_action_en"]


# ── /proof-packs happy path + cross-tenant download block ───────────


@pytest.mark.asyncio
async def test_list_proof_packs_returns_summaries(
    portal_app: FastAPI,
    portal_client: AsyncClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _install_auth(portal_app, _make_user())
    monkeypatch.setattr(
        "api.routers.customer_portal._list_proof_packs",
        lambda *, customer_id: [_fake_proof_event()],
    )
    res = await portal_client.get("/api/v1/portal/proof-packs")
    assert res.status_code == 200
    body = res.json()
    assert body["count"] == 1
    pack = body["packs"][0]
    assert pack["pack_id"] == "pk_alpha_001"
    assert pack["download_url"].endswith("/pk_alpha_001/download")


@pytest.mark.asyncio
async def test_download_proof_pack_404_when_unknown(
    portal_app: FastAPI,
    portal_client: AsyncClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _install_auth(portal_app, _make_user())
    monkeypatch.setattr(
        "api.routers.customer_portal._list_proof_packs",
        lambda *, customer_id: [],
    )
    res = await portal_client.get("/api/v1/portal/proof-packs/pk_missing/download")
    assert res.status_code == 404


@pytest.mark.asyncio
async def test_download_proof_pack_blocks_cross_tenant(
    portal_app: FastAPI,
    portal_client: AsyncClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _install_auth(portal_app, _make_user(tenant_id="ten_test_alpha"))
    cross = _fake_proof_event(
        event_id="pk_beta_001", customer_handle="ten_other_beta"
    )
    monkeypatch.setattr(
        "api.routers.customer_portal._list_proof_packs",
        lambda *, customer_id: [cross],
    )
    res = await portal_client.get("/api/v1/portal/proof-packs/pk_beta_001/download")
    assert res.status_code == 403


@pytest.mark.asyncio
async def test_download_proof_pack_returns_markdown(
    portal_app: FastAPI,
    portal_client: AsyncClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _install_auth(portal_app, _make_user())
    monkeypatch.setattr(
        "api.routers.customer_portal._list_proof_packs",
        lambda *, customer_id: [_fake_proof_event()],
    )
    res = await portal_client.get(
        "/api/v1/portal/proof-packs/pk_alpha_001/download"
    )
    assert res.status_code == 200
    # Either the real renderer or the documented fallback string.
    body = res.text
    assert body
    assert "proof_pack_pk_alpha_001.md" in res.headers.get(
        "content-disposition", ""
    )


# ── /feedback happy path + validation ───────────────────────────────


@pytest.mark.asyncio
async def test_submit_feedback_persists_row(
    portal_app: FastAPI, portal_client: AsyncClient
) -> None:
    _install_auth(portal_app, _make_user())
    fake_db = _FakeAsyncSession()
    _install_db(portal_app, fake_db)

    res = await portal_client.post(
        "/api/v1/portal/feedback",
        json={"rating": 5, "comment": "Excellent", "sprint_id": "spr_alpha_001"},
    )
    assert res.status_code == 201
    body = res.json()
    assert body["rating"] == 5
    assert body["comment_stored"] is True
    assert body["sprint_id"] == "spr_alpha_001"
    assert body["feedback_id"].startswith("fbk_")
    assert len(fake_db.added) == 1
    row = fake_db.added[0]
    assert row.tenant_id == "ten_test_alpha"
    assert row.rating == 5
    assert row.comment == "Excellent"
    assert fake_db.flushed is True


@pytest.mark.asyncio
async def test_submit_feedback_rejects_out_of_range_rating(
    portal_app: FastAPI, portal_client: AsyncClient
) -> None:
    _install_auth(portal_app, _make_user())
    _install_db(portal_app, _FakeAsyncSession())

    res = await portal_client.post(
        "/api/v1/portal/feedback",
        json={"rating": 9, "comment": ""},
    )
    assert res.status_code == 422


@pytest.mark.asyncio
async def test_submit_feedback_blocks_no_tenant(
    portal_app: FastAPI, portal_client: AsyncClient
) -> None:
    user = _make_user(tenant_id=None, system_role="super_admin")
    _install_auth(portal_app, user)
    _install_db(portal_app, _FakeAsyncSession())
    res = await portal_client.post(
        "/api/v1/portal/feedback",
        json={"rating": 4, "comment": ""},
    )
    assert res.status_code == 403
    assert res.json()["detail"] == "tenant_scope_required"


# ── /invoices happy path ───────────────────────────────────────────


@pytest.mark.asyncio
async def test_list_invoices_returns_tenant_invoices(
    portal_app: FastAPI, portal_client: AsyncClient
) -> None:
    _install_auth(portal_app, _make_user())
    fake = _FakeAsyncSession()

    invoice = MagicMock()
    invoice.id = "inv_alpha_001"
    invoice.invoice_number = "311111111100003-1-1"
    invoice.total_sar = 574.0
    invoice.vat_amount_sar = 74.0
    invoice.zatca_status = "cleared"
    invoice.issue_date = "2026-05-24"
    invoice.buyer_name = "Alpha Co"
    fake.invoices = [invoice]

    _install_db(portal_app, fake)

    res = await portal_client.get("/api/v1/portal/invoices")
    assert res.status_code == 200
    body = res.json()
    assert body["count"] == 1
    assert body["invoices"][0]["invoice_number"] == "311111111100003-1-1"
    assert body["invoices"][0]["status"] == "cleared"


# ── Unit: PDPL log sanitiser ───────────────────────────────────────


def test_log_safe_summary_masks_email_and_phone() -> None:
    msg = "Contact me at owner@alpha.sa or +966501112233 ASAP"
    out = _log_safe_summary(msg, max_len=200)
    assert "owner@alpha.sa" not in out
    assert "+966501112233" not in out
    assert "<email>" in out
    assert "<phone>" in out


def test_log_safe_summary_truncates() -> None:
    out = _log_safe_summary("x" * 200, max_len=10)
    assert len(out) <= 10
    assert out.endswith("…")


def test_log_safe_summary_empty_passes() -> None:
    assert _log_safe_summary("") == ""


def test_safe_id_strips_path_traversal() -> None:
    assert _safe_id("../../etc/passwd") == ".._.._etc_passwd"
    assert _safe_id("abc 123") == "abc_123"
    assert _safe_id("ok-_.id") == "ok-_.id"
