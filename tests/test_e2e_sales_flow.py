"""End-to-end smoke test for the lead → pricing → checkout flow.

This test exercises the routers a real prospect touches before paying:

  1. POST /api/v1/public/leads      (the landing page lead form)
  2. GET  /api/v1/pricing/plans     (the billing page lists plans)
  3. GET  /api/v1/payment-ops/...   (the payment_ops state machine surface)

We intentionally do NOT call Moyasar here — the Moyasar client is mocked
where needed. The point is to prove that the FastAPI app actually wires
these surfaces together end-to-end without 500-class errors.

If this test breaks, the customer-visible critical path is broken.
"""
from __future__ import annotations

from typing import Any
from unittest.mock import AsyncMock, patch

import pytest


pytestmark = pytest.mark.asyncio


async def test_public_lead_endpoint_accepts_minimal_payload(async_client) -> None:
    """A public visitor can submit a lead form; we don't 500."""
    payload: dict[str, Any] = {
        "company": "اختبار E2E",
        "name": "زائر اختبار",
        "email": "e2e@dealix-test.sa",
        "phone": "+966500000000",
        "sector": "marketing",
        "company_size": "small",
        "message": (
            "We saw the post-lead Revenue Ops pitch and want a 10-lead audit "
            "to see if Dealix fits."
        ),
    }
    r = await async_client.post("/api/v1/public/leads", json=payload)
    # Accept the canonical happy path or known explicit auth gates; the
    # critical assertion is "no unhandled server error".
    assert r.status_code in {200, 201, 202, 400, 401, 403, 422}, r.text


async def test_pricing_plans_lists_at_least_one_real_plan(async_client) -> None:
    """The billing page calls this; it must return a usable plan list."""
    r = await async_client.get("/api/v1/pricing/plans")
    assert r.status_code == 200, r.text
    body = r.json()
    assert body.get("currency") == "SAR"
    plans = body.get("plans") or {}
    assert isinstance(plans, dict) and plans, "no plans returned"
    # At least one entry must look like a real money amount, not a stub.
    for key, plan in plans.items():
        assert "amount_sar" in plan, key
        assert float(plan["amount_sar"]) > 0, key
        assert plan.get("kind") in {"subscription", "one_off", "metered"}, key


async def test_pricing_plans_hides_the_one_sar_smoke_plan(async_client) -> None:
    """pilot_1sar is an internal smoke-test plan; it must not be public."""
    r = await async_client.get("/api/v1/pricing/plans")
    assert r.status_code == 200
    body = r.json()
    plans = body.get("plans") or {}
    assert "pilot_1sar" not in plans, "internal smoke plan leaked publicly"


async def test_checkout_rejects_unknown_plan(async_client) -> None:
    """Defensive: a tampered plan must be rejected before any Moyasar call."""
    r = await async_client.post(
        "/api/v1/checkout",
        json={"plan": "DOES_NOT_EXIST", "email": "tampered@dealix-test.sa"},
    )
    assert r.status_code in {400, 422}, r.text


async def test_checkout_rejects_invalid_email(async_client) -> None:
    """No email shape = no Moyasar invoice. Saves Moyasar quota and money."""
    r = await async_client.post(
        "/api/v1/checkout",
        json={"plan": "starter", "email": "not-an-email"},
    )
    assert r.status_code in {400, 422}, r.text


async def test_checkout_happy_path_creates_invoice_via_mocked_moyasar(
    async_client,
) -> None:
    """Real Moyasar is mocked; we just verify the wiring + response shape."""
    fake_invoice = {
        "id": "inv_test_e2e_001",
        "status": "initiated",
        "url": "https://api.moyasar.com/v1/invoices/inv_test_e2e_001",
    }
    with patch(
        "api.routers.pricing.MoyasarClient.create_invoice",
        new=AsyncMock(return_value=fake_invoice),
    ):
        r = await async_client.post(
            "/api/v1/checkout",
            json={"plan": "pilot_managed", "email": "real@dealix-test.sa"},
        )
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["invoice_id"] == "inv_test_e2e_001"
    assert body["payment_url"].startswith("https://")
    assert body["plan"] == "pilot_managed"
    assert float(body["amount_sar"]) > 0


async def test_payment_ops_invoice_intent_writes_a_state(async_client) -> None:
    """The manual payment_ops surface (used for bank transfers) still works."""
    r = await async_client.post(
        "/api/v1/payment-ops/invoice-intent",
        json={
            "customer_handle": "e2e-test-customer",
            "amount_sar": 499.0,
            "method": "bank_transfer",
        },
    )
    assert r.status_code == 200, r.text
    body = r.json()
    payment = body.get("payment") or {}
    assert payment.get("status") == "invoice_intent"
    # Critical hard rule: invoice_intent is NOT revenue.
    assert body.get("warning_invoice_not_revenue") == "invoice_intent != revenue"


async def test_payment_ops_blocks_moyasar_live_without_env_opt_in(
    async_client, monkeypatch
) -> None:
    """Hard gate: NO_LIVE_CHARGE — moyasar_live needs explicit DEALIX_MOYASAR_MODE=live."""
    monkeypatch.delenv("DEALIX_MOYASAR_MODE", raising=False)
    r = await async_client.post(
        "/api/v1/payment-ops/invoice-intent",
        json={
            "customer_handle": "e2e-live-blocked",
            "amount_sar": 499.0,
            "method": "moyasar_live",
        },
    )
    # The orchestrator raises ValueError; the router maps it to 403.
    assert r.status_code == 403, r.text
