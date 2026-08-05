"""Canonical DepartmentPlan contracts for Company Intelligence strategy execution.

A DepartmentPlan translates department strategy into bounded, measurable
actions with KPIs. It sits between the Company Brain (configuration) and
the Action Queue (execution) — providing the goal-to-action bridge for
each of the 12 operational departments.

The models are persistence-neutral: no database, network, or LLM calls.

Entity ownership: DepartmentPlan → strategy_execution
    (department strategy translated into bounded actions).
Required fields: tenant_id, department, goal, actions, kpis.
Forbidden parallel names: AgentPlan, TeamPlan.
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

NonEmptyString = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------


class Department(StrEnum):
    """Operational departments in the Company OS."""

    SALES = "sales"
    MARKETING = "marketing"
    OPERATIONS = "operations"
    FINANCE = "finance"
    CUSTOMER_SUCCESS = "customer_success"
    PRODUCT = "product"
    ENGINEERING = "engineering"
    DATA = "data"
    PARTNERSHIPS = "partnerships"
    HR = "hr"
    LEGAL = "legal"
    EXECUTIVE = "executive"


class PlanStatus(StrEnum):
    """Lifecycle states for a department plan."""

    DRAFT = "draft"
    ACTIVE = "active"
    UNDER_REVIEW = "under_review"
    PAUSED = "paused"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class PlanPriority(StrEnum):
    """Priority levels for a department plan."""

    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


# ---------------------------------------------------------------------------
# Stable ID generation
# ---------------------------------------------------------------------------


def _stable_plan_id(payload: dict[str, Any]) -> str:
    canonical = json.dumps(
        payload,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
        default=str,
    )
    return f"plan_{sha256(canonical.encode('utf-8')).hexdigest()[:16]}"


# ---------------------------------------------------------------------------
# Canonical DepartmentPlan contract
# ---------------------------------------------------------------------------


class CanonicalDepartmentPlan(BaseModel):
    """One tenant-scoped, goal-oriented department plan.

    A DepartmentPlan breaks a department's strategic goal into bounded
    action references and measurable KPIs. It never authorizes external
    action by itself — actions flow through the Action → Draft → Approval
    chain.

    Key invariants:
      - Must have at least one action reference.
      - Must have at least one KPI.
      - Goal cannot be empty.
      - Plan ID is deterministic from the plan key.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    # Identity
    tenant_id: NonEmptyString
    plan_id: NonEmptyString
    deduplication_key: NonEmptyString

    # Department and goal
    department: Department
    goal: NonEmptyString
    description: str = ""

    # Priority
    priority: PlanPriority = PlanPriority.MEDIUM

    # Actions and KPIs
    action_ids: tuple[str, ...] = ()
    kpis: tuple[str, ...] = ()

    # Scoring
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)
    progress_pct: float = Field(default=0.0, ge=0.0, le=100.0)

    # Lifecycle
    status: PlanStatus = PlanStatus.DRAFT

    # Provenance
    source_id: NonEmptyString

    # Time window
    starts_at: datetime | None = None
    ends_at: datetime | None = None

    # Timestamps
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    last_reviewed_at: datetime | None = None

    @model_validator(mode="after")
    def enforce_plan_invariants(self) -> CanonicalDepartmentPlan:
        # Must have at least one action reference
        if len(self.action_ids) == 0:
            raise ValueError(
                "department plan requires at least one action reference"
            )

        # Must have at least one KPI
        if len(self.kpis) == 0:
            raise ValueError(
                "department plan requires at least one KPI"
            )

        # starts_at must be timezone-aware if set
        if self.starts_at is not None and self.starts_at.tzinfo is None:
            raise ValueError("starts_at must be timezone-aware")

        # ends_at must be timezone-aware if set
        if self.ends_at is not None and self.ends_at.tzinfo is None:
            raise ValueError("ends_at must be timezone-aware")

        # ends_at must be after starts_at if both set
        if (
            self.starts_at is not None
            and self.ends_at is not None
            and self.ends_at <= self.starts_at
        ):
            raise ValueError("ends_at must be after starts_at")

        # Verify deterministic ID
        expected_id = _stable_plan_id({
            "deduplication_key": self.deduplication_key,
            "department": self.department.value,
            "tenant_id": self.tenant_id,
        })
        if self.plan_id != expected_id:
            raise ValueError("plan_id does not match the canonical payload")

        return self


# ---------------------------------------------------------------------------
# Builder
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# DepartmentPlan state machine
# ---------------------------------------------------------------------------


_PLAN_TRANSITIONS: dict[PlanStatus, frozenset[PlanStatus]] = {
    PlanStatus.DRAFT: frozenset({
        PlanStatus.ACTIVE,
        PlanStatus.ARCHIVED,
    }),
    PlanStatus.ACTIVE: frozenset({
        PlanStatus.UNDER_REVIEW,
        PlanStatus.PAUSED,
        PlanStatus.COMPLETED,
        PlanStatus.ARCHIVED,
    }),
    PlanStatus.UNDER_REVIEW: frozenset({
        PlanStatus.ACTIVE,
        PlanStatus.ARCHIVED,
    }),
    PlanStatus.PAUSED: frozenset({
        PlanStatus.ACTIVE,
        PlanStatus.ARCHIVED,
    }),
    # Terminal states
    PlanStatus.COMPLETED: frozenset({
        PlanStatus.ARCHIVED,
    }),
    PlanStatus.ARCHIVED: frozenset(),
}


def valid_plan_transitions_from(
    status: PlanStatus,
) -> frozenset[PlanStatus]:
    """Return the set of valid next statuses from the given plan status."""
    return _PLAN_TRANSITIONS.get(status, frozenset())


def is_valid_plan_transition(
    from_status: PlanStatus,
    to_status: PlanStatus,
) -> bool:
    """Check whether a plan status transition is valid."""
    return to_status in valid_plan_transitions_from(from_status)


def transition_plan(
    plan: CanonicalDepartmentPlan,
    *,
    to_status: PlanStatus,
) -> CanonicalDepartmentPlan:
    """Return a new DepartmentPlan with an updated status after validating the transition.

    The returned plan is a new frozen instance — the original is unchanged.
    """
    if not is_valid_plan_transition(plan.status, to_status):
        raise ValueError(
            f"invalid plan transition: "
            f"{plan.status.value} → {to_status.value}"
        )
    return plan.model_copy(update={"status": to_status})


# ---------------------------------------------------------------------------
# Builder
# ---------------------------------------------------------------------------


def build_department_plan(
    *,
    tenant_id: str,
    deduplication_key: str,
    department: Department,
    goal: str,
    source_id: str,
    action_ids: tuple[str, ...] = ("placeholder_action",),
    kpis: tuple[str, ...] = ("placeholder_kpi",),
    description: str = "",
    priority: PlanPriority = PlanPriority.MEDIUM,
    confidence: float = 0.5,
    progress_pct: float = 0.0,
    status: PlanStatus = PlanStatus.DRAFT,
    starts_at: datetime | None = None,
    ends_at: datetime | None = None,
    last_reviewed_at: datetime | None = None,
) -> CanonicalDepartmentPlan:
    """Build a deterministic, idempotent, goal-oriented department plan."""

    plan_id = _stable_plan_id({
        "deduplication_key": deduplication_key.strip(),
        "department": department.value,
        "tenant_id": tenant_id.strip(),
    })

    return CanonicalDepartmentPlan(
        tenant_id=tenant_id,
        plan_id=plan_id,
        deduplication_key=deduplication_key,
        department=department,
        goal=goal,
        description=description,
        priority=priority,
        action_ids=action_ids,
        kpis=kpis,
        confidence=confidence,
        progress_pct=progress_pct,
        status=status,
        source_id=source_id,
        starts_at=starts_at,
        ends_at=ends_at,
        last_reviewed_at=last_reviewed_at,
    )
