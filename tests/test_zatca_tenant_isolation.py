"""Cross-tenant isolation contract for the ZATCA e-invoice endpoints.

`api/routers/zatca.py` looked invoices up by ID alone, with no
authentication dependency, and listed invoices for whatever tenant the
caller named in the query string. An e-invoice carries the buyer's
identity, VAT numbers and amounts, and submission reports to the tax
authority — so before this guard any caller past the shared API key could
read another tenant's invoice, enumerate their invoice book, or submit
their invoice to ZATCA.

The tenant now comes from the authenticated user and is applied to the
query, so an invoice outside the tenant is not found.
"""

from __future__ import annotations

import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from api.routers import zatca
from api.security.auth_deps import get_current_user
from db.models import AuditLogRecord, Base, ZATCAInvoiceRecord
from db.session import get_db

ATTACKER_TENANT = "tenant_a"
VICTIM_TENANT = "tenant_b"
VICTIM_INVOICE = "invoice_of_b"
VICTIM_BUYER = "Victim Buyer Co"
VICTIM_VAT = "300000000000003"


class _User:
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
            tables=[ZATCAInvoiceRecord.__table__, AuditLogRecord.__table__],
        )
    factory = async_sessionmaker(engine, expire_on_commit=False)
    async with factory() as session:
        session.add(
            ZATCAInvoiceRecord(
                id=VICTIM_INVOICE,
                tenant_id=VICTIM_TENANT,
                invoice_number="INV-B-001",
                issue_date="2026-07-01",
                issue_time="10:00:00",
                seller_vat_number=VICTIM_VAT,
                buyer_name=VICTIM_BUYER,
                subtotal_sar=1000.0,
                vat_amount_sar=150.0,
                total_sar=1150.0,
                zatca_status="draft",
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
    app.include_router(zatca.router)
    app.dependency_overrides[get_db] = override_db
    app.dependency_overrides[get_current_user] = lambda: user
    return AsyncClient(transport=ASGITransport(app=app), base_url="http://test")


@pytest.mark.asyncio
async def test_status_does_not_leak_another_tenants_invoice(session_factory):
    async with _build_client(session_factory, _User(ATTACKER_TENANT)) as client:
        response = await client.get(f"/api/v1/zatca/invoices/{VICTIM_INVOICE}/status")

    assert response.status_code == 404
    for secret in (VICTIM_BUYER, VICTIM_VAT):
        assert secret not in response.text


@pytest.mark.asyncio
async def test_status_serves_the_owning_tenant(session_factory):
    async with _build_client(session_factory, _User(VICTIM_TENANT)) as client:
        response = await client.get(f"/api/v1/zatca/invoices/{VICTIM_INVOICE}/status")

    assert response.status_code == 200
    assert response.json()["buyer_name"] == VICTIM_BUYER


@pytest.mark.asyncio
async def test_listing_cannot_target_another_tenant(session_factory):
    async with _build_client(session_factory, _User(ATTACKER_TENANT)) as client:
        response = await client.get(
            "/api/v1/zatca/invoices", params={"tenant_id": VICTIM_TENANT}
        )

    assert response.status_code == 403
    assert VICTIM_BUYER not in response.text


@pytest.mark.asyncio
async def test_listing_defaults_to_the_callers_own_invoices(session_factory):
    async with _build_client(session_factory, _User(ATTACKER_TENANT)) as client:
        response = await client.get("/api/v1/zatca/invoices")

    assert response.status_code == 200
    body = response.json()
    assert body["tenant_id"] == ATTACKER_TENANT
    assert body["invoices"] == []


@pytest.mark.asyncio
async def test_submission_cannot_touch_another_tenants_invoice(session_factory):
    """Submission reports to the tax authority — it must not cross tenants."""
    async with _build_client(session_factory, _User(ATTACKER_TENANT)) as client:
        response = await client.post(
            f"/api/v1/zatca/invoices/{VICTIM_INVOICE}/submit"
        )

    assert response.status_code == 404

    async with session_factory() as session:
        invoice = await session.get(ZATCAInvoiceRecord, VICTIM_INVOICE)
        assert invoice.zatca_status == "draft"


@pytest.mark.asyncio
async def test_generation_ignores_a_declared_tenant(session_factory):
    """A body-declared tenant must not decide who owns a new invoice."""
    async with _build_client(session_factory, _User(ATTACKER_TENANT)) as client:
        response = await client.post(
            "/api/v1/zatca/invoices",
            json={
                "tenant_id": VICTIM_TENANT,
                "invoice_number": "INV-SPOOF-001",
                "invoice_type": "simplified",
                "seller": {"name": "A", "vat_number": VICTIM_VAT},
                "buyer": {"name": "B"},
                "line_items": [
                    {"description": "x", "quantity": 1, "unit_price_sar": 10.0}
                ],
            },
        )

    assert response.status_code == 403


def test_invoice_routes_require_authentication():
    protected = {
        ("POST", "/api/v1/zatca/invoices"),
        ("POST", "/api/v1/zatca/invoices/{invoice_id}/submit"),
        ("GET", "/api/v1/zatca/invoices/{invoice_id}/status"),
        ("GET", "/api/v1/zatca/invoices"),
    }
    seen = set()
    for route in zatca.router.routes:
        for method in route.methods:
            if (method, route.path) not in protected:
                continue
            seen.add((method, route.path))
            calls = {dep.call for dep in route.dependant.dependencies}
            assert get_current_user in calls, f"{method} {route.path} is unauthenticated"

    assert seen == protected, f"routes missing from the router: {protected - seen}"
