"""Cross-tenant isolation contract for the autonomous deal endpoints.

`api/routers/autonomous.py` is mounted through a domain group. Before this
guard, `mark_paid`, `manual_payment_request` and `update_deal` had no
authentication dependency and loaded `DealRecord` by the ID in the request
body with no tenant filter — so any caller could move another tenant's deal
to `paid`, overwrite its amount, and trigger customer onboarding. `list_deals`
returned every tenant's deals.

The tenant now comes from the authenticated user and is applied to the query.
"""

from __future__ import annotations

import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from api.routers import autonomous
from api.security.auth_deps import get_current_user
from db.models import Base, CustomerRecord, DealRecord, TaskRecord

ATTACKER_TENANT = "tenant_a"
VICTIM_TENANT = "tenant_b"
VICTIM_DEAL = "deal_of_b"


class _User:
    def __init__(self, tenant_id: str, system_role: str = "user") -> None:
        self.id = f"user_of_{tenant_id}"
        self.tenant_id = tenant_id
        self.system_role = system_role


@pytest_asyncio.fixture
async def engine(monkeypatch):
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(
            Base.metadata.create_all,
            tables=[
                DealRecord.__table__,
                CustomerRecord.__table__,
                TaskRecord.__table__,
            ],
        )
    factory = async_sessionmaker(engine, expire_on_commit=False)

    async with factory() as session:
        session.add(
            DealRecord(
                id=VICTIM_DEAL,
                tenant_id=VICTIM_TENANT,
                lead_id="lead_of_b",
                stage="payment_requested",
                amount=1000.0,
            )
        )
        await session.commit()

    # The router builds its own sessions via async_session_factory().
    monkeypatch.setattr(autonomous, "async_session_factory", lambda: factory)
    yield factory
    await engine.dispose()


def _client(user: _User) -> AsyncClient:
    app = FastAPI()
    app.include_router(autonomous.router)
    app.dependency_overrides[get_current_user] = lambda: user
    return AsyncClient(transport=ASGITransport(app=app), base_url="http://test")


@pytest.mark.asyncio
async def test_mark_paid_cannot_touch_another_tenants_deal(engine):
    async with _client(_User(ATTACKER_TENANT)) as client:
        response = await client.post(
            "/api/v1/payments/mark-paid",
            json={"deal_id": VICTIM_DEAL, "amount": 999999},
        )

    assert response.status_code == 404

    async with engine() as session:
        deal = await session.get(DealRecord, VICTIM_DEAL)
        assert deal.stage == "payment_requested"
        assert deal.amount == 1000.0


@pytest.mark.asyncio
async def test_mark_paid_serves_the_owning_tenant(engine):
    async with _client(_User(VICTIM_TENANT)) as client:
        response = await client.post(
            "/api/v1/payments/mark-paid", json={"deal_id": VICTIM_DEAL}
        )

    assert response.status_code == 200

    async with engine() as session:
        deal = await session.get(DealRecord, VICTIM_DEAL)
        assert deal.stage == "paid"


@pytest.mark.asyncio
async def test_update_deal_cannot_touch_another_tenants_deal(engine):
    async with _client(_User(ATTACKER_TENANT)) as client:
        response = await client.patch(
            f"/api/v1/deals/{VICTIM_DEAL}", json={"stage": "paid", "amount": 1}
        )

    assert response.status_code == 404

    async with engine() as session:
        deal = await session.get(DealRecord, VICTIM_DEAL)
        assert deal.stage == "payment_requested"


@pytest.mark.asyncio
async def test_payment_request_cannot_touch_another_tenants_deal(engine):
    async with _client(_User(ATTACKER_TENANT)) as client:
        response = await client.post(
            "/api/v1/payments/manual-request", json={"deal_id": VICTIM_DEAL}
        )

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_declaring_the_victim_tenant_does_not_widen_access(engine):
    async with _client(_User(ATTACKER_TENANT)) as client:
        response = await client.post(
            "/api/v1/payments/mark-paid",
            json={"deal_id": VICTIM_DEAL, "tenant_id": VICTIM_TENANT},
        )

    assert response.status_code == 403


@pytest.mark.asyncio
async def test_listing_never_spans_tenants(engine):
    async with _client(_User(ATTACKER_TENANT)) as client:
        response = await client.get("/api/v1/deals")

    assert response.status_code == 200
    assert response.json()["items"] == []


def test_deal_routes_require_authentication():
    protected = {
        ("PATCH", "/api/v1/deals/{deal_id}"),
        ("GET", "/api/v1/deals"),
        ("POST", "/api/v1/payments/manual-request"),
        ("POST", "/api/v1/payments/mark-paid"),
    }
    found = {}
    for route in autonomous.router.routes:
        for method in route.methods:
            found[(method, route.path)] = {
                dep.call for dep in route.dependant.dependencies
            }

    for key in protected:
        assert key in found, f"route missing from the router: {key}"
        assert get_current_user in found[key], f"{key[0]} {key[1]} is unauthenticated"
