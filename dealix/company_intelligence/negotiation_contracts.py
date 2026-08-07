"""Canonical NegotiationStrategy contracts for Company Intelligence.

A NegotiationStrategy captures the intelligence and boundaries for how
Dealix handles commercial negotiations per opportunity. It defines the
approach, price boundaries, concession limits, and evidence-based
tactics — always requiring approval before any commitment.

Negotiation is the bridge between Opportunity scoring and Proposal
generation. It ensures the system can intelligently assist in deal
progression while respecting hard limits set by the tenant.

The models are persistence-neutral: no database, network, or LLM calls.

Entity ownership: NegotiationStrategy → deal_intelligence
    (negotiation intelligence, boundaries and tactics per opportunity).
Required fields: tenant_id, opportunity_id, approach, approval_required,
    source_id.
Forbidden parallel names: BargainStrategy, DealTactics.
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

NonEmptyString = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------


class NegotiationApproach(StrEnum):
    """Strategic approach for handling a negotiation."""

    COLLABORATIVE = "collaborative"
    CONSULTATIVE = "consultative"
    VALUE_BASED = "value_based"
    FIRM = "firm"
    FLEXIBLE = "flexible"


class NegotiationStage(StrEnum):
    """Current stage of a negotiation lifecycle."""

    DISCOVERY = "discovery"
    POSITIONING = "positioning"
    PROPOSAL = "proposal"
    COUNTER = "counter"
    CLOSING = "closing"
    STALEMATE = "stalemate"
    WALKAWAY = "walkaway"
    CLOSED_WON = "closed_won"
    CLOSED_LOST = "closed_lost"


class NegotiationBoundaryType(StrEnum):
    """Types of hard or soft boundaries in a negotiation."""

    PRICE_FLOOR = "price_floor"
    DISCOUNT_CEILING = "discount_ceiling"
    SCOPE_MINIMUM = "scope_minimum"
    TIMELINE_MINIMUM = "timeline_minimum"
    CUSTOM = "custom"


class NegotiationStrategyStatus(StrEnum):
    """Lifecycle states for a negotiation strategy."""

    DRAFT = "draft"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    ABANDONED = "abandoned"


# ---------------------------------------------------------------------------
# Stable ID generation
# ---------------------------------------------------------------------------


def _stable_strategy_id(payload: dict[str, Any]) -> str:
    canonical = json.dumps(
        payload,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
        default=str,
    )
    return f"negstrat_{sha256(canonical.encode('utf-8')).hexdigest()[:16]}"


# ---------------------------------------------------------------------------
# Negotiation boundary (embedded value object)
# ---------------------------------------------------------------------------


class NegotiationBoundary(BaseModel):
    """One hard or soft limit within a negotiation strategy.

    Boundaries define what the system cannot agree to without human
    escalation. Hard limits are non-negotiable; soft limits trigger
    a warning but allow the human approver to override.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    boundary_type: NegotiationBoundaryType
    value: NonEmptyString
    is_hard_limit: bool = True
    evidence_ref: str = ""
    description: str = ""


# ---------------------------------------------------------------------------
# Canonical NegotiationStrategy contract
# ---------------------------------------------------------------------------


class CanonicalNegotiationStrategy(BaseModel):
    """One tenant-scoped negotiation strategy for a specific opportunity.

    NegotiationStrategies provide the intelligence layer for deal
    progression. They define approach, boundaries, concession sequences,
    and value anchors — enabling the system to assist in negotiations
    while maintaining strict approval requirements.

    Key invariants:
      - approval_required must always be True (non-negotiable safety).
      - max_discount_pct must be between 0 and 1.
      - At least one value anchor or evidence ref is required.
      - Boundaries with hard limits cannot be overridden by the system.
      - Strategy ID is deterministic from tenant + opportunity.
      - CLOSED_WON and CLOSED_LOST are terminal stages.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    # Identity
    tenant_id: NonEmptyString
    strategy_id: NonEmptyString

    # Links
    opportunity_id: NonEmptyString
    offer_id: str = ""

    # Strategy
    approach: NegotiationApproach = NegotiationApproach.CONSULTATIVE
    stage: NegotiationStage = NegotiationStage.DISCOVERY

    # Boundaries
    boundaries: tuple[NegotiationBoundary, ...] = ()
    max_discount_pct: float = Field(default=0.0, ge=0.0, le=1.0)
    min_contract_months: int = Field(default=1, ge=0)

    # Tactics
    value_anchors: tuple[str, ...] = ()
    concession_sequence: tuple[str, ...] = ()
    walkaway_conditions: tuple[str, ...] = ()
    objection_responses: tuple[tuple[str, str], ...] = ()

    # Cultural and context notes
    cultural_notes: str = ""
    relationship_context: str = ""

    # Safety — ALWAYS True
    approval_required: bool = True

    # Status
    status: NegotiationStrategyStatus = NegotiationStrategyStatus.DRAFT
    description: str = ""

    # Scoring
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)
    win_probability: float = Field(default=0.0, ge=0.0, le=1.0)

    # Evidence
    evidence_refs: tuple[str, ...] = ()

    # Provenance
    source_id: NonEmptyString

    # Timestamps
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    @model_validator(mode="after")
    def enforce_negotiation_invariants(self) -> CanonicalNegotiationStrategy:
        # approval_required is ALWAYS True — non-negotiable safety
        if not self.approval_required:
            raise ValueError(
                "negotiation strategies always require approval"
            )

        # At least one value anchor or evidence ref
        if len(self.value_anchors) == 0 and len(self.evidence_refs) == 0:
            raise ValueError(
                "negotiation strategy requires at least one value anchor "
                "or evidence reference"
            )

        # Verify deterministic ID
        expected_id = _stable_strategy_id({
            "opportunity_id": self.opportunity_id,
            "tenant_id": self.tenant_id,
        })
        if self.strategy_id != expected_id:
            raise ValueError(
                "strategy_id does not match the canonical payload"
            )

        return self


# ---------------------------------------------------------------------------
# State machine
# ---------------------------------------------------------------------------

_NEGOTIATION_TRANSITIONS: dict[
    NegotiationStage, frozenset[NegotiationStage]
] = {
    NegotiationStage.DISCOVERY: frozenset(
        {NegotiationStage.POSITIONING, NegotiationStage.WALKAWAY}
    ),
    NegotiationStage.POSITIONING: frozenset(
        {NegotiationStage.PROPOSAL, NegotiationStage.WALKAWAY}
    ),
    NegotiationStage.PROPOSAL: frozenset(
        {
            NegotiationStage.COUNTER,
            NegotiationStage.CLOSING,
            NegotiationStage.STALEMATE,
            NegotiationStage.WALKAWAY,
        }
    ),
    NegotiationStage.COUNTER: frozenset(
        {
            NegotiationStage.PROPOSAL,
            NegotiationStage.CLOSING,
            NegotiationStage.STALEMATE,
            NegotiationStage.WALKAWAY,
        }
    ),
    NegotiationStage.CLOSING: frozenset(
        {NegotiationStage.CLOSED_WON, NegotiationStage.CLOSED_LOST}
    ),
    NegotiationStage.STALEMATE: frozenset(
        {
            NegotiationStage.COUNTER,
            NegotiationStage.WALKAWAY,
            NegotiationStage.CLOSING,
        }
    ),
    NegotiationStage.WALKAWAY: frozenset(
        {NegotiationStage.CLOSED_LOST}
    ),
    NegotiationStage.CLOSED_WON: frozenset(),   # terminal
    NegotiationStage.CLOSED_LOST: frozenset(),  # terminal
}

_STATUS_TRANSITIONS: dict[
    NegotiationStrategyStatus, frozenset[NegotiationStrategyStatus]
] = {
    NegotiationStrategyStatus.DRAFT: frozenset(
        {NegotiationStrategyStatus.ACTIVE, NegotiationStrategyStatus.ABANDONED}
    ),
    NegotiationStrategyStatus.ACTIVE: frozenset(
        {
            NegotiationStrategyStatus.PAUSED,
            NegotiationStrategyStatus.COMPLETED,
            NegotiationStrategyStatus.ABANDONED,
        }
    ),
    NegotiationStrategyStatus.PAUSED: frozenset(
        {NegotiationStrategyStatus.ACTIVE, NegotiationStrategyStatus.ABANDONED}
    ),
    NegotiationStrategyStatus.COMPLETED: frozenset(),   # terminal
    NegotiationStrategyStatus.ABANDONED: frozenset(),   # terminal
}


def valid_negotiation_stage_transitions_from(
    stage: NegotiationStage,
) -> frozenset[NegotiationStage]:
    """Return the set of valid target stages from *stage*."""
    return _NEGOTIATION_TRANSITIONS.get(stage, frozenset())


def is_valid_negotiation_stage_transition(
    from_stage: NegotiationStage,
    to_stage: NegotiationStage,
) -> bool:
    """Check whether *from_stage* → *to_stage* is a valid stage transition."""
    return to_stage in valid_negotiation_stage_transitions_from(from_stage)


def valid_strategy_transitions_from(
    status: NegotiationStrategyStatus,
) -> frozenset[NegotiationStrategyStatus]:
    """Return the set of valid target statuses from *status*."""
    return _STATUS_TRANSITIONS.get(status, frozenset())


def is_valid_strategy_transition(
    from_status: NegotiationStrategyStatus,
    to_status: NegotiationStrategyStatus,
) -> bool:
    """Check whether *from_status* → *to_status* is a valid status transition."""
    return to_status in valid_strategy_transitions_from(from_status)


def transition_negotiation_stage(
    strategy: CanonicalNegotiationStrategy,
    *,
    to_stage: NegotiationStage,
) -> CanonicalNegotiationStrategy:
    """Return a new strategy with *to_stage* applied.

    Raises ValueError on invalid transitions. The original is never mutated.
    """
    if not is_valid_negotiation_stage_transition(strategy.stage, to_stage):
        raise ValueError(
            f"invalid negotiation stage transition: "
            f"{strategy.stage.value} → {to_stage.value}"
        )
    updates: dict[str, Any] = {"stage": to_stage}
    return type(strategy).model_validate({**strategy.model_dump(), **updates})


def transition_negotiation_status(
    strategy: CanonicalNegotiationStrategy,
    *,
    to_status: NegotiationStrategyStatus,
) -> CanonicalNegotiationStrategy:
    """Return a new strategy with *to_status* applied.

    Raises ValueError on invalid transitions. The original is never mutated.
    """
    if not is_valid_strategy_transition(strategy.status, to_status):
        raise ValueError(
            f"invalid negotiation status transition: "
            f"{strategy.status.value} → {to_status.value}"
        )
    updates: dict[str, Any] = {"status": to_status}
    return type(strategy).model_validate({**strategy.model_dump(), **updates})


# ---------------------------------------------------------------------------
# Builder
# ---------------------------------------------------------------------------


def build_negotiation_strategy(
    *,
    tenant_id: str,
    opportunity_id: str,
    source_id: str,
    offer_id: str = "",
    approach: NegotiationApproach = NegotiationApproach.CONSULTATIVE,
    stage: NegotiationStage = NegotiationStage.DISCOVERY,
    boundaries: tuple[NegotiationBoundary, ...] = (),
    max_discount_pct: float = 0.0,
    min_contract_months: int = 1,
    value_anchors: tuple[str, ...] = (),
    concession_sequence: tuple[str, ...] = (),
    walkaway_conditions: tuple[str, ...] = (),
    objection_responses: tuple[tuple[str, str], ...] = (),
    cultural_notes: str = "",
    relationship_context: str = "",
    status: NegotiationStrategyStatus = NegotiationStrategyStatus.DRAFT,
    description: str = "",
    confidence: float = 0.5,
    win_probability: float = 0.0,
    evidence_refs: tuple[str, ...] = ("manual_assessment",),
) -> CanonicalNegotiationStrategy:
    """Build a deterministic, approval-gated negotiation strategy."""

    strategy_id = _stable_strategy_id({
        "opportunity_id": opportunity_id.strip(),
        "tenant_id": tenant_id.strip(),
    })

    return CanonicalNegotiationStrategy(
        tenant_id=tenant_id,
        strategy_id=strategy_id,
        opportunity_id=opportunity_id,
        offer_id=offer_id,
        approach=approach,
        stage=stage,
        boundaries=boundaries,
        max_discount_pct=max_discount_pct,
        min_contract_months=min_contract_months,
        value_anchors=value_anchors,
        concession_sequence=concession_sequence,
        walkaway_conditions=walkaway_conditions,
        objection_responses=objection_responses,
        cultural_notes=cultural_notes,
        relationship_context=relationship_context,
        approval_required=True,
        status=status,
        description=description,
        confidence=confidence,
        win_probability=win_probability,
        evidence_refs=evidence_refs,
        source_id=source_id,
    )
