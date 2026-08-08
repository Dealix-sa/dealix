"""Autonomy & Approval Engine for Company Intelligence.

Central decision engine for human-in-the-loop governance. Evaluates every
action request against the tenant's HumanLoopPolicy to determine whether
it can proceed autonomously or needs human approval — and at what level.

This engine enforces the non-negotiable safety invariant:
    **External actions ALWAYS require human approval.**

No policy configuration, autonomy level, or override can bypass this rule.
The engine is the single point of enforcement between the Action Queue
and the Execution layer.

The engine is persistence-neutral: no database, network, or LLM calls.

Entity ownership:
    Uses HumanLoopPolicy (approval_center) contracts.
    Uses Action (action_queue) contracts.
    Produces inputs for Approval (approval_center) contracts.
"""
from __future__ import annotations

import json
from datetime import UTC, datetime
from enum import StrEnum
from hashlib import sha256
from typing import Annotated, Any

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    StringConstraints,
    model_validator,
)

from dealix.company_intelligence.action_contracts import (
    ActionType,
    AutonomyLevel,
    CanonicalAction,
    RiskLevel,
)
from dealix.company_intelligence.human_loop_contracts import (
    CanonicalHumanLoopPolicy,
    EscalationTrigger,
    HumanLoopMode,
    requires_human_approval,
)

NonEmptyString = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------


class AutonomyDecisionType(StrEnum):
    """What the engine decides about an action."""

    AUTO_APPROVE = "auto_approve"
    QUEUE_FOR_APPROVAL = "queue_for_approval"
    ESCALATE = "escalate"
    BLOCK = "block"


class EscalationReason(StrEnum):
    """Why an action was escalated."""

    EXTERNAL_ACTION = "external_action"
    HIGH_RISK = "high_risk"
    LOW_CONFIDENCE = "low_confidence"
    FIRST_CONTACT = "first_contact"
    HIGH_VALUE = "high_value"
    BOUNDARY_VIOLATION = "boundary_violation"
    POLICY_OVERRIDE = "policy_override"
    SENSITIVE_CHANNEL = "sensitive_channel"


# ---------------------------------------------------------------------------
# Stable IDs
# ---------------------------------------------------------------------------


def _stable_evaluation_id(payload: dict[str, Any]) -> str:
    canonical = json.dumps(
        payload,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
        default=str,
    )
    return f"autoeval_{sha256(canonical.encode('utf-8')).hexdigest()[:16]}"


# ---------------------------------------------------------------------------
# Action Evaluation — the engine's output
# ---------------------------------------------------------------------------


class ActionEvaluation(BaseModel):
    """The Autonomy Engine's decision about a specific action.

    An ActionEvaluation captures the complete reasoning for why an action
    was approved, queued, escalated, or blocked. It provides the decision
    trail for auditing and learning.

    Key invariants:
        - External actions are ALWAYS QUEUE_FOR_APPROVAL or ESCALATE.
        - AUTO_APPROVE is never allowed for external or high-risk actions.
        - BLOCK means the action violates a hard constraint.
        - evaluation_id is deterministic.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    # Identity
    tenant_id: NonEmptyString
    evaluation_id: NonEmptyString

    # What was evaluated
    action_id: NonEmptyString
    action_type: ActionType
    policy_id: NonEmptyString

    # Decision
    decision: AutonomyDecisionType
    autonomy_level_required: AutonomyLevel
    autonomy_level_granted: AutonomyLevel

    # Reasoning
    escalation_reasons: tuple[EscalationReason, ...] = ()
    reasoning: NonEmptyString
    triggered_rules: tuple[str, ...] = ()

    # Context
    is_external: bool = False
    risk_level: RiskLevel = RiskLevel.LOW
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)

    # Approval routing
    approval_timeout_minutes: int = Field(default=60, ge=1, le=10080)
    notification_channels: tuple[str, ...] = ()

    # Provenance
    policy_mode: HumanLoopMode
    source_id: NonEmptyString
    evaluated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    @model_validator(mode="after")
    def enforce_evaluation_invariants(self) -> ActionEvaluation:
        # External actions can NEVER be auto-approved
        if self.is_external and self.decision == AutonomyDecisionType.AUTO_APPROVE:
            raise ValueError(
                "external actions cannot be auto-approved"
            )

        # HIGH/CRITICAL risk cannot be auto-approved
        if (
            self.risk_level in (RiskLevel.HIGH, RiskLevel.CRITICAL)
            and self.decision == AutonomyDecisionType.AUTO_APPROVE
        ):
            raise ValueError(
                "high/critical risk actions cannot be auto-approved"
            )

        # Verify deterministic ID
        expected_id = _stable_evaluation_id({
            "action_id": self.action_id,
            "policy_id": self.policy_id,
            "tenant_id": self.tenant_id,
        })
        if self.evaluation_id != expected_id:
            raise ValueError(
                "evaluation_id does not match the canonical payload"
            )

        return self


# ---------------------------------------------------------------------------
# Engine functions
# ---------------------------------------------------------------------------


def _collect_escalation_reasons(
    action: CanonicalAction,
    policy: CanonicalHumanLoopPolicy,
    *,
    is_first_contact: bool = False,
) -> list[EscalationReason]:
    """Collect all reasons this action would be escalated."""
    reasons: list[EscalationReason] = []

    # External action — always
    if action.external_effect:
        reasons.append(EscalationReason.EXTERNAL_ACTION)

    # High risk
    if action.risk_level in (RiskLevel.HIGH, RiskLevel.CRITICAL):
        reasons.append(EscalationReason.HIGH_RISK)

    # Check escalation rules from policy
    for rule in policy.escalation_rules:
        if (
            rule.trigger == EscalationTrigger.LOW_CONFIDENCE
            and action.confidence < rule.threshold
        ):
            reasons.append(EscalationReason.LOW_CONFIDENCE)
        elif (
            rule.trigger == EscalationTrigger.FIRST_CONTACT
            and is_first_contact
        ):
            reasons.append(EscalationReason.FIRST_CONTACT)
        elif (
            rule.trigger == EscalationTrigger.HIGH_VALUE
            and action.impact > rule.threshold
        ):
            reasons.append(EscalationReason.HIGH_VALUE)
        elif (
            rule.trigger == EscalationTrigger.SENSITIVE_CHANNEL
            and action.external_effect
        ):
            reasons.append(EscalationReason.SENSITIVE_CHANNEL)

    return list(dict.fromkeys(reasons))  # dedupe preserving order


def _determine_decision(
    action: CanonicalAction,
    policy: CanonicalHumanLoopPolicy,
    *,
    escalation_reasons: list[EscalationReason],
    is_first_contact: bool = False,
) -> AutonomyDecisionType:
    """Determine the autonomy decision for an action."""
    # External actions: NEVER auto-approve
    if action.external_effect:
        if EscalationReason.HIGH_RISK in escalation_reasons:
            return AutonomyDecisionType.ESCALATE
        return AutonomyDecisionType.QUEUE_FOR_APPROVAL

    # High/Critical risk: queue or escalate
    if action.risk_level in (RiskLevel.HIGH, RiskLevel.CRITICAL):
        return AutonomyDecisionType.ESCALATE

    # Check if policy allows auto-approval
    needs_approval = requires_human_approval(
        policy,
        action_type=action.action_type.value,
        risk_level=RiskLevel(action.risk_level),
        confidence=action.confidence,
        is_external=action.external_effect,
        is_first_contact=is_first_contact,
    )

    if needs_approval:
        if escalation_reasons:
            return AutonomyDecisionType.ESCALATE
        return AutonomyDecisionType.QUEUE_FOR_APPROVAL

    return AutonomyDecisionType.AUTO_APPROVE


def _build_reasoning(
    decision: AutonomyDecisionType,
    action: CanonicalAction,
    policy: CanonicalHumanLoopPolicy,
    escalation_reasons: list[EscalationReason],
) -> str:
    """Build a human-readable reasoning string for the decision."""
    parts = [f"Policy '{policy.name}' (mode: {policy.mode.value})"]

    if decision == AutonomyDecisionType.AUTO_APPROVE:
        parts.append(
            f"auto-approved internal {action.action_type.value} action "
            f"with {action.risk_level.value} risk"
        )
    elif decision == AutonomyDecisionType.QUEUE_FOR_APPROVAL:
        parts.append(
            f"queued {action.action_type.value} for human approval"
        )
        if action.external_effect:
            parts.append("(external action — always requires approval)")
    elif decision == AutonomyDecisionType.ESCALATE:
        reason_names = [r.value for r in escalation_reasons]
        parts.append(
            f"escalated due to: {', '.join(reason_names)}"
        )
    elif decision == AutonomyDecisionType.BLOCK:
        parts.append("blocked — violates hard constraint")

    return "; ".join(parts)


def evaluate_action(
    action: CanonicalAction,
    policy: CanonicalHumanLoopPolicy,
    *,
    source_id: str,
    is_first_contact: bool = False,
) -> ActionEvaluation:
    """Evaluate an action against a human-loop policy.

    This is the primary entry point for the Autonomy Engine. It determines
    whether an action can proceed autonomously, needs approval, should be
    escalated, or must be blocked.

    The non-negotiable invariant: external actions ALWAYS require human
    approval, regardless of policy configuration.
    """
    # Collect escalation reasons
    escalation_reasons = _collect_escalation_reasons(
        action, policy, is_first_contact=is_first_contact,
    )

    # Determine decision
    decision = _determine_decision(
        action, policy,
        escalation_reasons=escalation_reasons,
        is_first_contact=is_first_contact,
    )

    # Build reasoning
    reasoning = _build_reasoning(decision, action, policy, escalation_reasons)

    # Determine granted autonomy level
    if decision == AutonomyDecisionType.AUTO_APPROVE:
        granted_level = action.autonomy_level
    elif decision == AutonomyDecisionType.BLOCK:
        granted_level = AutonomyLevel.L0_OBSERVE
    else:
        # Queued or escalated — grant up to the policy's default
        granted_level = min(
            action.autonomy_level,
            policy.default_autonomy_level,
        )

    # Collect triggered rule descriptions
    triggered = []
    for rule in policy.escalation_rules:
        if rule.trigger == EscalationTrigger.LOW_CONFIDENCE:
            if action.confidence < rule.threshold:
                triggered.append(
                    f"low_confidence: {action.confidence} < {rule.threshold}"
                )
        elif rule.trigger == EscalationTrigger.FIRST_CONTACT and is_first_contact:
            triggered.append("first_contact: true")
        elif rule.trigger == EscalationTrigger.HIGH_VALUE:
            if action.impact > rule.threshold:
                triggered.append(
                    f"high_value: impact {action.impact} > {rule.threshold}"
                )

    # Build evaluation ID
    evaluation_id = _stable_evaluation_id({
        "action_id": action.action_id,
        "policy_id": policy.policy_id,
        "tenant_id": action.tenant_id,
    })

    return ActionEvaluation(
        tenant_id=action.tenant_id,
        evaluation_id=evaluation_id,
        action_id=action.action_id,
        action_type=action.action_type,
        policy_id=policy.policy_id,
        decision=decision,
        autonomy_level_required=action.autonomy_level,
        autonomy_level_granted=granted_level,
        escalation_reasons=tuple(escalation_reasons),
        reasoning=reasoning,
        triggered_rules=tuple(triggered),
        is_external=action.external_effect,
        risk_level=action.risk_level,
        confidence=action.confidence,
        approval_timeout_minutes=policy.response_timeout_minutes,
        notification_channels=policy.notification_channels,
        policy_mode=policy.mode,
        source_id=source_id,
    )


def can_auto_execute(
    action: CanonicalAction,
    policy: CanonicalHumanLoopPolicy,
    *,
    is_first_contact: bool = False,
) -> bool:
    """Quick check: can this action proceed without human approval?

    Convenience wrapper around evaluate_action for simple yes/no checks.
    External actions ALWAYS return False.
    """
    # Fast path: external is always no
    if action.external_effect:
        return False

    # Fast path: high risk is always no
    if action.risk_level in (RiskLevel.HIGH, RiskLevel.CRITICAL):
        return False

    return not requires_human_approval(
        policy,
        action_type=action.action_type.value,
        risk_level=RiskLevel(action.risk_level),
        confidence=action.confidence,
        is_external=action.external_effect,
        is_first_contact=is_first_contact,
    )


def classify_risk(
    *,
    is_external: bool,
    autonomy_level: AutonomyLevel,
    action_type: ActionType,
    confidence: float,
) -> RiskLevel:
    """Classify risk level based on action properties.

    Utility function for callers that need to determine risk before
    building an Action contract.
    """
    # External actions are always at least MEDIUM
    if is_external:
        if action_type in (
            ActionType.SEND_EXTERNAL,
            ActionType.INVOICE_REQUEST,
        ):
            return RiskLevel.CRITICAL
        return RiskLevel.HIGH

    # L5 actions are always HIGH
    if autonomy_level >= AutonomyLevel.L5_SENSITIVE_EXECUTE:
        return RiskLevel.HIGH

    # L4 actions are at least MEDIUM
    if autonomy_level >= AutonomyLevel.L4_CONTROLLED_EXECUTE:
        return RiskLevel.MEDIUM

    # Low confidence increases risk
    if confidence < 0.3:
        return RiskLevel.MEDIUM

    return RiskLevel.LOW
