"""HTTP integration coverage for api/routers/offers_checkout.

Drives the FastAPI surface end-to-end with a stubbed Moyasar factory so
the router lines are exercised and counted by --cov=api in CI. No real
network IO.
"""

from __future__ import annotations

from typing import Any

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient


def _make_app(*, enabled: bool, fail_factory: bool = False) -> TestClient:
    """Build a minimal FastAPI app wired to the offers_checkout router.

    The function ensures the feature flag is set BEFORE the router code
    reads it, then resets the service singleton so the stubbed factory
    is the one used.
    """
    # Apply flag via Settings cache invalidation rather than env so the
    # change is visible to the module's _feature_enabled() helper.
    import sys

    settings_mod = sys.modules["core.config.settings"]
    settings_mod.get_settings.cache_clear()
    if enabled:
        import os

        os.environ["OFFERS_SELF_SERVE_ENABLED"] = "true"
    else:
        import os as _os

        _os.environ.pop("OFFERS_SELF_SERVE_ENABLED", None)
    settings_mod.get_settings.cache_clear()

    from api.routers import offers_checkout as oc

    oc.reset_service_for_tests()

    async def _stub_factory(**kwargs: Any) -> dict[str, Any]:
        if fail_factory:
            raise RuntimeError("factory_misconfigured_for_test")
        return {"id": "inv_stub_1", "url": "https://moyasar.test/pay/inv_stub_1"}

    # Replace the real factory with the stub for this test instance.
    from dealix.payments.checkout import (
        InMemoryCheckoutStore,
        OfferCheckoutService,
    )

    oc._store = InMemoryCheckoutStore()
    oc._service = OfferCheckoutService(
        store=oc._store,
        hosted_payment_factory=_stub_factory,
        callback_base_url="https://api.dealix.test",
    )

    app = FastAPI()
    app.include_router(oc.router)
    return TestClient(app)


def test_catalog_endpoint_lists_five_offers():
    client = _make_app(enabled=False)  # catalog is always public
    r = client.get("/api/v1/offers/catalog")
    assert r.status_code == 200
    payload = r.json()
    assert len(payload["offers"]) == 5
    assert "diagnostic_free" in payload["allowed_offer_ids"]


def test_checkout_disabled_returns_503():
    client = _make_app(enabled=False)
    r = client.post(
        "/api/v1/offers/sprint_499/checkout",
        json={
            "source_passport_id": "p1",
            "lawful_basis": "consent",
            "consent_given": True,
        },
    )
    assert r.status_code == 503
    detail = r.json()["detail"]
    assert detail["error"] == "feature_disabled"
    assert "ar" in detail["reasons"]


def test_checkout_invalid_json_returns_400():
    client = _make_app(enabled=True)
    r = client.post(
        "/api/v1/offers/sprint_499/checkout",
        content=b"not json",
        headers={"Content-Type": "application/json"},
    )
    assert r.status_code == 400


def test_checkout_rejected_on_missing_passport_returns_422():
    client = _make_app(enabled=True)
    r = client.post(
        "/api/v1/offers/sprint_499/checkout",
        json={
            "source_passport_id": "",
            "lawful_basis": "consent",
            "consent_given": True,
        },
    )
    assert r.status_code == 422
    body = r.json()["detail"]
    assert body["status"] == "rejected"
    assert "source_passport_id_missing" in body["verdict"]["violation_codes"]


def test_checkout_free_diagnostic_returns_free():
    client = _make_app(enabled=True)
    r = client.post(
        "/api/v1/offers/diagnostic_free/checkout",
        json={
            "source_passport_id": "p_free",
            "lawful_basis": "consent",
            "consent_given": True,
        },
    )
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "free"
    assert body["hosted_payment_url"] is None


def test_checkout_sprint_returns_hosted_payment_url():
    client = _make_app(enabled=True)
    r = client.post(
        "/api/v1/offers/sprint_499/checkout",
        json={
            "source_passport_id": "p_sprint",
            "lawful_basis": "consent",
            "consent_given": True,
            "customer_handle": "ahmad",
            "locale": "ar",
        },
    )
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "ok"
    assert body["hosted_payment_url"].startswith("https://moyasar.test/pay/")
    assert body["amount_halalas"] == 49_900


def test_checkout_custom_ai_always_escalates():
    client = _make_app(enabled=True)
    r = client.post(
        "/api/v1/offers/custom_ai/checkout",
        json={
            "source_passport_id": "p_custom",
            "lawful_basis": "contract",
            "consent_given": False,
        },
    )
    assert r.status_code == 200
    assert r.json()["status"] == "escalated"


def test_checkout_misconfigured_factory_returns_500():
    client = _make_app(enabled=True, fail_factory=True)
    r = client.post(
        "/api/v1/offers/sprint_499/checkout",
        json={
            "source_passport_id": "p_misconfig",
            "lawful_basis": "consent",
            "consent_given": True,
        },
    )
    assert r.status_code == 500


@pytest.fixture(autouse=True)
def _cleanup_env():
    """Ensure the feature flag does not leak across tests."""
    yield
    import os
    import sys

    os.environ.pop("OFFERS_SELF_SERVE_ENABLED", None)
    settings_mod = sys.modules.get("core.config.settings")
    if settings_mod is not None:
        settings_mod.get_settings.cache_clear()
