"""Tests for the Autonomous Growth Engine."""

from __future__ import annotations

import pytest

from dealix.growth.autonomous_growth_engine import (
    AutonomousGrowthEngine,
    COMPLIANT_CHANNELS,
    _TIER_LTV,
    _SECTOR_WEIGHTS,
)


@pytest.fixture
def engine() -> AutonomousGrowthEngine:
    return AutonomousGrowthEngine()


# ---------------------------------------------------------------------------
# generate_weekly_targets
# ---------------------------------------------------------------------------


def test_weekly_targets_gap_zero(engine: AutonomousGrowthEngine) -> None:
    result = engine.generate_weekly_targets(current_mrr=5000, target_mrr=5000)
    assert result["gap_sar"] == 0


def test_weekly_targets_compliant_channels_only(engine: AutonomousGrowthEngine) -> None:
    result = engine.generate_weekly_targets(current_mrr=1000, target_mrr=10000)
    for action in result["weekly_actions"]:
        assert action["channel"] in COMPLIANT_CHANNELS, (
            f"Non-compliant channel: {action['channel']}"
        )
    assert result["compliant_channels_only"] is True


def test_weekly_targets_has_actions(engine: AutonomousGrowthEngine) -> None:
    result = engine.generate_weekly_targets(current_mrr=0, target_mrr=50000)
    assert len(result["weekly_actions"]) >= 2


def test_weekly_targets_outreach_capped_at_10(engine: AutonomousGrowthEngine) -> None:
    result = engine.generate_weekly_targets(current_mrr=0, target_mrr=500_000)
    outreach_actions = [a for a in result["weekly_actions"] if a["action"] == "warm_outreach"]
    if outreach_actions:
        assert outreach_actions[0]["count"] <= 10


# ---------------------------------------------------------------------------
# score_lead
# ---------------------------------------------------------------------------


def test_score_lead_returns_0_to_100(engine: AutonomousGrowthEngine) -> None:
    result = engine.score_lead("TechCo", "tech", "medium", ["data_quality", "no_crm"])
    assert 0 <= result["score"] <= 100


def test_score_lead_finance_high_sector(engine: AutonomousGrowthEngine) -> None:
    result = engine.score_lead("FinanceCo", "finance", "large", ["data_quality", "compliance"])
    assert result["sector_weight"] == _SECTOR_WEIGHTS["finance"]
    assert result["score"] >= 60


def test_score_lead_hot_tier(engine: AutonomousGrowthEngine) -> None:
    result = engine.score_lead(
        "BigCo", "finance", "large",
        ["data_quality", "no_crm", "lost_leads", "manual_reports"]
    )
    assert result["tier"] in ("hot", "warm")


def test_score_lead_cold_tier_no_offer(engine: AutonomousGrowthEngine) -> None:
    result = engine.score_lead("TinyCo", "food", "micro", [])
    assert result["tier"] == "cold"
    assert result["recommended_offer"] is None


def test_score_lead_pain_score_capped_at_30(engine: AutonomousGrowthEngine) -> None:
    many_pains = ["data_quality", "manual_reports", "no_crm", "lost_leads",
                  "inventory_issues", "cash_flow", "compliance", "growth_stagnant"]
    result = engine.score_lead("X", "tech", "large", many_pains)
    assert result["pain_score"] <= 30


def test_score_lead_unknown_sector_uses_default(engine: AutonomousGrowthEngine) -> None:
    result = engine.score_lead("Co", "unknown_sector", "small", [])
    assert result["sector_weight"] == 1.0


# ---------------------------------------------------------------------------
# generate_outreach_sequence
# ---------------------------------------------------------------------------


def test_outreach_sequence_returns_5_steps(engine: AutonomousGrowthEngine) -> None:
    seq = engine.generate_outreach_sequence({"company_name": "TestCo", "sector": "tech", "score": 70})
    assert len(seq) == 5


def test_outreach_sequence_all_compliant(engine: AutonomousGrowthEngine) -> None:
    seq = engine.generate_outreach_sequence({"company_name": "Co", "sector": "retail", "score": 50})
    for step in seq:
        assert step["compliant"] is True
        assert step["channel"] in COMPLIANT_CHANNELS, (
            f"Non-compliant channel in step {step['step']}: {step['channel']}"
        )


def test_outreach_sequence_steps_in_order(engine: AutonomousGrowthEngine) -> None:
    seq = engine.generate_outreach_sequence({"company_name": "Co", "sector": "tech", "score": 80})
    for i, step in enumerate(seq, start=1):
        assert step["step"] == i


def test_outreach_sequence_days_increase(engine: AutonomousGrowthEngine) -> None:
    seq = engine.generate_outreach_sequence({"company_name": "Co", "sector": "tech", "score": 60})
    days = [s["day"] for s in seq]
    assert days == sorted(days)


# ---------------------------------------------------------------------------
# calculate_ltv
# ---------------------------------------------------------------------------


def test_ltv_early_stage_discounted(engine: AutonomousGrowthEngine) -> None:
    full = engine.calculate_ltv("managed_ops", 12)
    early = engine.calculate_ltv("managed_ops", 2)
    assert early < full


def test_ltv_top_tier_highest(engine: AutonomousGrowthEngine) -> None:
    ltv_managed = engine.calculate_ltv("managed_ops", 12)
    ltv_sprint = engine.calculate_ltv("sprint_499", 12)
    assert ltv_managed > ltv_sprint


def test_ltv_free_diagnostic_is_zero(engine: AutonomousGrowthEngine) -> None:
    assert engine.calculate_ltv("free_diagnostic", 6) == 0.0


def test_ltv_unknown_tier_returns_zero(engine: AutonomousGrowthEngine) -> None:
    assert engine.calculate_ltv("nonexistent_tier", 12) == 0.0


# ---------------------------------------------------------------------------
# churn_risk_assessment
# ---------------------------------------------------------------------------


def test_churn_critical_inactive_client(engine: AutonomousGrowthEngine) -> None:
    result = engine.churn_risk_assessment("client_1", last_activity_days=90,
                                           invoices_paid=0, support_tickets=4)
    assert result["risk_level"] == "critical"
    assert result["churn_risk_score"] >= 70


def test_churn_low_healthy_client(engine: AutonomousGrowthEngine) -> None:
    result = engine.churn_risk_assessment("client_2", last_activity_days=5,
                                           invoices_paid=12, support_tickets=0)
    assert result["risk_level"] == "low"
    assert result["churn_risk_score"] < 20


def test_churn_score_capped_at_100(engine: AutonomousGrowthEngine) -> None:
    result = engine.churn_risk_assessment("client_3", last_activity_days=200,
                                           invoices_paid=0, support_tickets=10)
    assert result["churn_risk_score"] <= 100


def test_churn_returns_recommended_action(engine: AutonomousGrowthEngine) -> None:
    result = engine.churn_risk_assessment("client_4", last_activity_days=40,
                                           invoices_paid=2, support_tickets=1)
    assert "recommended_action" in result
    assert len(result["recommended_action"]) > 0


# ---------------------------------------------------------------------------
# expansion_opportunities
# ---------------------------------------------------------------------------


def test_expansion_upsell_available(engine: AutonomousGrowthEngine) -> None:
    opps = engine.expansion_opportunities("sprint_499", months_active=4)
    types = [o["type"] for o in opps]
    assert "upsell" in types


def test_expansion_top_tier_no_upsell(engine: AutonomousGrowthEngine) -> None:
    opps = engine.expansion_opportunities("custom_ai", months_active=12)
    types = [o["type"] for o in opps]
    assert "upsell" not in types


def test_expansion_referral_after_2_months(engine: AutonomousGrowthEngine) -> None:
    opps = engine.expansion_opportunities("sprint_499", months_active=3)
    types = [o["type"] for o in opps]
    assert "referral" in types


def test_expansion_no_referral_month_1(engine: AutonomousGrowthEngine) -> None:
    opps = engine.expansion_opportunities("sprint_499", months_active=1)
    types = [o["type"] for o in opps]
    # referral requires >= 2 months
    assert "referral" not in types


def test_expansion_unknown_tier_returns_empty(engine: AutonomousGrowthEngine) -> None:
    opps = engine.expansion_opportunities("unknown_tier", months_active=6)  # type: ignore[arg-type]
    assert opps == []
