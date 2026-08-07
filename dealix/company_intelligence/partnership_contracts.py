"""Canonical PartnershipOpportunity contracts for Company Intelligence.

Partnerships are a distinct opportunity class from sales opportunities.
They represent market-access, capability, or channel relationships with
partner companies — governed by the same evidence-first, approval-required
principles as the rest of the execution spine.

The models are persistence-neutral: no database, network, or LLM calls.

Entity ownership: PartnershipOpportunity → partnership_intelligence
    (partnership and market-access opportunity intelligence).
Required fields: tenant_id, company_id, partnership_type, score,
    score_reasons, next_action.
Forbidden parallel names: PartnerDeal, AllianceOpportunity.
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


class PartnershipType(StrEnum):
    """Categories of partnership opportunity."""

    CHANNEL_PARTNER = "channel_partner"
    TECHNOLOGY_PARTNER = "technology_partner"
    REFERRAL_PARTNER = "referral_partner"
    RESELLER = "reseller"
    INTEGRATOR = "integrator"
    CO_SELL = "co_sell"
    MARKET_ACCESS = "market_access"
    CAPABILITY = "capability"
    OTHER = "other"


class PartnershipStage(StrEnum):
    """Lifecycle stages for a partnership opportunity."""

    SIGNAL_DETECTED = "signal_detected"
    RESEARCHED = "researched"
    QUALIFIED = "qualified"
    PROPOSAL_DRAFTED = "proposal_drafted"
    UNDER_REVIEW = "under_review"
    APPROVED = "approved"
    ACTIVE = "active"
    PAUSED = "paused"
    DISSOLVED = "dissolved"


# ---------------------------------------------------------------------------
# Stable ID generation
# ---------------------------------------------------------------------------


def _stable_partnership_id(payload: dict[str, Any]) -> str:
    canonical = json.dumps(
        payload,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
        default=str,
    )
    return f"partner_{sha256(canonical.encode('utf-8')).hexdigest()[:16]}"


# ---------------------------------------------------------------------------
# Canonical PartnershipOpportunity contract
# ---------------------------------------------------------------------------


class CanonicalPartnershipOpportunity(BaseModel):
    """One tenant-scoped, evidence-graded partnership opportunity.

    PartnershipOpportunities track market-access and capability
    partnerships separately from sales Opportunities. They never
    authorize external action by themselves — that requires the
    Action → Draft → Approval chain.

    Key invariants:
      - External action is never authorized directly.
      - Approval is always required.
      - Score is bounded 0–100.
      - Dissolved partnerships are terminal.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    # Identity
    tenant_id: NonEmptyString
    partnership_id: NonEmptyString
    company_id: NonEmptyString

    # Classification
    partnership_type: PartnershipType
    stage: PartnershipStage = PartnershipStage.SIGNAL_DETECTED

    # Scoring
    score: int = Field(default=0, ge=0, le=100)
    score_reasons: dict[str, Any] = Field(default_factory=dict)
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)

    # Provenance
    source_id: NonEmptyString
    signal_ids: tuple[str, ...] = ()

    # Execution control
    next_action: str = ""
    proof_target: str = ""
    approval_required: bool = True
    external_action_allowed: bool = False

    # Context
    description: str = ""
    expected_value: str = ""

    # Timestamps
    detected_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    last_reviewed_at: datetime | None = None

    @model_validator(mode="after")
    def enforce_partnership_invariants(self) -> CanonicalPartnershipOpportunity:
        # Partnerships never authorize external action
        if self.external_action_allowed:
            raise ValueError(
                "partnership opportunities never authorize external execution"
            )

        # Approval is always required
        if not self.approval_required:
            raise ValueError(
                "partnership opportunities always require approval"
            )

        # Verify deterministic ID
        expected_id = _stable_partnership_id({
            "company_id": self.company_id,
            "partnership_type": self.partnership_type.value,
            "source_id": self.source_id,
            "tenant_id": self.tenant_id,
        })
        if self.partnership_id != expected_id:
            raise ValueError("partnership_id does not match the canonical payload")

        return self


# ---------------------------------------------------------------------------
# Builder
# ---------------------------------------------------------------------------


def build_partnership_opportunity(
    *,
    tenant_id: str,
    company_id: str,
    partnership_type: PartnershipType,
    source_id: str,
    stage: PartnershipStage = PartnershipStage.SIGNAL_DETECTED,
    score: int = 0,
    score_reasons: dict[str, Any] | None = None,
    confidence: float = 0.5,
    signal_ids: tuple[str, ...] = (),
    next_action: str = "",
    proof_target: str = "",
    description: str = "",
    expected_value: str = "",
    last_reviewed_at: datetime | None = None,
) -> CanonicalPartnershipOpportunity:
    """Build a deterministic, idempotent, evidence-graded partnership."""

    partnership_id = _stable_partnership_id({
        "company_id": company_id.strip(),
        "partnership_type": partnership_type.value,
        "source_id": source_id.strip(),
        "tenant_id": tenant_id.strip(),
    })

    return CanonicalPartnershipOpportunity(
        tenant_id=tenant_id,
        partnership_id=partnership_id,
        company_id=company_id,
        partnership_type=partnership_type,
        stage=stage,
        score=score,
        score_reasons=score_reasons or {},
        confidence=confidence,
        source_id=source_id,
        signal_ids=signal_ids,
        next_action=next_action,
        proof_target=proof_target,
        description=description,
        expected_value=expected_value,
        last_reviewed_at=last_reviewed_at,
    )


# ---------------------------------------------------------------------------
# State machine
# ---------------------------------------------------------------------------


_PARTNERSHIP_TRANSITIONS: dict[PartnershipStage, frozenset[PartnershipStage]] = {
    PartnershipStage.SIGNAL_DETECTED: frozenset({
        PartnershipStage.RESEARCHED,
        PartnershipStage.DISSOLVED,
    }),
    PartnershipStage.RESEARCHED: frozenset({
        PartnershipStage.QUALIFIED,
        PartnershipStage.DISSOLVED,
    }),
    PartnershipStage.QUALIFIED: frozenset({
        PartnershipStage.PROPOSAL_DRAFTED,
        PartnershipStage.DISSOLVED,
    }),
    PartnershipStage.PROPOSAL_DRAFTED: frozenset({
        PartnershipStage.UNDER_REVIEW,
        PartnershipStage.DISSOLVED,
    }),
    PartnershipStage.UNDER_REVIEW: frozenset({
        PartnershipStage.APPROVED,
        PartnershipStage.DISSOLVED,
    }),
    PartnershipStage.APPROVED: frozenset({
        PartnershipStage.ACTIVE,
        PartnershipStage.DISSOLVED,
    }),
    PartnershipStage.ACTIVE: frozenset({
        PartnershipStage.PAUSED,
        PartnershipStage.DISSOLVED,
    }),
    PartnershipStage.PAUSED: frozenset({
        PartnershipStage.ACTIVE,
        PartnershipStage.DISSOLVED,
    }),
    # Terminal
    PartnershipStage.DISSOLVED: frozenset(),
}


def valid_partnership_transitions_from(
    stage: PartnershipStage,
) -> frozenset[PartnershipStage]:
    """Return the set of valid next stages from the given stage."""
    return _PARTNERSHIP_TRANSITIONS.get(stage, frozenset())


def is_valid_partnership_transition(
    from_stage: PartnershipStage,
    to_stage: PartnershipStage,
) -> bool:
    """Check whether a transition between two partnership stages is valid."""
    return to_stage in valid_partnership_transitions_from(from_stage)


def transition_partnership(
    partnership: CanonicalPartnershipOpportunity,
    *,
    to_stage: PartnershipStage,
) -> CanonicalPartnershipOpportunity:
    """Return a new Partnership with an updated stage after validating the transition.

    The returned Partnership is a new frozen instance — the original is unchanged.
    """
    if not is_valid_partnership_transition(partnership.stage, to_stage):
        raise ValueError(
            f"invalid partnership transition: "
            f"{partnership.stage.value} → {to_stage.value}"
        )
    updates: dict[str, Any] = {"stage": to_stage}
    return type(partnership).model_validate({**partnership.model_dump(), **updates})
