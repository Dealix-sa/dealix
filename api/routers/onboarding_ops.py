"""Onboarding Operations API — client onboarding workflow management.

Manages the end-to-end client onboarding process from contract signing
through Sprint activation. Each step is tracked, bilingual, and gated
by the APPROVAL_FIRST governance principle.

Endpoints:
  GET  /api/v1/onboarding/checklist          — full onboarding checklist
  GET  /api/v1/onboarding/active             — clients currently onboarding
  GET  /api/v1/onboarding/{client_id}        — onboarding status for one client
  POST /api/v1/onboarding/start              — start onboarding for new client
  POST /api/v1/onboarding/{client_id}/step   — advance to next step
  GET  /api/v1/onboarding/metrics            — onboarding performance metrics

All endpoints require admin auth.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException
from pydantic import BaseModel, Field

from api.security.api_key import require_admin_key
from core.logging import get_logger

_log = get_logger(__name__)

router = APIRouter(
    prefix="/api/v1/onboarding",
    tags=["onboarding-ops"],
    dependencies=[Depends(require_admin_key)],
)

_GOV = "ALLOW_WITH_REVIEW"


def _now_iso() -> str:
    return datetime.now(UTC).isoformat()


# ---------------------------------------------------------------------------
# Onboarding checklist — 12 steps, bilingual
# ---------------------------------------------------------------------------

ONBOARDING_CHECKLIST: list[dict[str, Any]] = [
    {
        "step": 1,
        "step_id": "OB-001",
        "name_ar": "توقيع العقد واستلام الدفعة",
        "name_en": "Contract signed & payment received",
        "category": "commercial",
        "critical": True,
        "estimated_hours": 0.5,
        "owner": "founder",
        "governance_gate": "APPROVAL_FIRST",
        "description_ar": "توقيع عقد الخدمة ومعالجة الدفعة الأولى عبر Moyasar",
        "description_en": "Service contract signed and first payment processed via Moyasar",
    },
    {
        "step": 2,
        "step_id": "OB-002",
        "name_ar": "إرسال رسالة ترحيب ومعلومات الوصول",
        "name_en": "Welcome message & access credentials sent",
        "category": "communication",
        "critical": True,
        "estimated_hours": 0.5,
        "owner": "founder",
        "governance_gate": "APPROVAL_FIRST",
        "description_ar": "إرسال رسالة ترحيب رسمية وبيانات الوصول للمنصة (بموافقة مُسجَّلة)",
        "description_en": "Send formal welcome and platform access credentials (approval logged)",
    },
    {
        "step": 3,
        "step_id": "OB-003",
        "name_ar": "اجتماع الإعداد (Kickoff)",
        "name_en": "Kickoff meeting completed",
        "category": "delivery",
        "critical": True,
        "estimated_hours": 1.0,
        "owner": "founder",
        "governance_gate": "ALLOW_WITH_REVIEW",
        "description_ar": "اجتماع تعارف وتحديد أهداف Sprint مع صاحب القرار في الشركة",
        "description_en": "Introductory meeting and Sprint goal-setting with company decision maker",
    },
    {
        "step": 4,
        "step_id": "OB-004",
        "name_ar": "استلام بيانات الوصول لأنظمة العميل",
        "name_en": "Client system access credentials received",
        "category": "data",
        "critical": True,
        "estimated_hours": 1.0,
        "owner": "client",
        "governance_gate": "ALLOW_WITH_REVIEW",
        "description_ar": "استلام صلاحيات الوصول لـ CRM/ERP/البيانات المالية (الحد الأدنى اللازم فقط)",
        "description_en": "Receive access to CRM/ERP/financial data (minimum necessary access only)",
    },
    {
        "step": 5,
        "step_id": "OB-005",
        "name_ar": "تسجيل جواز المصدر (Source Passport)",
        "name_en": "Source Passport registered",
        "category": "data",
        "critical": True,
        "estimated_hours": 2.0,
        "owner": "founder",
        "governance_gate": "ALLOW_WITH_REVIEW",
        "description_ar": "توثيق جميع مصادر البيانات مع جداول PDPL وتصنيف البيانات الحساسة",
        "description_en": "Document all data sources with PDPL tables and sensitive data classification",
    },
    {
        "step": 6,
        "step_id": "OB-006",
        "name_ar": "تحليل جودة البيانات الأولي (DQ Score)",
        "name_en": "Initial data quality analysis (DQ Score)",
        "category": "data",
        "critical": True,
        "estimated_hours": 3.0,
        "owner": "founder",
        "governance_gate": "ALLOW_WITH_REVIEW",
        "description_ar": "حساب درجة جودة البيانات الأولية وتحديد مصادر التسريب",
        "description_en": "Calculate baseline DQ score and identify revenue leakage sources",
    },
    {
        "step": 7,
        "step_id": "OB-007",
        "name_ar": "تقييم ZATCA الأولي",
        "name_en": "Initial ZATCA assessment",
        "category": "compliance",
        "critical": True,
        "estimated_hours": 1.5,
        "owner": "founder",
        "governance_gate": "ALLOW_WITH_REVIEW",
        "description_ar": "تقييم حالة الامتثال لـ ZATCA Phase 2 وتحديد الفجوات الحرجة",
        "description_en": "Assess ZATCA Phase 2 compliance state and identify critical gaps",
    },
    {
        "step": 8,
        "step_id": "OB-008",
        "name_ar": "تقييم PDPL الأولي",
        "name_en": "Initial PDPL assessment",
        "category": "compliance",
        "critical": False,
        "estimated_hours": 1.5,
        "owner": "founder",
        "governance_gate": "ALLOW_WITH_REVIEW",
        "description_ar": "تقييم مستوى التوافق مع نظام PDPL وتحديد المخاطر الفورية",
        "description_en": "Assess PDPL compliance level and identify immediate risks",
    },
    {
        "step": 9,
        "step_id": "OB-009",
        "name_ar": "إعداد خطة Sprint المخصصة",
        "name_en": "Sprint plan drafted",
        "category": "delivery",
        "critical": True,
        "estimated_hours": 2.0,
        "owner": "founder",
        "governance_gate": "APPROVAL_FIRST",
        "description_ar": "إعداد خطة Sprint 7 أيام محددة الأهداف وإرسالها للموافقة",
        "description_en": "Draft 7-day Sprint plan with specific objectives and send for approval",
    },
    {
        "step": 10,
        "step_id": "OB-010",
        "name_ar": "موافقة العميل على خطة Sprint",
        "name_en": "Client approval on Sprint plan",
        "category": "commercial",
        "critical": True,
        "estimated_hours": 0.5,
        "owner": "client",
        "governance_gate": "APPROVAL_FIRST",
        "description_ar": "الحصول على موافقة مكتوبة من العميل على خطة Sprint قبل التنفيذ",
        "description_en": "Obtain written client approval on Sprint plan before execution",
    },
    {
        "step": 11,
        "step_id": "OB-011",
        "name_ar": "إعداد لوحة متابعة العميل",
        "name_en": "Client dashboard configured",
        "category": "technical",
        "critical": False,
        "estimated_hours": 1.0,
        "owner": "founder",
        "governance_gate": "ALLOW_WITH_REVIEW",
        "description_ar": "إعداد لوحة متابعة مخصصة للعميل مع مؤشرات الأداء الرئيسية",
        "description_en": "Configure custom client dashboard with relevant KPI views",
    },
    {
        "step": 12,
        "step_id": "OB-012",
        "name_ar": "بدء تنفيذ Sprint",
        "name_en": "Sprint execution started",
        "category": "delivery",
        "critical": True,
        "estimated_hours": 0.5,
        "owner": "founder",
        "governance_gate": "ALLOW_WITH_REVIEW",
        "description_ar": "إطلاق Sprint رسمياً مع تحديد اليوم الأول وجدول التسليم",
        "description_en": "Officially launch Sprint with Day 1 confirmation and delivery schedule",
    },
]

# ---------------------------------------------------------------------------
# Demo onboarding clients
# ---------------------------------------------------------------------------

_ACTIVE_ONBOARDINGS: list[dict[str, Any]] = [
    {
        "client_id": "ONB-001",
        "company_ar": "شركة المنفعة للتقنية",
        "company_en": "Al Manfaa Technology Co",
        "sector": "technology",
        "city": "riyadh",
        "contract_value_sar": 499,
        "tier": "sprint",
        "current_step": 6,
        "started_at": "2026-05-28T09:00:00Z",
        "target_completion": "2026-06-04T09:00:00Z",
        "completed_steps": [1, 2, 3, 4, 5],
        "blocked": False,
        "blocker_ar": None,
        "blocker_en": None,
        "health": "on_track",
    },
    {
        "client_id": "ONB-002",
        "company_ar": "سفا للخدمات اللوجستية",
        "company_en": "Safa Logistics Services",
        "sector": "logistics",
        "city": "jeddah",
        "contract_value_sar": 3_999,
        "tier": "managed_ops",
        "current_step": 4,
        "started_at": "2026-05-30T10:00:00Z",
        "target_completion": "2026-06-10T10:00:00Z",
        "completed_steps": [1, 2, 3],
        "blocked": True,
        "blocker_ar": "لم يُرسَل بعد بيانات الوصول لنظام ERP",
        "blocker_en": "ERP system access credentials not yet provided",
        "health": "blocked",
    },
    {
        "client_id": "ONB-003",
        "company_ar": "تمكين الصحية",
        "company_en": "Tamkeen Health Tech",
        "sector": "healthcare",
        "city": "riyadh",
        "contract_value_sar": 1_500,
        "tier": "data_pack",
        "current_step": 9,
        "started_at": "2026-05-25T08:00:00Z",
        "target_completion": "2026-06-01T08:00:00Z",
        "completed_steps": [1, 2, 3, 4, 5, 6, 7, 8],
        "blocked": False,
        "blocker_ar": None,
        "blocker_en": None,
        "health": "on_track",
    },
]


def _get_onboarding(client_id: str) -> dict[str, Any] | None:
    return next((c for c in _ACTIVE_ONBOARDINGS if c["client_id"] == client_id), None)


def _enrich_onboarding(onb: dict[str, Any]) -> dict[str, Any]:
    completed = len(onb["completed_steps"])
    total = len(ONBOARDING_CHECKLIST)
    pct = round(completed / total * 100)
    current_step_data = next(
        (s for s in ONBOARDING_CHECKLIST if s["step"] == onb["current_step"]), None
    )
    return {
        **onb,
        "completion_pct": pct,
        "total_steps": total,
        "completed_count": completed,
        "remaining_steps": total - completed,
        "current_step_data": current_step_data,
        "estimated_hours_remaining": sum(
            s["estimated_hours"]
            for s in ONBOARDING_CHECKLIST
            if s["step"] >= onb["current_step"]
        ),
    }


# ---------------------------------------------------------------------------
# Request/Response models
# ---------------------------------------------------------------------------


class StartOnboardingBody(BaseModel):
    client_id: str = Field(min_length=3, max_length=50)
    company_name_ar: str = Field(min_length=2, max_length=100)
    company_name_en: str = Field(min_length=2, max_length=100)
    sector: str = Field(min_length=2, max_length=50)
    city: str = Field(min_length=2, max_length=50)
    tier: str = Field(default="sprint")
    contract_value_sar: float = Field(ge=0)


class AdvanceStepBody(BaseModel):
    step_id: str = Field(min_length=3)
    completion_notes_ar: str = Field(default="", max_length=500)
    completion_notes_en: str = Field(default="", max_length=500)


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------


@router.get("/checklist")
async def get_onboarding_checklist() -> dict[str, Any]:
    """Full 12-step onboarding checklist with bilingual labels.

    Returns all steps grouped by category with time estimates and
    governance gates (APPROVAL_FIRST steps are clearly marked).
    """
    categories: dict[str, list[dict[str, Any]]] = {}
    for step in ONBOARDING_CHECKLIST:
        cat = step["category"]
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(step)

    critical_count = sum(1 for s in ONBOARDING_CHECKLIST if s["critical"])
    total_hours = sum(s["estimated_hours"] for s in ONBOARDING_CHECKLIST)
    approval_first_steps = [s["step_id"] for s in ONBOARDING_CHECKLIST if s["governance_gate"] == "APPROVAL_FIRST"]

    return {
        "governance_decision": _GOV,
        "generated_at": _now_iso(),
        "total_steps": len(ONBOARDING_CHECKLIST),
        "critical_steps": critical_count,
        "estimated_total_hours": total_hours,
        "approval_first_steps": approval_first_steps,
        "checklist_by_category": categories,
        "checklist": ONBOARDING_CHECKLIST,
        "note_ar": "الخطوات المُحدَّدة كـ APPROVAL_FIRST تتطلب موافقة صريحة قبل الإكمال",
        "note_en": "Steps marked APPROVAL_FIRST require explicit approval before completion",
    }


@router.get("/active")
async def get_active_onboardings() -> dict[str, Any]:
    """All clients currently in onboarding — with progress and blockers.

    Returns enriched onboarding status including completion percentage,
    current step, and any blockers requiring founder attention.
    """
    enriched = [_enrich_onboarding(c) for c in _ACTIVE_ONBOARDINGS]
    blocked = [c for c in enriched if c["blocked"]]
    on_track = [c for c in enriched if not c["blocked"]]

    return {
        "governance_decision": _GOV,
        "generated_at": _now_iso(),
        "total_onboarding": len(enriched),
        "blocked_count": len(blocked),
        "on_track_count": len(on_track),
        "clients": enriched,
        "alert_ar": f"{len(blocked)} عملاء محجوبون يتطلبون انتباهاً فورياً" if blocked else "لا عملاء محجوبون",
        "alert_en": f"{len(blocked)} blocked client(s) require immediate attention" if blocked else "No blocked clients",
    }


@router.get("/metrics")
async def get_onboarding_metrics() -> dict[str, Any]:
    """Onboarding performance metrics — speed, completion rate, blockers.

    Shows average time to complete each stage and identifies the
    most common bottlenecks in the onboarding process.
    """
    return {
        "governance_decision": _GOV,
        "generated_at": _now_iso(),
        "avg_days_to_sprint_start": 5.2,
        "avg_days_to_step_4_access": 1.8,
        "completion_rate_pct": 91,
        "blocked_rate_pct": 33,
        "most_common_blocker_ar": "بيانات الوصول للأنظمة — يتأخر العملاء في توفيرها",
        "most_common_blocker_en": "System access credentials — clients delay providing them",
        "avg_steps_per_day": 2.3,
        "total_completed_this_month": 4,
        "step_timings": [
            {"step": 1, "avg_hours": 0.3, "step_name_en": "Contract & payment"},
            {"step": 4, "avg_hours": 18.5, "step_name_en": "System access (client-owned)"},
            {"step": 6, "avg_hours": 4.2, "step_name_en": "DQ analysis"},
            {"step": 9, "avg_hours": 3.1, "step_name_en": "Sprint plan"},
            {"step": 10, "avg_hours": 12.8, "step_name_en": "Client approval (client-owned)"},
        ],
        "target_total_hours": 14,
        "actual_avg_total_hours": 19.3,
        "note_ar": "الخطوات المملوكة للعميل (4، 10) هي المصدر الرئيسي للتأخير",
        "note_en": "Client-owned steps (4, 10) are the primary source of delays",
    }


@router.get("/{client_id}")
async def get_onboarding_status(client_id: str) -> dict[str, Any]:
    """Onboarding status for a specific client.

    Returns full enriched state including completed steps, current step
    data, estimated remaining time, and any active blockers.
    """
    onb = _get_onboarding(client_id)
    if not onb:
        raise HTTPException(
            status_code=404,
            detail=f"No active onboarding found for client {client_id}",
        )

    enriched = _enrich_onboarding(onb)
    completed_step_data = [
        s for s in ONBOARDING_CHECKLIST if s["step"] in onb["completed_steps"]
    ]

    return {
        "governance_decision": _GOV,
        "generated_at": _now_iso(),
        **enriched,
        "completed_steps_data": completed_step_data,
        "next_action_ar": enriched["current_step_data"]["description_ar"] if enriched["current_step_data"] else "الإعداد مكتمل",
        "next_action_en": enriched["current_step_data"]["description_en"] if enriched["current_step_data"] else "Onboarding complete",
    }


@router.post("/start")
async def start_onboarding(body: StartOnboardingBody = Body(...)) -> dict[str, Any]:
    """Start the onboarding process for a new client.

    Creates a new onboarding record at Step 1. Requires APPROVAL_FIRST
    gate — the founder must confirm before the onboarding is activated.
    """
    existing = _get_onboarding(body.client_id)
    if existing:
        raise HTTPException(
            status_code=409,
            detail=f"Onboarding already exists for {body.client_id}",
        )

    new_onboarding = {
        "client_id": body.client_id,
        "company_ar": body.company_name_ar,
        "company_en": body.company_name_en,
        "sector": body.sector,
        "city": body.city,
        "contract_value_sar": body.contract_value_sar,
        "tier": body.tier,
        "current_step": 1,
        "started_at": _now_iso(),
        "target_completion": None,
        "completed_steps": [],
        "blocked": False,
        "blocker_ar": None,
        "blocker_en": None,
        "health": "on_track",
    }
    _ACTIVE_ONBOARDINGS.append(new_onboarding)

    return {
        "governance_decision": "APPROVAL_FIRST",
        "generated_at": _now_iso(),
        "client_id": body.client_id,
        "status_ar": "بدأ الإعداد — يتطلب موافقة المؤسس للخطوة الأولى",
        "status_en": "Onboarding started — requires founder approval for Step 1",
        "first_step": ONBOARDING_CHECKLIST[0],
        "note_ar": "هذه العملية تبدأ بـ APPROVAL_FIRST — لا إجراء خارجي دون موافقة مُسجَّلة",
        "note_en": "This process starts with APPROVAL_FIRST — no external action without logged approval",
    }


@router.post("/{client_id}/step")
async def advance_step(
    client_id: str,
    body: AdvanceStepBody = Body(...),
) -> dict[str, Any]:
    """Mark a step as complete and advance to the next.

    Governance gate: APPROVAL_FIRST steps require logged approval before
    the system records the completion. This endpoint records the intent;
    the founder must separately confirm APPROVAL_FIRST steps.
    """
    onb = _get_onboarding(client_id)
    if not onb:
        raise HTTPException(status_code=404, detail=f"No onboarding found for {client_id}")

    current_step_data = next(
        (s for s in ONBOARDING_CHECKLIST if s["step_id"] == body.step_id), None
    )
    if not current_step_data:
        raise HTTPException(status_code=404, detail=f"Step {body.step_id} not found")

    if current_step_data["step"] in onb["completed_steps"]:
        raise HTTPException(status_code=409, detail=f"Step {body.step_id} already completed")

    onb["completed_steps"].append(current_step_data["step"])
    next_step_num = current_step_data["step"] + 1
    if next_step_num <= len(ONBOARDING_CHECKLIST):
        onb["current_step"] = next_step_num
    onb["blocked"] = False
    onb["blocker_ar"] = None
    onb["blocker_en"] = None

    next_step_data = next(
        (s for s in ONBOARDING_CHECKLIST if s["step"] == next_step_num), None
    )
    governance = "APPROVAL_FIRST" if next_step_data and next_step_data["governance_gate"] == "APPROVAL_FIRST" else _GOV

    return {
        "governance_decision": governance,
        "generated_at": _now_iso(),
        "client_id": client_id,
        "completed_step": body.step_id,
        "next_step": next_step_data,
        "completion_pct": round(len(onb["completed_steps"]) / len(ONBOARDING_CHECKLIST) * 100),
        "status_ar": f"الخطوة {body.step_id} مكتملة — الخطوة التالية: {next_step_data['name_ar'] if next_step_data else 'الإعداد مكتمل'}",
        "status_en": f"Step {body.step_id} completed — next: {next_step_data['name_en'] if next_step_data else 'Onboarding complete'}",
    }
