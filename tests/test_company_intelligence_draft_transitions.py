"""Tests for Draft status state machine transitions.

Covers:
  - Generated → pending_approval → approved → copied/sent → replied → archived
  - Needs_edit → generated round-trip
  - Rejected → archived
  - Archived as terminal
  - Safety invariant: execution_allowed always False across all statuses
  - Invalid transition rejection
  - Frozen immutability of original after transition
"""
from __future__ import annotations

import pytest

from dealix.company_intelligence import (
    DraftChannel,
    DraftStatus,
    LawfulContactBasis,
    build_draft,
    is_valid_draft_transition,
    transition_draft,
    valid_draft_transitions_from,
)


def _draft(**overrides: object):
    defaults = dict(
        tenant_id="tenant-a",
        action_id="action-1",
        opportunity_id="opp-1",
        channel=DraftChannel.EMAIL,
        content="Hello, would you like a free diagnostic?",
        lawful_contact_basis=LawfulContactBasis.EXISTING_RELATIONSHIP,
        source_evidence=["crm-record-123"],
    )
    defaults.update(overrides)
    return build_draft(**defaults)


# ---------------------------------------------------------------------------
# Valid transitions
# ---------------------------------------------------------------------------


class TestValidTransitions:
    def test_generated_to_pending_approval(self) -> None:
        d = _draft()
        assert d.status == DraftStatus.GENERATED
        result = transition_draft(d, to_status=DraftStatus.PENDING_APPROVAL)
        assert result.status == DraftStatus.PENDING_APPROVAL

    def test_generated_to_needs_edit(self) -> None:
        d = _draft()
        result = transition_draft(d, to_status=DraftStatus.NEEDS_EDIT)
        assert result.status == DraftStatus.NEEDS_EDIT

    def test_generated_to_rejected(self) -> None:
        d = _draft()
        result = transition_draft(d, to_status=DraftStatus.REJECTED)
        assert result.status == DraftStatus.REJECTED

    def test_pending_approval_to_approved(self) -> None:
        d = _draft()
        d = transition_draft(d, to_status=DraftStatus.PENDING_APPROVAL)
        result = transition_draft(d, to_status=DraftStatus.APPROVED)
        assert result.status == DraftStatus.APPROVED

    def test_pending_approval_to_rejected(self) -> None:
        d = _draft()
        d = transition_draft(d, to_status=DraftStatus.PENDING_APPROVAL)
        result = transition_draft(d, to_status=DraftStatus.REJECTED)
        assert result.status == DraftStatus.REJECTED

    def test_approved_to_copied_manually(self) -> None:
        d = _draft()
        d = transition_draft(d, to_status=DraftStatus.PENDING_APPROVAL)
        d = transition_draft(d, to_status=DraftStatus.APPROVED)
        result = transition_draft(d, to_status=DraftStatus.COPIED_MANUALLY)
        assert result.status == DraftStatus.COPIED_MANUALLY

    def test_approved_to_sent_via_integration(self) -> None:
        d = _draft()
        d = transition_draft(d, to_status=DraftStatus.PENDING_APPROVAL)
        d = transition_draft(d, to_status=DraftStatus.APPROVED)
        result = transition_draft(d, to_status=DraftStatus.SENT_VIA_INTEGRATION)
        assert result.status == DraftStatus.SENT_VIA_INTEGRATION

    def test_copied_to_replied(self) -> None:
        d = _draft()
        d = transition_draft(d, to_status=DraftStatus.PENDING_APPROVAL)
        d = transition_draft(d, to_status=DraftStatus.APPROVED)
        d = transition_draft(d, to_status=DraftStatus.COPIED_MANUALLY)
        result = transition_draft(d, to_status=DraftStatus.REPLIED)
        assert result.status == DraftStatus.REPLIED

    def test_needs_edit_to_generated(self) -> None:
        d = _draft()
        d = transition_draft(d, to_status=DraftStatus.NEEDS_EDIT)
        result = transition_draft(d, to_status=DraftStatus.GENERATED)
        assert result.status == DraftStatus.GENERATED


# ---------------------------------------------------------------------------
# Full lifecycle
# ---------------------------------------------------------------------------


class TestFullLifecycle:
    def test_happy_path_to_replied(self) -> None:
        """Generated → pending → approved → copied → replied → archived."""
        d = _draft()
        d = transition_draft(d, to_status=DraftStatus.PENDING_APPROVAL)
        d = transition_draft(d, to_status=DraftStatus.APPROVED)
        d = transition_draft(d, to_status=DraftStatus.COPIED_MANUALLY)
        d = transition_draft(d, to_status=DraftStatus.REPLIED)
        d = transition_draft(d, to_status=DraftStatus.ARCHIVED)
        assert d.status == DraftStatus.ARCHIVED

    def test_edit_cycle(self) -> None:
        """Generated → needs_edit → generated → pending → approved."""
        d = _draft()
        d = transition_draft(d, to_status=DraftStatus.NEEDS_EDIT)
        d = transition_draft(d, to_status=DraftStatus.GENERATED)
        d = transition_draft(d, to_status=DraftStatus.PENDING_APPROVAL)
        d = transition_draft(d, to_status=DraftStatus.APPROVED)
        assert d.status == DraftStatus.APPROVED


# ---------------------------------------------------------------------------
# Archived from any non-terminal
# ---------------------------------------------------------------------------


class TestArchivedFromAny:
    @pytest.mark.parametrize("status", [
        DraftStatus.GENERATED,
        DraftStatus.NEEDS_EDIT,
        DraftStatus.APPROVED,
        DraftStatus.REJECTED,
        DraftStatus.COPIED_MANUALLY,
        DraftStatus.SENT_VIA_INTEGRATION,
        DraftStatus.REPLIED,
    ])
    def test_archived_reachable(self, status: DraftStatus) -> None:
        d = _draft()
        # Transition to the parametrized status first (via valid path)
        if status == DraftStatus.GENERATED:
            pass  # already there
        elif status == DraftStatus.NEEDS_EDIT:
            d = transition_draft(d, to_status=DraftStatus.NEEDS_EDIT)
        elif status == DraftStatus.APPROVED:
            d = transition_draft(d, to_status=DraftStatus.PENDING_APPROVAL)
            d = transition_draft(d, to_status=DraftStatus.APPROVED)
        elif status == DraftStatus.REJECTED:
            d = transition_draft(d, to_status=DraftStatus.REJECTED)
        elif status == DraftStatus.COPIED_MANUALLY:
            d = transition_draft(d, to_status=DraftStatus.PENDING_APPROVAL)
            d = transition_draft(d, to_status=DraftStatus.APPROVED)
            d = transition_draft(d, to_status=DraftStatus.COPIED_MANUALLY)
        elif status == DraftStatus.SENT_VIA_INTEGRATION:
            d = transition_draft(d, to_status=DraftStatus.PENDING_APPROVAL)
            d = transition_draft(d, to_status=DraftStatus.APPROVED)
            d = transition_draft(d, to_status=DraftStatus.SENT_VIA_INTEGRATION)
        elif status == DraftStatus.REPLIED:
            d = transition_draft(d, to_status=DraftStatus.PENDING_APPROVAL)
            d = transition_draft(d, to_status=DraftStatus.APPROVED)
            d = transition_draft(d, to_status=DraftStatus.COPIED_MANUALLY)
            d = transition_draft(d, to_status=DraftStatus.REPLIED)

        assert d.status == status
        result = transition_draft(d, to_status=DraftStatus.ARCHIVED)
        assert result.status == DraftStatus.ARCHIVED


# ---------------------------------------------------------------------------
# Terminal state
# ---------------------------------------------------------------------------


class TestTerminalState:
    def test_archived_is_terminal(self) -> None:
        assert valid_draft_transitions_from(DraftStatus.ARCHIVED) == frozenset()

    def test_archived_transition_rejected(self) -> None:
        d = _draft()
        d = transition_draft(d, to_status=DraftStatus.ARCHIVED)
        with pytest.raises(ValueError, match="invalid draft transition"):
            transition_draft(d, to_status=DraftStatus.GENERATED)


# ---------------------------------------------------------------------------
# Invalid transitions
# ---------------------------------------------------------------------------


class TestInvalidTransitions:
    def test_generated_cannot_skip_to_approved(self) -> None:
        d = _draft()
        with pytest.raises(ValueError, match="invalid draft transition"):
            transition_draft(d, to_status=DraftStatus.APPROVED)

    def test_generated_cannot_skip_to_copied(self) -> None:
        d = _draft()
        with pytest.raises(ValueError, match="invalid draft transition"):
            transition_draft(d, to_status=DraftStatus.COPIED_MANUALLY)

    def test_rejected_cannot_go_to_approved(self) -> None:
        d = _draft()
        d = transition_draft(d, to_status=DraftStatus.REJECTED)
        with pytest.raises(ValueError, match="invalid draft transition"):
            transition_draft(d, to_status=DraftStatus.APPROVED)

    def test_is_valid_transition_check(self) -> None:
        assert is_valid_draft_transition(
            DraftStatus.GENERATED, DraftStatus.PENDING_APPROVAL
        )
        assert not is_valid_draft_transition(
            DraftStatus.ARCHIVED, DraftStatus.GENERATED
        )


# ---------------------------------------------------------------------------
# Safety invariant — execution always blocked
# ---------------------------------------------------------------------------


class TestExecutionSafety:
    @pytest.mark.parametrize("to_status", [
        DraftStatus.PENDING_APPROVAL,
        DraftStatus.NEEDS_EDIT,
        DraftStatus.REJECTED,
        DraftStatus.ARCHIVED,
    ])
    def test_execution_blocked_across_transitions(
        self, to_status: DraftStatus
    ) -> None:
        d = _draft()
        result = transition_draft(d, to_status=to_status)
        assert result.execution_allowed is False
        assert result.approval_required is True

    def test_execution_blocked_after_approval(self) -> None:
        d = _draft()
        d = transition_draft(d, to_status=DraftStatus.PENDING_APPROVAL)
        d = transition_draft(d, to_status=DraftStatus.APPROVED)
        assert d.execution_allowed is False
        assert d.approval_required is True


# ---------------------------------------------------------------------------
# Immutability
# ---------------------------------------------------------------------------


class TestImmutability:
    def test_original_unchanged_after_transition(self) -> None:
        d = _draft()
        result = transition_draft(d, to_status=DraftStatus.PENDING_APPROVAL)
        assert d.status == DraftStatus.GENERATED
        assert result.status == DraftStatus.PENDING_APPROVAL
        assert d.draft_id == result.draft_id
