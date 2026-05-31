"""Retention risk assessment, churn factors, and playbooks for Dealix Saudi B2B clients.

All data is static; no LLM or external API calls are made.
All generated assessments carry a mandatory governance decision and must be
reviewed and approved before sharing with any client.

Prefix: /api/v1/retention-risk
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel, Field

router = APIRouter(
    prefix="/api/v1/retention-risk",
    tags=["Analytics"],
)

# ---------------------------------------------------------------------------
# Governance constants
# ---------------------------------------------------------------------------

_GOV_REVIEW = "ALLOW_WITH_REVIEW"
_GOV_APPROVAL = "APPROVAL_FIRST"

_DISCLAIMER_EN = (
    "This retention risk assessment is a draft generated from inputs provided. "
    "All scores, labels, and recommended actions are estimates and must be "
    "reviewed and confirmed by the customer success team before acting on them."
)
_DISCLAIMER_AR = (
    "تقييم مخاطر الاحتفاظ هذا مسودة أُنشئت استناداً إلى المدخلات المقدمة. "
    "جميع الدرجات والتصنيفات والإجراءات الموصى بها تقديرية ويجب على فريق نجاح "
    "العملاء مراجعتها وتأكيدها قبل اتخاذ أي إجراء."
)

# ---------------------------------------------------------------------------
# Static data: churn risk factors
# ---------------------------------------------------------------------------

_CHURN_RISK_FACTORS: list[dict[str, Any]] = [
    {
        "factor_id": "low_usage",
        "factor_en": "Low platform usage",
        "factor_ar": "انخفاض استخدام المنصة",
        "weight": 20,
    },
    {
        "factor_id": "champion_left",
        "factor_en": "Internal champion has left the company",
        "factor_ar": "غادر البطل الداخلي الشركة",
        "weight": 20,
    },
    {
        "factor_id": "missed_payments",
        "factor_en": "Missed or late payments on record",
        "factor_ar": "سجل مدفوعات فائتة أو متأخرة",
        "weight": 15,
    },
    {
        "factor_id": "no_expansion",
        "factor_en": "No account expansion in over 6 months",
        "factor_ar": "لا توسع في الحساب منذ أكثر من 6 أشهر",
        "weight": 10,
    },
    {
        "factor_id": "low_nps",
        "factor_en": "Low NPS score (below 8)",
        "factor_ar": "درجة NPS منخفضة (أقل من 8)",
        "weight": 15,
    },
    {
        "factor_id": "support_escalations",
        "factor_en": "Multiple support escalations in the last 90 days",
        "factor_ar": "تصعيدات دعم متعددة في آخر 90 يوماً",
        "weight": 10,
    },
    {
        "factor_id": "competitor_engaged",
        "factor_en": "Client is actively evaluating a competitor",
        "factor_ar": "العميل يقيّم منافساً بشكل نشط",
        "weight": 5,
    },
    {
        "factor_id": "contract_expiring_soon",
        "factor_en": "Contract is expiring within 90 days",
        "factor_ar": "العقد على وشك الانتهاء خلال 90 يوماً",
        "weight": 5,
    },
]

# ---------------------------------------------------------------------------
# Static data: retention playbooks
# ---------------------------------------------------------------------------

_RETENTION_PLAYBOOKS: dict[str, dict[str, Any]] = {
    "red": {
        "label_en": "At-Risk — Immediate Intervention Required",
        "label_ar": "في خطر — تدخل فوري مطلوب",
        "actions_en": [
            "Schedule an emergency executive sponsor call within 48 hours.",
            "Prepare a tailored recovery plan addressing the top two risk factors.",
            "Offer a structured success review and updated value narrative.",
        ],
        "actions_ar": [
            "جدولة مكالمة طارئة مع الراعي التنفيذي خلال 48 ساعة.",
            "إعداد خطة تعافٍ مخصصة تعالج أبرز عاملَي خطر.",
            "تقديم مراجعة نجاح منظمة وسرد قيمة محدَّث.",
        ],
    },
    "amber": {
        "label_en": "Watch — Proactive Engagement Needed",
        "label_ar": "مراقبة — مشاركة استباقية مطلوبة",
        "actions_en": [
            "Schedule a proactive check-in call with the client champion within two weeks.",
            "Share a usage report and highlight unrealised value opportunities.",
            "Introduce the next feature or module relevant to the client's use case.",
        ],
        "actions_ar": [
            "جدولة مكالمة متابعة استباقية مع بطل العميل خلال أسبوعين.",
            "مشاركة تقرير الاستخدام وإبراز فرص القيمة غير المحققة.",
            "تقديم الميزة أو الوحدة التالية ذات الصلة بحالة استخدام العميل.",
        ],
    },
    "green": {
        "label_en": "Healthy — Maintain Momentum",
        "label_ar": "سليم — الحفاظ على الزخم",
        "actions_en": [
            "Send a quarterly success summary and celebrate key wins with the client.",
            "Introduce an expansion conversation using positive signals as entry points.",
            "Request a referral or case study from the satisfied client.",
        ],
        "actions_ar": [
            "إرسال ملخص نجاح ربعي والاحتفال بالإنجازات الرئيسية مع العميل.",
            "بدء محادثة التوسع باستخدام الإشارات الإيجابية كنقاط دخول.",
            "طلب إحالة أو دراسة حالة من العميل الراضي.",
        ],
    },
}

# ---------------------------------------------------------------------------
# Static data: early warning indicators
# ---------------------------------------------------------------------------

_EARLY_WARNING_INDICATORS: list[dict[str, Any]] = [
    {
        "indicator_en": "Login frequency drops by 30% or more over 30 days",
        "indicator_ar": "انخفاض تكرار تسجيل الدخول بنسبة 30% أو أكثر خلال 30 يوماً",
        "detection_method_en": "Monitor weekly active user counts from platform analytics.",
    },
    {
        "indicator_en": "Support ticket volume doubles compared to prior quarter",
        "indicator_ar": "تضاعف حجم تذاكر الدعم مقارنةً بالربع السابق",
        "detection_method_en": "Track support ticket volume trend from the helpdesk system.",
    },
    {
        "indicator_en": "NPS score falls below 7 in the last survey",
        "indicator_ar": "انخفاض درجة NPS دون 7 في آخر استطلاع",
        "detection_method_en": "Review NPS survey responses after each quarterly check-in.",
    },
    {
        "indicator_en": "Primary contact stops responding to emails or calls",
        "indicator_ar": "توقف جهة الاتصال الرئيسية عن الرد على الرسائل والمكالمات",
        "detection_method_en": "Flag unresponsive accounts in CRM after two missed follow-ups.",
    },
    {
        "indicator_en": "Client requests a contract review or pricing negotiation outside renewal cycle",
        "indicator_ar": "طلب العميل مراجعة العقد أو التفاوض على الأسعار خارج دورة التجديد",
        "detection_method_en": "Log contract-related client requests in the account notes.",
    },
]

# ---------------------------------------------------------------------------
# Pydantic models
# ---------------------------------------------------------------------------


class RetentionRiskInput(BaseModel):
    client_name: str
    usage_score: float = Field(..., ge=0, le=100)
    nps_score: float = Field(..., ge=0, le=10)
    months_since_last_expansion: int = Field(..., ge=0)
    support_escalations_last_90d: int = Field(..., ge=0)
    champion_left: bool = False
    missed_payments: bool = False
    contract_expiring_within_90d: bool = False
    competitor_engaged: bool = False


# ---------------------------------------------------------------------------
# Pure-function core
# ---------------------------------------------------------------------------


def _assess_retention_risk(inp: RetentionRiskInput) -> dict[str, Any]:
    """Compute a retention risk assessment from validated input.

    Returns a structured dict with risk score, label, recommended playbook,
    top risk factors, and disclaimers.
    """
    risk_score = 0
    top_risk_factors: list[str] = []

    # low_usage
    if inp.usage_score < 40:
        risk_score += 20
        top_risk_factors.append("low_usage")
    elif inp.usage_score < 60:
        risk_score += 10
        top_risk_factors.append("low_usage")

    # champion_left
    if inp.champion_left:
        risk_score += 20
        top_risk_factors.append("champion_left")

    # missed_payments
    if inp.missed_payments:
        risk_score += 15
        top_risk_factors.append("missed_payments")

    # no_expansion
    if inp.months_since_last_expansion > 6:
        risk_score += 10
        top_risk_factors.append("no_expansion")

    # low_nps
    if inp.nps_score < 7:
        risk_score += 15
        top_risk_factors.append("low_nps")
    elif inp.nps_score < 8:
        risk_score += 7
        top_risk_factors.append("low_nps")

    # support_escalations
    escalation_contribution = min(inp.support_escalations_last_90d * 3, 10)
    if escalation_contribution > 0:
        risk_score += escalation_contribution
        top_risk_factors.append("support_escalations")

    # competitor_engaged
    if inp.competitor_engaged:
        risk_score += 5
        top_risk_factors.append("competitor_engaged")

    # contract_expiring_soon
    if inp.contract_expiring_within_90d:
        risk_score += 5
        top_risk_factors.append("contract_expiring_soon")

    risk_score = min(risk_score, 100)

    if risk_score >= 60:
        risk_label = "red"
    elif risk_score >= 30:
        risk_label = "amber"
    else:
        risk_label = "green"

    return {
        "client_name": inp.client_name,
        "risk_score": risk_score,
        "risk_label": risk_label,
        "playbook": _RETENTION_PLAYBOOKS[risk_label],
        "top_risk_factors": top_risk_factors,
        "disclaimer_en": _DISCLAIMER_EN,
        "disclaimer_ar": _DISCLAIMER_AR,
        "governance_decision": _GOV_APPROVAL,
    }


# ---------------------------------------------------------------------------
# Router endpoints
# ---------------------------------------------------------------------------


@router.get("/risk-factors", summary="All 8 churn risk factors")
def get_risk_factors() -> dict[str, Any]:
    """Return all churn risk factors with bilingual labels, weights, and total weight."""
    return {
        "risk_factors": _CHURN_RISK_FACTORS,
        "total_weight": sum(f["weight"] for f in _CHURN_RISK_FACTORS),
        "governance_decision": _GOV_REVIEW,
    }


@router.get("/early-warning-indicators", summary="All 5 early warning indicators")
def get_early_warning_indicators() -> dict[str, Any]:
    """Return all early warning indicators with bilingual labels and detection methods."""
    return {
        "indicators": _EARLY_WARNING_INDICATORS,
        "total_indicators": len(_EARLY_WARNING_INDICATORS),
        "governance_decision": _GOV_REVIEW,
    }


@router.post("/assess", summary="Assess retention risk for an account")
def assess_retention_risk(body: RetentionRiskInput) -> dict[str, Any]:
    """Accept account data and return a structured retention risk assessment.

    Governance decision: APPROVAL_FIRST.
    """
    return _assess_retention_risk(body)
