"""Renewal management framework for Dealix Saudi B2B client accounts.

All data is static; no LLM or external API calls are made.
All generated assessments carry a mandatory governance decision and must be
reviewed before acting on them.

Prefix: /api/v1/renewal-management
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel, Field

router = APIRouter(
    prefix="/api/v1/renewal-management",
    tags=["Sales"],
)

# ---------------------------------------------------------------------------
# Governance constants
# ---------------------------------------------------------------------------

_GOV_REVIEW = "ALLOW_WITH_REVIEW"
_GOV_APPROVAL = "APPROVAL_FIRST"

# ---------------------------------------------------------------------------
# Static data: renewal timeline milestones
# ---------------------------------------------------------------------------

_RENEWAL_TIMELINE: list[dict[str, Any]] = [
    {
        "order": 1,
        "weeks_before_renewal": 12,
        "milestone_en": "Health Check",
        "milestone_ar": "فحص الصحة",
        "owner_en": "Customer Success Manager",
        "owner_ar": "مدير نجاح العميل",
        "action_items_en": [
            "Review product adoption metrics and identify unused features.",
            "Survey champion NPS and flag any support issues.",
        ],
        "action_items_ar": [
            "مراجعة مقاييس اعتماد المنتج وتحديد الميزات غير المستخدمة.",
            "قياس صافي نقاط المروج للبطل ورصد أي مشكلات دعم.",
        ],
    },
    {
        "order": 2,
        "weeks_before_renewal": 8,
        "milestone_en": "Value Review",
        "milestone_ar": "مراجعة القيمة",
        "owner_en": "Customer Success Manager",
        "owner_ar": "مدير نجاح العميل",
        "action_items_en": [
            "Build a verified ROI summary comparing baseline to current outcomes.",
            "Identify upsell opportunities and add them to the renewal brief.",
        ],
        "action_items_ar": [
            "إعداد ملخص عائد على الاستثمار موثق يقارن خط الأساس بالنتائج الحالية.",
            "تحديد فرص البيع التصاعدي وإدراجها في ملف التجديد.",
        ],
    },
    {
        "order": 3,
        "weeks_before_renewal": 6,
        "milestone_en": "Renewal Proposal",
        "milestone_ar": "عرض التجديد",
        "owner_en": "Account Executive",
        "owner_ar": "مدير الحساب",
        "action_items_en": [
            "Send the renewal proposal with updated pricing and contract terms.",
            "Schedule a call with the economic buyer to walk through the proposal.",
        ],
        "action_items_ar": [
            "إرسال عرض التجديد مع التسعير المحدث وشروط العقد.",
            "جدولة مكالمة مع المشتري الاقتصادي لاستعراض العرض.",
        ],
    },
    {
        "order": 4,
        "weeks_before_renewal": 4,
        "milestone_en": "Negotiation",
        "milestone_ar": "التفاوض",
        "owner_en": "Account Executive",
        "owner_ar": "مدير الحساب",
        "action_items_en": [
            "Address commercial objections and document agreed concessions.",
            "Confirm legal and procurement requirements for contract execution.",
        ],
        "action_items_ar": [
            "معالجة الاعتراضات التجارية وتوثيق التنازلات المتفق عليها.",
            "تأكيد المتطلبات القانونية والمشتريات لتنفيذ العقد.",
        ],
    },
    {
        "order": 5,
        "weeks_before_renewal": 2,
        "milestone_en": "Close or Escalate",
        "milestone_ar": "الإغلاق أو التصعيد",
        "owner_en": "Account Executive",
        "owner_ar": "مدير الحساب",
        "action_items_en": [
            "Obtain signed contract or escalate to founder if at-risk.",
            "Log renewal outcome and trigger onboarding for expanded scope.",
        ],
        "action_items_ar": [
            "الحصول على العقد الموقع أو التصعيد للمؤسس إذا كان الحساب في خطر.",
            "تسجيل نتيجة التجديد وتفعيل إعداد النطاق الموسع.",
        ],
    },
]

# ---------------------------------------------------------------------------
# Static data: renewal risk thresholds
# ---------------------------------------------------------------------------

_RENEWAL_RISK_THRESHOLDS: dict[str, dict[str, Any]] = {
    "red": {
        "label_en": "At Risk",
        "label_ar": "في خطر",
        "nrr_below": 90,
        "health_score_below": 40,
        "action_en": "Escalate to founder. Launch retention intervention within 48 hours.",
        "action_ar": "التصعيد إلى المؤسس. إطلاق تدخل الاحتفاظ خلال 48 ساعة.",
    },
    "amber": {
        "label_en": "Needs Attention",
        "label_ar": "يحتاج إلى اهتمام",
        "nrr_below": 105,
        "health_score_below": 65,
        "action_en": "Schedule executive sponsor meeting and prepare flat-renewal offer.",
        "action_ar": "جدولة اجتماع الراعي التنفيذي وإعداد عرض تجديد مستوٍ.",
    },
    "green": {
        "label_en": "Healthy",
        "label_ar": "بصحة جيدة",
        "nrr_below": None,
        "health_score_below": None,
        "action_en": "Proceed with expansion conversation and upsell offer.",
        "action_ar": "المضي قدماً في محادثة التوسع وعرض البيع التصاعدي.",
    },
}

# ---------------------------------------------------------------------------
# Static data: upsell triggers at renewal
# ---------------------------------------------------------------------------

_UPSELL_TRIGGERS_AT_RENEWAL: list[dict[str, Any]] = [
    {
        "trigger_en": "Client has onboarded more than 20 users in the past 90 days",
        "trigger_ar": "أضاف العميل أكثر من 20 مستخدماً خلال الـ 90 يوماً الماضية",
        "upsell_path_en": "Propose team or enterprise tier upgrade.",
    },
    {
        "trigger_en": "Client has requested three or more custom integrations",
        "trigger_ar": "طلب العميل ثلاثة تكاملات مخصصة أو أكثر",
        "upsell_path_en": "Offer integration retainer or dedicated engineering hours.",
    },
    {
        "trigger_en": "Client has expanded into a new business unit since contract start",
        "trigger_ar": "توسع العميل في وحدة عمل جديدة منذ بداية العقد",
        "upsell_path_en": "Propose multi-entity or multi-region contract expansion.",
    },
    {
        "trigger_en": "Client NPS score is 8 or above from two consecutive surveys",
        "trigger_ar": "بلغ مؤشر NPS للعميل 8 أو أعلى في استطلاعين متتاليين",
        "upsell_path_en": "Request a case study and introduce referral incentive program.",
    },
]

# ---------------------------------------------------------------------------
# Pydantic models
# ---------------------------------------------------------------------------


class RenewalAssessmentInput(BaseModel):
    client_name: str
    current_arr_sar: float = Field(..., ge=0)
    contract_end_date: str
    nrr_pct: float = Field(..., ge=0)
    health_score: float = Field(..., ge=0, le=100)
    champion_engaged: bool = True
    decision_maker_met: bool = False
    has_open_support_issues: bool = False


# ---------------------------------------------------------------------------
# Pure-function core
# ---------------------------------------------------------------------------


def _assess_renewal(inp: RenewalAssessmentInput) -> dict[str, Any]:
    """Compute a renewal risk assessment and recommended ARR target.

    Returns a structured dict with risk_category, renewal_probability_pct,
    recommended_arr_target_sar, upsell_eligible, and governance decision.
    """
    if inp.nrr_pct < 90 or inp.health_score < 40:
        risk_category = "red"
    elif inp.nrr_pct < 105 or inp.health_score < 65:
        risk_category = "amber"
    else:
        risk_category = "green"

    risk_threshold_data = _RENEWAL_RISK_THRESHOLDS[risk_category]

    base_probability = {"green": 85, "amber": 60, "red": 30}[risk_category]
    probability = base_probability
    if inp.champion_engaged:
        probability += 5
    if inp.decision_maker_met:
        probability += 5
    if inp.has_open_support_issues:
        probability -= 10
    renewal_probability_pct = max(0, min(100, probability))

    arr_multiplier = {"green": 1.2, "amber": 1.0, "red": 0.9}[risk_category]
    recommended_arr_target_sar = inp.current_arr_sar * arr_multiplier

    upsell_eligible = risk_category == "green"

    return {
        "client_name": inp.client_name,
        "risk_category": risk_category,
        "risk_threshold_data": risk_threshold_data,
        "renewal_probability_pct": renewal_probability_pct,
        "recommended_arr_target_sar": recommended_arr_target_sar,
        "upsell_eligible": upsell_eligible,
        "governance_decision": _GOV_APPROVAL,
        "disclaimer_en": (
            "Renewal probability and ARR targets are estimates based on static thresholds. "
            "Validate against live CRM data and champion feedback before finalising."
        ),
        "disclaimer_ar": (
            "احتمالية التجديد وأهداف ARR تقديرية مبنية على حدود ثابتة. "
            "يُرجى التحقق من بيانات CRM الحية وملاحظات البطل قبل الاتفاق النهائي."
        ),
    }


# ---------------------------------------------------------------------------
# Router endpoints
# ---------------------------------------------------------------------------


@router.get("/timeline", summary="All 5 renewal timeline milestones")
def get_timeline() -> dict[str, Any]:
    """Return all renewal timeline milestones with bilingual labels and action items."""
    return {
        "timeline": _RENEWAL_TIMELINE,
        "total_milestones": len(_RENEWAL_TIMELINE),
        "governance_decision": _GOV_REVIEW,
    }


@router.get("/upsell-triggers", summary="All 4 upsell triggers at renewal")
def get_upsell_triggers() -> dict[str, Any]:
    """Return all upsell triggers with bilingual descriptions and upsell paths."""
    return {
        "upsell_triggers": _UPSELL_TRIGGERS_AT_RENEWAL,
        "total_triggers": len(_UPSELL_TRIGGERS_AT_RENEWAL),
        "governance_decision": _GOV_REVIEW,
    }


@router.post("/assess", summary="Assess renewal risk and recommend ARR target")
def assess_renewal(body: RenewalAssessmentInput) -> dict[str, Any]:
    """Accept client renewal data and return a structured risk assessment.

    Governance decision: APPROVAL_FIRST.
    """
    return _assess_renewal(body)
