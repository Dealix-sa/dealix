"""Tests for the Billing Gateway API (Moyasar sandbox)."""

from __future__ import annotations

import pytest

from api.routers.billing_gateway import (
    PaymentLinkRequest,
    WebhookEvent,
    apply_webhook_event,
    create_payment_link,
    get_invoice,
    simulate_payment_success,
    _new_payment_id,
    _invoices,
)


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------


def _make_request(
    amount_sar: float = 499.0,
    tier: str = "sprint_499",
) -> PaymentLinkRequest:
    return PaymentLinkRequest(
        client_name="Test Client",
        client_email="test@example.com",
        amount_sar=amount_sar,
        description="Test payment",
        offer_tier=tier,
    )


# ---------------------------------------------------------------------------
# Unit tests
# ---------------------------------------------------------------------------


def test_payment_id_format() -> None:
    pid = _new_payment_id()
    assert pid.startswith("pay_")
    assert len(pid) > 8


def test_create_payment_link_returns_record() -> None:
    req = _make_request()
    record = create_payment_link(req)
    assert record["status"] == "pending"
    assert record["amount_sar"] == 499.0
    assert record["offer_tier"] == "sprint_499"
    assert "checkout_url" in record
    assert "payment_id" in record


def test_created_link_stored_in_invoices() -> None:
    req = _make_request(amount_sar=1500.0, tier="data_pack_1500")
    record = create_payment_link(req)
    pid = record["payment_id"]
    assert get_invoice(pid) is not None
    assert get_invoice(pid)["amount_sar"] == 1500.0


def test_get_invoice_unknown_returns_none() -> None:
    result = get_invoice("pay_does_not_exist_xyz")
    assert result is None


def test_checkout_url_contains_payment_id() -> None:
    req = _make_request()
    record = create_payment_link(req)
    assert record["payment_id"] in record["checkout_url"]


def test_webhook_event_updates_status() -> None:
    req = _make_request(amount_sar=2999.0, tier="managed_ops")
    record = create_payment_link(req)
    pid = record["payment_id"]

    event = WebhookEvent(
        event_type="payment.paid",
        payment_id=pid,
        amount=2999.0,
        status="paid",
    )
    updated = apply_webhook_event(event)
    assert updated is not None
    assert updated["status"] == "paid"
    assert updated["last_webhook_event"] == "payment.paid"


def test_webhook_unknown_payment_returns_none() -> None:
    event = WebhookEvent(
        event_type="payment.paid",
        payment_id="pay_nonexistent_xyz",
        amount=100.0,
        status="paid",
    )
    result = apply_webhook_event(event)
    assert result is None


def test_simulate_success_marks_paid() -> None:
    req = _make_request(amount_sar=499.0)
    record = create_payment_link(req)
    pid = record["payment_id"]

    updated = simulate_payment_success(pid)
    assert updated is not None
    assert updated["status"] == "paid"
    assert "paid_at" in updated


def test_simulate_success_unknown_returns_none() -> None:
    result = simulate_payment_success("pay_ghost_xyz")
    assert result is None


def test_multiple_tiers_stored_independently() -> None:
    tiers = [
        ("sprint_499", 499.0),
        ("data_pack_1500", 1500.0),
        ("managed_ops", 2999.0),
    ]
    ids = []
    for tier, amount in tiers:
        req = _make_request(amount_sar=amount, tier=tier)
        record = create_payment_link(req)
        ids.append(record["payment_id"])

    # All stored separately
    assert len(set(ids)) == 3
    for pid in ids:
        assert get_invoice(pid) is not None
