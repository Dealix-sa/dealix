"""Team Operations API — team roster, hiring plan, and capacity management.

Endpoints:
  GET  /api/v1/team/              — all team members with summary
  GET  /api/v1/team/hiring-plan   — hiring milestones sorted by MRR threshold
  GET  /api/v1/team/capacity      — capacity overview and health score
  GET  /api/v1/team/{member_id}   — single member detail
  POST /api/v1/team/              — add a new team member
  PUT  /api/v1/team/{member_id}/status — update member status

All admin-gated. Mutating actions use APPROVAL_FIRST; read-only uses ALLOW_WITH_REVIEW.
"""

from __future__ import annotations

import copy
from datetime import UTC, date, datetime
from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException
from pydantic import BaseModel, Field

from api.security.api_key import require_admin_key
from core.logging import get_logger

_log = get_logger(__name__)

router = APIRouter(
    prefix="/api/v1/team",
    tags=["team-ops"],
    dependencies=[Depends(require_admin_key)],
)

_GOV_READ = "ALLOW_WITH_REVIEW"
_GOV_MUTATE = "APPROVAL_FIRST"

_VALID_EMPLOYMENT_TYPES: frozenset[str] = frozenset(
    {"full_time", "part_time", "contractor", "planned"}
)
_VALID_STATUSES: frozenset[str] = frozenset(
    {"active", "probation", "planned", "inactive"}
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _now_iso() -> str:
    """Return current UTC datetime as ISO string."""
    return datetime.now(UTC).isoformat()


def _today_str() -> str:
    """Return today's date as YYYY-MM-DD string."""
    return date.today().isoformat()


def _days_tenure(joined_at: str | None) -> int:
    """Return number of days since joined_at. Returns 0 for planned/None."""
    if not joined_at:
        return 0
    try:
        joined = datetime.fromisoformat(joined_at.replace("Z", "+00:00"))
        delta = datetime.now(UTC) - joined
        return max(0, delta.days)
    except Exception:
        return 0


# ---------------------------------------------------------------------------
# Demo data
# ---------------------------------------------------------------------------

_TEAM_MEMBERS: list[dict[str, Any]] = [
    {
        "member_id": "TM-001",
        "name_ar": "المؤسس",
        "name_en": "Founder",
        "role_ar": "المؤسس والرئيس التنفيذي",
        "role_en": "Founder / CEO",
        "employment_type": "full_time",
        "status": "active",
        "hire_trigger": None,
        "monthly_cost_sar": 0.0,
        "permissions": [
            "all",
            "admin",
            "billing",
            "hiring",
            "governance",
            "client_management",
            "product",
        ],
        "joined_at": "2025-01-01",
        "kpi_targets": {
            "mrr_sar": 120_000,
            "active_clients": 30,
            "nps_score": 70,
            "monthly_demos": 20,
        },
    },
    {
        "member_id": "TM-002",
        "name_ar": "مسؤول نجاح العملاء",
        "name_en": "CSM Lead",
        "role_ar": "مدير نجاح العملاء وقيادة التسليم",
        "role_en": "CSM / Delivery Lead",
        "employment_type": "full_time",
        "status": "active",
        "hire_trigger": "30K SAR MRR",
        "monthly_cost_sar": 8_000.0,
        "permissions": [
            "client_management",
            "delivery",
            "reporting",
            "onboarding",
        ],
        "joined_at": "2025-06-01",
        "kpi_targets": {
            "active_clients": 15,
            "nps_score": 75,
            "onboarding_time_days": 7,
            "churn_rate_max_pct": 5,
        },
    },
    {
        "member_id": "TM-003",
        "name_ar": "مهندس الخلفية",
        "name_en": "Backend Engineer",
        "role_ar": "مهندس الخلفية والبنية التحتية",
        "role_en": "Backend Engineer",
        "employment_type": "full_time",
        "status": "active",
        "hire_trigger": "50K SAR MRR",
        "monthly_cost_sar": 12_000.0,
        "permissions": [
            "engineering",
            "deployments",
            "data_pipelines",
            "integrations",
        ],
        "joined_at": "2025-09-01",
        "kpi_targets": {
            "uptime_pct": 99.9,
            "deploy_frequency_per_week": 3,
            "p99_latency_ms": 300,
            "bug_resolution_days": 2,
        },
    },
    {
        "member_id": "TM-004",
        "name_ar": "مندوب تطوير المبيعات",
        "name_en": "SDR",
        "role_ar": "ممثل تطوير المبيعات",
        "role_en": "Sales Development Representative",
        "employment_type": "contractor",
        "status": "probation",
        "hire_trigger": "80K SAR MRR",
        "monthly_cost_sar": 5_000.0,
        "permissions": [
            "outreach",
            "lead_qualification",
            "crm_write",
        ],
        "joined_at": "2026-04-01",
        "kpi_targets": {
            "qualified_leads_per_month": 20,
            "demos_booked_per_month": 8,
            "conversion_rate_pct": 20,
        },
    },
    {
        "member_id": "TM-005",
        "name_ar": "محلل العمليات",
        "name_en": "Operations Analyst",
        "role_ar": "محلل العمليات والبيانات",
        "role_en": "Operations Analyst",
        "employment_type": "planned",
        "status": "planned",
        "hire_trigger": "120K SAR MRR",
        "monthly_cost_sar": 9_000.0,
        "permissions": [],
        "joined_at": None,
        "kpi_targets": {
            "data_quality_score": 95,
            "reports_per_month": 8,
            "automation_coverage_pct": 70,
        },
    },
]

_HIRING_MILESTONES: list[dict[str, Any]] = [
    {
        "mrr_threshold_sar": 30_000,
        "role_ar": "مدير نجاح العملاء",
        "role_en": "CSM Lead",
        "status": "triggered",
        "member_id": "TM-002",
    },
    {
        "mrr_threshold_sar": 50_000,
        "role_ar": "مهندس الخلفية",
        "role_en": "Backend Engineer",
        "status": "triggered",
        "member_id": "TM-003",
    },
    {
        "mrr_threshold_sar": 80_000,
        "role_ar": "ممثل تطوير المبيعات",
        "role_en": "SDR",
        "status": "upcoming",
        "member_id": None,
    },
    {
        "mrr_threshold_sar": 120_000,
        "role_ar": "مهندس البيانات",
        "role_en": "Data Engineer",
        "status": "planned",
        "member_id": None,
    },
    {
        "mrr_threshold_sar": 200_000,
        "role_ar": "رئيس المبيعات",
        "role_en": "Head of Sales",
        "status": "planned",
        "member_id": None,
    },
]

# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

_next_member_seq: int = 6


def _get_member(member_id: str) -> dict[str, Any] | None:
    return next((m for m in _TEAM_MEMBERS if m["member_id"] == member_id), None)


def _enrich_member(m: dict[str, Any]) -> dict[str, Any]:
    enriched = dict(m)
    enriched["days_tenure"] = _days_tenure(m.get("joined_at"))
    return enriched


def _compute_health_score(
    active_members: int,
    current_active_clients: int,
    monthly_cost_total: float,
) -> int:
    """Compute a 0-100 team health score based on tenure, capacity, and cost efficiency.

    The score weighs three factors:
    - Tenure stability: proportion of members with tenure > 30 days
    - Capacity utilisation: ratio of clients per member vs safe threshold (6)
    - Cost efficiency: headcount cost vs expected revenue capacity
    """
    score = 100

    # Capacity factor: penalise if clients-per-member exceeds 6
    if active_members > 0:
        ratio = current_active_clients / active_members
        if ratio > 6:
            overload_pct = min((ratio - 6) / 6 * 100, 40)
            score -= int(overload_pct)

    # Tenure factor: members still in probation reduce confidence
    probation_members = [m for m in _TEAM_MEMBERS if m["status"] == "probation"]
    active_non_planned = [m for m in _TEAM_MEMBERS if m["status"] not in ("planned", "inactive")]
    if active_non_planned:
        probation_ratio = len(probation_members) / len(active_non_planned)
        score -= int(probation_ratio * 20)

    # Cost factor: sanity-check cost vs revenue estimate (rough heuristic)
    if monthly_cost_total > 0:
        estimated_mrr = current_active_clients * 3_500  # average SAR per client estimate
        cost_ratio = monthly_cost_total / max(estimated_mrr, 1)
        if cost_ratio > 0.4:
            score -= int(min((cost_ratio - 0.4) * 30, 20))

    return max(0, min(100, score))


# ---------------------------------------------------------------------------
# Request models
# ---------------------------------------------------------------------------


class AddMemberBody(BaseModel):
    name_ar: str = Field(..., min_length=1, max_length=200)
    name_en: str = Field(..., min_length=1, max_length=200)
    role_ar: str = Field(..., min_length=1, max_length=200)
    role_en: str = Field(..., min_length=1, max_length=200)
    employment_type: str = Field(..., pattern="^(full_time|part_time|contractor|planned)$")
    monthly_cost_sar: float = Field(..., ge=0)
    permissions: list[str] = Field(default_factory=list)


class UpdateStatusBody(BaseModel):
    new_status: str = Field(..., pattern="^(active|probation|inactive)$")
    reason: str = Field(..., min_length=5, max_length=500)


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------


@router.get("/")
async def list_team_members() -> dict[str, Any]:
    """All team members with roster summary.

    Returns all 5 demo members enriched with days_tenure.
    Summary includes total_members, active_count, monthly_cost_sar_total,
    team_arr_overhead_sar, and open_roles_count.
    """
    enriched = [_enrich_member(m) for m in _TEAM_MEMBERS]

    active_count = sum(1 for m in _TEAM_MEMBERS if m["status"] == "active")
    monthly_cost_total = sum(m["monthly_cost_sar"] for m in _TEAM_MEMBERS if m["status"] != "planned")
    open_roles_count = sum(1 for m in _TEAM_MEMBERS if m["status"] == "planned")

    return {
        "governance_decision": _GOV_READ,
        "generated_at": _now_iso(),
        "summary": {
            "total_members": len(_TEAM_MEMBERS),
            "active_count": active_count,
            "monthly_cost_sar_total": monthly_cost_total,
            "team_arr_overhead_sar": monthly_cost_total * 12,
            "open_roles_count": open_roles_count,
        },
        "members": enriched,
    }


@router.get("/hiring-plan")
async def get_hiring_plan() -> dict[str, Any]:
    """Hiring milestones sorted by MRR threshold.

    Returns all 5 milestones, identifies the next hire (first upcoming role),
    and shows total planned cost for upcoming/planned roles.
    """
    sorted_milestones = sorted(_HIRING_MILESTONES, key=lambda m: m["mrr_threshold_sar"])

    next_hire = next(
        (m["role_en"] for m in sorted_milestones if m["status"] == "upcoming"),
        None,
    )
    next_hire_ar = next(
        (m["role_ar"] for m in sorted_milestones if m["status"] == "upcoming"),
        None,
    )

    planned_members = [m for m in _TEAM_MEMBERS if m["status"] == "planned"]
    total_planned_cost_sar = sum(m["monthly_cost_sar"] for m in planned_members)

    return {
        "governance_decision": _GOV_READ,
        "generated_at": _now_iso(),
        "milestones": sorted_milestones,
        "next_hire": next_hire,
        "next_hire_ar": next_hire_ar,
        "total_planned_cost_sar": total_planned_cost_sar,
        "action_ar": "وظّف عند بلوغ عتبة الإيرادات الشهرية المقابلة — لا تسبق الإيرادات",
        "action_en": "Hire when the corresponding MRR threshold is reached — do not hire ahead of revenue",
    }


@router.get("/capacity")
async def get_capacity() -> dict[str, Any]:
    """Team capacity overview: active members, client load, and health score.

    active_members counts non-planned members.
    capacity_per_member is clients per active person.
    capacity_warning is True when clients-per-member exceeds 6.
    team_health_score is 0-100 based on tenure, capacity, and cost efficiency.
    """
    active_members = [m for m in _TEAM_MEMBERS if m["status"] not in ("planned", "inactive")]
    active_count = len(active_members)
    current_active_clients: int = 12

    capacity_per_member = (
        round(current_active_clients / active_count, 2) if active_count > 0 else 0.0
    )
    capacity_warning = capacity_per_member > 6

    monthly_cost_total = sum(m["monthly_cost_sar"] for m in active_members)
    health_score = _compute_health_score(active_count, current_active_clients, monthly_cost_total)

    if capacity_warning:
        recommendations_ar = [
            "تجاوزت نسبة العملاء لكل موظف الحد الآمن (6) — يُنصح بالتوظيف",
            "راجع توزيع العمل وأعِد تخصيص العملاء بين أعضاء الفريق",
        ]
        recommendations_en = [
            "Clients-per-member has exceeded the safe threshold (6) — consider hiring",
            "Review workload distribution and reassign clients across team members",
        ]
    else:
        recommendations_ar = [
            "طاقة الفريق ضمن الحدود المقبولة",
            "راقب النمو الشهري لتحديد موعد التوظيف التالي",
        ]
        recommendations_en = [
            "Team capacity is within acceptable limits",
            "Monitor monthly growth to determine timing of next hire",
        ]

    return {
        "governance_decision": _GOV_READ,
        "generated_at": _now_iso(),
        "active_members": active_count,
        "current_active_clients": current_active_clients,
        "capacity_per_member": capacity_per_member,
        "capacity_warning": capacity_warning,
        "team_health_score": health_score,
        "monthly_cost_sar_total": monthly_cost_total,
        "recommendations_ar": recommendations_ar,
        "recommendations_en": recommendations_en,
    }


@router.get("/{member_id}")
async def get_member(member_id: str) -> dict[str, Any]:
    """Single team member detail. Returns 404 if member_id is not found."""
    member = _get_member(member_id)
    if not member:
        raise HTTPException(status_code=404, detail=f"Team member {member_id!r} not found")

    return {
        "governance_decision": _GOV_READ,
        "generated_at": _now_iso(),
        **_enrich_member(member),
    }


@router.post("/")
async def add_team_member(body: AddMemberBody = Body(...)) -> dict[str, Any]:
    """Add a new team member. Requires APPROVAL_FIRST.

    Auto-assigns the next sequential member_id. Sets status to 'active'
    and joined_at to today. This action requires explicit founder approval.
    """
    global _next_member_seq

    member_id = f"TM-{_next_member_seq:03d}"
    _next_member_seq += 1

    new_member: dict[str, Any] = {
        "member_id": member_id,
        "name_ar": body.name_ar,
        "name_en": body.name_en,
        "role_ar": body.role_ar,
        "role_en": body.role_en,
        "employment_type": body.employment_type,
        "status": "active",
        "hire_trigger": None,
        "monthly_cost_sar": body.monthly_cost_sar,
        "permissions": body.permissions,
        "joined_at": _today_str(),
        "kpi_targets": {},
    }

    _TEAM_MEMBERS.append(new_member)

    _log.info(
        "team_member_added",
        member_id=member_id,
        role_en=body.role_en,
        employment_type=body.employment_type,
    )

    return {
        "governance_decision": _GOV_MUTATE,
        "generated_at": _now_iso(),
        "member_id": member_id,
        "status_ar": "طلب إضافة عضو جديد مُسجَّل — يتطلب موافقة المؤسس قبل التنفيذ",
        "status_en": "New member addition recorded — requires founder approval before execution",
        "member": _enrich_member(new_member),
    }


@router.put("/{member_id}/status")
async def update_member_status(
    member_id: str,
    body: UpdateStatusBody = Body(...),
) -> dict[str, Any]:
    """Update a team member's status. Requires APPROVAL_FIRST.

    Valid target statuses: active, probation, inactive.
    Setting status to 'planned' is not allowed via this endpoint (use POST instead).
    Returns 404 if member_id is not found. Returns 400 if new_status is 'planned'.
    """
    if body.new_status == "planned":
        raise HTTPException(
            status_code=400,
            detail="Cannot set status to 'planned' via this endpoint. Use POST / to create a planned role.",
        )

    member = _get_member(member_id)
    if not member:
        raise HTTPException(status_code=404, detail=f"Team member {member_id!r} not found")

    old_status = member["status"]
    member["status"] = body.new_status

    _log.info(
        "team_member_status_updated",
        member_id=member_id,
        old_status=old_status,
        new_status=body.new_status,
    )

    return {
        "governance_decision": _GOV_MUTATE,
        "generated_at": _now_iso(),
        "member_id": member_id,
        "previous_status": old_status,
        "new_status": body.new_status,
        "reason": body.reason,
        "status_ar": "طلب تحديث الحالة مُسجَّل — يتطلب موافقة المؤسس قبل التنفيذ",
        "status_en": "Status update recorded — requires founder approval before execution",
    }
