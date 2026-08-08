"""Company Operator — central orchestrator for autonomous company operations.

The CompanyOperator is the coordination layer that ties together all
Company Intelligence engines to operate a company across departments.
It routes tasks, manages department configurations, prioritizes actions,
generates daily operating summaries, and ensures every department works
under the same governance framework.

The Operator does NOT replace humans. It amplifies human capacity by:
    - Handling routine work autonomously (internal, low-risk)
    - Drafting all external communications for approval
    - Prioritizing work across departments
    - Maintaining company-wide context and memory
    - Enforcing consistent communication style
    - Tracking outcomes and learning from them

Safety invariants:
    - External actions ALWAYS require human approval
    - Execution is NEVER allowed without the approval chain
    - No department can bypass the human-loop governance
    - Financial actions always escalate

The operator is persistence-neutral: no database, network, or LLM calls.

Entity ownership:
    Orchestrates across all entity owners.
    Does NOT own any entity directly — delegates to canonical owners.
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

from dealix.company_intelligence.action_contracts import (
    ActionType,
    AutonomyLevel,
    CanonicalAction,
    RiskLevel,
)
from dealix.company_intelligence.department_contracts import Department

NonEmptyString = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------


class OperatingHealth(StrEnum):
    """Overall health status of a department or company."""

    EXCELLENT = "excellent"
    GOOD = "good"
    NEEDS_ATTENTION = "needs_attention"
    AT_RISK = "at_risk"
    CRITICAL = "critical"


class TaskRouteResult(StrEnum):
    """Result of routing a task to a department."""

    ROUTED = "routed"
    QUEUED = "queued"
    ESCALATED = "escalated"
    BLOCKED = "blocked"


# ---------------------------------------------------------------------------
# Department capability map
# ---------------------------------------------------------------------------


# What each department can do — maps action types to departments
_DEPARTMENT_ACTION_MAP: dict[ActionType, tuple[Department, ...]] = {
    ActionType.RESEARCH: (
        Department.DATA, Department.MARKETING, Department.SALES,
    ),
    ActionType.QUALIFY: (
        Department.SALES, Department.PARTNERSHIPS,
    ),
    ActionType.PREPARE_DRAFT: (
        Department.MARKETING, Department.SALES, Department.CUSTOMER_SUCCESS,
    ),
    ActionType.SCHEDULE_MEETING: (
        Department.SALES, Department.CUSTOMER_SUCCESS, Department.PARTNERSHIPS,
    ),
    ActionType.CONDUCT_DISCOVERY: (
        Department.SALES, Department.CUSTOMER_SUCCESS,
    ),
    ActionType.PREPARE_PROPOSAL: (
        Department.SALES, Department.EXECUTIVE,
    ),
    ActionType.SEND_EXTERNAL: (
        Department.SALES, Department.MARKETING, Department.CUSTOMER_SUCCESS,
    ),
    ActionType.RECORD_OUTCOME: (
        Department.OPERATIONS, Department.CUSTOMER_SUCCESS,
    ),
    ActionType.RECORD_PROOF: (
        Department.FINANCE, Department.OPERATIONS,
    ),
    ActionType.DELIVERY_TASK: (
        Department.OPERATIONS, Department.ENGINEERING, Department.PRODUCT,
    ),
    ActionType.APPROVAL_REQUEST: (
        Department.EXECUTIVE, Department.LEGAL,
    ),
    ActionType.INVOICE_REQUEST: (
        Department.FINANCE,
    ),
    ActionType.INTERNAL_UPDATE: (
        Department.OPERATIONS, Department.HR,
    ),
    ActionType.LEARNING_PROPOSAL: (
        Department.DATA, Department.PRODUCT,
    ),
    ActionType.SYSTEM_TASK: (
        Department.ENGINEERING, Department.DATA,
    ),
}


# ---------------------------------------------------------------------------
# Stable IDs
# ---------------------------------------------------------------------------


def _stable_snapshot_id(payload: dict[str, Any]) -> str:
    canonical = json.dumps(
        payload,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
        default=str,
    )
    return f"opsnapshot_{sha256(canonical.encode('utf-8')).hexdigest()[:16]}"


def _stable_routing_id(payload: dict[str, Any]) -> str:
    canonical = json.dumps(
        payload,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
        default=str,
    )
    return f"route_{sha256(canonical.encode('utf-8')).hexdigest()[:16]}"


# ---------------------------------------------------------------------------
# Department Status
# ---------------------------------------------------------------------------


class DepartmentSnapshot(BaseModel):
    """Point-in-time status of a single department.

    Captures active actions, pending approvals, health metrics, and
    capacity for the department. Used by the CompanyOperator to build
    the company-wide operating picture.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    department: Department
    health: OperatingHealth = OperatingHealth.GOOD

    # Action counts
    active_actions: int = Field(default=0, ge=0)
    pending_approvals: int = Field(default=0, ge=0)
    completed_today: int = Field(default=0, ge=0)
    failed_today: int = Field(default=0, ge=0)
    blocked_actions: int = Field(default=0, ge=0)

    # KPI tracking
    kpi_scores: tuple[tuple[str, float], ...] = ()

    # Capacity
    capacity_pct: float = Field(default=100.0, ge=0.0, le=100.0)

    # Active plan (if any)
    active_plan_id: str = ""
    plan_progress_pct: float = Field(default=0.0, ge=0.0, le=100.0)


# ---------------------------------------------------------------------------
# Task Routing Decision
# ---------------------------------------------------------------------------


class TaskRoutingDecision(BaseModel):
    """Decision about which department handles a task and why.

    Routing decisions are logged for audit and learning. They capture
    the reasoning, the target department, and any escalation context.

    Key invariants:
        - routing_id is deterministic.
        - External tasks always have requires_approval=True.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    # Identity
    tenant_id: NonEmptyString
    routing_id: NonEmptyString

    # What was routed
    action_id: NonEmptyString
    action_type: ActionType

    # Routing decision
    target_department: Department
    result: TaskRouteResult
    reasoning: NonEmptyString

    # Escalation context
    requires_approval: bool = True
    risk_level: RiskLevel = RiskLevel.LOW

    # Alternatives considered
    alternative_departments: tuple[Department, ...] = ()

    # Provenance
    source_id: NonEmptyString
    routed_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    @model_validator(mode="after")
    def enforce_routing_invariants(self) -> TaskRoutingDecision:
        # Verify deterministic ID
        expected_id = _stable_routing_id({
            "action_id": self.action_id,
            "action_type": self.action_type.value,
            "tenant_id": self.tenant_id,
        })
        if self.routing_id != expected_id:
            raise ValueError(
                "routing_id does not match the canonical payload"
            )
        return self


# ---------------------------------------------------------------------------
# Company Operating Snapshot
# ---------------------------------------------------------------------------


class CompanyOperatingSnapshot(BaseModel):
    """Company-wide operating snapshot for the Daily Command.

    Aggregates department snapshots, top priorities, pending approvals,
    and overall health into a single view that powers executive decision
    making.

    Key invariants:
        - snapshot_id is deterministic from tenant + date.
        - never_auto_external is always True.
        - execution_allowed is always False (snapshot doesn't execute).
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    # Identity
    tenant_id: NonEmptyString
    snapshot_id: NonEmptyString
    snapshot_date: NonEmptyString

    # Department snapshots
    departments: tuple[DepartmentSnapshot, ...] = ()

    # Company-wide metrics
    overall_health: OperatingHealth = OperatingHealth.GOOD
    total_active_actions: int = Field(default=0, ge=0)
    total_pending_approvals: int = Field(default=0, ge=0)
    total_completed_today: int = Field(default=0, ge=0)
    total_failed_today: int = Field(default=0, ge=0)
    total_blocked_actions: int = Field(default=0, ge=0)

    # Priority items
    top_priorities: tuple[str, ...] = ()
    approval_items: tuple[str, ...] = ()
    blockers: tuple[str, ...] = ()

    # Revenue intelligence
    active_opportunities: int = Field(default=0, ge=0)
    pipeline_value_sar: float = Field(default=0.0, ge=0.0)

    # Proof and learning
    proof_events_today: int = Field(default=0, ge=0)
    learning_events_today: int = Field(default=0, ge=0)

    # Safety — ALWAYS
    never_auto_external: bool = True
    execution_allowed: bool = False

    # Provenance
    source_id: NonEmptyString
    generated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    @model_validator(mode="after")
    def enforce_snapshot_invariants(self) -> CompanyOperatingSnapshot:
        if not self.never_auto_external:
            raise ValueError(
                "company snapshots cannot authorize external actions"
            )
        if self.execution_allowed:
            raise ValueError(
                "company snapshots never authorize execution"
            )

        expected_id = _stable_snapshot_id({
            "snapshot_date": self.snapshot_date,
            "tenant_id": self.tenant_id,
        })
        if self.snapshot_id != expected_id:
            raise ValueError(
                "snapshot_id does not match the canonical payload"
            )

        return self


# ---------------------------------------------------------------------------
# Engine functions
# ---------------------------------------------------------------------------


def route_task(
    action: CanonicalAction,
    *,
    source_id: str,
    department_capacities: dict[Department, float] | None = None,
) -> TaskRoutingDecision:
    """Route an action to the most appropriate department.

    Uses the department capability map and capacity data to determine
    the best department for handling the action. Falls back to
    OPERATIONS if no mapping exists.
    """
    capacities = department_capacities or {}

    # Find capable departments
    capable = list(
        _DEPARTMENT_ACTION_MAP.get(action.action_type, (Department.OPERATIONS,))
    )

    if not capable:
        capable = [Department.OPERATIONS]

    # Select the department with the most capacity
    best_dept = capable[0]
    best_capacity = capacities.get(best_dept, 100.0)

    for dept in capable[1:]:
        dept_capacity = capacities.get(dept, 100.0)
        if dept_capacity > best_capacity:
            best_dept = dept
            best_capacity = dept_capacity

    # Determine routing result
    if best_capacity <= 0:
        result = TaskRouteResult.BLOCKED
        reasoning = (
            f"All capable departments at zero capacity. "
            f"Action {action.action_type.value} blocked."
        )
    elif action.risk_level in (RiskLevel.HIGH, RiskLevel.CRITICAL):
        result = TaskRouteResult.ESCALATED
        reasoning = (
            f"High-risk action {action.action_type.value} escalated to "
            f"{best_dept.value} with executive notification."
        )
    elif action.external_effect:
        result = TaskRouteResult.QUEUED
        reasoning = (
            f"External action {action.action_type.value} queued for "
            f"{best_dept.value} pending human approval."
        )
    else:
        result = TaskRouteResult.ROUTED
        reasoning = (
            f"Internal action {action.action_type.value} routed to "
            f"{best_dept.value} (capacity: {best_capacity:.0f}%)."
        )

    # Alternatives are the other capable departments
    alternatives = tuple(d for d in capable if d != best_dept)

    routing_id = _stable_routing_id({
        "action_id": action.action_id,
        "action_type": action.action_type.value,
        "tenant_id": action.tenant_id,
    })

    return TaskRoutingDecision(
        tenant_id=action.tenant_id,
        routing_id=routing_id,
        action_id=action.action_id,
        action_type=action.action_type,
        target_department=best_dept,
        result=result,
        reasoning=reasoning,
        requires_approval=action.approval_required,
        risk_level=action.risk_level,
        alternative_departments=alternatives,
        source_id=source_id,
    )


def build_department_snapshot(
    department: Department,
    *,
    actions: list[CanonicalAction] | None = None,
    kpi_scores: tuple[tuple[str, float], ...] = (),
    active_plan_id: str = "",
    plan_progress_pct: float = 0.0,
) -> DepartmentSnapshot:
    """Build a point-in-time snapshot of a department's operating state.

    Analyzes the department's current action queue to determine health,
    workload, and capacity.
    """
    dept_actions = actions or []

    active = sum(
        1 for a in dept_actions
        if a.status.value in ("queued", "in_progress", "approved")
    )
    pending = sum(
        1 for a in dept_actions
        if a.status.value == "awaiting_approval"
    )
    completed = sum(
        1 for a in dept_actions if a.status.value == "completed"
    )
    failed = sum(
        1 for a in dept_actions if a.status.value == "failed"
    )
    blocked = sum(
        1 for a in dept_actions if a.status.value == "blocked"
    )

    # Calculate capacity (100% minus active/10 work units)
    capacity = max(0.0, 100.0 - (active * 10.0))

    # Determine health
    if failed > active:
        health = OperatingHealth.CRITICAL
    elif blocked > 0 or pending > active:
        health = OperatingHealth.AT_RISK
    elif failed > 0:
        health = OperatingHealth.NEEDS_ATTENTION
    elif active > 0 and completed >= active:
        health = OperatingHealth.EXCELLENT
    else:
        health = OperatingHealth.GOOD

    return DepartmentSnapshot(
        department=department,
        health=health,
        active_actions=active,
        pending_approvals=pending,
        completed_today=completed,
        failed_today=failed,
        blocked_actions=blocked,
        kpi_scores=kpi_scores,
        capacity_pct=capacity,
        active_plan_id=active_plan_id,
        plan_progress_pct=plan_progress_pct,
    )


def generate_operating_snapshot(
    *,
    tenant_id: str,
    snapshot_date: str,
    source_id: str,
    department_snapshots: list[DepartmentSnapshot],
    top_priorities: tuple[str, ...] = (),
    approval_items: tuple[str, ...] = (),
    blockers: tuple[str, ...] = (),
    active_opportunities: int = 0,
    pipeline_value_sar: float = 0.0,
    proof_events_today: int = 0,
    learning_events_today: int = 0,
) -> CompanyOperatingSnapshot:
    """Generate a company-wide operating snapshot.

    Aggregates department snapshots into a single view for the Daily
    Command. This is the executive dashboard for AI-operated companies.
    """
    # Aggregate metrics
    total_active = sum(d.active_actions for d in department_snapshots)
    total_pending = sum(d.pending_approvals for d in department_snapshots)
    total_completed = sum(d.completed_today for d in department_snapshots)
    total_failed = sum(d.failed_today for d in department_snapshots)
    total_blocked = sum(d.blocked_actions for d in department_snapshots)

    # Determine overall health
    health_scores = {
        OperatingHealth.EXCELLENT: 5,
        OperatingHealth.GOOD: 4,
        OperatingHealth.NEEDS_ATTENTION: 3,
        OperatingHealth.AT_RISK: 2,
        OperatingHealth.CRITICAL: 1,
    }

    if department_snapshots:
        avg_health = sum(
            health_scores[d.health] for d in department_snapshots
        ) / len(department_snapshots)

        if avg_health >= 4.5:
            overall_health = OperatingHealth.EXCELLENT
        elif avg_health >= 3.5:
            overall_health = OperatingHealth.GOOD
        elif avg_health >= 2.5:
            overall_health = OperatingHealth.NEEDS_ATTENTION
        elif avg_health >= 1.5:
            overall_health = OperatingHealth.AT_RISK
        else:
            overall_health = OperatingHealth.CRITICAL
    else:
        overall_health = OperatingHealth.GOOD

    # Build snapshot ID
    snapshot_id = _stable_snapshot_id({
        "snapshot_date": snapshot_date.strip(),
        "tenant_id": tenant_id.strip(),
    })

    return CompanyOperatingSnapshot(
        tenant_id=tenant_id,
        snapshot_id=snapshot_id,
        snapshot_date=snapshot_date,
        departments=tuple(department_snapshots),
        overall_health=overall_health,
        total_active_actions=total_active,
        total_pending_approvals=total_pending,
        total_completed_today=total_completed,
        total_failed_today=total_failed,
        total_blocked_actions=total_blocked,
        top_priorities=top_priorities,
        approval_items=approval_items,
        blockers=blockers,
        active_opportunities=active_opportunities,
        pipeline_value_sar=pipeline_value_sar,
        proof_events_today=proof_events_today,
        learning_events_today=learning_events_today,
        never_auto_external=True,
        execution_allowed=False,
        source_id=source_id,
    )


def prioritize_actions(
    actions: list[CanonicalAction],
) -> list[CanonicalAction]:
    """Prioritize actions across all departments by priority score.

    Returns actions sorted by priority_score (highest first), with
    external-effect actions pushed to the top of their priority band
    since they need human attention.
    """
    def sort_key(action: CanonicalAction) -> tuple[float, int, float]:
        # Sort by: external-first (desc), priority_score (desc), urgency (desc)
        return (
            -float(action.external_effect),
            -1 if action.risk_level in (RiskLevel.HIGH, RiskLevel.CRITICAL) else 0,
            -action.priority_score,
        )

    return sorted(actions, key=sort_key)


def get_capable_departments(action_type: ActionType) -> tuple[Department, ...]:
    """Return departments capable of handling the given action type."""
    return _DEPARTMENT_ACTION_MAP.get(action_type, (Department.OPERATIONS,))
