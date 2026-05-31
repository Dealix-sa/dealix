"""Saudi Revenue Advisor — Saudi-market-specific B2B revenue guidance.

Public read-only endpoints (no auth required — lead-gen tool).
All pricing data carries the mandatory estimate disclaimer.

Prefix: /api/v1/saudi-revenue-advisor
"""

from __future__ import annotations

import logging
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict, Field

log = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/v1/saudi-revenue-advisor",
    tags=["Analytics"],
)

# Mandatory disclaimer on every pricing response.
_DISCLAIMER_AR = "هذه تقديرات — ليست ضمانات"
_DISCLAIMER_EN = "These are estimates — not guarantees"

# ---------------------------------------------------------------------------
# Static data: pricing guidance per sector
# ---------------------------------------------------------------------------

_PRICING_GUIDANCE: dict[str, dict[str, Any]] = {
    "b2b_saas": {
        "min_sar": 2_000,
        "max_sar": 25_000,
        "avg_sar": 8_000,
        "pricing_model": "monthly_retainer",
        "justification_ar": (
            "برمجيات B2B السحابية تُسعَّر شهرياً بناءً على عدد المستخدمين أو الاستهلاك."
        ),
        "justification_en": (
            "B2B SaaS is priced monthly based on seats or usage tiers."
        ),
    },
    "agency": {
        "min_sar": 5_000,
        "max_sar": 40_000,
        "avg_sar": 15_000,
        "pricing_model": "monthly_retainer",
        "justification_ar": (
            "وكالات التسويق والاستشارات تتقاضى رسوماً شهرية ثابتة مع نطاق عمل محدد."
        ),
        "justification_en": (
            "Marketing and consulting agencies charge a fixed monthly retainer with a defined scope."
        ),
    },
    "healthcare_clinic": {
        "min_sar": 3_000,
        "max_sar": 20_000,
        "avg_sar": 7_500,
        "pricing_model": "monthly_retainer",
        "justification_ar": (
            "العيادات الصحية تحتاج حلولاً مخصصة للامتثال وإدارة المرضى بتكلفة شهرية ثابتة."
        ),
        "justification_en": (
            "Healthcare clinics require tailored compliance and patient-management "
            "solutions with predictable monthly costs."
        ),
    },
    "real_estate": {
        "min_sar": 4_000,
        "max_sar": 30_000,
        "avg_sar": 12_000,
        "pricing_model": "monthly_retainer",
        "justification_ar": (
            "شركات العقارات تتبنى نماذج شهرية لأدوات الإيرادات وإدارة العملاء."
        ),
        "justification_en": (
            "Real-estate firms adopt monthly models for revenue tooling and client management."
        ),
    },
    "logistics": {
        "min_sar": 3_500,
        "max_sar": 22_000,
        "avg_sar": 9_000,
        "pricing_model": "monthly_retainer",
        "justification_ar": (
            "شركات اللوجستيات تُفضّل الدفع الشهري المرتبط بحجم العمليات."
        ),
        "justification_en": (
            "Logistics companies prefer monthly billing tied to operational volume."
        ),
    },
    "fintech": {
        "min_sar": 8_000,
        "max_sar": 60_000,
        "avg_sar": 22_000,
        "pricing_model": "monthly_retainer",
        "justification_ar": (
            "الشركات التقنية المالية تدفع أسعاراً مرتفعة نظراً لمتطلبات الامتثال التنظيمي."
        ),
        "justification_en": (
            "Fintech firms pay premium rates driven by regulatory compliance requirements."
        ),
    },
    "engineering": {
        "min_sar": 5_000,
        "max_sar": 35_000,
        "avg_sar": 13_000,
        "pricing_model": "monthly_retainer",
        "justification_ar": (
            "شركات الهندسة والمقاولات تتعاقد بشكل شهري على حلول إدارة المشاريع والإيرادات."
        ),
        "justification_en": (
            "Engineering and contracting firms engage on monthly contracts for project "
            "and revenue-management solutions."
        ),
    },
}

# ---------------------------------------------------------------------------
# Static data: deal velocity per sector
# ---------------------------------------------------------------------------

_DEAL_VELOCITY: dict[str, dict[str, Any]] = {
    "b2b_saas": {
        "avg_days_to_close": 21,
        "typical_decision_makers": ["CTO", "CEO", "Head of Product"],
        "top_objections": [
            "التكلفة مرتفعة / Cost is high",
            "نحتاج وقتاً لمراجعة الميزانية / Need time to review budget",
            "لدينا حل داخلي / We have an internal solution",
        ],
        "success_factors": [
            "Demo tailored to their existing workflow",
            "ROI proof from a comparable company",
            "Trial period offer",
        ],
    },
    "agency": {
        "avg_days_to_close": 14,
        "typical_decision_makers": ["Founder", "CEO", "Marketing Director"],
        "top_objections": [
            "لدينا وكالة حالياً / We already have an agency",
            "النتائج غير مضمونة / Results are not guaranteed",
            "الميزانية محدودة / Budget is limited",
        ],
        "success_factors": [
            "Portfolio of sector-specific case studies",
            "Clear deliverables timeline",
            "Flexible contract length",
        ],
    },
    "healthcare_clinic": {
        "avg_days_to_close": 30,
        "typical_decision_makers": ["Clinic Director", "CFO", "Operations Manager"],
        "top_objections": [
            "متطلبات الامتثال معقدة / Compliance requirements are complex",
            "الموظفون يحتاجون تدريباً / Staff need training",
            "التكامل مع الأنظمة الحالية / Integration with existing systems",
        ],
        "success_factors": [
            "PDPL and CBAHI compliance documentation",
            "Dedicated onboarding support",
            "Integration with existing EMR/HIS",
        ],
    },
    "real_estate": {
        "avg_days_to_close": 25,
        "typical_decision_makers": ["CEO", "Commercial Director", "CFO"],
        "top_objections": [
            "السوق متقلب حالياً / Market is currently volatile",
            "نحتاج موافقة مجلس الإدارة / Need board approval",
            "العائد على الاستثمار غير واضح / ROI is unclear",
        ],
        "success_factors": [
            "Vision 2030 alignment narrative",
            "Demonstrated pipeline growth from comparable firms",
            "Flexible payment terms",
        ],
    },
    "logistics": {
        "avg_days_to_close": 20,
        "typical_decision_makers": ["Operations Director", "CEO", "Head of Fleet"],
        "top_objections": [
            "الهامش ضيق / Margins are tight",
            "النظام الحالي كافٍ / Current system is sufficient",
            "وقت التطبيق طويل / Long implementation time",
        ],
        "success_factors": [
            "Cost-per-shipment reduction proof points",
            "Fast implementation promise (< 2 weeks)",
            "Integration with SAP or Oracle if used",
        ],
    },
    "fintech": {
        "avg_days_to_close": 45,
        "typical_decision_makers": ["CEO", "Chief Compliance Officer", "CTO", "Board"],
        "top_objections": [
            "متطلبات SAMA صارمة / SAMA requirements are strict",
            "مخاوف أمنية / Security concerns",
            "نحتاج إلى تقييم شامل / Need a comprehensive evaluation",
        ],
        "success_factors": [
            "SAMA compliance documentation",
            "Security audit reports",
            "References from regulated financial entities",
        ],
    },
    "engineering": {
        "avg_days_to_close": 28,
        "typical_decision_makers": ["Project Director", "CFO", "CEO"],
        "top_objections": [
            "المشاريع موسمية / Projects are seasonal",
            "الفريق غير متفرغ للتطبيق / Team is not available for implementation",
            "التكاليف التشغيلية عالية / Operating costs are high",
        ],
        "success_factors": [
            "Demonstrated project margin improvement",
            "Lightweight onboarding requiring < 1 week",
            "Arabic-language interface",
        ],
    },
}

# ---------------------------------------------------------------------------
# Static data: seasonal timing
# ---------------------------------------------------------------------------

_SEASONAL_TIMING: list[dict[str, Any]] = [
    {
        "period": "Ramadan",
        "period_ar": "رمضان",
        "impact": "deal_velocity_reduced_40_percent",
        "recommendation_ar": (
            "ارسل المقترحات قبل رمضان بأسبوعين، وركّز على التواصل الخفيف خلاله."
        ),
        "recommendation_en": (
            "Send proposals two weeks before Ramadan. Limit outreach during the month "
            "to light follow-up only."
        ),
    },
    {
        "period": "Q1 Budget Release (January–March)",
        "period_ar": "إطلاق ميزانية الربع الأول (يناير–مارس)",
        "impact": "high_budget_availability",
        "recommendation_ar": (
            "هذا الوقت الأمثل لتقديم العروض الكبيرة لأن الميزانيات السنوية لرؤية 2030 تُعتمد."
        ),
        "recommendation_en": (
            "Prime time for large proposals. Annual Vision 2030 budgets are approved and "
            "decision-makers are actively looking to commit."
        ),
    },
    {
        "period": "Hajj Season (Dhu al-Hijja)",
        "period_ar": "موسم الحج (ذو الحجة)",
        "impact": "deal_pause",
        "recommendation_ar": (
            "توقف صانعو القرار عن التوقيع خلال موسم الحج. جدّد المتابعة بعده مباشرة."
        ),
        "recommendation_en": (
            "Decision-makers are unavailable during Hajj season. Resume follow-up "
            "immediately after."
        ),
    },
    {
        "period": "National Day (September 23)",
        "period_ar": "اليوم الوطني (23 سبتمبر)",
        "impact": "increased_b2b_activity",
        "recommendation_ar": (
            "شهر سبتمبر نشيط تجارياً مع انعقاد فعاليات وطنية واسعة. وقت جيد للشبكات المهنية."
        ),
        "recommendation_en": (
            "September sees strong commercial activity around national celebrations. "
            "Good window for networking and proposal follow-up."
        ),
    },
    {
        "period": "Summer Slowdown (July–August)",
        "period_ar": "تباطؤ الصيف (يوليو–أغسطس)",
        "impact": "reduced_availability",
        "recommendation_ar": (
            "كثير من المديرين في إجازات. استخدم هذه الفترة لبناء المحتوى وتأهيل الفرص."
        ),
        "recommendation_en": (
            "Many executives are on leave. Use this period for content creation and "
            "pipeline qualification rather than closing pushes."
        ),
    },
    {
        "period": "Year-End Budget Flush (November–December)",
        "period_ar": "صرف ميزانية نهاية العام (نوفمبر–ديسمبر)",
        "impact": "high_urgency_close_window",
        "recommendation_ar": (
            "الشركات تسعى لصرف الميزانيات المتبقية. أسرع في إرسال العروض والمقترحات."
        ),
        "recommendation_en": (
            "Companies seek to deploy remaining budgets. Accelerate proposals and push "
            "for signed agreements before year-end."
        ),
    },
]

# ---------------------------------------------------------------------------
# Pydantic request model
# ---------------------------------------------------------------------------


class DealCoachRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    sector: str = Field(..., min_length=2, max_length=64, description="B2B sector identifier")
    deal_size_sar: int = Field(..., ge=0, description="Estimated deal value in SAR")
    decision_maker_title: str = Field(..., min_length=1, max_length=128)
    days_in_pipeline: int = Field(..., ge=0, description="Days this deal has been in the pipeline")


# ---------------------------------------------------------------------------
# Business logic (pure Python — no LLM)
# ---------------------------------------------------------------------------

_KNOWN_SECTORS = set(_PRICING_GUIDANCE.keys())


def get_pricing_guidance(sector: str) -> dict[str, Any]:
    """Return pricing guidance for the given sector.

    Raises KeyError when sector is unknown.
    """
    data = _PRICING_GUIDANCE.get(sector)
    if data is None:
        raise KeyError(sector)
    return {
        **data,
        "sector": sector,
        "disclaimer_ar": _DISCLAIMER_AR,
        "disclaimer_en": _DISCLAIMER_EN,
        "governance_decision": "ALLOW_WITH_REVIEW",
    }


def get_deal_velocity(sector: str) -> dict[str, Any]:
    """Return deal-velocity metrics for the given sector.

    Raises KeyError when sector is unknown.
    """
    data = _DEAL_VELOCITY.get(sector)
    if data is None:
        raise KeyError(sector)
    return {
        **data,
        "sector": sector,
        "disclaimer_ar": _DISCLAIMER_AR,
        "disclaimer_en": _DISCLAIMER_EN,
        "governance_decision": "ALLOW_WITH_REVIEW",
    }


def get_seasonal_timing() -> dict[str, Any]:
    """Return the full seasonal timing guidance list."""
    return {
        "windows": _SEASONAL_TIMING,
        "disclaimer_ar": _DISCLAIMER_AR,
        "disclaimer_en": _DISCLAIMER_EN,
        "governance_decision": "ALLOW_WITH_REVIEW",
    }


def compute_deal_coaching(
    sector: str,
    deal_size_sar: int,
    decision_maker_title: str,
    days_in_pipeline: int,
) -> dict[str, Any]:
    """Compute coaching advice for a deal without any LLM calls.

    Returns urgency, recommended actions, risk factors, and bilingual next-best-action.
    """
    # Determine urgency
    if days_in_pipeline >= 60:
        urgency = "high"
    elif days_in_pipeline >= 30:
        urgency = "medium"
    else:
        urgency = "low"

    # Velocity benchmark for this sector (fallback to 30 days if unknown)
    velocity = _DEAL_VELOCITY.get(sector, {})
    avg_days = velocity.get("avg_days_to_close", 30)

    is_stalled = days_in_pipeline > avg_days * 1.5
    is_large = deal_size_sar >= 20_000

    # Build recommended actions
    recommended_actions: list[str] = []

    if is_stalled:
        recommended_actions.append(
            "Schedule a discovery call to uncover any unresolved blockers."
        )
    else:
        recommended_actions.append(
            "Send a value-focused follow-up referencing a comparable client outcome."
        )

    if is_large:
        recommended_actions.append(
            "Prepare a formal proposal with ZATCA-compliant pricing breakdown."
        )
    else:
        recommended_actions.append(
            "Offer a short pilot or proof-of-concept to lower commitment friction."
        )

    title_lower = decision_maker_title.lower()
    if any(t in title_lower for t in ("cfo", "finance", "مالي")):
        recommended_actions.append(
            "Lead with ROI and payback-period numbers tailored to their sector."
        )
    elif any(t in title_lower for t in ("cto", "tech", "technology", "تقني")):
        recommended_actions.append(
            "Provide a technical integration overview and a sandbox environment."
        )
    else:
        recommended_actions.append(
            "Request a 30-minute senior-to-senior introduction to accelerate trust."
        )

    # Risk factors
    risk_factors: list[str] = []
    if is_stalled:
        risk_factors.append("Deal has exceeded sector average close time — stall risk.")
    if is_large and urgency == "low":
        risk_factors.append(
            "Large deal with low urgency — budget cycle or internal approval may be pending."
        )
    if sector == "fintech":
        risk_factors.append("Regulatory review cycle may add 2–4 weeks to decision timeline.")
    if not risk_factors:
        risk_factors.append("No critical risk factors detected at this stage.")

    # Bilingual next-best-action
    if urgency == "high" or is_stalled:
        next_best_ar = "طلب اجتماع عاجل مع صاحب القرار لحسم الصفقة هذا الأسبوع."
        next_best_en = "Request an urgent meeting with the decision-maker to close this week."
    elif urgency == "medium":
        next_best_ar = "أرسل ملخصاً للقيمة المقترحة مع توقيت تسليم واضح."
        next_best_en = "Send a value summary with a clear delivery timeline."
    else:
        next_best_ar = "تأكد من فهم العميل للقيمة وحدد موعداً للخطوة التالية."
        next_best_en = "Confirm the prospect understands the value proposition and set a next-step date."

    return {
        "sector": sector,
        "urgency": urgency,
        "recommended_actions": recommended_actions,
        "risk_factors": risk_factors,
        "next_best_action_ar": next_best_ar,
        "next_best_action_en": next_best_en,
        "disclaimer_ar": _DISCLAIMER_AR,
        "disclaimer_en": _DISCLAIMER_EN,
        "governance_decision": "ALLOW_WITH_REVIEW",
    }


# ---------------------------------------------------------------------------
# Router endpoints
# ---------------------------------------------------------------------------


@router.get("/pricing-guidance/{sector}")
def pricing_guidance(sector: str) -> dict[str, Any]:
    """Return recommended SAR pricing ranges for the given Saudi B2B sector.

    All values are estimates derived from market benchmarks, not guarantees.
    """
    try:
        return get_pricing_guidance(sector)
    except KeyError:
        raise HTTPException(
            status_code=404,
            detail={
                "error": f"Sector '{sector}' not found.",
                "available_sectors": sorted(_KNOWN_SECTORS),
                "governance_decision": "ALLOW",
            },
        )


@router.get("/deal-velocity/{sector}")
def deal_velocity(sector: str) -> dict[str, Any]:
    """Return typical deal-velocity metrics for the given Saudi B2B sector."""
    try:
        return get_deal_velocity(sector)
    except KeyError:
        raise HTTPException(
            status_code=404,
            detail={
                "error": f"Sector '{sector}' not found.",
                "available_sectors": sorted(_KNOWN_SECTORS),
                "governance_decision": "ALLOW",
            },
        )


@router.get("/seasonal-timing")
def seasonal_timing() -> dict[str, Any]:
    """Return Saudi market seasonal timing advice for B2B deal planning."""
    return get_seasonal_timing()


@router.post("/deal-coach")
def deal_coach(body: DealCoachRequest) -> dict[str, Any]:
    """Return AI-free coaching advice for a deal in the Saudi B2B pipeline.

    Urgency and recommended actions are derived from sector benchmarks only.
    No LLM calls are made.
    """
    return compute_deal_coaching(
        sector=body.sector,
        deal_size_sar=body.deal_size_sar,
        decision_maker_title=body.decision_maker_title,
        days_in_pipeline=body.days_in_pipeline,
    )
