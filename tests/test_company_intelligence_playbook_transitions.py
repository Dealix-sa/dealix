"""Tests for PlaybookVersion approval state machine transitions.

Covers:
  - Proposed → under_review → approved pipeline
  - Proposed → rejected shortcut
  - Approved → superseded lifecycle
  - Rejected and superseded as terminal
  - approved_at auto-set on approval
  - Invalid transition rejection
  - Frozen immutability of original after transition
"""
from __future__ import annotations

import pytest

from dealix.company_intelligence.playbook_contracts import (
    PlaybookApprovalStatus,
    build_playbook_version,
    is_valid_playbook_transition,
    transition_playbook,
    valid_playbook_transitions_from,
)


def _playbook(**overrides: object):
    defaults = dict(
        tenant_id="tenant-a",
        playbook_name="outreach_v1",
        version=1,
        change_reason="Initial playbook creation",
        source_id="source-1",
        evidence_refs=("manual_observation",),
    )
    defaults.update(overrides)
    return build_playbook_version(**defaults)


# ---------------------------------------------------------------------------
# Valid transitions
# ---------------------------------------------------------------------------


class TestValidTransitions:
    def test_proposed_to_under_review(self) -> None:
        p = _playbook(approval_status=PlaybookApprovalStatus.PROPOSED)
        result = transition_playbook(p, to_status=PlaybookApprovalStatus.UNDER_REVIEW)
        assert result.approval_status == PlaybookApprovalStatus.UNDER_REVIEW

    def test_proposed_to_rejected(self) -> None:
        p = _playbook(approval_status=PlaybookApprovalStatus.PROPOSED)
        result = transition_playbook(p, to_status=PlaybookApprovalStatus.REJECTED)
        assert result.approval_status == PlaybookApprovalStatus.REJECTED

    def test_under_review_to_approved(self) -> None:
        p = _playbook(approval_status=PlaybookApprovalStatus.UNDER_REVIEW)
        result = transition_playbook(p, to_status=PlaybookApprovalStatus.APPROVED)
        assert result.approval_status == PlaybookApprovalStatus.APPROVED
        assert result.approved_at is not None

    def test_under_review_to_rejected(self) -> None:
        p = _playbook(approval_status=PlaybookApprovalStatus.UNDER_REVIEW)
        result = transition_playbook(p, to_status=PlaybookApprovalStatus.REJECTED)
        assert result.approval_status == PlaybookApprovalStatus.REJECTED

    def test_approved_to_superseded(self) -> None:
        p = _playbook(approval_status=PlaybookApprovalStatus.UNDER_REVIEW)
        p = transition_playbook(p, to_status=PlaybookApprovalStatus.APPROVED)
        result = transition_playbook(p, to_status=PlaybookApprovalStatus.SUPERSEDED)
        assert result.approval_status == PlaybookApprovalStatus.SUPERSEDED


# ---------------------------------------------------------------------------
# Full lifecycle
# ---------------------------------------------------------------------------


class TestFullLifecycle:
    def test_full_approval_lifecycle(self) -> None:
        """Proposed → under_review → approved → superseded."""
        p = _playbook(approval_status=PlaybookApprovalStatus.PROPOSED)
        p = transition_playbook(p, to_status=PlaybookApprovalStatus.UNDER_REVIEW)
        p = transition_playbook(p, to_status=PlaybookApprovalStatus.APPROVED)
        p = transition_playbook(p, to_status=PlaybookApprovalStatus.SUPERSEDED)
        assert p.approval_status == PlaybookApprovalStatus.SUPERSEDED


# ---------------------------------------------------------------------------
# approved_at behavior
# ---------------------------------------------------------------------------


class TestApprovedAt:
    def test_approved_at_set_automatically(self) -> None:
        p = _playbook(approval_status=PlaybookApprovalStatus.UNDER_REVIEW)
        result = transition_playbook(p, to_status=PlaybookApprovalStatus.APPROVED)
        assert result.approved_at is not None

    def test_approved_at_custom_value(self) -> None:
        from datetime import UTC, datetime

        ts = datetime(2026, 1, 1, tzinfo=UTC)
        p = _playbook(approval_status=PlaybookApprovalStatus.UNDER_REVIEW)
        result = transition_playbook(
            p, to_status=PlaybookApprovalStatus.APPROVED, approved_at=ts
        )
        assert result.approved_at == ts


# ---------------------------------------------------------------------------
# Terminal states
# ---------------------------------------------------------------------------


class TestTerminalStates:
    @pytest.mark.parametrize("status", [
        PlaybookApprovalStatus.REJECTED,
        PlaybookApprovalStatus.SUPERSEDED,
    ])
    def test_terminal_has_no_transitions(
        self, status: PlaybookApprovalStatus
    ) -> None:
        assert valid_playbook_transitions_from(status) == frozenset()

    def test_rejected_transition_rejected(self) -> None:
        p = _playbook(approval_status=PlaybookApprovalStatus.REJECTED)
        with pytest.raises(ValueError, match="invalid playbook transition"):
            transition_playbook(p, to_status=PlaybookApprovalStatus.PROPOSED)

    def test_superseded_transition_rejected(self) -> None:
        p = _playbook(approval_status=PlaybookApprovalStatus.UNDER_REVIEW)
        p = transition_playbook(p, to_status=PlaybookApprovalStatus.APPROVED)
        p = transition_playbook(p, to_status=PlaybookApprovalStatus.SUPERSEDED)
        with pytest.raises(ValueError, match="invalid playbook transition"):
            transition_playbook(p, to_status=PlaybookApprovalStatus.APPROVED)


# ---------------------------------------------------------------------------
# Invalid transitions
# ---------------------------------------------------------------------------


class TestInvalidTransitions:
    def test_proposed_cannot_jump_to_approved(self) -> None:
        p = _playbook(approval_status=PlaybookApprovalStatus.PROPOSED)
        with pytest.raises(ValueError, match="invalid playbook transition"):
            transition_playbook(p, to_status=PlaybookApprovalStatus.APPROVED)

    def test_proposed_cannot_jump_to_superseded(self) -> None:
        p = _playbook(approval_status=PlaybookApprovalStatus.PROPOSED)
        with pytest.raises(ValueError, match="invalid playbook transition"):
            transition_playbook(p, to_status=PlaybookApprovalStatus.SUPERSEDED)

    def test_approved_cannot_return_to_under_review(self) -> None:
        p = _playbook(approval_status=PlaybookApprovalStatus.UNDER_REVIEW)
        p = transition_playbook(p, to_status=PlaybookApprovalStatus.APPROVED)
        with pytest.raises(ValueError, match="invalid playbook transition"):
            transition_playbook(p, to_status=PlaybookApprovalStatus.UNDER_REVIEW)

    def test_is_valid_transition_check(self) -> None:
        assert is_valid_playbook_transition(
            PlaybookApprovalStatus.PROPOSED, PlaybookApprovalStatus.UNDER_REVIEW
        )
        assert not is_valid_playbook_transition(
            PlaybookApprovalStatus.REJECTED, PlaybookApprovalStatus.PROPOSED
        )


# ---------------------------------------------------------------------------
# Immutability
# ---------------------------------------------------------------------------


class TestImmutability:
    def test_original_unchanged_after_transition(self) -> None:
        p = _playbook(approval_status=PlaybookApprovalStatus.PROPOSED)
        result = transition_playbook(p, to_status=PlaybookApprovalStatus.UNDER_REVIEW)
        assert p.approval_status == PlaybookApprovalStatus.PROPOSED
        assert result.approval_status == PlaybookApprovalStatus.UNDER_REVIEW
        assert p.playbook_version_id == result.playbook_version_id
