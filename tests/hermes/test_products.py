from __future__ import annotations

from dealix.hermes.assets import (
    AssetUsageEvent,
    plan_commercialization,
    promote_asset,
)
from dealix.hermes.products import (
    check_offer_readiness,
    is_productization_candidate,
    recommend_repositioning,
    score_experiment,
    score_offer_market_fit,
)


def test_offer_market_fit_double_down():
    fit = score_offer_market_fit(
        offer_id="ai_trust_kit",
        outreach_count=100,
        reply_count=40,
        qualified_call_count=20,
        proposal_count=15,
        win_count=10,
        payment_count=10,
        retainer_conversion_count=6,
        referral_count=3,
        delivery_margin_pct=55,
    )
    assert fit.band in ("scale", "double_down", "iterate")
    rec = recommend_repositioning(fit)
    assert rec.decision in ("scale", "niche_down", "bundle", "reprice")


def test_offer_market_fit_kill():
    fit = score_offer_market_fit(
        offer_id="dead_offer",
        outreach_count=200,
        reply_count=2,
        qualified_call_count=0,
        proposal_count=0,
        win_count=0,
        payment_count=0,
        retainer_conversion_count=0,
        referral_count=0,
        delivery_margin_pct=10,
    )
    assert fit.band == "kill"
    rec = recommend_repositioning(fit)
    assert rec.decision == "kill"


def test_experiment_inconclusive_when_ci_crosses_zero():
    res = score_experiment(
        "exp_1",
        control_n=100,
        treatment_n=100,
        control_metric=0.10,
        treatment_metric=0.12,
        confidence_interval=(-0.01, 0.05),
    )
    assert res.verdict == "inconclusive"


def test_offer_readiness_gate_fails_with_missing_checks():
    gate = check_offer_readiness(
        "ai_trust_kit",
        {
            "delivery_playbook_present": True,
            "pricing_documented": True,
            "approval_flow_documented": True,
            "data_handling_documented": False,
            "claim_verifier_pass": True,
            "trust_signals_min_3": False,
            "owner_assigned": True,
        },
    )
    assert gate.ready is False
    assert "trust_signals_min_3" in gate.failing_checks


def test_productization_candidate_requires_3_uses():
    c = is_productization_candidate(
        asset_id="ai_governance_checklist",
        times_used=2,
        influenced_revenue_sar=5000,
        reusable=True,
        low_risk=True,
    )
    assert c.is_candidate is False


def test_promote_asset_path():
    decision = promote_asset(
        AssetUsageEvent(
            asset_id="ai_governance_checklist",
            times_used=5,
            influenced_revenue_sar=12000,
            reusable=True,
            low_risk=True,
        )
    )
    assert decision.promoted is True


def test_plan_commercialization_smb():
    plan = plan_commercialization(
        asset_id="ai_governance_checklist",
        asset_kind="checklist",
        typical_buyer_size="smb",
        typical_outcome_value_sar=20000,
        requires_data_handling=True,
        requires_external_send=False,
    )
    assert plan.tier == "entry"
    assert "data_handling_addendum" in plan.required_assets
    assert plan.required_legal_review is False
