"""Money — revenue verification + quality scoring."""

from __future__ import annotations

from dealix.hermes.money import (
    RevenueEvent,
    RevenueEventKind,
    RevenueQualityScorer,
    RevenueVerifier,
)


def _event(
    *,
    kind: RevenueEventKind,
    amount: int = 1000,
    payment_reference: str | None = None,
    deal_id: str | None = None,
    partner_id: str | None = None,
) -> RevenueEvent:
    return RevenueEvent(
        event_id="ev_test",
        kind=kind,
        customer_id="cust_1",
        offer_id="offer_1",
        amount_sar=amount,
        payment_reference=payment_reference,
        deal_id=deal_id,
        partner_id=partner_id,
    )


def test_payment_received_without_reference_is_rejected() -> None:
    verifier = RevenueVerifier()
    event = _event(kind=RevenueEventKind.PAYMENT_RECEIVED, amount=1000)
    result = verifier.verify(event)
    assert result.accepted is False
    assert "payment_reference" in result.reason


def test_payment_received_with_reference_is_accepted() -> None:
    verifier = RevenueVerifier()
    event = _event(
        kind=RevenueEventKind.PAYMENT_RECEIVED,
        amount=1000,
        payment_reference="moyasar_inv_42",
    )
    result = verifier.verify(event)
    assert result.accepted is True
    assert result.verification_source == "payment_received"


def test_proposal_sent_is_rejected_not_a_verification_kind() -> None:
    verifier = RevenueVerifier()
    event = _event(kind=RevenueEventKind.PROPOSAL_SENT, amount=1000)
    result = verifier.verify(event)
    assert result.accepted is False
    assert "not a verification source" in result.reason


def test_recurring_revenue_scores_higher_than_one_off() -> None:
    scorer = RevenueQualityScorer()
    recurring = _event(kind=RevenueEventKind.RETAINER_STARTED, amount=5000)
    one_off = _event(
        kind=RevenueEventKind.PAYMENT_RECEIVED,
        amount=5000,
        payment_reference="moyasar_x",
    )
    rec_score = scorer.score(recurring).score
    one_score = scorer.score(one_off).score
    assert rec_score > one_score
    assert scorer.score(recurring).recurring is True


def test_tiny_amount_reduces_quality_score() -> None:
    scorer = RevenueQualityScorer()
    tiny = _event(
        kind=RevenueEventKind.PAYMENT_RECEIVED,
        amount=500,
        payment_reference="moyasar_y",
    )
    big = _event(
        kind=RevenueEventKind.PAYMENT_RECEIVED,
        amount=5000,
        payment_reference="moyasar_z",
    )
    tiny_score = scorer.score(tiny).score
    big_score = scorer.score(big).score
    assert tiny_score < big_score
