"""Canonical Proposal contracts for Company Intelligence.

A Proposal packages an approved Offer for a specific Opportunity with
version tracking, approval gates, and evidence requirements. Proposals
are the bridge between the commercial offer ladder and the customer
engagement — always requiring approval before any external action.

The models are persistence-neutral: no database, network, or LLM calls.

Entity ownership: Proposal → proposal_intelligence
    (proposal factory using approved offers, evidence and capacity constraints).
Required fields: tenant_id, opportunity_id, offer_id, version, status,
    approval_id.
Forbidden parallel names: QuoteProposal, CommercialProposalRecord.
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


class ProposalStatus(StrEnum):
    """Lifecycle states for a proposal."""

    DRAFT = "draft"
    PENDING_REVIEW = "pending_review"
    APPROVED = "approved"
    SENT = "sent"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    EXPIRED = "expired"
    WITHDRAWN = "withdrawn"


# ---------------------------------------------------------------------------
# Stable ID generation
# ---------------------------------------------------------------------------


def _stable_proposal_id(payload: dict[str, Any]) -> str:
    canonical = json.dumps(
        payload,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
        default=str,
    )
    return f"proposal_{sha256(canonical.encode('utf-8')).hexdigest()[:16]}"


# ---------------------------------------------------------------------------
# Canonical Proposal contract
# ---------------------------------------------------------------------------


class CanonicalProposal(BaseModel):
    """One tenant-scoped, versioned proposal for a specific opportunity.

    Proposals are the customer-facing output of the commercial offer
    ladder. They are always draft-first and require explicit approval
    before they can be sent. Sending a proposal is an external action
    that flows through the Draft → Approval chain.

    Key invariants:
      - A proposal is not an invoice; an invoice is not revenue.
      - Version must be positive.
      - Approval ID is required (even if pending).
      - No direct external action authorization.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    # Identity
    tenant_id: NonEmptyString
    proposal_id: NonEmptyString

    # Links
    opportunity_id: NonEmptyString
    offer_id: NonEmptyString
    company_id: str = ""
    action_id: str = ""

    # Versioning
    version: int = Field(default=1, ge=1)

    # Approval
    approval_id: NonEmptyString
    status: ProposalStatus = ProposalStatus.DRAFT

    # Content
    content_summary: str = ""
    pricing_note: str = ""

    # Scoring
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)

    # Evidence
    evidence_refs: tuple[str, ...] = ()

    # Provenance
    source_id: NonEmptyString

    # Timestamps
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    sent_at: datetime | None = None
    expires_at: datetime | None = None

    @model_validator(mode="after")
    def enforce_proposal_invariants(self) -> CanonicalProposal:
        # sent_at must be timezone-aware if set
        if self.sent_at is not None and self.sent_at.tzinfo is None:
            raise ValueError("sent_at must be timezone-aware")

        # expires_at must be timezone-aware if set
        if self.expires_at is not None and self.expires_at.tzinfo is None:
            raise ValueError("expires_at must be timezone-aware")

        # Sent proposals must have sent_at
        if self.status == ProposalStatus.SENT and self.sent_at is None:
            raise ValueError("sent proposals must have a sent_at timestamp")

        # Draft proposals must not have sent_at
        if self.status == ProposalStatus.DRAFT and self.sent_at is not None:
            raise ValueError("draft proposals must not have a sent_at timestamp")

        # Verify deterministic ID
        expected_id = _stable_proposal_id({
            "offer_id": self.offer_id,
            "opportunity_id": self.opportunity_id,
            "tenant_id": self.tenant_id,
            "version": self.version,
        })
        if self.proposal_id != expected_id:
            raise ValueError("proposal_id does not match the canonical payload")

        return self


# ---------------------------------------------------------------------------
# Builder
# ---------------------------------------------------------------------------


def build_proposal(
    *,
    tenant_id: str,
    opportunity_id: str,
    offer_id: str,
    approval_id: str,
    source_id: str,
    company_id: str = "",
    action_id: str = "",
    version: int = 1,
    status: ProposalStatus = ProposalStatus.DRAFT,
    content_summary: str = "",
    pricing_note: str = "",
    confidence: float = 0.5,
    evidence_refs: tuple[str, ...] = (),
    sent_at: datetime | None = None,
    expires_at: datetime | None = None,
) -> CanonicalProposal:
    """Build a deterministic, versioned, approval-gated proposal."""

    proposal_id = _stable_proposal_id({
        "offer_id": offer_id.strip(),
        "opportunity_id": opportunity_id.strip(),
        "tenant_id": tenant_id.strip(),
        "version": version,
    })

    return CanonicalProposal(
        tenant_id=tenant_id,
        proposal_id=proposal_id,
        opportunity_id=opportunity_id,
        offer_id=offer_id,
        company_id=company_id,
        action_id=action_id,
        version=version,
        approval_id=approval_id,
        status=status,
        content_summary=content_summary,
        pricing_note=pricing_note,
        confidence=confidence,
        evidence_refs=evidence_refs,
        source_id=source_id,
        sent_at=sent_at,
        expires_at=expires_at,
    )
