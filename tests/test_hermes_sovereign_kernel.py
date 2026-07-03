from __future__ import annotations

from dealix.hermes.sovereign.cycle import (
    asset_from_outcome,
    mark_executed,
    plan_execution,
    recommend_decision,
    record_outcome,
    signal_to_opportunity,
)
from dealix.hermes.sovereign.models import AssetType, OutcomeStatus, Signal
from dealix.hermes.sovereign.policy import ActionRoute, route_action, trust_check
from dealix.hermes.sovereign.scoring import compute_money_score, compute_opportunity_score


def test_sovereign_only_actions_are_held_for_sami() -> None:
    decision = route_action("open_public_api")

    assert decision.route == ActionRoute.SOVEREIGN_ONLY
    assert decision.requires_approval is True
    assert decision.allowed is False


def test_blocked_always_actions_are_blocked() -> None:
    decision = route_action("regulated_finance")

    assert decision.route == ActionRoute.BLOCK
    assert decision.requires_approval is False
    assert decision.allowed is False


def test_external_actions_require_approval() -> None:
    decision = route_action("send_email", external_action=True)

    assert decision.route == ActionRoute.HOLD_FOR_APPROVAL
    assert decision.requires_approval is True
    assert decision.allowed is False


def test_internal_drafts_can_execute_without_external_action() -> None:
    decision = route_action("draft_partner_pitch")

    assert decision.route == ActionRoute.EXECUTE
    assert decision.requires_approval is False
    assert decision.allowed is True


def test_trust_check_requires_agent_owner_and_kpis() -> None:
    result = trust_check(agent_owner="", agent_kpis=[])

    assert result.passed is False
    assert "agent_owner_missing" in result.reasons
    assert "agent_kpis_missing" in result.reasons


def test_opportunity_score_formula_is_deterministic() -> None:
    score = compute_opportunity_score(
        cash_speed_score=5,
        strategic_score=5,
        repeatability_score=4,
        data_moat_score=4,
        difficulty_score=2,
        risk_score=1,
    )

    assert score == 3.35


def test_money_score_formula_is_deterministic() -> None:
    score = compute_money_score(
        cash_speed_score=5,
        close_probability_score=4,
        deal_value_score=5,
        strategic_score=4,
        risk_score=2,
    )

    assert score == 3.9


def test_signal_to_asset_cycle_requires_outcome_and_asset_review() -> None:
    signal = Signal(
        source="sami",
        signal_type="partner",
        title="Agency white-label opportunity",
        content="Agency can distribute Dealix to B2B clients.",
        confidence=0.82,
    )
    opportunity = signal_to_opportunity(
        signal,
        opportunity_type="partner",
        estimated_value_sar=50000,
        cash_speed_score=3,
        strategic_score=5,
        repeatability_score=5,
        data_moat_score=4,
        difficulty_score=3,
        risk_score=2,
        recommended_action="draft_partner_pitch",
    )
    decision = recommend_decision(opportunity)
    execution = plan_execution(
        decision,
        action_type="draft_partner_pitch",
        expected_result="Partner pitch draft",
    )
    executed = mark_executed(execution)
    outcome = record_outcome(
        executed,
        status=OutcomeStatus.DRAFTED,
        actual_result="Partner pitch drafted.",
        learning="White-label framing is clearer than agent framing.",
    )
    asset = asset_from_outcome(
        outcome,
        asset_type=AssetType.TEMPLATE,
        title="Agency white-label pitch template",
        commercializable=True,
    )

    assert opportunity.status == "open"
    assert opportunity.opportunity_score > 0
    assert executed.status == "outcome_required"
    assert outcome.asset_review_required is True
    assert asset.reusable is True
    assert asset.commercializable is True
