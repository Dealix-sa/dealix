"""Pipeline velocity benchmarks and deal stall analysis for Dealix Saudi B2B.

All data is static; no LLM or external API calls are made.
All generated analyses carry a mandatory governance decision and must be
reviewed before acting on them.

Prefix: /api/v1/pipeline-velocity
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter(
    prefix="/api/v1/pipeline-velocity",
    tags=["Analytics"],
)

# ---------------------------------------------------------------------------
# Governance constants
# ---------------------------------------------------------------------------

_GOV_REVIEW = "ALLOW_WITH_REVIEW"
_GOV_APPROVAL = "APPROVAL_FIRST"

# ---------------------------------------------------------------------------
# Static data: stage velocity benchmarks
# ---------------------------------------------------------------------------

_STAGE_VELOCITY_BENCHMARKS: list[dict[str, Any]] = [
    {
        "stage_id": "discovery",
        "stage_name_en": "Discovery",
        "stage_name_ar": "الاكتشاف",
        "benchmark_days": 7,
        "stall_threshold_days": 14,
        "exit_criteria_en": "Pain confirmed, key stakeholders identified, budget range established.",
        "exit_criteria_ar": "تأكيد الألم وتحديد أصحاب المصلحة الرئيسيين وتحديد نطاق الميزانية.",
    },
    {
        "stage_id": "qualification",
        "stage_name_en": "Qualification",
        "stage_name_ar": "التأهيل",
        "benchmark_days": 5,
        "stall_threshold_days": 10,
        "exit_criteria_en": "BANT confirmed: budget, authority, need, and timeline all validated.",
        "exit_criteria_ar": "تأكيد BANT: التحقق من الميزانية والصلاحية والحاجة والجدول الزمني.",
    },
    {
        "stage_id": "demo",
        "stage_name_en": "Demo",
        "stage_name_ar": "العرض التوضيحي",
        "benchmark_days": 7,
        "stall_threshold_days": 14,
        "exit_criteria_en": "Demo delivered, follow-up questions answered, champion engaged.",
        "exit_criteria_ar": "تقديم العرض والإجابة على أسئلة المتابعة وتفاعل البطل الداخلي.",
    },
    {
        "stage_id": "proposal",
        "stage_name_en": "Proposal",
        "stage_name_ar": "العرض",
        "benchmark_days": 10,
        "stall_threshold_days": 20,
        "exit_criteria_en": "Proposal submitted, pricing reviewed, decision criteria clarified.",
        "exit_criteria_ar": "تقديم العرض ومراجعة التسعير وتوضيح معايير القرار.",
    },
    {
        "stage_id": "negotiation",
        "stage_name_en": "Negotiation",
        "stage_name_ar": "التفاوض",
        "benchmark_days": 14,
        "stall_threshold_days": 28,
        "exit_criteria_en": "Terms agreed, legal review completed, verbal commitment received.",
        "exit_criteria_ar": "الاتفاق على الشروط وإتمام المراجعة القانونية والحصول على التزام شفهي.",
    },
    {
        "stage_id": "closed",
        "stage_name_en": "Closed",
        "stage_name_ar": "مغلق",
        "benchmark_days": 3,
        "stall_threshold_days": 7,
        "exit_criteria_en": "Contract signed, payment received, onboarding scheduled.",
        "exit_criteria_ar": "توقيع العقد واستلام الدفعة وجدولة الإعداد.",
    },
]

_VALID_STAGES: set[str] = {s["stage_id"] for s in _STAGE_VELOCITY_BENCHMARKS}

# ---------------------------------------------------------------------------
# Static data: pipeline health signals
# ---------------------------------------------------------------------------

_PIPELINE_HEALTH_SIGNALS: list[dict[str, Any]] = [
    {
        "signal_en": "No activity logged for more than 7 days",
        "signal_ar": "لم يُسجَّل أي نشاط منذ أكثر من 7 أيام",
        "action_en": "Send a brief check-in message and log the outreach.",
        "action_ar": "أرسل رسالة متابعة قصيرة وسجّل التواصل.",
    },
    {
        "signal_en": "Deal has been in the same stage longer than the stall threshold",
        "signal_ar": "الصفقة في المرحلة ذاتها لفترة تتجاوز حد التوقف",
        "action_en": "Review blockers with the champion and escalate if needed.",
        "action_ar": "راجع العوائق مع البطل الداخلي وصعّد الأمر إذا لزم.",
    },
    {
        "signal_en": "No identified internal champion for the deal",
        "signal_ar": "لا يوجد بطل داخلي محدد للصفقة",
        "action_en": "Map the org chart and identify a potential champion immediately.",
        "action_ar": "ارسم هيكل المنظمة وحدد بطلاً محتملاً على الفور.",
    },
    {
        "signal_en": "Deal value is high but qualification has not been completed",
        "signal_ar": "قيمة الصفقة مرتفعة لكن عملية التأهيل لم تكتمل",
        "action_en": "Prioritise a qualification call before investing further resources.",
        "action_ar": "أعطِ الأولوية لمكالمة تأهيل قبل استثمار موارد إضافية.",
    },
    {
        "signal_en": "Proposal submitted more than two weeks ago with no feedback",
        "signal_ar": "قُدِّم العرض منذ أكثر من أسبوعين دون أي ملاحظات",
        "action_en": "Request a 15-minute call to gather feedback and address concerns.",
        "action_ar": "اطلب مكالمة مدتها 15 دقيقة لجمع الملاحظات ومعالجة المخاوف.",
    },
]

# ---------------------------------------------------------------------------
# Pydantic models
# ---------------------------------------------------------------------------


class DealVelocityInput(BaseModel):
    deal_name: str
    stage: str
    days_in_stage: int = Field(..., ge=0)
    deal_value_sar: float = Field(..., ge=0)
    has_champion: bool = False
    last_activity_days_ago: int = Field(..., ge=0)


# ---------------------------------------------------------------------------
# Pure-function core
# ---------------------------------------------------------------------------


def _analyze_velocity(inp: DealVelocityInput) -> dict[str, Any]:
    """Compute a velocity analysis for a deal in a given pipeline stage.

    Returns a structured dict with velocity_status, urgency_score,
    days_over_benchmark, recommended actions, and governance decision.
    """
    if inp.stage not in _VALID_STAGES:
        raise HTTPException(
            status_code=422,
            detail=f"Invalid stage '{inp.stage}'. Must be one of: {sorted(_VALID_STAGES)}",
        )

    benchmark = next(s for s in _STAGE_VELOCITY_BENCHMARKS if s["stage_id"] == inp.stage)
    benchmark_days: int = benchmark["benchmark_days"]
    stall_threshold_days: int = benchmark["stall_threshold_days"]

    if inp.days_in_stage <= benchmark_days:
        velocity_status = "on_track"
    elif inp.days_in_stage <= stall_threshold_days:
        velocity_status = "slow"
    else:
        velocity_status = "stalled"

    days_over_benchmark = max(0, inp.days_in_stage - benchmark_days)

    base = min(inp.days_in_stage / stall_threshold_days * 60, 60)
    urgency_score = base
    if inp.last_activity_days_ago > 7:
        urgency_score += 20
    if not inp.has_champion:
        urgency_score += 20
    urgency_score = min(int(urgency_score), 100)

    if velocity_status == "stalled":
        recommended_action_en = "Escalate: request senior sponsor meeting immediately"
        recommended_action_ar = "تصعيد: اطلب اجتماع الراعي الكبير فورًا"
    elif velocity_status == "slow":
        recommended_action_en = "Accelerate: schedule next step within 48 hours"
        recommended_action_ar = "تسريع: جدولة الخطوة التالية خلال 48 ساعة"
    else:
        recommended_action_en = "Maintain: follow up per standard cadence"
        recommended_action_ar = "استمرار: المتابعة وفق الجدول الزمني المعتاد"

    return {
        "deal_name": inp.deal_name,
        "velocity_status": velocity_status,
        "days_over_benchmark": days_over_benchmark,
        "urgency_score": urgency_score,
        "recommended_action_en": recommended_action_en,
        "recommended_action_ar": recommended_action_ar,
        "governance_decision": _GOV_REVIEW,
    }


# ---------------------------------------------------------------------------
# Router endpoints
# ---------------------------------------------------------------------------


@router.get("/benchmarks", summary="All 6 stage velocity benchmarks")
def get_benchmarks() -> dict[str, Any]:
    """Return all stage velocity benchmarks with bilingual labels and thresholds."""
    return {
        "benchmarks": _STAGE_VELOCITY_BENCHMARKS,
        "total_stages": len(_STAGE_VELOCITY_BENCHMARKS),
        "governance_decision": _GOV_REVIEW,
    }


@router.get("/health-signals", summary="All 5 pipeline health signals")
def get_health_signals() -> dict[str, Any]:
    """Return all pipeline health signals with bilingual labels and actions."""
    return {
        "signals": _PIPELINE_HEALTH_SIGNALS,
        "total_signals": len(_PIPELINE_HEALTH_SIGNALS),
        "governance_decision": _GOV_REVIEW,
    }


@router.post("/analyze", summary="Analyze deal velocity for a given stage")
def analyze_deal_velocity(body: DealVelocityInput) -> dict[str, Any]:
    """Accept deal data and return a structured velocity analysis.

    Governance decision: ALLOW_WITH_REVIEW.
    """
    return _analyze_velocity(body)
