"""Tests for the canonical DepartmentPlan contracts.

Covers:
  - Deterministic ID generation and idempotency
  - Confidence and progress bounds
  - Plan invariants (actions and KPIs required)
  - Time window validation
  - Fail-closed on invalid inputs
  - Builder convenience
  - Entity ownership registry alignment
  - Frozen immutability
"""
from __future__ import annotations

from datetime import UTC, datetime, timedelta

import pytest

from dealix.company_intelligence.department_contracts import (
    CanonicalDepartmentPlan,
    Department,
    PlanPriority,
    PlanStatus,
    build_department_plan,
)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


def _plan(**overrides: object) -> CanonicalDepartmentPlan:
    """Build a minimal valid department plan, overriding any fields."""
    defaults: dict[str, object] = dict(
        tenant_id="tenant-a",
        deduplication_key="plan-q3-sales",
        department=Department.SALES,
        goal="Close 5 pilot customers in Q3",
        source_id="source-1",
        action_ids=("action-1",),
        kpis=("pilots_closed",),
    )
    defaults.update(overrides)
    return build_department_plan(**defaults)


# ---------------------------------------------------------------------------
# Deterministic identity
# ---------------------------------------------------------------------------


class TestDeterministicIdentity:
    def test_same_inputs_produce_same_id(self) -> None:
        a = _plan()
        b = _plan()
        assert a.plan_id == b.plan_id

    def test_different_deduplication_key_produces_different_id(self) -> None:
        a = _plan(deduplication_key="plan-q3-sales")
        b = _plan(deduplication_key="plan-q4-sales")
        assert a.plan_id != b.plan_id

    def test_different_department_produces_different_id(self) -> None:
        a = _plan(department=Department.SALES)
        b = _plan(department=Department.MARKETING)
        assert a.plan_id != b.plan_id

    def test_different_tenant_produces_different_id(self) -> None:
        a = _plan(tenant_id="tenant-a")
        b = _plan(tenant_id="tenant-b")
        assert a.plan_id != b.plan_id

    def test_plan_id_format(self) -> None:
        a = _plan()
        assert a.plan_id.startswith("plan_")
        assert len(a.plan_id) == 5 + 16  # "plan_" + 16 hex chars

    def test_whitespace_in_deduplication_key_is_stripped(self) -> None:
        a = _plan(deduplication_key="  plan-q3-sales  ")
        b = _plan(deduplication_key="plan-q3-sales")
        assert a.plan_id == b.plan_id

    def test_goal_does_not_affect_id(self) -> None:
        """Goal is mutable metadata — it must not affect the stable ID."""
        a = _plan(goal="Close 5 pilot customers")
        b = _plan(goal="Close 10 enterprise deals")
        assert a.plan_id == b.plan_id


# ---------------------------------------------------------------------------
# Score bounds
# ---------------------------------------------------------------------------


class TestScoreBounds:
    def test_default_confidence(self) -> None:
        a = _plan()
        assert a.confidence == 0.5

    def test_confidence_above_one_rejected(self) -> None:
        with pytest.raises(ValueError):
            _plan(confidence=1.5)

    def test_confidence_below_zero_rejected(self) -> None:
        with pytest.raises(ValueError):
            _plan(confidence=-0.1)

    def test_progress_bounds(self) -> None:
        a = _plan(progress_pct=0.0)
        assert a.progress_pct == 0.0
        b = _plan(progress_pct=100.0)
        assert b.progress_pct == 100.0
        with pytest.raises(ValueError):
            _plan(progress_pct=101.0)
        with pytest.raises(ValueError):
            _plan(progress_pct=-1.0)


# ---------------------------------------------------------------------------
# Plan invariants
# ---------------------------------------------------------------------------


class TestPlanInvariants:
    def test_empty_actions_rejected(self) -> None:
        with pytest.raises(ValueError, match="action reference"):
            _plan(action_ids=())

    def test_empty_kpis_rejected(self) -> None:
        with pytest.raises(ValueError, match="KPI"):
            _plan(kpis=())

    def test_single_action_and_kpi_accepted(self) -> None:
        a = _plan(action_ids=("action-1",), kpis=("kpi-1",))
        assert len(a.action_ids) == 1
        assert len(a.kpis) == 1

    def test_multiple_actions_and_kpis(self) -> None:
        a = _plan(
            action_ids=("action-1", "action-2", "action-3"),
            kpis=("kpi-1", "kpi-2"),
        )
        assert len(a.action_ids) == 3
        assert len(a.kpis) == 2


# ---------------------------------------------------------------------------
# Time window validation
# ---------------------------------------------------------------------------


class TestTimeWindow:
    def test_no_time_window_accepted(self) -> None:
        a = _plan(starts_at=None, ends_at=None)
        assert a.starts_at is None
        assert a.ends_at is None

    def test_valid_time_window(self) -> None:
        now = datetime.now(UTC)
        a = _plan(
            starts_at=now,
            ends_at=now + timedelta(days=90),
        )
        assert a.starts_at is not None
        assert a.ends_at is not None

    def test_ends_before_starts_rejected(self) -> None:
        now = datetime.now(UTC)
        with pytest.raises(ValueError, match="ends_at must be after"):
            _plan(
                starts_at=now,
                ends_at=now - timedelta(days=1),
            )

    def test_ends_equal_starts_rejected(self) -> None:
        now = datetime.now(UTC)
        with pytest.raises(ValueError, match="ends_at must be after"):
            _plan(starts_at=now, ends_at=now)


# ---------------------------------------------------------------------------
# Departments coverage
# ---------------------------------------------------------------------------


class TestDepartments:
    def test_all_departments_are_valid(self) -> None:
        for dept in Department:
            a = _plan(department=dept)
            assert a.department == dept

    def test_twelve_departments_exist(self) -> None:
        assert len(Department) == 12


# ---------------------------------------------------------------------------
# Extra field protection
# ---------------------------------------------------------------------------


class TestExtraFieldProtection:
    def test_extra_fields_forbidden(self) -> None:
        a = _plan()
        data = a.model_dump()
        data["rogue_field"] = "injected"
        with pytest.raises(ValueError):
            CanonicalDepartmentPlan(**data)


# ---------------------------------------------------------------------------
# Builder defaults
# ---------------------------------------------------------------------------


class TestBuilderDefaults:
    def test_default_status_is_draft(self) -> None:
        a = _plan()
        assert a.status == PlanStatus.DRAFT

    def test_default_priority_is_medium(self) -> None:
        a = _plan()
        assert a.priority == PlanPriority.MEDIUM

    def test_default_progress_is_zero(self) -> None:
        a = _plan()
        assert a.progress_pct == 0.0

    def test_builder_with_full_context(self) -> None:
        now = datetime.now(UTC)
        a = build_department_plan(
            tenant_id="tenant-a",
            deduplication_key="plan-q3-full",
            department=Department.SALES,
            goal="Close 5 pilot customers in Q3",
            source_id="source-1",
            action_ids=("action-1", "action-2"),
            kpis=("pilots_closed", "pipeline_value"),
            description="Q3 sales execution plan",
            priority=PlanPriority.HIGH,
            confidence=0.8,
            progress_pct=25.0,
            status=PlanStatus.ACTIVE,
            starts_at=now,
            ends_at=now + timedelta(days=90),
            last_reviewed_at=now,
        )
        assert a.department == Department.SALES
        assert a.priority == PlanPriority.HIGH
        assert a.status == PlanStatus.ACTIVE
        assert a.progress_pct == 25.0
        assert len(a.action_ids) == 2
        assert len(a.kpis) == 2


# ---------------------------------------------------------------------------
# Frozen immutability
# ---------------------------------------------------------------------------


class TestFrozenImmutability:
    def test_plan_is_frozen(self) -> None:
        a = _plan()
        with pytest.raises(Exception):
            a.status = PlanStatus.ACTIVE  # type: ignore[misc]


# ---------------------------------------------------------------------------
# Entity ownership registry alignment
# ---------------------------------------------------------------------------


class TestEntityOwnershipAlignment:
    """Verify the contract satisfies the required fields from
    company_intelligence_entity_ownership.json for DepartmentPlan."""

    def test_required_fields_present(self) -> None:
        a = _plan()
        # Required: tenant_id, department, goal, actions, kpis
        assert hasattr(a, "tenant_id") and a.tenant_id
        assert hasattr(a, "department") and a.department
        assert hasattr(a, "goal") and a.goal
        assert hasattr(a, "action_ids") and len(a.action_ids) > 0
        assert hasattr(a, "kpis") and len(a.kpis) > 0

    def test_empty_tenant_rejected(self) -> None:
        with pytest.raises(ValueError):
            build_department_plan(
                tenant_id="",
                deduplication_key="plan-1",
                department=Department.SALES,
                goal="Test goal",
                source_id="source-1",
            )

    def test_empty_goal_rejected(self) -> None:
        with pytest.raises(ValueError):
            build_department_plan(
                tenant_id="tenant-a",
                deduplication_key="plan-1",
                department=Department.SALES,
                goal="",
                source_id="source-1",
            )

    def test_empty_deduplication_key_rejected(self) -> None:
        with pytest.raises(ValueError):
            build_department_plan(
                tenant_id="tenant-a",
                deduplication_key="",
                department=Department.SALES,
                goal="Test goal",
                source_id="source-1",
            )

    def test_empty_source_id_rejected(self) -> None:
        with pytest.raises(ValueError):
            build_department_plan(
                tenant_id="tenant-a",
                deduplication_key="plan-1",
                department=Department.SALES,
                goal="Test goal",
                source_id="",
            )
