"""The billing API must exist, and must not serve another tenant's money.

``api/routers/billing.py`` was a complete SaaS billing surface — subscribe,
upgrade, cancel, invoices, pay, features — with authentication and tenant
scoping on every route. It was imported nowhere, so **none of its routes were
mounted**: the product had no billing API at all. Three tests in
``test_saas_billing_onboarding.py`` exercise those paths, but they are xfailed
for a missing PostgreSQL, which is true and which also hid the 404s
underneath.

Mounting it surfaced why dead code rots: the module annotates its response
models with ``datetime`` under ``from __future__ import annotations`` and
never imported it, so building the OpenAPI schema raised
``PydanticUserError: ... is not fully defined`` and took the whole app with
it. Nothing had ever built those schemas.

These tests use an in-memory SQLite database and override the auth dependency,
so they run everywhere rather than xfailing on a database that CI does not
have. A route that only a PostgreSQL-equipped machine can check is a route
nobody checks.
"""

from __future__ import annotations

import uuid

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from db.models import Base
from db.models_subscription import (
    FeatureFlagRecord,
    InvoiceRecord,
    PlanRecord,
    SubscriptionRecord,
)

TENANT_A = "tnt_buyer"
TENANT_B = "tnt_victim"


class _User:
    """Minimal stand-in for the authenticated user the router reads."""

    def __init__(self, tenant_id: str | None) -> None:
        self.id = f"usr_{uuid.uuid4().hex[:8]}"
        self.tenant_id = tenant_id
        self.email = "buyer@example.com"
        self.name = "Buyer"
        self.system_role = "member"


@pytest_asyncio.fixture
async def db_session() -> AsyncSession:
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        # Only the billing tables: creating the whole metadata fails on SQLite
        # once any test has imported a model with a PostgreSQL-only column.
        await conn.run_sync(
            Base.metadata.create_all,
            tables=[
                PlanRecord.__table__,
                SubscriptionRecord.__table__,
                InvoiceRecord.__table__,
                # subscribe() writes plan-derived feature flags
                FeatureFlagRecord.__table__,
            ],
        )
    factory = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    async with factory() as session:
        yield session
    await engine.dispose()


@pytest_asyncio.fixture
async def seeded(db_session):
    """One public plan, and one invoice belonging to the *victim* tenant."""
    plan = PlanRecord(
        id="pln_starter",
        slug="starter",
        name_en="Starter",
        name_ar="المبتدئ",
        price_sar_monthly=299.0,
        is_public=True,
        is_custom=False,
        sort_order=1,
        features={"crm": True},
    )
    victim_invoice = InvoiceRecord(
        id="inv_victim",
        tenant_id=TENANT_B,
        invoice_number="INV-VICTIM-001",
        status="open",
        total_sar=25000.0,
    )
    db_session.add_all([plan, victim_invoice])
    await db_session.commit()
    return {"plan": plan, "victim_invoice": victim_invoice}


@pytest_asyncio.fixture
async def client(db_session, monkeypatch):
    """App with the DB and the authenticated user swapped for test doubles."""
    from api.main import app
    from api.security.auth_deps import get_current_user
    from db.session import get_db as get_db_session

    monkeypatch.setenv("API_KEYS", "")
    monkeypatch.setenv("ADMIN_API_KEYS", "")

    app.dependency_overrides[get_db_session] = lambda: db_session
    app.dependency_overrides[get_current_user] = lambda: _User(TENANT_A)
    try:
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as ac:
            yield ac
    finally:
        app.dependency_overrides.clear()


# ── The routes exist at all ───────────────────────────────────────────────


BILLING_ROUTES = [
    ("GET", "/api/v1/billing/plans"),
    ("GET", "/api/v1/billing/subscription"),
    ("POST", "/api/v1/billing/subscribe"),
    ("POST", "/api/v1/billing/upgrade"),
    ("POST", "/api/v1/billing/cancel"),
    ("GET", "/api/v1/billing/invoices"),
    ("POST", "/api/v1/billing/invoices/{invoice_id}/pay"),
    ("GET", "/api/v1/billing/features"),
]


@pytest.mark.parametrize(("method", "path"), BILLING_ROUTES)
def test_route_is_mounted(method, path):
    """The regression: every one of these was a 404 because nothing imported
    the router. A SaaS product with no billing API cannot be sold."""
    from api.main import app

    mounted = {
        (m, route_path)
        for route_path, ops in app.openapi()["paths"].items()
        for m in (op.upper() for op in ops)
    }

    assert (method, path) in mounted, f"{method} {path} is not mounted"


def test_openapi_schema_builds():
    """Mounting the router used to crash schema generation outright.

    `datetime` was used in the response models but never imported, and under
    `from __future__ import annotations` pydantic could not resolve it. This
    fails loudly if the import is dropped again.
    """
    from api.main import app

    schema = app.openapi()

    assert "/api/v1/billing/subscription" in schema["paths"]
    assert "SubscriptionOut" in schema["components"]["schemas"]


# ── Tenant isolation ──────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_invoice_list_shows_only_the_callers_tenant(client, seeded):
    resp = await client.get("/api/v1/billing/invoices")

    assert resp.status_code == 200, resp.text
    numbers = [row["invoice_number"] for row in resp.json()]
    assert "INV-VICTIM-001" not in numbers, "another tenant's invoice was listed"


@pytest.mark.asyncio
async def test_paying_another_tenants_invoice_is_refused(client, seeded):
    """The invoice id is a caller-supplied handle; ownership must be checked."""
    resp = await client.post("/api/v1/billing/invoices/inv_victim/pay")

    assert resp.status_code == 404, (
        f"a tenant generated a payment link for another tenant's invoice: {resp.text}"
    )


@pytest.mark.asyncio
async def test_a_user_with_no_tenant_is_refused(db_session, seeded, monkeypatch):
    from api.main import app
    from api.security.auth_deps import get_current_user
    from db.session import get_db as get_db_session

    monkeypatch.setenv("API_KEYS", "")
    app.dependency_overrides[get_db_session] = lambda: db_session
    app.dependency_overrides[get_current_user] = lambda: _User(None)
    try:
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as ac:
            resp = await ac.get("/api/v1/billing/invoices")
    finally:
        app.dependency_overrides.clear()

    assert resp.status_code == 400, resp.text


# ── Money comes from the server, not the request ──────────────────────────


@pytest.mark.asyncio
async def test_subscribe_prices_from_the_plan_record(client, seeded):
    """`plan_slug` is a name, not an amount — the price is looked up here."""
    resp = await client.post(
        "/api/v1/billing/subscribe",
        json={"plan_slug": "starter", "billing_cycle": "monthly", "seat_count": 2},
    )

    assert resp.status_code == 200, resp.text
    assert resp.json()["plan_id"] == "pln_starter"


@pytest.mark.asyncio
async def test_subscribing_to_an_unknown_plan_is_refused(client, seeded):
    resp = await client.post(
        "/api/v1/billing/subscribe",
        json={"plan_slug": "does-not-exist", "billing_cycle": "monthly"},
    )

    assert resp.status_code == 404, resp.text


# ── The payment return destination ────────────────────────────────────────


@pytest.mark.asyncio
async def test_pay_invoice_sends_the_customer_to_an_absolute_return_url(
    db_session, seeded, monkeypatch
):
    """``callback_url`` is where the *customer's browser* goes after paying.

    It used to be the relative string ``/api/v1/webhooks/moyasar`` — wrong
    twice over: a relative URL is not somewhere Moyasar can redirect to, and
    the webhook is a POST-only JSON API, so a customer who had just paid
    landed on an error.

    Asserted against the value actually handed to the payment client rather
    than by grepping the source, so a comment mentioning the old URL cannot
    make this pass or fail.
    """
    from api.main import app
    from api.routers import billing
    from api.security.auth_deps import get_current_user
    from db.session import get_db as get_db_session

    monkeypatch.setenv("API_KEYS", "")
    monkeypatch.setenv("APP_URL", "https://api.dealix.me")

    own_invoice = InvoiceRecord(
        id="inv_own",
        tenant_id=TENANT_A,
        invoice_number="INV-OWN-001",
        status="open",
        total_sar=299.0,
    )
    db_session.add(own_invoice)
    await db_session.commit()

    captured: dict[str, object] = {}

    async def _fake_link(req):
        captured["callback_url"] = req.callback_url
        captured["amount_halalas"] = req.amount_halalas

        class _Link:
            invoice_id = "inv_moyasar"
            payment_url = "https://moyasar.test/pay/abc"

        return _Link()

    monkeypatch.setattr(billing, "create_moyasar_payment_link", _fake_link)

    app.dependency_overrides[get_db_session] = lambda: db_session
    app.dependency_overrides[get_current_user] = lambda: _User(TENANT_A)
    try:
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as ac:
            resp = await ac.post("/api/v1/billing/invoices/inv_own/pay")
    finally:
        app.dependency_overrides.clear()

    assert resp.status_code == 200, resp.text
    callback = str(captured["callback_url"])
    assert callback.startswith("https://"), f"return URL is not absolute: {callback}"
    assert "/webhooks/" not in callback, (
        f"the customer is redirected to a webhook endpoint: {callback}"
    )
    assert callback == "https://api.dealix.me/checkout/return"
    # The charge comes from the stored invoice, never from the request.
    assert captured["amount_halalas"] == 29900
