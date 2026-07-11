"""Fail-closed regression tests for canonical deal intelligence."""

from __future__ import annotations

from datetime import date

import pytest

from dealix.deal_intelligence import DealEvent, DealRecord, DealStage, analyze_deal, compute_portfolio, next_action

TODAY = date(2026, 7, 11)


def _deal(*events: str, source: str = "inbound", value_sar: int = 499) -> DealRecord:
    return DealRecord(
        deal_id="deal-fail-closed",
        account_name="Approved Client",
        source=source,
        value_sar=value_sar,
        created_at="2026-07-01",
        last_touch_at="2026-07-10",
        events=tuple(
            DealEvent(event_type=event, occurred_at=f"2026-07-{index + 2:02d}")
            for index, event in enumerate(events)
        ),
    )


def test_unknown_event_type_is_rejected_instead_of_silently_ignored() -> None:
    with pytest.raises(ValueError, match="event_type must be one of"):
        DealEvent(event_type="paymant_received", occurred_at="2026-07-02")


def test_payment_without_contact_permission_does_not_recognize_revenue() -> None:
    deal = _deal("invoice_sent", "payment_received", source="public_web_research", value_sar=25_000)

    snapshot = analyze_deal(deal, TODAY)
    _, metrics = compute_portfolio([deal], TODAY)

    assert snapshot.stage == DealStage.RESEARCH_HOLD
    assert snapshot.valid_payment is False
    assert "commercial_event_without_permission:invoice_sent" in snapshot.anomalies
    assert "payment_without_permission" in snapshot.anomalies
    assert metrics.recognized_revenue_sar == 0
    assert next_action(snapshot).action_key == "repair_evidence_chain"


def test_lost_after_payment_is_excluded_from_recognized_revenue() -> None:
    deal = _deal("invoice_sent", "payment_received", "lost", value_sar=7_500)

    snapshot = analyze_deal(deal, TODAY)
    _, metrics = compute_portfolio([deal], TODAY)

    assert snapshot.stage == DealStage.LOST
    assert snapshot.valid_payment is True
    assert snapshot.close_ready is False
    assert "lost_after_valid_payment" in snapshot.anomalies
    assert metrics.recognized_revenue_sar == 0
    assert next_action(snapshot).action_key == "repair_evidence_chain"


def test_events_after_lost_are_flagged_and_do_not_reopen_deal() -> None:
    snapshot = analyze_deal(
        _deal("lost", "invoice_sent", "payment_received", "proof_pack_delivered"),
        TODAY,
    )

    assert snapshot.stage == DealStage.LOST
    assert snapshot.valid_payment is False
    assert snapshot.proof_delivered is False
    assert "event_after_lost:invoice_sent" in snapshot.anomalies
    assert "event_after_lost:payment_received" in snapshot.anomalies
    assert "event_after_lost:proof_pack_delivered" in snapshot.anomalies
