"""Cross-tenant isolation contract for the PDPL personal-data endpoints.

Before this guard existed, `/api/v1/pdpl/data/{contact_id}` and its
`/export` sibling took the tenant from a query parameter and looked the
contact up by ID alone. The declared tenant was written to the audit log
but never checked, so any caller past the shared API key could:

  * export another tenant's contact — name, email, phone, plus up to 500
    audit rows; and
  * irreversibly anonymise and soft-delete that contact.

The tenant is now taken from the authenticated user and applied to the
query itself. These tests drive the real routes over HTTP against a
seeded database so they fail if the tenant filter is ever dropped again.
"""

from __future__ import annotations

import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from api.routers import pdpl
from api.security.auth_deps import get_current_user
from db.models import AuditLogRecord, Base, ContactRecord, LeadRecord
from db.session import get_db

ATTACKER_TENANT = "tenant_a"
VICTIM_TENANT = "tenant_b"
VICTIM_CONTACT = "contact_of_b"
VICTIM_NAME = "Victim Person"
VICTIM_EMAIL = "victim@tenant-b.example"
VICTIM_PHONE = "+966500000001"


class _User:
    """Stand-in for an authenticated UserRecord."""

    def __init__(self, tenant_id: str, system_role: str = "user") -> None:
        self.id = f"user_of_{tenant_id}"
        self.tenant_id = tenant_id
        self.system_role = system_role


@pytest_asyncio.fixture
async def session_factory():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(
            Base.metadata.create_all,
            tables=[
                ContactRecord.__table__,
                AuditLogRecord.__table__,
                LeadRecord.__table__,
            ],
        )
    factory = async_sessionmaker(engine, expire_on_commit=False)
    async with factory() as session:
        session.add(
            ContactRecord(
                id=VICTIM_CONTACT,
                tenant_id=VICTIM_TENANT,
                account_id="acct_b",
                name=VICTIM_NAME,
                email=VICTIM_EMAIL,
                phone=VICTIM_PHONE,
            )
        )
        await session.commit()
    yield factory
    await engine.dispose()


def _build_client(session_factory, user: _User) -> AsyncClient:
    async def override_db():
        async with session_factory() as session:
            yield session
            await session.commit()

    app = FastAPI()
    app.include_router(pdpl.router)
    app.dependency_overrides[get_db] = override_db
    app.dependency_overrides[get_current_user] = lambda: user
    return AsyncClient(transport=ASGITransport(app=app), base_url="http://test")


# ── Export (Art. 14) ─────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_export_does_not_leak_another_tenants_contact(session_factory):
    async with _build_client(session_factory, _User(ATTACKER_TENANT)) as client:
        response = await client.get(
            f"/api/v1/pdpl/data/{VICTIM_CONTACT}/export",
            params={"tenant_id": ATTACKER_TENANT},
        )

    assert response.status_code == 404
    body = response.text
    for secret in (VICTIM_NAME, VICTIM_EMAIL, VICTIM_PHONE):
        assert secret not in body


@pytest.mark.asyncio
async def test_export_ignores_a_declared_victim_tenant(session_factory):
    """Naming the victim tenant outright must not widen access either."""
    async with _build_client(session_factory, _User(ATTACKER_TENANT)) as client:
        response = await client.get(
            f"/api/v1/pdpl/data/{VICTIM_CONTACT}/export",
            params={"tenant_id": VICTIM_TENANT},
        )

    assert response.status_code == 403
    assert VICTIM_EMAIL not in response.text


@pytest.mark.asyncio
async def test_export_serves_the_owning_tenant(session_factory):
    """The fix must not break the legitimate data-portability path."""
    async with _build_client(session_factory, _User(VICTIM_TENANT)) as client:
        response = await client.get(
            f"/api/v1/pdpl/data/{VICTIM_CONTACT}/export",
            params={"tenant_id": VICTIM_TENANT},
        )

    assert response.status_code == 200
    assert VICTIM_EMAIL in response.text


# ── Erasure (Art. 13) ────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_erasure_cannot_destroy_another_tenants_contact(session_factory):
    async with _build_client(session_factory, _User(ATTACKER_TENANT)) as client:
        response = await client.request(
            "DELETE",
            f"/api/v1/pdpl/data/{VICTIM_CONTACT}",
            params={"tenant_id": ATTACKER_TENANT},
        )

    assert response.status_code == 404

    async with session_factory() as session:
        victim = await session.get(ContactRecord, VICTIM_CONTACT)
        assert victim.name == VICTIM_NAME
        assert victim.email == VICTIM_EMAIL
        assert victim.deleted_at is None


@pytest.mark.asyncio
async def test_erasure_serves_the_owning_tenant(session_factory):
    async with _build_client(session_factory, _User(VICTIM_TENANT)) as client:
        response = await client.request(
            "DELETE",
            f"/api/v1/pdpl/data/{VICTIM_CONTACT}",
            params={"tenant_id": VICTIM_TENANT},
        )

    assert response.status_code == 200

    async with session_factory() as session:
        victim = await session.get(ContactRecord, VICTIM_CONTACT)
        assert victim.name == "[ERASED]"
        assert victim.deleted_at is not None


# ── Audit report (Art. 18) ───────────────────────────────────────────


@pytest.mark.asyncio
async def test_audit_report_cannot_target_another_tenant(session_factory):
    async with _build_client(session_factory, _User(ATTACKER_TENANT)) as client:
        response = await client.get(
            "/api/v1/pdpl/audit/report",
            params={"tenant_id": VICTIM_TENANT, "report_month": "2026-07"},
        )

    assert response.status_code == 403


@pytest.mark.asyncio
async def test_audit_report_defaults_to_the_callers_tenant(session_factory):
    """Omitting the parameter resolves from identity, not to a global view."""
    async with _build_client(session_factory, _User(ATTACKER_TENANT)) as client:
        response = await client.get(
            "/api/v1/pdpl/audit/report", params={"report_month": "2026-07"}
        )

    assert response.status_code == 200
    assert response.json()["tenant_id"] == ATTACKER_TENANT


# ── Consent dashboard ────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_consent_dashboard_does_not_serve_unpartitioned_records(
    session_factory,
):
    """The consent store has no tenant column, so it must serve nothing."""
    async with _build_client(session_factory, _User(ATTACKER_TENANT)) as client:
        response = await client.get(
            "/api/v1/pdpl/consent/dashboard", params={"tenant_id": ATTACKER_TENANT}
        )

    assert response.status_code == 200
    body = response.json()
    assert body["tenant_scoped"] is False
    assert body["records_available"] is False


# ── Identity is required at all ──────────────────────────────────────


def test_personal_data_routes_require_authentication():
    """Every route that moves personal data depends on the current user."""
    protected = {
        ("GET", "/api/v1/pdpl/data/{contact_id}/export"),
        ("DELETE", "/api/v1/pdpl/data/{contact_id}"),
        ("GET", "/api/v1/pdpl/audit/report"),
        ("GET", "/api/v1/pdpl/consent/dashboard"),
        ("POST", "/api/v1/pdpl/consent/request"),
        ("POST", "/api/v1/pdpl/consent/grant"),
        ("POST", "/api/v1/pdpl/consent/revoke"),
        ("POST", "/api/v1/pdpl/breach/notify"),
    }
    seen = set()
    for route in pdpl.router.routes:
        for method in route.methods:
            if (method, route.path) not in protected:
                continue
            seen.add((method, route.path))
            calls = {dep.call for dep in route.dependant.dependencies}
            assert get_current_user in calls, f"{method} {route.path} is unauthenticated"

    assert seen == protected, f"routes missing from the router: {protected - seen}"
