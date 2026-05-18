"""Checkout endpoint — provider-error (502) and happy-path coverage.

The Moyasar HTTP client is mocked so these tests need no live keys and
exercise the two branches of ``POST /api/v1/checkout``:
  * ``create_invoice`` raises an account_inactive_error -> HTTP 502
  * ``create_invoice`` returns an invoice object        -> HTTP 200
"""
from __future__ import annotations

from unittest.mock import AsyncMock, patch

import pytest


@pytest.mark.asyncio
async def test_checkout_returns_502_when_account_inactive(async_client) -> None:
    """A Moyasar account_inactive_error must surface as a clean 502, not a 500."""
    err = RuntimeError("account_inactive_error: merchant verification pending")
    with patch(
        "api.routers.pricing.MoyasarClient.create_invoice",
        new=AsyncMock(side_effect=err),
    ):
        res = await async_client.post(
            "/api/v1/checkout",
            json={"plan": "pilot_1sar", "email": "buyer@example.com"},
        )
    assert res.status_code == 502
    assert res.json().get("detail") == "payment_provider_error"


@pytest.mark.asyncio
async def test_checkout_happy_path_returns_invoice(async_client) -> None:
    """A successful create_invoice returns the invoice id + payment url."""
    invoice = {
        "id": "inv_test_abc123",
        "status": "initiated",
        "url": "https://pay.moyasar.test/inv_test_abc123",
    }
    with patch(
        "api.routers.pricing.MoyasarClient.create_invoice",
        new=AsyncMock(return_value=invoice),
    ):
        res = await async_client.post(
            "/api/v1/checkout",
            json={"plan": "pilot_1sar", "email": "buyer@example.com"},
        )
    assert res.status_code == 200
    data = res.json()
    assert data["invoice_id"] == "inv_test_abc123"
    assert data["payment_url"] == "https://pay.moyasar.test/inv_test_abc123"
    assert data["plan"] == "pilot_1sar"
    assert data["amount_sar"] == 1.0


@pytest.mark.asyncio
async def test_checkout_rejects_unknown_plan(async_client) -> None:
    res = await async_client.post(
        "/api/v1/checkout",
        json={"plan": "no_such_plan", "email": "buyer@example.com"},
    )
    assert res.status_code == 400
