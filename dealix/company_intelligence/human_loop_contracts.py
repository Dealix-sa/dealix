"""Canonical HumanLoopPolicy contracts for Company Intelligence.

A HumanLoopPolicy defines tenant-scoped governance for when and how humans
must be involved in the Dealix execution spine. It configures autonomy
thresholds per action type, escalation triggers, and approval requirements —
providing the configurable human-in-the-loop control that allows tenants to
tune how much autonomy the system has.

The fundamental safety invariant is that external actions ALWAYS require
human approval, regardless of how permissive the policy is configured.
This is enforced by the model validator and cannot be overridden.

The models are persistence-neutral: no database, network, or LLM calls.

Entity ownership: HumanLoopPolicy → approval_center
    (configurable human-in-the-loop policies and escalation rules).
Required fields: tenant_id, default_autonomy_level, source_id.
Forbidden parallel names: ApprovalPolicy, HumanGatePolicy.
"""
from __future__ import annotations

import json
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

from dealix.company_intelligence.action_contracts import AutonomyLevel, RiskLevel

NonEmptyString = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------


class HumanLoopMode(StrEnum):
    """Operating modes for human involvement.

    Each mode defines a default posture for how much human input is required.
    Even in AUTONOMOUS mode, external actions ALWAYS require approval.
    """

    FULL_APPROVAL = "full_approval"
    SMART_APPROVAL = "smart_approval"
    NOTIFY_AND_PROCEED = "notify_and_proceed"
    AUTONOMOUS = "autonomous"


class EscalationTrigger(StrEnum):
    """Events or conditions that trigger escalation to a human."""

    LOW_CONFIDENCE = "low_confidence"
    HIGH_RISK = "high_risk"
    EXTERNAL_ACTION = "external_action"
    FIRST_CONTACT = "first_contact"
    HIGH_VALUE = "high_value"
    SENSITIVE_CHANNEL = "sensitive_channel"
    POLICY_EXCEPTION = "policy_exception"


class TimeoutAction(StrEnum):
    """What the system does when a human doesn't respond in time."""

    QUEUE = "queue"
    ESCALATE = "escalate"
    CANCEL = "cancel"


class HumanLoopPolicyStatus(StrEnum):
    """Lifecycle states for a human loop policy."""

    DRAFT = "draft"
    ACTIVE = "active"
    UNDER_REVIEW = "under_review"
    SUSPENDED = "suspended"


# ---------------------------------------------------------------------------
# Stable ID generation
# ---------------------------------------------------------------------------


def _stable_policy_id(payload: dict[str, Any]) -> str:
    canonical = json.dumps(
        payload,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
        default=str,
    )
    return f"hlpolicy_{sha256(canonical.encode('utf-8')).hexdigest()[:16]}"


# ---------------------------------------------------------------------------
# Escalation rule (embedded value object)
# ---------------------------------------------------------------------------


class EscalationRule(BaseModel):
    """One trigger-threshold pair that forces human involvement.

    When the trigger condition is met and the measured value exceeds
    (or falls below) the threshold, the action is escalated to the
    human regardless of the policy's default mode.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    trigger: EscalationTrigger
    threshold: float = Field(default=0.5, ge=0.0, le=1.0)
    required_autonomy_level: AutonomyLevel = AutonomyLevel.L0_OBSERVE
    description: str = ""


# ---------------------------------------------------------------------------
# Canonical HumanLoopPolicy contract
# ---------------------------------------------------------------------------


class CanonicalHumanLoopPolicy(BaseModel):
    """One tenant-scoped human-in-the-loop governance policy.

    HumanLoopPolicies define how much autonomy the system has for a
    given tenant. They control:
      - The default autonomy level for all actions
      - Per-action-type autonomy overrides
      - Escalation rules that force human involvement
      - Notification and timeout behavior
      - Maximum risk level for autonomous actions

    Key invariants:
      - never_auto_external must ALWAYS be True (non-negotiable safety).
      - External actions always require human approval regardless of mode.
      - default_autonomy_level cannot exceed L3_INTERNAL_EXECUTE when
        never_auto_external is True (which is always).
      - At least one evidence reference is required.
      - Policy ID is deterministic from tenant + name.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    # Identity
    tenant_id: NonEmptyString
    policy_id: NonEmptyString

    # Policy configuration
    name: NonEmptyString
    mode: HumanLoopMode = HumanLoopMode.SMART_APPROVAL
    default_autonomy_level: AutonomyLevel = AutonomyLevel.L2_DRAFT
    description: str = ""

    # Per-action-type overrides (action_type value → autonomy level value)
    action_type_overrides: tuple[tuple[str, int], ...] = ()

    # Escalation
    escalation_rules: tuple[EscalationRule, ...] = ()
    max_autonomous_risk: RiskLevel = RiskLevel.LOW

    # Safety — ALWAYS True
    never_auto_external: bool = True
    auto_approve_internal: bool = False

    # Notification
    notification_channels: tuple[str, ...] = ()
    response_timeout_minutes: int = Field(default=60, ge=1, le=10080)
    timeout_action: TimeoutAction = TimeoutAction.QUEUE

    # Status
    status: HumanLoopPolicyStatus = HumanLoopPolicyStatus.DRAFT

    # Scoring
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)

    # Evidence
    evidence_refs: tuple[str, ...] = ()

    # Provenance
    source_id: NonEmptyString

    @model_validator(mode="after")
    def enforce_human_loop_invariants(self) -> CanonicalHumanLoopPolicy:
        # never_auto_external is ALWAYS True — non-negotiable safety
        if not self.never_auto_external:
            raise ValueError(
                "external actions always require human approval "
                "(never_auto_external must be True)"
            )

        # default_autonomy_level cannot exceed L3 when external is blocked
        if self.default_autonomy_level > AutonomyLevel.L3_INTERNAL_EXECUTE:
            raise ValueError(
                "default_autonomy_level cannot exceed L3_INTERNAL_EXECUTE "
                "when never_auto_external is True"
            )

        # AUTONOMOUS mode with auto_approve_internal=False makes no sense
        # but is not forbidden — it just means "autonomous intent, but still
        # requires approval" which effectively behaves like SMART_APPROVAL.

        # At least one evidence reference
        if len(self.evidence_refs) == 0:
            raise ValueError(
                "human loop policy requires at least one evidence reference"
            )

        # Action type overrides must have valid autonomy levels
        valid_levels = {level.value for level in AutonomyLevel}
        for action_type, level_value in self.action_type_overrides:
            if level_value not in valid_levels:
                raise ValueError(
                    f"invalid autonomy level {level_value} "
                    f"in override for action type '{action_type}'"
                )

        # Verify deterministic ID
        expected_id = _stable_policy_id({
            "name": self.name,
            "tenant_id": self.tenant_id,
        })
        if self.policy_id != expected_id:
            raise ValueError("policy_id does not match the canonical payload")

        return self


# ---------------------------------------------------------------------------
# State machine
# ---------------------------------------------------------------------------

_POLICY_TRANSITIONS: dict[
    HumanLoopPolicyStatus, frozenset[HumanLoopPolicyStatus]
] = {
    HumanLoopPolicyStatus.DRAFT: frozenset(
        {HumanLoopPolicyStatus.ACTIVE, HumanLoopPolicyStatus.SUSPENDED}
    ),
    HumanLoopPolicyStatus.ACTIVE: frozenset(
        {HumanLoopPolicyStatus.UNDER_REVIEW, HumanLoopPolicyStatus.SUSPENDED}
    ),
    HumanLoopPolicyStatus.UNDER_REVIEW: frozenset(
        {HumanLoopPolicyStatus.ACTIVE, HumanLoopPolicyStatus.SUSPENDED}
    ),
    HumanLoopPolicyStatus.SUSPENDED: frozenset(
        {HumanLoopPolicyStatus.ACTIVE}
    ),
}


def valid_policy_transitions_from(
    status: HumanLoopPolicyStatus,
) -> frozenset[HumanLoopPolicyStatus]:
    """Return the set of valid target states from *status*."""
    return _POLICY_TRANSITIONS.get(status, frozenset())


def is_valid_policy_transition(
    from_status: HumanLoopPolicyStatus,
    to_status: HumanLoopPolicyStatus,
) -> bool:
    """Check whether *from_status* → *to_status* is a valid transition."""
    return to_status in valid_policy_transitions_from(from_status)


def transition_policy(
    policy: CanonicalHumanLoopPolicy,
    *,
    to_status: HumanLoopPolicyStatus,
) -> CanonicalHumanLoopPolicy:
    """Return a new CanonicalHumanLoopPolicy with *to_status* applied.

    Raises ValueError on invalid transitions. The original is never mutated.
    """
    if not is_valid_policy_transition(policy.status, to_status):
        raise ValueError(
            f"invalid human loop policy transition: "
            f"{policy.status.value} → {to_status.value}"
        )
    updates: dict[str, Any] = {"status": to_status}
    return type(policy).model_validate({**policy.model_dump(), **updates})


# ---------------------------------------------------------------------------
# Policy evaluation helpers
# ---------------------------------------------------------------------------


def requires_human_approval(
    policy: CanonicalHumanLoopPolicy,
    *,
    action_type: str,
    risk_level: RiskLevel,
    confidence: float,
    is_external: bool,
    is_first_contact: bool = False,
) -> bool:
    """Evaluate whether an action requires human approval under *policy*.

    This is the central decision function for the human-in-the-loop system.
    It considers the policy's mode, escalation rules, risk thresholds,
    and the action's properties to determine if a human must approve.

    External actions ALWAYS return True regardless of policy configuration.
    """
    # External actions ALWAYS require human approval — non-negotiable
    if is_external:
        return True

    # FULL_APPROVAL mode — everything needs approval
    if policy.mode == HumanLoopMode.FULL_APPROVAL:
        return True

    # Check risk level against maximum autonomous risk
    if risk_level > policy.max_autonomous_risk:
        return True

    # Check escalation rules
    for rule in policy.escalation_rules:
        if rule.trigger == EscalationTrigger.LOW_CONFIDENCE:
            if confidence < rule.threshold:
                return True
        elif rule.trigger == EscalationTrigger.HIGH_RISK:
            if risk_level.value >= rule.threshold * 5:  # scale to risk enum
                return True
        elif rule.trigger == EscalationTrigger.EXTERNAL_ACTION:
            if is_external:
                return True
        elif rule.trigger == EscalationTrigger.FIRST_CONTACT:
            if is_first_contact:
                return True

    # Check per-action-type overrides
    for override_type, required_level in policy.action_type_overrides:
        if override_type == action_type:
            # If the required level is above L3, human approval needed
            if required_level > AutonomyLevel.L3_INTERNAL_EXECUTE:
                return True
            break

    # SMART_APPROVAL — approve internal low-risk actions automatically
    if policy.mode == HumanLoopMode.SMART_APPROVAL:
        if policy.auto_approve_internal and not is_external:
            return False
        return True

    # NOTIFY_AND_PROCEED — no approval needed for non-external
    if policy.mode == HumanLoopMode.NOTIFY_AND_PROCEED:
        return False

    # AUTONOMOUS — no approval needed for non-external
    if policy.mode == HumanLoopMode.AUTONOMOUS:
        return False

    # Default: require approval (fail-closed)
    return True


# ---------------------------------------------------------------------------
# Builder
# ---------------------------------------------------------------------------


def build_human_loop_policy(
    *,
    tenant_id: str,
    name: str,
    source_id: str,
    mode: HumanLoopMode = HumanLoopMode.SMART_APPROVAL,
    default_autonomy_level: AutonomyLevel = AutonomyLevel.L2_DRAFT,
    description: str = "",
    action_type_overrides: tuple[tuple[str, int], ...] = (),
    escalation_rules: tuple[EscalationRule, ...] = (),
    max_autonomous_risk: RiskLevel = RiskLevel.LOW,
    auto_approve_internal: bool = False,
    notification_channels: tuple[str, ...] = (),
    response_timeout_minutes: int = 60,
    timeout_action: TimeoutAction = TimeoutAction.QUEUE,
    status: HumanLoopPolicyStatus = HumanLoopPolicyStatus.DRAFT,
    confidence: float = 0.5,
    evidence_refs: tuple[str, ...] = ("policy_configuration",),
) -> CanonicalHumanLoopPolicy:
    """Build a deterministic, safety-enforced human loop policy."""

    policy_id = _stable_policy_id({
        "name": name.strip(),
        "tenant_id": tenant_id.strip(),
    })

    return CanonicalHumanLoopPolicy(
        tenant_id=tenant_id,
        policy_id=policy_id,
        name=name,
        mode=mode,
        default_autonomy_level=default_autonomy_level,
        description=description,
        action_type_overrides=action_type_overrides,
        escalation_rules=escalation_rules,
        max_autonomous_risk=max_autonomous_risk,
        never_auto_external=True,
        auto_approve_internal=auto_approve_internal,
        notification_channels=notification_channels,
        response_timeout_minutes=response_timeout_minutes,
        timeout_action=timeout_action,
        status=status,
        confidence=confidence,
        evidence_refs=evidence_refs,
        source_id=source_id,
    )
