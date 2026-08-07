"""Tests for the canonical Proposal contracts.

Covers:
  - Deterministic ID generation and idempotency
  - Confidence scoring bounds
  - Version validation
  - Status invariants (sent requires sent_at, draft forbids sent_at)
  - Fail-closed on invalid inputs
  - Builder convenience
  - Entity ownership registry alignment
  - Frozen immutability
"""
from __future__ import annotations

from datetime import UTC, datetime, timedelta

import pytest

from dealix.company_intelligence.proposal_contracts import (
    CanonicalProposal,
    ProposalStatus,
    build_proposal,
)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


def _proposal(**overrides: object) -> CanonicalProposal:
    """Build a minimal valid proposal, overriding any fields."""
    defaults: dict[str, object] = dict(
        tenant_id="tenant-a",
        opportunity_id="opp-1",
        offer_id="offer-free-diagnostic",
        approval_id="approval-1",
        source_id="source-1",
    )
    defaults.update(overrides)
    return build_proposal(**defaults)


# ---------------------------------------------------------------------------
# Deterministic identity
# ---------------------------------------------------------------------------


class TestDeterministicIdentity:
    def test_same_inputs_produce_same_id(self) -> None:
        a = _proposal()
        b = _proposal()
        assert a.proposal_id == b.proposal_id

    def test_different_opportunity_produces_different_id(self) -> None:
        a = _proposal(opportunity_id="opp-1")
        b = _proposal(opportunity_id="opp-2")
        assert a.proposal_id != b.proposal_id

    def test_different_offer_produces_different_id(self) -> None:
        a = _proposal(offer_id="offer-1")
        b = _proposal(offer_id="offer-2")
        assert a.proposal_id != b.proposal_id

    def test_different_version_produces_different_id(self) -> None:
        a = _proposal(version=1)
        b = _proposal(version=2)
        assert a.proposal_id != b.proposal_id

    def test_different_tenant_produces_different_id(self) -> None:
        a = _proposal(tenant_id="tenant-a")
        b = _proposal(tenant_id="tenant-b")
        assert a.proposal_id != b.proposal_id

    def test_proposal_id_format(self) -> None:
        a = _proposal()
        assert a.proposal_id.startswith("proposal_")
        assert len(a.proposal_id) == 9 + 16  # "proposal_" + 16 hex chars

    def test_whitespace_in_opportunity_id_is_stripped(self) -> None:
        a = _proposal(opportunity_id="  opp-1  ")
        b = _proposal(opportunity_id="opp-1")
        assert a.proposal_id == b.proposal_id


# ---------------------------------------------------------------------------
# Version validation
# ---------------------------------------------------------------------------


class TestVersionValidation:
    def test_default_version_is_one(self) -> None:
        a = _proposal()
        assert a.version == 1

    def test_version_zero_rejected(self) -> None:
        with pytest.raises(ValueError):
            _proposal(version=0)

    def test_negative_version_rejected(self) -> None:
        with pytest.raises(ValueError):
            _proposal(version=-1)

    def test_high_version_accepted(self) -> None:
        a = _proposal(version=100)
        assert a.version == 100


# ---------------------------------------------------------------------------
# Confidence scoring
# ---------------------------------------------------------------------------


class TestConfidenceScoring:
    def test_default_confidence(self) -> None:
        a = _proposal()
        assert a.confidence == 0.5

    def test_confidence_above_one_rejected(self) -> None:
        with pytest.raises(ValueError):
            _proposal(confidence=1.5)

    def test_confidence_below_zero_rejected(self) -> None:
        with pytest.raises(ValueError):
            _proposal(confidence=-0.1)


# ---------------------------------------------------------------------------
# Status invariants
# ---------------------------------------------------------------------------


class TestStatusInvariants:
    def test_sent_requires_sent_at(self) -> None:
        with pytest.raises(ValueError, match="sent_at"):
            _proposal(status=ProposalStatus.SENT, sent_at=None)

    def test_draft_forbids_sent_at(self) -> None:
        with pytest.raises(ValueError, match="sent_at"):
            _proposal(
                status=ProposalStatus.DRAFT,
                sent_at=datetime.now(UTC),
            )

    def test_sent_with_timestamp(self) -> None:
        now = datetime.now(UTC)
        a = _proposal(status=ProposalStatus.SENT, sent_at=now)
        assert a.status == ProposalStatus.SENT
        assert a.sent_at == now


# ---------------------------------------------------------------------------
# Extra field protection
# ---------------------------------------------------------------------------


class TestExtraFieldProtection:
    def test_extra_fields_forbidden(self) -> None:
        a = _proposal()
        data = a.model_dump()
        data["rogue_field"] = "injected"
        with pytest.raises(ValueError):
            CanonicalProposal(**data)


# ---------------------------------------------------------------------------
# Builder defaults
# ---------------------------------------------------------------------------


class TestBuilderDefaults:
    def test_default_status_is_draft(self) -> None:
        a = _proposal()
        assert a.status == ProposalStatus.DRAFT

    def test_default_version_is_one(self) -> None:
        a = _proposal()
        assert a.version == 1

    def test_default_evidence_empty(self) -> None:
        a = _proposal()
        assert a.evidence_refs == ()

    def test_builder_with_full_context(self) -> None:
        now = datetime.now(UTC)
        a = build_proposal(
            tenant_id="tenant-a",
            opportunity_id="opp-1",
            offer_id="offer-pilot",
            approval_id="approval-1",
            source_id="source-1",
            company_id="company-1",
            action_id="action-1",
            version=2,
            status=ProposalStatus.SENT,
            content_summary="Revenue Command Pilot — 30 day engagement",
            pricing_note="Quote after discovery",
            confidence=0.85,
            evidence_refs=("discovery-call-notes", "icp-fit-analysis"),
            sent_at=now,
            expires_at=now + timedelta(days=30),
        )
        assert a.version == 2
        assert a.status == ProposalStatus.SENT
        assert a.confidence == 0.85
        assert len(a.evidence_refs) == 2
        assert a.sent_at == now


# ---------------------------------------------------------------------------
# Frozen immutability
# ---------------------------------------------------------------------------


class TestFrozenImmutability:
    def test_proposal_is_frozen(self) -> None:
        a = _proposal()
        with pytest.raises(Exception):
            a.status = ProposalStatus.APPROVED  # type: ignore[misc]


# ---------------------------------------------------------------------------
# Entity ownership registry alignment
# ---------------------------------------------------------------------------


class TestEntityOwnershipAlignment:
    """Verify the contract satisfies the required fields from
    company_intelligence_entity_ownership.json for Proposal."""

    def test_required_fields_present(self) -> None:
        a = _proposal()
        # Required: tenant_id, opportunity_id, offer_id, version, status, approval_id
        assert hasattr(a, "tenant_id") and a.tenant_id
        assert hasattr(a, "opportunity_id") and a.opportunity_id
        assert hasattr(a, "offer_id") and a.offer_id
        assert hasattr(a, "version") and isinstance(a.version, int)
        assert hasattr(a, "status") and a.status
        assert hasattr(a, "approval_id") and a.approval_id

    def test_empty_tenant_rejected(self) -> None:
        with pytest.raises(ValueError):
            build_proposal(
                tenant_id="",
                opportunity_id="opp-1",
                offer_id="offer-1",
                approval_id="approval-1",
                source_id="source-1",
            )

    def test_empty_opportunity_id_rejected(self) -> None:
        with pytest.raises(ValueError):
            build_proposal(
                tenant_id="tenant-a",
                opportunity_id="",
                offer_id="offer-1",
                approval_id="approval-1",
                source_id="source-1",
            )

    def test_empty_offer_id_rejected(self) -> None:
        with pytest.raises(ValueError):
            build_proposal(
                tenant_id="tenant-a",
                opportunity_id="opp-1",
                offer_id="",
                approval_id="approval-1",
                source_id="source-1",
            )

    def test_empty_approval_id_rejected(self) -> None:
        with pytest.raises(ValueError):
            build_proposal(
                tenant_id="tenant-a",
                opportunity_id="opp-1",
                offer_id="offer-1",
                approval_id="",
                source_id="source-1",
            )
