"""Tests for the Company Operator.

Covers task routing, department snapshots, operating snapshots,
action prioritization, and safety invariants.
"""
from __future__ import annotations

import pytest

from dealix.company_intelligence.action_contracts import (
    ActionType,
    AutonomyLevel,
    RiskLevel,
    build_action,
)
from dealix.company_intelligence.company_operator import (
    CompanyOperatingSnapshot,
    DepartmentSnapshot,
    OperatingHealth,
    TaskRouteResult,
    TaskRoutingDecision,
    build_department_snapshot,
    generate_operating_snapshot,
    get_capable_departments,
    prioritize_actions,
    route_task,
)
from dealix.company_intelligence.department_contracts import Department

TENANT = "tenant_test_operator"
SOURCE = "test_source"


def _make_action(**overrides):
    defaults = {
        "tenant_id": TENANT,
        "idempotency_key": "op_action_001",
        "action_type": ActionType.INTERNAL_UPDATE,
        "department": "operations",
        "autonomy_level": AutonomyLevel.L2_DRAFT,
        "risk_level": RiskLevel.LOW,
    }
    defaults.update(overrides)
    return build_action(**defaults)


# -----------------------------------------------------------------------
# Department capability mapping
# -----------------------------------------------------------------------


class TestDepartmentCapabilities:
    def test_research_maps_to_data_first(self):
        departments = get_capable_departments(ActionType.RESEARCH)
        assert Department.DATA in departments

    def test_send_external_maps_to_sales(self):
        departments = get_capable_departments(ActionType.SEND_EXTERNAL)
        assert Department.SALES in departments

    def test_invoice_maps_to_finance(self):
        departments = get_capable_departments(ActionType.INVOICE_REQUEST)
        assert Department.FINANCE in departments

    def test_delivery_maps_to_operations(self):
        departments = get_capable_departments(ActionType.DELIVERY_TASK)
        assert Department.OPERATIONS in departments

    def test_learning_maps_to_data(self):
        departments = get_capable_departments(ActionType.LEARNING_PROPOSAL)
        assert Department.DATA in departments


# -----------------------------------------------------------------------
# Task routing
# -----------------------------------------------------------------------


class TestTaskRouting:
    def test_route_internal_action(self):
        action = _make_action()
        routing = route_task(action, source_id=SOURCE)
        assert isinstance(routing, TaskRoutingDecision)
        assert routing.tenant_id == TENANT
        assert routing.action_id == action.action_id
        assert routing.result == TaskRouteResult.ROUTED

    def test_deterministic_routing_id(self):
        action = _make_action()
        r1 = route_task(action, source_id=SOURCE)
        r2 = route_task(action, source_id=SOURCE)
        assert r1.routing_id == r2.routing_id
        assert r1.routing_id.startswith("route_")

    def test_external_action_queued(self):
        action = _make_action(
            idempotency_key="ext_route_001",
            action_type=ActionType.SEND_EXTERNAL,
            autonomy_level=AutonomyLevel.L4_CONTROLLED_EXECUTE,
            external_effect=True,
        )
        routing = route_task(action, source_id=SOURCE)
        assert routing.result == TaskRouteResult.QUEUED
        assert "pending human approval" in routing.reasoning

    def test_high_risk_escalated(self):
        action = _make_action(
            idempotency_key="risk_route_001",
            risk_level=RiskLevel.HIGH,
        )
        routing = route_task(action, source_id=SOURCE)
        assert routing.result == TaskRouteResult.ESCALATED

    def test_routes_to_highest_capacity_department(self):
        action = _make_action(
            idempotency_key="cap_route_001",
            action_type=ActionType.RESEARCH,
        )
        capacities = {
            Department.DATA: 20.0,
            Department.MARKETING: 80.0,
            Department.SALES: 50.0,
        }
        routing = route_task(
            action, source_id=SOURCE,
            department_capacities=capacities,
        )
        assert routing.target_department == Department.MARKETING

    def test_blocked_when_zero_capacity(self):
        action = _make_action(
            idempotency_key="blocked_route",
            action_type=ActionType.INVOICE_REQUEST,
        )
        capacities = {Department.FINANCE: 0.0}
        routing = route_task(
            action, source_id=SOURCE,
            department_capacities=capacities,
        )
        assert routing.result == TaskRouteResult.BLOCKED

    def test_alternative_departments_populated(self):
        action = _make_action(
            idempotency_key="alt_route",
            action_type=ActionType.RESEARCH,
        )
        routing = route_task(action, source_id=SOURCE)
        assert len(routing.alternative_departments) >= 1


# -----------------------------------------------------------------------
# Department snapshots
# -----------------------------------------------------------------------


class TestDepartmentSnapshot:
    def test_empty_department_good_health(self):
        snapshot = build_department_snapshot(Department.SALES)
        assert snapshot.department == Department.SALES
        assert snapshot.health == OperatingHealth.GOOD
        assert snapshot.active_actions == 0
        assert snapshot.capacity_pct == 100.0

    def test_snapshot_with_actions(self):
        actions = [
            _make_action(
                idempotency_key=f"snap_{i}",
                department="sales",
            )
            for i in range(3)
        ]
        snapshot = build_department_snapshot(
            Department.SALES, actions=actions,
        )
        assert snapshot.active_actions == 3  # queued = active
        assert snapshot.capacity_pct == 70.0  # 100 - 3*10

    def test_failed_actions_flag_issues(self):
        from dealix.company_intelligence.action_contracts import (
            ActionStatus,
            transition_action,
        )
        action = _make_action(idempotency_key="fail_snap")
        in_progress = transition_action(
            action, to_status=ActionStatus.IN_PROGRESS,
        )
        failed = transition_action(
            in_progress, to_status=ActionStatus.FAILED,
        )
        snapshot = build_department_snapshot(
            Department.OPERATIONS, actions=[failed],
        )
        assert snapshot.failed_today == 1
        assert snapshot.health == OperatingHealth.CRITICAL

    def test_kpi_scores_captured(self):
        snapshot = build_department_snapshot(
            Department.MARKETING,
            kpi_scores=(
                ("leads_generated", 85.0),
                ("content_published", 92.0),
            ),
        )
        assert len(snapshot.kpi_scores) == 2


# -----------------------------------------------------------------------
# Company operating snapshot
# -----------------------------------------------------------------------


class TestOperatingSnapshot:
    def test_basic_snapshot(self):
        snapshot = generate_operating_snapshot(
            tenant_id=TENANT,
            snapshot_date="2026-08-08",
            source_id=SOURCE,
            department_snapshots=[],
        )
        assert isinstance(snapshot, CompanyOperatingSnapshot)
        assert snapshot.tenant_id == TENANT
        assert snapshot.snapshot_date == "2026-08-08"
        assert snapshot.never_auto_external is True
        assert snapshot.execution_allowed is False

    def test_deterministic_id(self):
        s1 = generate_operating_snapshot(
            tenant_id=TENANT,
            snapshot_date="2026-08-08",
            source_id=SOURCE,
            department_snapshots=[],
        )
        s2 = generate_operating_snapshot(
            tenant_id=TENANT,
            snapshot_date="2026-08-08",
            source_id=SOURCE,
            department_snapshots=[],
        )
        assert s1.snapshot_id == s2.snapshot_id
        assert s1.snapshot_id.startswith("opsnapshot_")

    def test_aggregates_department_metrics(self):
        dept_snapshots = [
            DepartmentSnapshot(
                department=Department.SALES,
                health=OperatingHealth.GOOD,
                active_actions=5,
                pending_approvals=2,
                completed_today=10,
                failed_today=0,
                blocked_actions=0,
            ),
            DepartmentSnapshot(
                department=Department.MARKETING,
                health=OperatingHealth.EXCELLENT,
                active_actions=3,
                pending_approvals=1,
                completed_today=8,
                failed_today=0,
                blocked_actions=0,
            ),
        ]
        snapshot = generate_operating_snapshot(
            tenant_id=TENANT,
            snapshot_date="2026-08-08",
            source_id=SOURCE,
            department_snapshots=dept_snapshots,
        )
        assert snapshot.total_active_actions == 8
        assert snapshot.total_pending_approvals == 3
        assert snapshot.total_completed_today == 18
        assert snapshot.overall_health in (
            OperatingHealth.GOOD, OperatingHealth.EXCELLENT,
        )

    def test_critical_departments_lower_health(self):
        dept_snapshots = [
            DepartmentSnapshot(
                department=Department.FINANCE,
                health=OperatingHealth.CRITICAL,
            ),
            DepartmentSnapshot(
                department=Department.SALES,
                health=OperatingHealth.CRITICAL,
            ),
        ]
        snapshot = generate_operating_snapshot(
            tenant_id=TENANT,
            snapshot_date="2026-08-08",
            source_id=SOURCE,
            department_snapshots=dept_snapshots,
        )
        assert snapshot.overall_health == OperatingHealth.CRITICAL

    def test_revenue_intelligence_captured(self):
        snapshot = generate_operating_snapshot(
            tenant_id=TENANT,
            snapshot_date="2026-08-08",
            source_id=SOURCE,
            department_snapshots=[],
            active_opportunities=15,
            pipeline_value_sar=250000.0,
        )
        assert snapshot.active_opportunities == 15
        assert snapshot.pipeline_value_sar == 250000.0


# -----------------------------------------------------------------------
# Action prioritization
# -----------------------------------------------------------------------


class TestActionPrioritization:
    def test_higher_priority_first(self):
        high = _make_action(
            idempotency_key="high_pri",
            impact=0.9, urgency=0.9, confidence=0.9,
        )
        low = _make_action(
            idempotency_key="low_pri",
            impact=0.1, urgency=0.1, confidence=0.1,
        )
        result = prioritize_actions([low, high])
        assert result[0].action_id == high.action_id

    def test_external_actions_prioritized(self):
        """External actions get attention first (need human approval)."""
        internal = _make_action(
            idempotency_key="internal_pri",
            impact=0.9, urgency=0.9, confidence=0.9,
        )
        external = _make_action(
            idempotency_key="external_pri",
            action_type=ActionType.SEND_EXTERNAL,
            autonomy_level=AutonomyLevel.L4_CONTROLLED_EXECUTE,
            external_effect=True,
            impact=0.5, urgency=0.5, confidence=0.5,
        )
        result = prioritize_actions([internal, external])
        assert result[0].action_id == external.action_id

    def test_empty_list_returns_empty(self):
        assert prioritize_actions([]) == []


# -----------------------------------------------------------------------
# Safety invariants
# -----------------------------------------------------------------------


class TestOperatorSafety:
    def test_snapshot_never_auto_external(self):
        """Cannot create a snapshot that authorizes external actions."""
        with pytest.raises(ValueError, match="cannot authorize external"):
            CompanyOperatingSnapshot(
                tenant_id=TENANT,
                snapshot_id="opsnapshot_fake",
                snapshot_date="2026-08-08",
                never_auto_external=False,
                execution_allowed=False,
                source_id=SOURCE,
            )

    def test_snapshot_never_allows_execution(self):
        """Cannot create a snapshot that authorizes execution."""
        with pytest.raises(ValueError, match="never authorize execution"):
            CompanyOperatingSnapshot(
                tenant_id=TENANT,
                snapshot_id="opsnapshot_fake",
                snapshot_date="2026-08-08",
                never_auto_external=True,
                execution_allowed=True,
                source_id=SOURCE,
            )

    def test_routing_external_requires_approval(self):
        """External actions always have requires_approval in routing."""
        action = _make_action(
            idempotency_key="safety_ext",
            action_type=ActionType.SEND_EXTERNAL,
            autonomy_level=AutonomyLevel.L4_CONTROLLED_EXECUTE,
            external_effect=True,
        )
        routing = route_task(action, source_id=SOURCE)
        assert routing.requires_approval is True
