from __future__ import annotations

from dealix.hermes.money import (
    RevenueEvent,
    compute_delivery_margin,
    is_verified,
    score_founder_time_cost,
    score_revenue_quality,
    sum_verified_revenue,
)
from dealix.hermes.money.verified_revenue import RevenueStatus


def _event(amount: float, source: str, status: RevenueStatus, evidence: str = "ev_1"):
    return RevenueEvent(
        event_id="r1",
        amount_sar=amount,
        source=source,
        status=status,
        customer_id="c1",
        occurred_at=0,
        evidence_ref=evidence,
    )


def test_only_payment_received_is_verified():
    assert is_verified(_event(1000, "payment_received", RevenueStatus.PAID)) is True
    assert is_verified(_event(1000, "verbal_promise", RevenueStatus.PAID)) is False
    assert is_verified(
        _event(1000, "payment_received", RevenueStatus.PROPOSAL_SENT)
    ) is False


def test_verified_revenue_requires_evidence_ref():
    assert is_verified(_event(1000, "payment_received", RevenueStatus.PAID, "")) is False


def test_sum_verified_revenue():
    events = [
        _event(1000, "payment_received", RevenueStatus.PAID),
        _event(2000, "verbal_promise", RevenueStatus.PROPOSAL_SENT),
        _event(3000, "retainer_active", RevenueStatus.RETAINER_ACTIVE),
    ]
    assert sum_verified_revenue(events) == 4000.0


def test_revenue_quality_band_thresholds():
    s = score_revenue_quality(
        margin=0.6,
        repeatability=0.6,
        retainer_potential=0.7,
        data_moat=0.5,
        partner_potential=0.4,
        low_delivery_burden=0.5,
        risk=0.2,
        founder_time_dependency=0.2,
    )
    assert 30 <= s.score <= 100
    assert s.band in ("caution", "good", "great", "exceptional")


def test_revenue_quality_kill_band():
    s = score_revenue_quality(
        margin=0.1,
        repeatability=0.1,
        retainer_potential=0.1,
        data_moat=0.0,
        partner_potential=0.0,
        low_delivery_burden=0.2,
        risk=0.9,
        founder_time_dependency=0.9,
    )
    assert s.band == "kill"


def test_founder_time_flag_no_asset():
    cost = score_founder_time_cost(
        founder_hours_required=20,
        decision_complexity=0.8,
        relationship_sensitivity=0.7,
        delegation_possible=0.1,
        strategic_value=0.2,
        builds_asset_or_retainer=False,
    )
    assert cost.band in ("high", "blocker")
    assert cost.expand_recommendation is False
    assert any("reposition or kill" in n for n in cost.notes)


def test_delivery_margin_flags_thin_margin():
    m = compute_delivery_margin(
        revenue_sar=10_000,
        delivery_hours=50,
        blended_hour_cost_sar=250,
        agent_cost_sar=100,
    )
    # 50 * 250 + 100 = 12_600 → loss
    assert m.gross_margin_sar < 0
    assert any("margin below 30%" in n for n in m.notes)
