"""Tests for DepartmentPlan state machine transitions.

Covers:
  - Draft → active activation
  - Active → under_review / paused / completed lifecycle
  - Recovery: paused/under_review → active
  - Archived as terminal
  - Completed → archived one-way
  - Invalid transition rejection
  - Frozen immutability of original after transition
"""
from __future__ import annotations

import pytest

from dealix.company_intelligence.department_contracts import (
    Department,
    PlanStatus,
    build_department_plan,
    is_valid_plan_transition,
    transition_plan,
    valid_plan_transitions_from,
)


def _plan(**overrides: object):
    defaults = dict(
        tenant_id="tenant-a",
        deduplication_key="key-1",
        department=Department.SALES,
        goal="Increase pipeline coverage",
        source_id="source-1",
        action_ids=("action-1",),
        kpis=("pipeline-coverage-ratio",),
    )
    defaults.update(overrides)
    return build_department_plan(**defaults)


# ---------------------------------------------------------------------------
# Valid transitions
# ---------------------------------------------------------------------------


class TestValidTransitions:
    def test_draft_to_active(self) -> None:
        p = _plan(status=PlanStatus.DRAFT)
        t = transition_plan(p, to_status=PlanStatus.ACTIVE)
        assert t.status == PlanStatus.ACTIVE

    def test_draft_to_archived(self) -> None:
        p = _plan(status=PlanStatus.DRAFT)
        t = transition_plan(p, to_status=PlanStatus.ARCHIVED)
        assert t.status == PlanStatus.ARCHIVED

    def test_active_to_under_review(self) -> None:
        p = _plan(status=PlanStatus.ACTIVE)
        t = transition_plan(p, to_status=PlanStatus.UNDER_REVIEW)
        assert t.status == PlanStatus.UNDER_REVIEW

    def test_active_to_paused(self) -> None:
        p = _plan(status=PlanStatus.ACTIVE)
        t = transition_plan(p, to_status=PlanStatus.PAUSED)
        assert t.status == PlanStatus.PAUSED

    def test_active_to_completed(self) -> None:
        p = _plan(status=PlanStatus.ACTIVE)
        t = transition_plan(p, to_status=PlanStatus.COMPLETED)
        assert t.status == PlanStatus.COMPLETED

    def test_under_review_to_active(self) -> None:
        p = _plan(status=PlanStatus.UNDER_REVIEW)
        t = transition_plan(p, to_status=PlanStatus.ACTIVE)
        assert t.status == PlanStatus.ACTIVE

    def test_paused_to_active(self) -> None:
        p = _plan(status=PlanStatus.PAUSED)
        t = transition_plan(p, to_status=PlanStatus.ACTIVE)
        assert t.status == PlanStatus.ACTIVE

    def test_completed_to_archived(self) -> None:
        p = _plan(status=PlanStatus.COMPLETED)
        t = transition_plan(p, to_status=PlanStatus.ARCHIVED)
        assert t.status == PlanStatus.ARCHIVED


# ---------------------------------------------------------------------------
# Full lifecycle
# ---------------------------------------------------------------------------


class TestFullLifecycle:
    def test_full_plan_lifecycle(self) -> None:
        """Draft → active → under_review → active → completed → archived."""
        p = _plan(status=PlanStatus.DRAFT)
        p = transition_plan(p, to_status=PlanStatus.ACTIVE)
        p = transition_plan(p, to_status=PlanStatus.UNDER_REVIEW)
        p = transition_plan(p, to_status=PlanStatus.ACTIVE)
        p = transition_plan(p, to_status=PlanStatus.COMPLETED)
        p = transition_plan(p, to_status=PlanStatus.ARCHIVED)
        assert p.status == PlanStatus.ARCHIVED

    def test_pause_resume_cycle(self) -> None:
        p = _plan(status=PlanStatus.ACTIVE)
        p = transition_plan(p, to_status=PlanStatus.PAUSED)
        p = transition_plan(p, to_status=PlanStatus.ACTIVE)
        assert p.status == PlanStatus.ACTIVE


# ---------------------------------------------------------------------------
# Terminal state
# ---------------------------------------------------------------------------


class TestTerminalState:
    def test_archived_is_terminal(self) -> None:
        assert valid_plan_transitions_from(PlanStatus.ARCHIVED) == frozenset()

    def test_archived_transition_rejected(self) -> None:
        p = _plan(status=PlanStatus.ARCHIVED)
        with pytest.raises(ValueError, match="invalid plan transition"):
            transition_plan(p, to_status=PlanStatus.DRAFT)


# ---------------------------------------------------------------------------
# Invalid transitions
# ---------------------------------------------------------------------------


class TestInvalidTransitions:
    def test_draft_cannot_jump_to_completed(self) -> None:
        p = _plan(status=PlanStatus.DRAFT)
        with pytest.raises(ValueError, match="invalid plan transition"):
            transition_plan(p, to_status=PlanStatus.COMPLETED)

    def test_completed_cannot_reactivate(self) -> None:
        p = _plan(status=PlanStatus.COMPLETED)
        with pytest.raises(ValueError, match="invalid plan transition"):
            transition_plan(p, to_status=PlanStatus.ACTIVE)

    def test_paused_cannot_jump_to_completed(self) -> None:
        p = _plan(status=PlanStatus.PAUSED)
        with pytest.raises(ValueError, match="invalid plan transition"):
            transition_plan(p, to_status=PlanStatus.COMPLETED)

    def test_is_valid_transition_check(self) -> None:
        assert is_valid_plan_transition(
            PlanStatus.DRAFT, PlanStatus.ACTIVE
        )
        assert not is_valid_plan_transition(
            PlanStatus.DRAFT, PlanStatus.COMPLETED
        )


# ---------------------------------------------------------------------------
# Immutability
# ---------------------------------------------------------------------------


class TestImmutability:
    def test_original_unchanged_after_transition(self) -> None:
        p = _plan(status=PlanStatus.DRAFT)
        t = transition_plan(p, to_status=PlanStatus.ACTIVE)
        assert p.status == PlanStatus.DRAFT
        assert t.status == PlanStatus.ACTIVE
        assert p.plan_id == t.plan_id
