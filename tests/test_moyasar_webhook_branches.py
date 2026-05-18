"""Moyasar webhook — explicit per-event-type dispatch branches.

Covers the B2 dispatch added to ``moyasar_webhook``:
  * payment_paid     -> records an L5 revenue proof event
  * payment_failed   -> sets payments.status / error_reason (no proof event)
  * payment_refunded -> flips payments.status (no proof event)
  * invoice_created  -> recorded only, NOT revenue (no proof event)

All bodies carry a valid ``secret_token`` so they pass signature
verification. ``_set_payment_status`` returns False without a real DB,
which is fine — these tests assert the dispatch outcome + proof-ledger
side effects, not DB persistence.
"""
from __future__ import annotations

from unittest.mock import patch

import pytest

_SECRET = "whsec_branch_test"


def _signed_body(event_id: str, event_type: str, payment: dict | None = None) -> dict:
    return {
        "id": event_id,
        "type": event_type,
        "secret_token": _SECRET,
        "data": {"object": "payment", **(payment or {})},
    }


@pytest.mark.asyncio
async def test_payment_paid_records_l5_proof_event(
    async_client, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("MOYASAR_WEBHOOK_SECRET", _SECRET)
    recorded: list = []

    class _FakeLedger:
        def record(self, event):  # noqa: ANN001
            recorded.append(event)
            return event

    body = _signed_body(
        "evt_paid_1",
        "payment_paid",
        {"id": "pay_paid_1", "status": "paid", "amount": 100,
         "currency": "SAR", "metadata": {"plan": "pilot_1sar"}},
    )
    with patch(
        "auto_client_acquisition.proof_ledger.factory.get_default_ledger",
        return_value=_FakeLedger(),
    ):
        res = await async_client.post("/api/v1/webhooks/moyasar", json=body)

    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "ok"
    assert data["handled"] == "revenue_confirmed"
    assert len(recorded) == 1
    ev = recorded[0]
    assert ev.level == "L5"
    assert ev.customer_visible is False
    assert ev.publish_consent is False
    assert ev.approved_by is None


@pytest.mark.asyncio
async def test_payment_captured_also_records_revenue(
    async_client, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("MOYASAR_WEBHOOK_SECRET", _SECRET)
    body = _signed_body(
        "evt_cap_1", "payment_captured",
        {"id": "pay_cap_1", "status": "captured", "amount": 100},
    )
    res = await async_client.post("/api/v1/webhooks/moyasar", json=body)
    assert res.status_code == 200
    assert res.json()["handled"] == "revenue_confirmed"


@pytest.mark.asyncio
async def test_payment_failed_branch_no_proof_event(
    async_client, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("MOYASAR_WEBHOOK_SECRET", _SECRET)
    recorded: list = []

    class _FakeLedger:
        def record(self, event):  # noqa: ANN001
            recorded.append(event)
            return event

    body = _signed_body(
        "evt_failed_1", "payment_failed",
        {"id": "pay_failed_1", "status": "failed",
         "source": {"message": "insufficient funds"}},
    )
    with patch(
        "auto_client_acquisition.proof_ledger.factory.get_default_ledger",
        return_value=_FakeLedger(),
    ):
        res = await async_client.post("/api/v1/webhooks/moyasar", json=body)

    assert res.status_code == 200
    assert res.json()["handled"] == "failed"
    # A failed payment is NOT revenue — no proof event recorded.
    assert recorded == []


@pytest.mark.asyncio
async def test_payment_refunded_branch_no_proof_event(
    async_client, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("MOYASAR_WEBHOOK_SECRET", _SECRET)
    recorded: list = []

    class _FakeLedger:
        def record(self, event):  # noqa: ANN001
            recorded.append(event)
            return event

    body = _signed_body(
        "evt_refund_1", "payment_refunded",
        {"id": "pay_refund_1", "status": "refunded", "amount": 100},
    )
    with patch(
        "auto_client_acquisition.proof_ledger.factory.get_default_ledger",
        return_value=_FakeLedger(),
    ):
        res = await async_client.post("/api/v1/webhooks/moyasar", json=body)

    assert res.status_code == 200
    assert res.json()["handled"] == "refunded"
    assert recorded == []


@pytest.mark.asyncio
async def test_invoice_created_is_not_revenue(
    async_client, monkeypatch: pytest.MonkeyPatch
) -> None:
    """invoice_created != revenue — recorded only, no proof event."""
    monkeypatch.setenv("MOYASAR_WEBHOOK_SECRET", _SECRET)
    recorded: list = []

    class _FakeLedger:
        def record(self, event):  # noqa: ANN001
            recorded.append(event)
            return event

    body = _signed_body(
        "evt_inv_1", "invoice_created",
        {"id": "inv_1", "status": "initiated", "amount": 100},
    )
    with patch(
        "auto_client_acquisition.proof_ledger.factory.get_default_ledger",
        return_value=_FakeLedger(),
    ):
        res = await async_client.post("/api/v1/webhooks/moyasar", json=body)

    assert res.status_code == 200
    assert res.json()["handled"] == "recorded"
    assert recorded == []
