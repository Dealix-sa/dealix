"""Deterministic helpers for the Hermes value cycle."""

from __future__ import annotations

from dataclasses import replace

from dealix.hermes.sovereign.models import (
    Asset,
    AssetType,
    Decision,
    DecisionType,
    Execution,
    ExecutionStatus,
    Opportunity,
    OpportunityType,
    Outcome,
    OutcomeStatus,
    Signal,
)
from dealix.hermes.sovereign.policy import ActionRoute, route_action
from dealix.hermes.sovereign.scoring import lifecycle_recommendation, score_opportunity


def signal_to_opportunity(
    signal: Signal,
    *,
    opportunity_type: OpportunityType | str,
    estimated_value_sar: float = 0.0,
    cash_speed_score: int = 1,
    strategic_score: int = 1,
    repeatability_score: int = 1,
    data_moat_score: int = 1,
    difficulty_score: int = 1,
    risk_score: int = 1,
    recommended_action: str = "request_more_info",
) -> Opportunity:
    """Convert a Signal into a scored Opportunity.

    Low-confidence signals are still represented, but marked as archived so the
    system keeps source memory without forcing execution.
    """

    status = "open" if signal.confidence >= 0.35 else "archived"
    opp = Opportunity(
        signal_id=signal.id,
        opportunity_type=opportunity_type,
        title=signal.title,
        description=signal.content,
        estimated_value_sar=estimated_value_sar,
        cash_speed_score=cash_speed_score,
        strategic_score=strategic_score,
        repeatability_score=repeatability_score,
        data_moat_score=data_moat_score,
        difficulty_score=difficulty_score,
        risk_score=risk_score,
        recommended_action=recommended_action,
        status=status,
    )
    return score_opportunity(opp)


def recommend_decision(opp: Opportunity) -> Decision:
    """Create a deterministic decision recommendation for an opportunity."""

    rec = lifecycle_recommendation(opp)
    if opp.status == "archived":
        decision_type = DecisionType.DEFER
        recommendation = "Archive until better signal quality exists."
    elif rec == "scale":
        decision_type = DecisionType.SCALE
        recommendation = "Scale this path after approval and proof review."
    elif rec == "execute":
        decision_type = DecisionType.EXECUTE
        recommendation = opp.recommended_action or "Execute a small controlled next step."
    elif rec == "defer_or_request_more_info":
        decision_type = DecisionType.REQUEST_MORE_INFO
        recommendation = "Request more data before execution."
    else:
        decision_type = DecisionType.KILL
        recommendation = "Retire this path and preserve learning."

    requires_approval = opp.sovereignty_level not in {"S0_SAFE_INTERNAL", "S1_INTERNAL"}
    return Decision(
        opportunity_id=opp.id,
        decision_type=decision_type,
        context=opp.description,
        options=["execute", "defer", "retire", "scale", "request_more_info"],
        recommendation=recommendation,
        risk_level="high" if opp.risk_score >= 4 else "medium" if opp.risk_score >= 2 else "low",
        sovereignty_level=opp.sovereignty_level,
        requires_approval=requires_approval,
    )


def plan_execution(
    decision: Decision,
    *,
    action_type: str,
    agent_id: str = "hermes_kernel",
    external_action: bool = False,
    expected_result: str = "",
) -> Execution:
    """Plan an execution step and apply sovereignty routing."""

    routed = route_action(action_type, external_action=external_action)
    status: ExecutionStatus | str
    if routed.route == ActionRoute.EXECUTE:
        status = ExecutionStatus.PLANNED
    elif routed.route == ActionRoute.HOLD_FOR_APPROVAL:
        status = ExecutionStatus.HELD_FOR_APPROVAL
    else:
        status = ExecutionStatus.BLOCKED

    return Execution(
        decision_id=decision.id,
        agent_id=agent_id,
        action_type=action_type,
        sovereignty_level=routed.sovereignty_level.value,
        external_action=external_action,
        requires_approval=routed.requires_approval,
        expected_result=expected_result,
        status=status,
    )


def mark_executed(execution: Execution) -> Execution:
    """Mark an execution as performed while keeping outcome required."""

    if execution.status == ExecutionStatus.BLOCKED:
        return execution
    return replace(execution, status=ExecutionStatus.OUTCOME_REQUIRED)


def record_outcome(
    execution: Execution,
    *,
    status: OutcomeStatus | str,
    actual_result: str,
    revenue_sar: float = 0.0,
    learning: str = "",
) -> Outcome:
    """Record the required outcome for an execution."""

    return Outcome(
        execution_id=execution.id,
        status=status,
        actual_result=actual_result,
        revenue_sar=revenue_sar,
        learning=learning,
        asset_review_required=True,
    )


def asset_from_outcome(
    outcome: Outcome,
    *,
    asset_type: AssetType | str = AssetType.TEMPLATE,
    title: str = "Reusable Hermes asset",
    commercializable: bool = False,
) -> Asset:
    """Create an asset candidate from an outcome."""

    return Asset(
        outcome_id=outcome.id,
        asset_type=asset_type,
        title=title,
        description=outcome.learning or outcome.actual_result,
        reusable=True,
        commercializable=commercializable,
    )
