"""Tests for Proposal state machine transitions.

Covers:
  - All valid forward transitions
  - Terminal state enforcement
  - Invalid transition rejection
  - Transition with sent_at propagation
  - Frozen immutability of original after transition
"""
from __future__ import annotations

from datetime import UTC, datetime

import pytest

from dealix.company_intelligence.proposal_contracts import (
    ProposalStatus,
    build_proposal,
    is_valid_proposal_transition,
    transition_proposal,
    valid_proposal_transitions_from,
)


def _proposal(**overrides: object):
    defaults = dict(
        tenant_id="tenant-a",
        opportunity_id="opp-1",
        offer_id="offer-free-diagnostic",
        approval_id="approval-1",
        source_id="source-1",
    )
    defaults.update(overrides)
    return build_proposal(**defaults)


# ---------------------------------------------------------------------------
# Valid transitions
# ---------------------------------------------------------------------------


class TestValidTransitions:
    def test_draft_to_pending_review(self) -> None:
        p = _proposal(status=ProposalStatus.DRAFT)
        t = transition_proposal(p, to_status=ProposalStatus.PENDING_REVIEW)
        assert t.status == ProposalStatus.PENDING_REVIEW

    def test_draft_to_withdrawn(self) -> None:
        p = _proposal(status=ProposalStatus.DRAFT)
        t = transition_proposal(p, to_status=ProposalStatus.WITHDRAWN)
        assert t.status == ProposalStatus.WITHDRAWN

    def test_pending_review_to_approved(self) -> None:
        p = _proposal(status=ProposalStatus.PENDING_REVIEW)
        t = transition_proposal(p, to_status=ProposalStatus.APPROVED)
        assert t.status == ProposalStatus.APPROVED

    def test_pending_review_to_rejected(self) -> None:
        p = _proposal(status=ProposalStatus.PENDING_REVIEW)
        t = transition_proposal(p, to_status=ProposalStatus.REJECTED)
        assert t.status == ProposalStatus.REJECTED

    def test_approved_to_sent_with_timestamp(self) -> None:
        p = _proposal(status=ProposalStatus.APPROVED)
        now = datetime.now(UTC)
        t = transition_proposal(p, to_status=ProposalStatus.SENT, sent_at=now)
        assert t.status == ProposalStatus.SENT
        assert t.sent_at == now

    def test_approved_to_expired(self) -> None:
        p = _proposal(status=ProposalStatus.APPROVED)
        t = transition_proposal(p, to_status=ProposalStatus.EXPIRED)
        assert t.status == ProposalStatus.EXPIRED

    def test_sent_to_accepted(self) -> None:
        now = datetime.now(UTC)
        p = _proposal(status=ProposalStatus.SENT, sent_at=now)
        t = transition_proposal(p, to_status=ProposalStatus.ACCEPTED)
        assert t.status == ProposalStatus.ACCEPTED

    def test_sent_to_rejected(self) -> None:
        now = datetime.now(UTC)
        p = _proposal(status=ProposalStatus.SENT, sent_at=now)
        t = transition_proposal(p, to_status=ProposalStatus.REJECTED)
        assert t.status == ProposalStatus.REJECTED

    def test_sent_to_expired(self) -> None:
        now = datetime.now(UTC)
        p = _proposal(status=ProposalStatus.SENT, sent_at=now)
        t = transition_proposal(p, to_status=ProposalStatus.EXPIRED)
        assert t.status == ProposalStatus.EXPIRED


# ---------------------------------------------------------------------------
# Terminal states
# ---------------------------------------------------------------------------


class TestTerminalStates:
    @pytest.mark.parametrize("status", [
        ProposalStatus.ACCEPTED,
        ProposalStatus.REJECTED,
        ProposalStatus.EXPIRED,
        ProposalStatus.WITHDRAWN,
    ])
    def test_terminal_states_have_no_transitions(self, status: ProposalStatus) -> None:
        assert valid_proposal_transitions_from(status) == frozenset()

    @pytest.mark.parametrize("status", [
        ProposalStatus.ACCEPTED,
        ProposalStatus.REJECTED,
        ProposalStatus.EXPIRED,
        ProposalStatus.WITHDRAWN,
    ])
    def test_terminal_transition_rejected(self, status: ProposalStatus) -> None:
        with pytest.raises(ValueError, match="invalid proposal transition"):
            # Use a workaround: build with appropriate state
            if status == ProposalStatus.ACCEPTED:
                now = datetime.now(UTC)
                p = _proposal(status=ProposalStatus.SENT, sent_at=now)
                p = transition_proposal(p, to_status=ProposalStatus.ACCEPTED)
            else:
                p = _proposal(status=status)
            transition_proposal(p, to_status=ProposalStatus.DRAFT)


# ---------------------------------------------------------------------------
# Invalid transitions
# ---------------------------------------------------------------------------


class TestInvalidTransitions:
    def test_draft_cannot_jump_to_sent(self) -> None:
        p = _proposal(status=ProposalStatus.DRAFT)
        with pytest.raises(ValueError, match="invalid proposal transition"):
            transition_proposal(p, to_status=ProposalStatus.SENT)

    def test_draft_cannot_jump_to_accepted(self) -> None:
        p = _proposal(status=ProposalStatus.DRAFT)
        with pytest.raises(ValueError, match="invalid proposal transition"):
            transition_proposal(p, to_status=ProposalStatus.ACCEPTED)

    def test_pending_cannot_jump_to_sent(self) -> None:
        p = _proposal(status=ProposalStatus.PENDING_REVIEW)
        with pytest.raises(ValueError, match="invalid proposal transition"):
            transition_proposal(p, to_status=ProposalStatus.SENT)

    def test_is_valid_transition_check(self) -> None:
        assert is_valid_proposal_transition(
            ProposalStatus.DRAFT, ProposalStatus.PENDING_REVIEW
        )
        assert not is_valid_proposal_transition(
            ProposalStatus.DRAFT, ProposalStatus.SENT
        )


# ---------------------------------------------------------------------------
# Immutability
# ---------------------------------------------------------------------------


class TestImmutability:
    def test_original_unchanged_after_transition(self) -> None:
        p = _proposal(status=ProposalStatus.DRAFT)
        t = transition_proposal(p, to_status=ProposalStatus.PENDING_REVIEW)
        assert p.status == ProposalStatus.DRAFT
        assert t.status == ProposalStatus.PENDING_REVIEW
        assert p.proposal_id == t.proposal_id
