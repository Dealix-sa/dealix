"""Sanity tests for the growth + money modules."""

from __future__ import annotations

from dealix.hermes.growth.attribution import multi_touch, revenue_weighting
from dealix.hermes.growth.channel_quality import ChannelMetrics, score_channel
from dealix.hermes.growth.message_quality import MessageMetrics, score_message
from dealix.hermes.growth.offer_market_fit import score as omf_score
from dealix.hermes.growth.revenue_attribution import attribute
from dealix.hermes.growth.trust_signals import (
    TrustSignal,
    TrustSignalKind,
    TrustSignalLedger,
)
from dealix.hermes.money.cost_intelligence import CostEntry, CostKind, register_cost, total_cost
from dealix.hermes.money.margin_analysis import analyse_margin
from dealix.hermes.money.pricing_engine import PricingInputs, recommend_price
from dealix.hermes.money.revenue_quality import score_revenue_quality


def test_channel_quality_scores_inactive_channel_as_F():
    metrics = ChannelMetrics(
        name="cold_outreach",
        touches=0, leads=0, qualified=0,
        proposals=0, payments=0,
        verified_revenue_sar=0.0, cost_sar=0.0,
    )
    score = score_channel(metrics)
    assert score.grade == "F"


def test_channel_quality_recognises_strong_channel():
    metrics = ChannelMetrics(
        name="partner_referrals",
        touches=100, leads=60, qualified=40,
        proposals=20, payments=12,
        verified_revenue_sar=240_000.0, cost_sar=20_000.0,
    )
    score = score_channel(metrics)
    assert score.grade in ("A", "B")


def test_message_quality_zero_sent_returns_F():
    metrics = MessageMetrics("m_1", sent=0, replies=0, qualified_replies=0,
                             booked_calls=0, proposals=0, deals_won=0)
    assert score_message(metrics).grade == "F"


def test_offer_market_fit_scale_decision():
    fit = omf_score(
        offer_id="ai_trust_kit",
        reply_rate=0.3, call_rate=0.5, proposal_rate=0.6,
        win_rate=0.5, payment_rate=0.5, retainer_conversion=0.4,
        delivery_margin=0.55,
    )
    assert fit.decision == "scale"


def test_multi_touch_weights_sum_to_one():
    touches = [
        {"at": "2025-01-01", "source": "geo:ai_gov"},
        {"at": "2025-02-01", "source": "outbound"},
        {"at": "2025-03-01", "source": "partner:acme"},
    ]
    weights = multi_touch.weights(touches)
    assert abs(sum(weights.values()) - 1.0) < 1e-6


def test_attribute_normalised_weights_sum_to_one():
    touches = [
        {"at": "2025-01-01", "source": "geo:ai_gov"},
        {"at": "2025-02-01", "source": "outbound"},
    ]
    attribution = attribute(
        deal_id="d1",
        verified_revenue_sar=20_000,
        touches=touches,
        assets=("evidence_pack",),
        agents=("revenue_hunter",),
        partner="acme",
    )
    total = sum(attribution.weights.values())
    assert abs(total - 1.0) < 1e-3 or total == 0.0


def test_trust_signal_ledger_minimum():
    ledger = TrustSignalLedger()
    ok, _ = ledger.check_claim("ai_governance", minimum=1)
    assert not ok
    ledger.record(TrustSignal("ts_1", TrustSignalKind.CASE_STUDY, "ai_governance"))
    ok, _ = ledger.check_claim("ai_governance", minimum=1)
    assert ok


def test_revenue_quality_high_drives_scale():
    score = score_revenue_quality(
        deal_id="d1",
        margin=0.8, repeatability=0.7, retainer_potential=0.7,
        data_moat=0.5, partner_potential=0.5,
        delivery_burden=0.2, risk=0.1,
    )
    assert score.verdict.value == "high"


def test_cost_intelligence_total():
    register_cost(CostEntry(deal_id="d2", kind=CostKind.HUMAN, amount_sar=2000, description="founder time"))
    register_cost(CostEntry(deal_id="d2", kind=CostKind.AGENT, amount_sar=300, description="agent"))
    assert total_cost("d2") == 2300


def test_margin_kill_threshold():
    report = analyse_margin(deal_id="d_neg", revenue_sar=5_000, cost_sar=8_000)
    assert report.verdict == "kill"


def test_pricing_engine_requires_approval():
    rec = recommend_price(PricingInputs(
        offer_id="ai_trust_kit",
        buyer_type="enterprise", sector="bfsi", urgency="high",
        delivery_complexity="medium", proof_level="strong",
        risk_level="medium", retainer_potential=True, partner_involved=False,
    ))
    assert rec.requires_approval
    assert rec.target_price_sar >= rec.floor_price_sar
