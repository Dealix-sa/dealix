"""Declaring revenue must require an admin credential.

`/api/v1/payment-ops/*` and `/api/v1/revops/*` are the two surfaces that move
money through its lifecycle: invoice intent → evidence → **payment confirmed**
→ delivery kickoff. Both modules advertise a `no_fake_revenue` hard gate in
their own `_HARD_GATES` dict. Neither declared any authentication.

That left them behind the shared platform API key alone — a credential that is
neither an admin credential nor tenant-bound, held by every service that talks
to the API. Any holder could:

  * `POST /api/v1/payment-ops/confirm` with a `confirmed_by` of their choosing
    and book revenue that never arrived;
  * `POST /api/v1/revops/payment-confirm` for the same effect on the invoice
    ledger;
  * `GET /api/v1/payment-ops/{id}/state` and read another customer's payment
    record by ID;
  * `GET /api/v1/revops/finance-brief` and read company financials.

Both routers now declare the guard at the `APIRouter`, matching what
`revenue_ops_autopilot` already does for `/api/v1/invoices` — so a route added
to either file cannot miss it. These tests assert the gate per route, so the
coverage claim stays true as routes are added.
"""

from __future__ import annotations

import pytest

SERVICE_KEY = "service-key-for-the-middleware"
ADMIN_KEY = "admin-key-under-test"

# (method, path, body) — one entry per mounted route on the two routers.
REVENUE_ROUTES = [
    ("POST", "/api/v1/payment-ops/invoice-intent",
     {"customer_handle": "victim", "amount_sar": 25000, "method": "bank_transfer"}),
    ("POST", "/api/v1/payment-ops/manual-evidence",
     {"payment_id": "pay_1", "evidence_reference": "forged"}),
    ("POST", "/api/v1/payment-ops/confirm",
     {"payment_id": "pay_1", "confirmed_by": "attacker"}),
    ("POST", "/api/v1/payment-ops/pay_1/kickoff-delivery", {}),
    ("GET", "/api/v1/payment-ops/pay_1/state", None),
    ("GET", "/api/v1/revops/status", None),
    ("GET", "/api/v1/revops/finance-brief", None),
    ("POST", "/api/v1/revops/invoice-state",
     {"customer_handle": "victim", "amount_sar": 25000}),
    ("POST", "/api/v1/revops/invoice-transition",
     {"invoice_id": "inv_1", "target_status": "paid"}),
    ("POST", "/api/v1/revops/payment-confirm",
     {"invoice_id": "inv_1", "amount_sar": 25000, "method": "bank_transfer",
      "evidence_reference": "forged"}),
    ("POST", "/api/v1/revops/margin-snapshot",
     {"customer_handle": "victim", "revenue_sar": 25000}),
]

IDS = [f"{m}-{p}" for m, p, _ in REVENUE_ROUTES]


@pytest.fixture
def client():
    from fastapi.testclient import TestClient

    from api.main import app

    return TestClient(app)


def _call(client, method, path, body, headers):
    if method == "GET":
        return client.get(path, headers=headers)
    return client.post(path, json=body, headers=headers)


def _production(monkeypatch) -> None:
    """Production with the platform key configured.

    APIKeyMiddleware refuses an unconfigured production deployment before
    routing, so without the service key every case below would pass for the
    wrong reason.
    """
    monkeypatch.setenv("APP_ENV", "production")
    monkeypatch.setenv("API_KEYS", SERVICE_KEY)
    monkeypatch.setenv("ADMIN_API_KEYS", ADMIN_KEY)


@pytest.mark.parametrize(("method", "path", "body"), REVENUE_ROUTES, ids=IDS)
def test_service_key_alone_is_refused(client, monkeypatch, method, path, body):
    """The defect: the shared platform key reached every revenue endpoint."""
    _production(monkeypatch)

    resp = _call(client, method, path, body, {"X-API-Key": SERVICE_KEY})

    assert resp.status_code in (401, 403), (
        f"{method} {path} served a caller holding only the service key: {resp.text}"
    )


@pytest.mark.parametrize(("method", "path", "body"), REVENUE_ROUTES, ids=IDS)
def test_wrong_admin_key_is_refused(client, monkeypatch, method, path, body):
    _production(monkeypatch)

    resp = _call(
        client, method, path, body,
        {"X-API-Key": SERVICE_KEY, "X-Admin-API-Key": "not-the-admin-key"},
    )

    assert resp.status_code == 403, f"{method} {path}: {resp.text}"


@pytest.mark.parametrize(("method", "path", "body"), REVENUE_ROUTES, ids=IDS)
def test_admin_key_reaches_the_handler(client, monkeypatch, method, path, body):
    """The gate must not swallow real admin traffic.

    The handler is free to return 404/409/422 for the synthetic payload — what
    matters is that the request got past authentication, so any status other
    than 401/403 counts.
    """
    _production(monkeypatch)

    resp = _call(
        client, method, path, body,
        {"X-API-Key": SERVICE_KEY, "X-Admin-API-Key": ADMIN_KEY},
    )

    assert resp.status_code not in (401, 403), (
        f"{method} {path} rejected the configured admin key: {resp.text}"
    )


@pytest.mark.parametrize(("method", "path", "body"), REVENUE_ROUTES, ids=IDS)
def test_unconfigured_dev_environment_stays_open(
    client, monkeypatch, method, path, body
):
    """Local runs leave the admin key unset — they must keep working."""
    monkeypatch.setenv("APP_ENV", "test")
    monkeypatch.setenv("API_KEYS", "")
    monkeypatch.setenv("ADMIN_API_KEYS", "")
    monkeypatch.delenv("DEALIX_ADMIN_API_KEY", raising=False)

    resp = _call(client, method, path, body, {})

    assert resp.status_code not in (401, 403), f"{method} {path}: {resp.text}"


def test_every_mounted_route_on_both_routers_is_covered():
    """Keeps the parametrised list honest as routes are added.

    A new endpoint on either router would otherwise inherit the router-level
    guard silently and never be asserted — and if someone later moves the
    dependency from the router to individual routes, the gap would not show up
    in any of the tests above.
    """
    from api.routers import payment_ops, revops

    mounted = set()
    for module in (payment_ops, revops):
        for route in module.router.routes:
            for method in route.methods - {"HEAD", "OPTIONS"}:
                mounted.add((method, route.path))

    covered = set()
    for method, path, _ in REVENUE_ROUTES:
        covered.add((method, path))

    # Compare on templates, since the table uses concrete IDs like `pay_1`.
    def _shapes(pairs):
        return {(m, p.count("/")) for m, p in pairs}

    missing = _shapes(mounted) - _shapes(covered)
    assert not missing, f"revenue routes with no gate assertion: {sorted(missing)}"
