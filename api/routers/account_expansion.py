"""Account expansion signals, playbooks, and assessment for Dealix Saudi B2B clients.

All data is static; no LLM or external API calls are made.
All generated assessments carry a mandatory governance decision and must be
reviewed and approved before sharing with any client.

Prefix: /api/v1/account-expansion
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter(
    prefix="/api/v1/account-expansion",
    tags=["Sales"],
)

# ---------------------------------------------------------------------------
# Governance constants
# ---------------------------------------------------------------------------

_GOV_REVIEW = "ALLOW_WITH_REVIEW"
_GOV_APPROVAL = "APPROVAL_FIRST"

# ---------------------------------------------------------------------------
# Static data: expansion signals
# ---------------------------------------------------------------------------

_EXPANSION_SIGNALS: list[dict[str, Any]] = [
    {
        "signal_id": "high_usage_rate",
        "signal_en": "High platform usage rate",
        "signal_ar": "معدل استخدام مرتفع للمنصة",
        "weight": 30,
        "trigger_action_en": "Schedule executive business review to discuss expansion modules.",
        "trigger_action_ar": "جدولة مراجعة أعمال تنفيذية لمناقشة وحدات التوسع.",
    },
    {
        "signal_id": "champion_promotion",
        "signal_en": "Internal champion received a promotion",
        "signal_ar": "حصل البطل الداخلي على ترقية",
        "weight": 25,
        "trigger_action_en": "Re-engage promoted champion with updated value narrative and expanded proposal.",
        "trigger_action_ar": "إعادة التواصل مع البطل المُرقَّى بسرد قيمة محدَّث واقتراح موسَّع.",
    },
    {
        "signal_id": "new_budget_cycle",
        "signal_en": "Client is entering a new budget cycle",
        "signal_ar": "العميل على وشك دخول دورة ميزانية جديدة",
        "weight": 15,
        "trigger_action_en": "Present ROI summary and expansion proposal before budget is allocated.",
        "trigger_action_ar": "تقديم ملخص عائد الاستثمار ومقترح التوسع قبل تخصيص الميزانية.",
    },
    {
        "signal_id": "positive_nps",
        "signal_en": "NPS score at or above 8 out of 10",
        "signal_ar": "درجة NPS تساوي 8 أو أكثر من 10",
        "weight": 20,
        "trigger_action_en": "Request a referral and introduce the next tier of services.",
        "trigger_action_ar": "طلب إحالة وتقديم المستوى التالي من الخدمات.",
    },
    {
        "signal_id": "team_growth",
        "signal_en": "Client team has grown significantly",
        "signal_ar": "نما فريق العميل بشكل ملحوظ",
        "weight": 10,
        "trigger_action_en": "Propose seat expansion and onboarding support for new team members.",
        "trigger_action_ar": "اقتراح توسيع المقاعد ودعم الإعداد لأعضاء الفريق الجدد.",
    },
    {
        "signal_id": "zatca_phase_expansion",
        "signal_en": "Client is entering a new ZATCA compliance phase",
        "signal_ar": "العميل على وشك الدخول في مرحلة امتثال جديدة لهيئة الزكاة والضريبة والجمارك",
        "weight": 20,
        "trigger_action_en": "Lead with ZATCA readiness assessment and relevant compliance module upsell.",
        "trigger_action_ar": "البدء بتقييم جاهزية هيئة الزكاة وعرض وحدة الامتثال ذات الصلة.",
    },
]

# ---------------------------------------------------------------------------
# Static data: expansion playbooks
# ---------------------------------------------------------------------------

_EXPANSION_PLAYBOOKS: dict[str, dict[str, Any]] = {
    "upsell_tier": {
        "name_en": "Tier Upsell Playbook",
        "name_ar": "دليل ترقية المستوى",
        "steps_en": [
            "Prepare a tailored ROI summary showing value delivered at the current tier.",
            "Present a side-by-side comparison of current and next-tier capabilities.",
            "Obtain internal sponsor sign-off before sending the commercial proposal.",
        ],
        "steps_ar": [
            "إعداد ملخص عائد استثمار مخصص يوضح القيمة المحققة في المستوى الحالي.",
            "تقديم مقارنة جانبية بين قدرات المستوى الحالي والمستوى التالي.",
            "الحصول على موافقة الراعي الداخلي قبل إرسال المقترح التجاري.",
        ],
    },
    "cross_sell_module": {
        "name_en": "Cross-Sell Module Playbook",
        "name_ar": "دليل بيع الوحدات الإضافية",
        "steps_en": [
            "Identify the highest-value unactivated module based on client use case.",
            "Run a 30-minute demo focused on the client's specific pain point.",
            "Propose a pilot period with defined success criteria before full activation.",
        ],
        "steps_ar": [
            "تحديد الوحدة غير المُفعَّلة ذات أعلى قيمة بناءً على حالة استخدام العميل.",
            "تقديم عرض توضيحي مدته 30 دقيقة يركز على نقطة الألم المحددة للعميل.",
            "اقتراح فترة تجريبية بمعايير نجاح محددة قبل التفعيل الكامل.",
        ],
    },
    "seat_expansion": {
        "name_en": "Seat Expansion Playbook",
        "name_ar": "دليل توسيع المقاعد",
        "steps_en": [
            "Audit current usage data to identify under-licensed teams or departments.",
            "Present a per-seat cost comparison against productivity gains.",
            "Coordinate with client IT and procurement to streamline the expansion process.",
        ],
        "steps_ar": [
            "مراجعة بيانات الاستخدام الحالية لتحديد الفرق أو الأقسام غير المرخصة بالكامل.",
            "تقديم مقارنة تكلفة المقعد الواحد مقابل مكاسب الإنتاجية.",
            "التنسيق مع تقنية المعلومات والمشتريات لدى العميل لتبسيط عملية التوسع.",
        ],
    },
}

# ---------------------------------------------------------------------------
# Valid tiers
# ---------------------------------------------------------------------------

_VALID_ACCOUNT_TIERS: set[str] = {"standard", "growth", "strategic"}

# ---------------------------------------------------------------------------
# Pydantic models
# ---------------------------------------------------------------------------


class ExpansionAssessmentInput(BaseModel):
    client_name: str
    current_tier: str
    mrr_sar: float = Field(..., ge=0)
    usage_score: float = Field(..., ge=0, le=100)
    nps_score: float = Field(..., ge=0, le=10)
    months_as_customer: int = Field(..., ge=1)
    champion_promoted: bool = False
    new_budget_cycle: bool = False


# ---------------------------------------------------------------------------
# Pure-function core
# ---------------------------------------------------------------------------


def _assess_expansion(inp: ExpansionAssessmentInput) -> dict[str, Any]:
    """Compute an expansion assessment from validated input.

    Raises HTTPException 422 if current_tier is not a valid value.
    Returns a structured dict with score, label, recommended playbook,
    top signals, and next MRR target.
    """
    if inp.current_tier not in _VALID_ACCOUNT_TIERS:
        raise HTTPException(
            status_code=422,
            detail={
                "error": f"Invalid current_tier '{inp.current_tier}'.",
                "valid_values": sorted(_VALID_ACCOUNT_TIERS),
                "governance_decision": _GOV_REVIEW,
            },
        )

    # Score computation
    usage_component = inp.usage_score * 0.3
    nps_component = inp.nps_score * 10 * 0.2
    tenure_component = min(inp.months_as_customer / 12, 1) * 100 * 0.2
    champion_component = 25.0 if inp.champion_promoted else 0.0
    budget_component = 15.0 if inp.new_budget_cycle else 0.0

    expansion_score = round(
        usage_component + nps_component + tenure_component + champion_component + budget_component,
        2,
    )

    if expansion_score >= 70:
        expansion_label = "high"
        recommended_playbook = "upsell_tier"
        mrr_multiplier = 1.3
    elif expansion_score >= 40:
        expansion_label = "medium"
        recommended_playbook = "cross_sell_module"
        mrr_multiplier = 1.15
    else:
        expansion_label = "low"
        recommended_playbook = "seat_expansion"
        mrr_multiplier = 1.05

    # Top signals that apply
    top_signals: list[str] = []
    if inp.usage_score >= 75:
        top_signals.append("high_usage_rate")
    if inp.champion_promoted:
        top_signals.append("champion_promotion")
    if inp.new_budget_cycle:
        top_signals.append("new_budget_cycle")
    if inp.nps_score >= 8:
        top_signals.append("positive_nps")

    next_mrr_target_sar = round(inp.mrr_sar * mrr_multiplier, 2)

    return {
        "client_name": inp.client_name,
        "expansion_score": expansion_score,
        "expansion_label": expansion_label,
        "recommended_playbook": recommended_playbook,
        "top_signals": top_signals,
        "next_mrr_target_sar": next_mrr_target_sar,
        "governance_decision": _GOV_APPROVAL,
    }


# ---------------------------------------------------------------------------
# Router endpoints
# ---------------------------------------------------------------------------


@router.get("/signals", summary="All 6 expansion signal definitions")
def get_signals() -> dict[str, Any]:
    """Return all expansion signal definitions with bilingual labels and trigger actions."""
    return {
        "signals": _EXPANSION_SIGNALS,
        "total_signals": len(_EXPANSION_SIGNALS),
        "governance_decision": _GOV_REVIEW,
    }


@router.get("/playbooks", summary="All 3 expansion playbooks")
def get_playbooks() -> dict[str, Any]:
    """Return all expansion playbooks with bilingual names and steps."""
    return {
        "playbooks": _EXPANSION_PLAYBOOKS,
        "governance_decision": _GOV_REVIEW,
    }


@router.post("/assess", summary="Assess expansion readiness for an account")
def assess_expansion(body: ExpansionAssessmentInput) -> dict[str, Any]:
    """Accept account data and return a structured expansion assessment.

    Governance decision: APPROVAL_FIRST.
    """
    return _assess_expansion(body)
