"""Tests for Approval state machine transitions.

Covers:
  - Pending → granted / rejected / timed_out / withdrawn
  - Timed-out → pending recovery
  - Granted/rejected/withdrawn as terminal
  - decision_at auto-set on grant/reject/withdraw
  - Invalid transition rejection
  - Frozen immutability of original after transition
"""
from __future__ import annotations

from datetime import UTC, datetime

import pytest

from dealix.company_intelligence import (
    CanonicalApproval,
    CanonicalApprovalStatus,
    is_valid_approval_transition,
    transition_approval,
    valid_approval_transitions_from,
)


def _approval(**overrides: object) -> CanonicalApproval:
    defaults: dict[str, object] = dict(
        tenant_id="tenant-a",
        approval_id="appr-1",
        action_id="action-1",
        object_type="draft",
        object_id="draft-1",
        action_type="send_email",
        proof_target="approved outcome",
    )
    defaults.update(overrides)
    return CanonicalApproval(**defaults)


# ---------------------------------------------------------------------------
# Valid transitions
# ---------------------------------------------------------------------------


class TestValidTransitions:
    def test_pending_to_granted(self) -> None:
        a = _approval(status=CanonicalApprovalStatus.PENDING)
        result = transition_approval(a, to_status=CanonicalApprovalStatus.GRANTED)
        assert result.status == CanonicalApprovalStatus.GRANTED
        assert result.decision_at is not None

    def test_pending_to_rejected(self) -> None:
        a = _approval(status=CanonicalApprovalStatus.PENDING)
        result = transition_approval(a, to_status=CanonicalApprovalStatus.REJECTED)
        assert result.status == CanonicalApprovalStatus.REJECTED
        assert result.decision_at is not None

    def test_pending_to_timed_out(self) -> None:
        a = _approval(status=CanonicalApprovalStatus.PENDING)
        result = transition_approval(a, to_status=CanonicalApprovalStatus.TIMED_OUT)
        assert result.status == CanonicalApprovalStatus.TIMED_OUT

    def test_pending_to_withdrawn(self) -> None:
        a = _approval(status=CanonicalApprovalStatus.PENDING)
        result = transition_approval(a, to_status=CanonicalApprovalStatus.WITHDRAWN)
        assert result.status == CanonicalApprovalStatus.WITHDRAWN
        assert result.decision_at is not None

    def test_timed_out_to_pending(self) -> None:
        a = _approval(status=CanonicalApprovalStatus.TIMED_OUT)
        result = transition_approval(a, to_status=CanonicalApprovalStatus.PENDING)
        assert result.status == CanonicalApprovalStatus.PENDING


# ---------------------------------------------------------------------------
# Full lifecycle
# ---------------------------------------------------------------------------


class TestFullLifecycle:
    def test_pending_timeout_rerequest_grant(self) -> None:
        """Pending → timed_out → pending → granted."""
        a = _approval(status=CanonicalApprovalStatus.PENDING)
        a = transition_approval(a, to_status=CanonicalApprovalStatus.TIMED_OUT)
        a = transition_approval(a, to_status=CanonicalApprovalStatus.PENDING)
        a = transition_approval(a, to_status=CanonicalApprovalStatus.GRANTED)
        assert a.status == CanonicalApprovalStatus.GRANTED
        assert a.decision_at is not None


# ---------------------------------------------------------------------------
# decision_at behavior
# ---------------------------------------------------------------------------


class TestDecisionAt:
    def test_decision_at_auto_set_on_grant(self) -> None:
        a = _approval(status=CanonicalApprovalStatus.PENDING)
        result = transition_approval(a, to_status=CanonicalApprovalStatus.GRANTED)
        assert result.decision_at is not None

    def test_decision_at_custom_value(self) -> None:
        ts = datetime(2026, 8, 1, tzinfo=UTC)
        a = _approval(status=CanonicalApprovalStatus.PENDING)
        result = transition_approval(
            a, to_status=CanonicalApprovalStatus.GRANTED, decision_at=ts
        )
        assert result.decision_at == ts

    def test_decision_at_set_on_rejection(self) -> None:
        a = _approval(status=CanonicalApprovalStatus.PENDING)
        result = transition_approval(a, to_status=CanonicalApprovalStatus.REJECTED)
        assert result.decision_at is not None

    def test_decision_at_set_on_withdrawal(self) -> None:
        a = _approval(status=CanonicalApprovalStatus.PENDING)
        result = transition_approval(a, to_status=CanonicalApprovalStatus.WITHDRAWN)
        assert result.decision_at is not None


# ---------------------------------------------------------------------------
# Terminal states
# ---------------------------------------------------------------------------


class TestTerminalStates:
    @pytest.mark.parametrize("status", [
        CanonicalApprovalStatus.GRANTED,
        CanonicalApprovalStatus.REJECTED,
        CanonicalApprovalStatus.WITHDRAWN,
    ])
    def test_terminal_has_no_transitions(
        self, status: CanonicalApprovalStatus
    ) -> None:
        assert valid_approval_transitions_from(status) == frozenset()

    def test_granted_transition_rejected(self) -> None:
        a = _approval(status=CanonicalApprovalStatus.PENDING)
        a = transition_approval(a, to_status=CanonicalApprovalStatus.GRANTED)
        with pytest.raises(ValueError, match="invalid approval transition"):
            transition_approval(a, to_status=CanonicalApprovalStatus.PENDING)

    def test_rejected_transition_rejected(self) -> None:
        a = _approval(status=CanonicalApprovalStatus.REJECTED)
        with pytest.raises(ValueError, match="invalid approval transition"):
            transition_approval(a, to_status=CanonicalApprovalStatus.PENDING)

    def test_withdrawn_transition_rejected(self) -> None:
        a = _approval(status=CanonicalApprovalStatus.WITHDRAWN)
        with pytest.raises(ValueError, match="invalid approval transition"):
            transition_approval(a, to_status=CanonicalApprovalStatus.GRANTED)


# ---------------------------------------------------------------------------
# Invalid transitions
# ---------------------------------------------------------------------------


class TestInvalidTransitions:
    def test_timed_out_cannot_skip_to_granted(self) -> None:
        a = _approval(status=CanonicalApprovalStatus.TIMED_OUT)
        with pytest.raises(ValueError, match="invalid approval transition"):
            transition_approval(a, to_status=CanonicalApprovalStatus.GRANTED)

    def test_is_valid_transition_check(self) -> None:
        assert is_valid_approval_transition(
            CanonicalApprovalStatus.PENDING, CanonicalApprovalStatus.GRANTED
        )
        assert not is_valid_approval_transition(
            CanonicalApprovalStatus.GRANTED, CanonicalApprovalStatus.PENDING
        )


# ---------------------------------------------------------------------------
# Immutability
# ---------------------------------------------------------------------------


class TestImmutability:
    def test_original_unchanged_after_transition(self) -> None:
        a = _approval(status=CanonicalApprovalStatus.PENDING)
        result = transition_approval(a, to_status=CanonicalApprovalStatus.GRANTED)
        assert a.status == CanonicalApprovalStatus.PENDING
        assert result.status == CanonicalApprovalStatus.GRANTED
        assert a.approval_id == result.approval_id


# ---------------------------------------------------------------------------
# Safety invariant — execution requires granted
# ---------------------------------------------------------------------------


class TestExecutionSafety:
    def test_execution_requires_granted_status(self) -> None:
        with pytest.raises(ValueError, match="execution requires granted"):
            CanonicalApproval(
                tenant_id="tenant-a",
                approval_id="appr-1",
                action_id="action-1",
                object_type="draft",
                object_id="draft-1",
                action_type="send_email",
                proof_target="outcome",
                status=CanonicalApprovalStatus.PENDING,
                execution_allowed=True,
            )

    def test_execution_allowed_when_granted(self) -> None:
        a = CanonicalApproval(
            tenant_id="tenant-a",
            approval_id="appr-1",
            action_id="action-1",
            object_type="draft",
            object_id="draft-1",
            action_type="send_email",
            proof_target="outcome",
            status=CanonicalApprovalStatus.GRANTED,
            execution_allowed=True,
            decision_at=datetime.now(UTC),
        )
        assert a.execution_allowed is True
        assert a.status == CanonicalApprovalStatus.GRANTED
