"""Tests for the canonical, non-sending deal intelligence core."""

from __future__ import annotations

from datetime import date
from pathlib import Path

import pytest

from dealix.deal_intelligence import (
    DealBook,
    DealBookError,
    DealEvent,
    DealRecord,
    DealStage,
    analyze_deal,
    compute_portfolio,
    load_book,
    next_action,
    save_book_atomic,
)

TODAY = date(2026, 7, 11)


def _deal(*events: str, source: str = "inbound", value_sar: int = 499) -> DealRecord:
    return DealRecord(
        deal_id="deal-1",
        account_name="Approved Client",
        source=source,
        value_sar=value_sar,
        created_at="2026-07-01",
        last_touch_at="2026-07-10",
        events=tuple(
            DealEvent(event_type=event, occurred_at=f"2026-07-{index + 1:02d}")
            for index, event in enumerate(events)
        ),
    )


def test_valid_evidence_chain_reaches_proof_and_recognizes_revenue() -> None:
    deal = _deal("invoice_sent", "payment_received", "proof_pack_delivered")

    snapshot = analyze_deal(deal, TODAY)
    _, metrics = compute_portfolio([deal], TODAY)

    assert snapshot.stage == DealStage.PROOF_DELIVERED
    assert snapshot.valid_payment is True
    assert snapshot.proof_delivered is True
    assert snapshot.close_ready is True
    assert snapshot.anomalies == ()
    assert metrics.recognized_revenue_sar == 499
    assert metrics.weighted_pipeline_sar == 0


def test_payment_cannot_jump_over_missing_invoice() -> None:
    snapshot = analyze_deal(_deal("payment_received"), TODAY)

    assert snapshot.valid_payment is False
    assert snapshot.stage == DealStage.NEW
    assert "payment_before_invoice" in snapshot.anomalies
    assert next_action(snapshot).action_key == "repair_evidence_chain"


def test_cross_company_or_external_evidence_is_not_combined() -> None:
    paid = _deal("invoice_sent", "payment_received")
    proof_only = DealRecord(
        deal_id="deal-2",
        account_name="Other Client",
        source="referral",
        value_sar=2500,
        created_at="2026-07-01",
        last_touch_at="2026-07-10",
        events=(DealEvent("proof_pack_delivered", "2026-07-05"),),
    )

    snapshots, metrics = compute_portfolio([paid, proof_only], TODAY)

    assert snapshots[0].stage == DealStage.PAID
    assert snapshots[0].proof_delivered is False
    assert "proof_before_valid_payment" in snapshots[1].anomalies
    assert metrics.recognized_revenue_sar == 499


def test_high_value_research_target_stays_non_contactable() -> None:
    snapshot = analyze_deal(
        _deal(source="public_web_research", value_sar=100_000),
        TODAY,
    )
    action = next_action(snapshot)

    assert snapshot.stage == DealStage.RESEARCH_HOLD
    assert snapshot.contact_permission_confirmed is False
    assert snapshot.forecast_probability == 0
    assert action.action_key == "obtain_permission_or_warm_intro"
    assert action.requires_approval is False
    assert action.external_action_allowed is False


def test_contact_event_without_permission_is_an_anomaly_not_progress() -> None:
    snapshot = analyze_deal(
        _deal("message_sent_manual", source="manual_research"),
        TODAY,
    )

    assert snapshot.stage == DealStage.RESEARCH_HOLD
    assert "contact_without_permission" in snapshot.anomalies


def test_weighted_forecast_excludes_paid_and_lost_deals() -> None:
    proposed = _deal("invoice_sent", value_sar=10_000)
    paid = DealRecord(
        deal_id="deal-paid",
        account_name="Paid Client",
        source="referral",
        value_sar=5_000,
        created_at="2026-07-01",
        last_touch_at="2026-07-10",
        events=(
            DealEvent("invoice_sent", "2026-07-02"),
            DealEvent("payment_received", "2026-07-03"),
        ),
    )
    lost = DealRecord(
        deal_id="deal-lost",
        account_name="Lost Client",
        source="inbound",
        value_sar=20_000,
        created_at="2026-07-01",
        last_touch_at="2026-07-10",
        events=(DealEvent("lost", "2026-07-04"),),
    )

    _, metrics = compute_portfolio([proposed, paid, lost], TODAY)

    assert metrics.recognized_revenue_sar == 5_000
    assert metrics.open_pipeline_sar == 10_000
    assert metrics.weighted_pipeline_sar == 6_000


def test_optional_closed_won_requires_payment_and_proof() -> None:
    invalid = analyze_deal(_deal("invoice_sent", "closed_won"), TODAY)
    valid = analyze_deal(
        _deal("invoice_sent", "payment_received", "proof_pack_delivered", "closed_won"),
        TODAY,
    )

    assert "closed_won_before_payment_and_proof" in invalid.anomalies
    assert invalid.close_ready is False
    assert valid.close_ready is True


def test_stalled_stage_changes_rationale_without_enabling_execution() -> None:
    deal = DealRecord(
        deal_id="stalled",
        account_name="Stalled Client",
        source="inbound",
        created_at="2026-06-01",
        last_touch_at="2026-06-20",
        events=(DealEvent("invoice_sent", "2026-06-10"),),
    )

    snapshot = analyze_deal(deal, TODAY)
    action = next_action(snapshot)

    assert snapshot.stalled is True
    assert action.requires_approval is True
    assert action.external_action_allowed is False
    assert action.rationale.startswith("STALLED")


def test_atomic_store_round_trip_and_malformed_state_fails_loudly(tmp_path: Path) -> None:
    path = tmp_path / "private" / "deal-book.json"
    book = DealBook(deals=(_deal("invoice_sent"),), history=({"cycle": "2026-07-11"},))

    save_book_atomic(book, path)
    loaded = load_book(path)

    assert loaded.deals[0].account_name == "Approved Client"
    assert loaded.history[0]["cycle"] == "2026-07-11"

    path.write_text("{not-json", encoding="utf-8")
    with pytest.raises(DealBookError, match="valid deal book"):
        load_book(path)
