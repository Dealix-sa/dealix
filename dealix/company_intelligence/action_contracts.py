"""Canonical Action Queue contracts for the Company Intelligence execution spine.

Every Company Loop stage produces or consumes Actions. This contract provides
the single normalized shape for queued, prioritized, tenant-scoped work items.

The models are persistence-neutral: no database, network, or LLM calls. They
connect Opportunity → Action → Draft → Approval → Outcome and feed the Daily
Command with its top-priority action list.
"""
from __future__ import annotations

import json
from datetime import UTC, datetime
from enum import IntEnum, StrEnum
from hashlib import sha256
from typing import Annotated, Any

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    StringConstraints,
    model_validator,
)

NonEmptyString = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------


class ActionType(StrEnum):
    """Categories of work items the Action Queue can hold."""

    RESEARCH = "research"
    QUALIFY = "qualify"
    PREPARE_DRAFT = "prepare_draft"
    SCHEDULE_MEETING = "schedule_meeting"
    CONDUCT_DISCOVERY = "conduct_discovery"
    PREPARE_PROPOSAL = "prepare_proposal"
    SEND_EXTERNAL = "send_external"
    RECORD_OUTCOME = "record_outcome"
    RECORD_PROOF = "record_proof"
    DELIVERY_TASK = "delivery_task"
    APPROVAL_REQUEST = "approval_request"
    INVOICE_REQUEST = "invoice_request"
    INTERNAL_UPDATE = "internal_update"
    LEARNING_PROPOSAL = "learning_proposal"
    SYSTEM_TASK = "system_task"


class AutonomyLevel(IntEnum):
    """Maps to the L0–L5 authority model from the operating manual.

    Higher levels require more human involvement before execution.
    """

    L0_OBSERVE = 0
    L1_ANALYZE = 1
    L2_DRAFT = 2
    L3_INTERNAL_EXECUTE = 3
    L4_CONTROLLED_EXECUTE = 4
    L5_SENSITIVE_EXECUTE = 5


class ActionStatus(StrEnum):
    """Valid states in the Action lifecycle."""

    QUEUED = "queued"
    IN_PROGRESS = "in_progress"
    BLOCKED = "blocked"
    AWAITING_APPROVAL = "awaiting_approval"
    APPROVED = "approved"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    EXPIRED = "expired"


class RiskLevel(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


# Valid state transitions — fail-closed on anything not listed.
_VALID_TRANSITIONS: dict[ActionStatus, frozenset[ActionStatus]] = {
    ActionStatus.QUEUED: frozenset({
        ActionStatus.IN_PROGRESS,
        ActionStatus.BLOCKED,
        ActionStatus.CANCELLED,
        ActionStatus.EXPIRED,
    }),
    ActionStatus.IN_PROGRESS: frozenset({
        ActionStatus.COMPLETED,
        ActionStatus.FAILED,
        ActionStatus.BLOCKED,
        ActionStatus.AWAITING_APPROVAL,
        ActionStatus.CANCELLED,
    }),
    ActionStatus.BLOCKED: frozenset({
        ActionStatus.QUEUED,
        ActionStatus.CANCELLED,
        ActionStatus.EXPIRED,
    }),
    ActionStatus.AWAITING_APPROVAL: frozenset({
        ActionStatus.APPROVED,
        ActionStatus.CANCELLED,
        ActionStatus.EXPIRED,
    }),
    ActionStatus.APPROVED: frozenset({
        ActionStatus.IN_PROGRESS,
        ActionStatus.CANCELLED,
    }),
    ActionStatus.COMPLETED: frozenset(),
    ActionStatus.FAILED: frozenset({
        ActionStatus.QUEUED,  # retry
    }),
    ActionStatus.CANCELLED: frozenset(),
    ActionStatus.EXPIRED: frozenset(),
}


def is_valid_transition(from_status: ActionStatus, to_status: ActionStatus) -> bool:
    """Check whether a status transition is allowed."""
    return to_status in _VALID_TRANSITIONS.get(from_status, frozenset())


def valid_transitions_from(status: ActionStatus) -> frozenset[ActionStatus]:
    """Return the set of states reachable from *status*."""
    return _VALID_TRANSITIONS.get(status, frozenset())


# ---------------------------------------------------------------------------
# Priority scoring
# ---------------------------------------------------------------------------


def compute_priority_score(
    *,
    impact: float,
    urgency: float,
    confidence: float,
    reversibility: float,
    effort: float,
    risk: float,
) -> float:
    """Priority = (Impact × Urgency × Confidence × Reversibility) ÷ (Effort × Risk).

    All inputs are 0.0–1.0. Effort and Risk are clamped to a minimum of 0.01
    to prevent division-by-zero while preserving the formula's intent.
    """
    for name, value in [
        ("impact", impact),
        ("urgency", urgency),
        ("confidence", confidence),
        ("reversibility", reversibility),
        ("effort", effort),
        ("risk", risk),
    ]:
        if not 0.0 <= value <= 1.0:
            raise ValueError(f"{name} must be between 0.0 and 1.0, got {value}")

    denominator = max(effort, 0.01) * max(risk, 0.01)
    return round((impact * urgency * confidence * reversibility) / denominator, 6)


# ---------------------------------------------------------------------------
# Stable ID generation (matches outcome_contracts pattern)
# ---------------------------------------------------------------------------


def _stable_action_id(payload: dict[str, Any]) -> str:
    canonical = json.dumps(
        payload,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
        default=str,
    )
    return f"action_{sha256(canonical.encode('utf-8')).hexdigest()[:16]}"


# ---------------------------------------------------------------------------
# Canonical Action contract
# ---------------------------------------------------------------------------


class CanonicalAction(BaseModel):
    """One queued, prioritized, tenant-scoped work item.

    Actions are the central node of the execution spine. Every Company Loop
    stage produces or consumes them.  An Action never authorizes external
    execution by itself — that requires an explicit Approval transition.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    # Identity
    tenant_id: NonEmptyString
    action_id: NonEmptyString
    idempotency_key: NonEmptyString

    # Classification
    action_type: ActionType
    department: NonEmptyString
    risk_level: RiskLevel = RiskLevel.MEDIUM
    autonomy_level: AutonomyLevel

    # Context links
    loop_id: str = ""
    stage_id: str = ""
    opportunity_id: str = ""
    trigger: str = ""
    objective: str = ""

    # Priority inputs
    impact: float = Field(default=0.5, ge=0.0, le=1.0)
    urgency: float = Field(default=0.5, ge=0.0, le=1.0)
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)
    reversibility: float = Field(default=0.5, ge=0.0, le=1.0)
    effort: float = Field(default=0.5, ge=0.0, le=1.0)
    risk: float = Field(default=0.5, ge=0.0, le=1.0)
    priority_score: float = Field(default=0.0, ge=0.0)

    # Execution
    status: ActionStatus = ActionStatus.QUEUED
    approval_required: bool = True
    external_effect: bool = False
    proof_requirement: str = ""
    expected_output: str = ""
    failure_owner: str = ""
    max_retries: int = Field(default=0, ge=0, le=5)
    retry_count: int = Field(default=0, ge=0)

    # Timestamps
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    due_at: datetime | None = None

    @model_validator(mode="after")
    def enforce_action_invariants(self) -> CanonicalAction:
        # External effects always require approval
        if self.external_effect and not self.approval_required:
            raise ValueError("actions with external effects require approval")

        # L5 sensitive actions always require approval
        if self.autonomy_level >= AutonomyLevel.L5_SENSITIVE_EXECUTE and not self.approval_required:
            raise ValueError("L5 sensitive actions require approval")

        # External effects need at least L4
        if self.external_effect and self.autonomy_level < AutonomyLevel.L4_CONTROLLED_EXECUTE:
            raise ValueError("external effects require autonomy level L4 or higher")

        # Retry count cannot exceed max
        if self.retry_count > self.max_retries:
            raise ValueError("retry_count exceeds max_retries")

        # Verify priority score matches inputs
        expected_score = compute_priority_score(
            impact=self.impact,
            urgency=self.urgency,
            confidence=self.confidence,
            reversibility=self.reversibility,
            effort=self.effort,
            risk=self.risk,
        )
        if abs(self.priority_score - expected_score) > 1e-4:
            raise ValueError(
                f"priority_score {self.priority_score} does not match "
                f"computed score {expected_score}"
            )

        # Verify deterministic ID
        expected_id = _stable_action_id({
            "action_type": self.action_type.value,
            "department": self.department,
            "idempotency_key": self.idempotency_key,
            "tenant_id": self.tenant_id,
        })
        if self.action_id != expected_id:
            raise ValueError("action_id does not match the canonical payload")

        return self


# ---------------------------------------------------------------------------
# Builder
# ---------------------------------------------------------------------------


def build_action(
    *,
    tenant_id: str,
    idempotency_key: str,
    action_type: ActionType,
    department: str,
    risk_level: RiskLevel = RiskLevel.MEDIUM,
    autonomy_level: AutonomyLevel,
    loop_id: str = "",
    stage_id: str = "",
    opportunity_id: str = "",
    trigger: str = "",
    objective: str = "",
    impact: float = 0.5,
    urgency: float = 0.5,
    confidence: float = 0.5,
    reversibility: float = 0.5,
    effort: float = 0.5,
    risk: float = 0.5,
    approval_required: bool = True,
    external_effect: bool = False,
    proof_requirement: str = "",
    expected_output: str = "",
    failure_owner: str = "",
    max_retries: int = 0,
    due_at: datetime | None = None,
) -> CanonicalAction:
    """Build a deterministic, idempotent, prioritized action."""

    priority_score = compute_priority_score(
        impact=impact,
        urgency=urgency,
        confidence=confidence,
        reversibility=reversibility,
        effort=effort,
        risk=risk,
    )

    action_id = _stable_action_id({
        "action_type": action_type.value,
        "department": department.strip(),
        "idempotency_key": idempotency_key.strip(),
        "tenant_id": tenant_id.strip(),
    })

    return CanonicalAction(
        tenant_id=tenant_id,
        action_id=action_id,
        idempotency_key=idempotency_key,
        action_type=action_type,
        department=department,
        risk_level=risk_level,
        autonomy_level=autonomy_level,
        loop_id=loop_id,
        stage_id=stage_id,
        opportunity_id=opportunity_id,
        trigger=trigger,
        objective=objective,
        impact=impact,
        urgency=urgency,
        confidence=confidence,
        reversibility=reversibility,
        effort=effort,
        risk=risk,
        priority_score=priority_score,
        approval_required=approval_required,
        external_effect=external_effect,
        proof_requirement=proof_requirement,
        expected_output=expected_output,
        failure_owner=failure_owner,
        max_retries=max_retries,
        due_at=due_at,
    )


def transition_action(
    action: CanonicalAction,
    *,
    to_status: ActionStatus,
) -> CanonicalAction:
    """Return a new Action with an updated status after validating the transition.

    The returned Action is a new frozen instance — the original is unchanged.
    """
    if not is_valid_transition(action.status, to_status):
        raise ValueError(
            f"invalid transition {action.status.value} → {to_status.value}; "
            f"allowed: {sorted(s.value for s in valid_transitions_from(action.status))}"
        )

    retry_count = action.retry_count
    if action.status == ActionStatus.FAILED and to_status == ActionStatus.QUEUED:
        retry_count = action.retry_count + 1

    updates = {"status": to_status, "retry_count": retry_count}
    return type(action).model_validate({**action.model_dump(), **updates})
