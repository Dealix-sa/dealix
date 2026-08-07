"""Tests for the canonical PlaybookVersion self-improvement contracts.

Covers:
  - Deterministic ID generation and idempotency
  - Confidence scoring bounds
  - Version validation
  - Evidence requirements
  - Approval invariants
  - Fail-closed on invalid inputs
  - Builder convenience
  - Entity ownership registry alignment
  - Frozen immutability
"""
from __future__ import annotations

from datetime import UTC, datetime

import pytest

from dealix.company_intelligence.playbook_contracts import (
    CanonicalPlaybookVersion,
    PlaybookApprovalStatus,
    build_playbook_version,
)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


def _playbook(**overrides: object) -> CanonicalPlaybookVersion:
    """Build a minimal valid playbook version, overriding any fields."""
    defaults: dict[str, object] = dict(
        tenant_id="tenant-a",
        playbook_name="sales_qualification",
        version=1,
        change_reason="Improve qualification criteria based on pilot outcomes",
        source_id="source-1",
        evidence_refs=("learning-event-1",),
    )
    defaults.update(overrides)
    return build_playbook_version(**defaults)


# ---------------------------------------------------------------------------
# Deterministic identity
# ---------------------------------------------------------------------------


class TestDeterministicIdentity:
    def test_same_inputs_produce_same_id(self) -> None:
        a = _playbook()
        b = _playbook()
        assert a.playbook_version_id == b.playbook_version_id

    def test_different_name_produces_different_id(self) -> None:
        a = _playbook(playbook_name="sales_qualification")
        b = _playbook(playbook_name="outreach_cadence")
        assert a.playbook_version_id != b.playbook_version_id

    def test_different_version_produces_different_id(self) -> None:
        a = _playbook(version=1)
        b = _playbook(version=2)
        assert a.playbook_version_id != b.playbook_version_id

    def test_different_tenant_produces_different_id(self) -> None:
        a = _playbook(tenant_id="tenant-a")
        b = _playbook(tenant_id="tenant-b")
        assert a.playbook_version_id != b.playbook_version_id

    def test_playbook_id_format(self) -> None:
        a = _playbook()
        assert a.playbook_version_id.startswith("playbook_")
        assert len(a.playbook_version_id) == 9 + 16  # "playbook_" + 16 hex chars

    def test_whitespace_in_name_is_stripped(self) -> None:
        a = _playbook(playbook_name="  sales_qualification  ")
        b = _playbook(playbook_name="sales_qualification")
        assert a.playbook_version_id == b.playbook_version_id

    def test_change_reason_does_not_affect_id(self) -> None:
        """Change reason is mutable metadata — it must not affect the stable ID."""
        a = _playbook(change_reason="Reason A")
        b = _playbook(change_reason="Reason B")
        assert a.playbook_version_id == b.playbook_version_id


# ---------------------------------------------------------------------------
# Version validation
# ---------------------------------------------------------------------------


class TestVersionValidation:
    def test_version_zero_rejected(self) -> None:
        with pytest.raises(ValueError):
            _playbook(version=0)

    def test_negative_version_rejected(self) -> None:
        with pytest.raises(ValueError):
            _playbook(version=-1)

    def test_high_version_accepted(self) -> None:
        a = _playbook(version=50)
        assert a.version == 50


# ---------------------------------------------------------------------------
# Confidence scoring
# ---------------------------------------------------------------------------


class TestConfidenceScoring:
    def test_default_confidence(self) -> None:
        a = _playbook()
        assert a.confidence == 0.5

    def test_confidence_above_one_rejected(self) -> None:
        with pytest.raises(ValueError):
            _playbook(confidence=1.5)

    def test_confidence_below_zero_rejected(self) -> None:
        with pytest.raises(ValueError):
            _playbook(confidence=-0.1)


# ---------------------------------------------------------------------------
# Evidence requirements
# ---------------------------------------------------------------------------


class TestEvidenceRequirements:
    def test_empty_evidence_rejected(self) -> None:
        with pytest.raises(ValueError, match="evidence reference"):
            _playbook(evidence_refs=())

    def test_single_evidence_accepted(self) -> None:
        a = _playbook(evidence_refs=("ref-1",))
        assert a.evidence_refs == ("ref-1",)

    def test_multiple_evidence_accepted(self) -> None:
        a = _playbook(evidence_refs=("ref-1", "ref-2", "ref-3"))
        assert len(a.evidence_refs) == 3


# ---------------------------------------------------------------------------
# Approval invariants
# ---------------------------------------------------------------------------


class TestApprovalInvariants:
    def test_approved_requires_approved_at(self) -> None:
        with pytest.raises(ValueError, match="approved_at"):
            _playbook(
                approval_status=PlaybookApprovalStatus.APPROVED,
                approved_at=None,
            )

    def test_proposed_forbids_approved_at(self) -> None:
        with pytest.raises(ValueError, match="approved_at"):
            _playbook(
                approval_status=PlaybookApprovalStatus.PROPOSED,
                approved_at=datetime.now(UTC),
            )

    def test_under_review_forbids_approved_at(self) -> None:
        with pytest.raises(ValueError, match="approved_at"):
            _playbook(
                approval_status=PlaybookApprovalStatus.UNDER_REVIEW,
                approved_at=datetime.now(UTC),
            )

    def test_approved_with_timestamp(self) -> None:
        now = datetime.now(UTC)
        a = _playbook(
            approval_status=PlaybookApprovalStatus.APPROVED,
            approved_at=now,
        )
        assert a.approval_status == PlaybookApprovalStatus.APPROVED
        assert a.approved_at == now

    def test_rejected_status_accepted(self) -> None:
        a = _playbook(approval_status=PlaybookApprovalStatus.REJECTED)
        assert a.approval_status == PlaybookApprovalStatus.REJECTED


# ---------------------------------------------------------------------------
# Extra field protection
# ---------------------------------------------------------------------------


class TestExtraFieldProtection:
    def test_extra_fields_forbidden(self) -> None:
        a = _playbook()
        data = a.model_dump()
        data["rogue_field"] = "injected"
        with pytest.raises(ValueError):
            CanonicalPlaybookVersion(**data)


# ---------------------------------------------------------------------------
# Builder defaults
# ---------------------------------------------------------------------------


class TestBuilderDefaults:
    def test_default_approval_is_proposed(self) -> None:
        a = _playbook()
        assert a.approval_status == PlaybookApprovalStatus.PROPOSED

    def test_default_confidence(self) -> None:
        a = _playbook()
        assert a.confidence == 0.5

    def test_default_evidence(self) -> None:
        a = build_playbook_version(
            tenant_id="tenant-a",
            playbook_name="test_playbook",
            version=1,
            change_reason="Test reason",
            source_id="source-1",
        )
        assert a.evidence_refs == ("manual_observation",)

    def test_builder_with_full_context(self) -> None:
        now = datetime.now(UTC)
        a = build_playbook_version(
            tenant_id="tenant-a",
            playbook_name="sales_qualification",
            version=3,
            change_reason="Add ICP fit scoring from pilot feedback",
            source_id="source-1",
            evidence_refs=("learning-1", "outcome-2", "proof-3"),
            learning_event_ids=("learn-1", "learn-2"),
            description="Updated qualification criteria",
            changes_summary="Added ICP fit score threshold >= 0.6",
            approval_status=PlaybookApprovalStatus.APPROVED,
            confidence=0.85,
            approved_at=now,
        )
        assert a.version == 3
        assert a.approval_status == PlaybookApprovalStatus.APPROVED
        assert a.confidence == 0.85
        assert len(a.evidence_refs) == 3
        assert len(a.learning_event_ids) == 2


# ---------------------------------------------------------------------------
# Frozen immutability
# ---------------------------------------------------------------------------


class TestFrozenImmutability:
    def test_playbook_is_frozen(self) -> None:
        a = _playbook()
        with pytest.raises(Exception):
            a.approval_status = PlaybookApprovalStatus.APPROVED  # type: ignore[misc]


# ---------------------------------------------------------------------------
# Entity ownership registry alignment
# ---------------------------------------------------------------------------


class TestEntityOwnershipAlignment:
    """Verify the contract satisfies the required fields from
    company_intelligence_entity_ownership.json for PlaybookVersion."""

    def test_required_fields_present(self) -> None:
        a = _playbook()
        # Required: tenant_id, playbook_name, version, change_reason, evidence_refs, approval_status
        assert hasattr(a, "tenant_id") and a.tenant_id
        assert hasattr(a, "playbook_name") and a.playbook_name
        assert hasattr(a, "version") and isinstance(a.version, int)
        assert hasattr(a, "change_reason") and a.change_reason
        assert hasattr(a, "evidence_refs") and len(a.evidence_refs) > 0
        assert hasattr(a, "approval_status") and a.approval_status

    def test_empty_tenant_rejected(self) -> None:
        with pytest.raises(ValueError):
            build_playbook_version(
                tenant_id="",
                playbook_name="test",
                version=1,
                change_reason="Test",
                source_id="source-1",
            )

    def test_empty_playbook_name_rejected(self) -> None:
        with pytest.raises(ValueError):
            build_playbook_version(
                tenant_id="tenant-a",
                playbook_name="",
                version=1,
                change_reason="Test",
                source_id="source-1",
            )

    def test_empty_change_reason_rejected(self) -> None:
        with pytest.raises(ValueError):
            build_playbook_version(
                tenant_id="tenant-a",
                playbook_name="test",
                version=1,
                change_reason="",
                source_id="source-1",
            )

    def test_empty_source_id_rejected(self) -> None:
        with pytest.raises(ValueError):
            build_playbook_version(
                tenant_id="tenant-a",
                playbook_name="test",
                version=1,
                change_reason="Test",
                source_id="",
            )
