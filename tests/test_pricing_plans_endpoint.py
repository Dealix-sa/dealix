"""Commercial trust tests for public pricing, checkout, and usage recording.

The launch surfaces fail closed until the founder approves #917. No real
database, Redis, or payment-provider call is required.
"""
from __future__ import annotations

import pytest

from api.routers.pricing import ALLOWED_PLANS


@pytest.mark.asyncio
async def test_public_pricing_fails_closed_by_default(async_client):
    res = await async_client.get("/api/v1/pricing/plans")
    assert res.status_code == 200
    body = res.json()
    assert body == {
        "currency": "SAR",
        "plans": {},
        "public_pricing_enabled": False,
        "status": "founder_approval_required",
    }


@pytest.mark.asyncio
async def test_public_pricing_requires_explicit_approved_ids(
    async_client, monkeypatch: pytest.MonkeyPatch
):
    monkeypatch.setenv("DEALIX_PUBLIC_PRICING_ENABLED", "true")
    monkeypatch.setenv(
        "DEALIX_PUBLIC_PLAN_IDS",
        "starter,pilot_1sar,unknown_plan",
    )
    res = await async_client.get("/api/v1/pricing/plans")
    body = res.json()
    assert body["public_pricing_enabled"] is True
    assert body["status"] == "approved"
    assert set(body["plans"]) == {"starter"}
    assert "pilot_1sar" not in body["plans"]


def test_test_plan_is_never_a_normal_checkout_plan():
    assert "pilot_1sar" not in ALLOWED_PLANS


@pytest.mark.asyncio
async def test_checkout_fails_closed_before_provider_call(async_client):
    res = await async_client.post(
        "/api/v1/checkout",
        json={"plan": "starter", "email": "founder@example.com"},
    )
    assert res.status_code == 503
    assert res.json()["detail"] == "checkout_not_founder_approved"


@pytest.mark.asyncio
async def test_1sar_plan_requires_separate_nonproduction_gate(
    async_client, monkeypatch: pytest.MonkeyPatch
):
    monkeypatch.setenv("DEALIX_CHECKOUT_ENABLED", "true")
    monkeypatch.delenv("DEALIX_ENABLE_1SAR_CHECKOUT", raising=False)
    res = await async_client.post(
        "/api/v1/checkout",
        json={"plan": "pilot_1sar", "email": "founder@example.com"},
    )
    assert res.status_code == 400
    assert res.json()["detail"] == "test_plan_disabled"


@pytest.mark.asyncio
async def test_1sar_plan_is_impossible_in_production(
    async_client, monkeypatch: pytest.MonkeyPatch
):
    monkeypatch.setenv("DEALIX_CHECKOUT_ENABLED", "true")
    monkeypatch.setenv("DEALIX_ENABLE_1SAR_CHECKOUT", "true")
    monkeypatch.setenv("APP_ENV", "production")
    res = await async_client.post(
        "/api/v1/checkout",
        json={"plan": "pilot_1sar", "email": "founder@example.com"},
    )
    assert res.status_code == 400
    assert res.json()["detail"] == "test_plan_disabled"


@pytest.mark.asyncio
async def test_pricing_menu_reports_not_sales_ready_by_default(async_client):
    res = await async_client.get("/api/v1/pricing/menu")
    assert res.status_code == 200
    body = res.json()
    assert body["currency"] == "SAR"
    assert body["sales_ready"] is False
    assert body["checkout_status"] == "founder_approval_required"
    assert "pilot_1sar" not in body["plans"]
    assert isinstance(body["service_catalog"], list)
    assert body["service_catalog"]


@pytest.mark.asyncio
async def test_usage_record_requires_metered_plan(async_client):
    res = await async_client.post(
        "/api/v1/pricing/usage",
        json={"plan": "growth", "customer_handle": "acme", "event_id": "x1"},
    )
    assert res.status_code == 400
    assert "metered" in res.json()["detail"].lower()


@pytest.mark.asyncio
async def test_usage_record_requires_event_id(async_client):
    res = await async_client.post(
        "/api/v1/pricing/usage",
        json={"plan": "laas_per_reply", "customer_handle": "acme"},
    )
    assert res.status_code == 400
    assert "event_id" in res.json()["detail"]


@pytest.mark.asyncio
async def test_usage_record_idempotent(async_client):
    payload = {
        "plan": "laas_per_reply",
        "customer_handle": "test_handle_idem",
        "event_id": "test_msg_001",
    }
    res1 = await async_client.post("/api/v1/pricing/usage", json=payload)
    assert res1.status_code == 200
    assert res1.json()["status"] == "recorded"
    res2 = await async_client.post("/api/v1/pricing/usage", json=payload)
    assert res2.status_code == 200
    assert res2.json()["status"] == "duplicate"
    assert res1.json()["amount_halalas"] == res2.json()["amount_halalas"]
