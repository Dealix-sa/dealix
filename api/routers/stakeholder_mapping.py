"""Stakeholder mapping for Saudi B2B enterprise deals.

Provides stakeholder archetypes, Saudi-specific decision-making patterns,
an influence map template, and a stakeholder assessment function. All data
is static; no LLM or external API calls are made.

Prefix: /api/v1/stakeholder-mapping
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel, Field

router = APIRouter(
    prefix="/api/v1/stakeholder-mapping",
    tags=["Sales"],
)

# ---------------------------------------------------------------------------
# Governance constants
# ---------------------------------------------------------------------------

_GOV_REVIEW = "ALLOW_WITH_REVIEW"

# ---------------------------------------------------------------------------
# Static data: stakeholder archetypes
# ---------------------------------------------------------------------------

_STAKEHOLDER_ARCHETYPES: dict[str, Any] = {
    "economic_buyer": {
        "archetype_id": "economic_buyer",
        "name_en": "Economic Buyer",
        "name_ar": "المشتري الاقتصادي",
        "motivation_en": "Return on investment, budget alignment, and strategic fit",
        "motivation_ar": "العائد على الاستثمار والتوافق مع الميزانية والملاءمة الاستراتيجية",
        "engagement_strategy_en": "Lead with ROI data, board-level business case, and risk mitigation",
        "engagement_strategy_ar": "ابدأ ببيانات العائد على الاستثمار والحجة التجارية للمجلس وتخفيف المخاطر",
        "risk_if_ignored_en": "Deal stalls or is killed at final approval stage",
    },
    "champion": {
        "archetype_id": "champion",
        "name_en": "Internal Champion",
        "name_ar": "البطل الداخلي",
        "motivation_en": "Solve a personal pain point and gain internal recognition",
        "motivation_ar": "حل نقطة ألم شخصية واكتساب الاعتراف الداخلي",
        "engagement_strategy_en": "Arm with demo materials, proof points, and objection responses for internal selling",
        "engagement_strategy_ar": "زوّده بمواد العرض والأدلة والردود على الاعتراضات للبيع الداخلي",
        "risk_if_ignored_en": "No internal advocate; deal loses momentum",
    },
    "technical_evaluator": {
        "archetype_id": "technical_evaluator",
        "name_en": "Technical Evaluator",
        "name_ar": "المُقيِّم الفني",
        "motivation_en": "Security, integration compatibility, and implementation risk",
        "motivation_ar": "الأمان وتوافق التكامل ومخاطر التنفيذ",
        "engagement_strategy_en": "Provide technical documentation, security posture, and architecture diagrams",
        "engagement_strategy_ar": "قدم وثائق فنية ووضعية الأمان ومخططات البنية",
        "risk_if_ignored_en": "Technical veto blocks procurement even after commercial agreement",
    },
    "end_user": {
        "archetype_id": "end_user",
        "name_en": "End User",
        "name_ar": "المستخدم النهائي",
        "motivation_en": "Ease of use, reduced workload, and daily workflow improvement",
        "motivation_ar": "سهولة الاستخدام وتقليل عبء العمل وتحسين سير العمل اليومي",
        "engagement_strategy_en": "Run hands-on workshops and gather feedback to shape adoption plan",
        "engagement_strategy_ar": "نظم ورش عمل تطبيقية واجمع الملاحظات لتشكيل خطة التبني",
        "risk_if_ignored_en": "Low adoption post-go-live leads to churn at renewal",
    },
    "blocker": {
        "archetype_id": "blocker",
        "name_en": "Blocker",
        "name_ar": "المعرقل",
        "motivation_en": "Protecting existing vendor relationships, budget, or influence",
        "motivation_ar": "حماية علاقات البائعين الحاليين أو الميزانية أو النفوذ",
        "engagement_strategy_en": "Identify root concern early; involve a senior sponsor to neutralize",
        "engagement_strategy_ar": "حدد المخاوف الجذرية مبكراً؛ أشرك راعياً كبيراً للتحييد",
        "risk_if_ignored_en": "Actively undermines deal at critical decision points",
    },
}

# ---------------------------------------------------------------------------
# Static data: Saudi decision-making patterns
# ---------------------------------------------------------------------------

_DECISION_MAKING_PATTERNS: list[dict[str, Any]] = [
    {
        "pattern_en": "Consensus is required across key stakeholders before a decision is finalised (majlis culture)",
        "pattern_ar": "يُشترط الإجماع بين أصحاب المصلحة الرئيسيين قبل اتخاذ القرار النهائي (ثقافة المجلس)",
        "implication_en": "Map all influencers early; one unsatisfied stakeholder can block a unanimous decision",
    },
    {
        "pattern_en": "Senior leadership approval is always required regardless of organisational layer",
        "pattern_ar": "تتطلب الموافقة دائماً من القيادة العليا بغض النظر عن المستوى التنظيمي",
        "implication_en": "Secure an executive sponsor and prepare a concise C-level briefing document",
    },
    {
        "pattern_en": "A trusted intermediary or referral significantly accelerates deal progression",
        "pattern_ar": "يُسرِّع وسيط موثوق أو إحالة معروفة تقدم الصفقة بشكل ملحوظ",
        "implication_en": "Leverage partner referrals or mutual connections before cold outreach",
    },
    {
        "pattern_en": "Decisions and approvals typically slow during Ramadan",
        "pattern_ar": "تتباطأ القرارات والموافقات عادةً خلال شهر رمضان",
        "implication_en": "Plan for extended timelines during Ramadan and adjust forecast dates accordingly",
    },
]

# ---------------------------------------------------------------------------
# Static data: influence map template
# ---------------------------------------------------------------------------

_INFLUENCE_MAP_TEMPLATE: list[dict[str, Any]] = [
    {
        "level_name_en": "Senior Leadership",
        "level_name_ar": "القيادة العليا",
        "typical_roles_en": ["CEO / Managing Director", "CFO", "Board Member"],
        "dealix_value_prop_en": "Strategic visibility, governance assurance, and measurable ROI at the executive level",
    },
    {
        "level_name_en": "Mid Management",
        "level_name_ar": "الإدارة الوسطى",
        "typical_roles_en": ["Operations Director", "Finance Manager", "Commercial Manager"],
        "dealix_value_prop_en": "Operational efficiency, accurate reporting, and reduced manual workload for their teams",
    },
    {
        "level_name_en": "Operational",
        "level_name_ar": "المستوى التشغيلي",
        "typical_roles_en": ["Data Analyst", "Financial Analyst", "Operations Coordinator"],
        "dealix_value_prop_en": "Automated workflows, fewer repetitive tasks, and faster access to reliable data",
    },
]

# ---------------------------------------------------------------------------
# Valid options
# ---------------------------------------------------------------------------

_VALID_ARCHETYPES: set[str] = {
    "economic_buyer",
    "champion",
    "technical_evaluator",
    "end_user",
    "blocker",
}

# ---------------------------------------------------------------------------
# Pydantic models
# ---------------------------------------------------------------------------


class StakeholderAssessmentInput(BaseModel):
    prospect_company: str
    identified_champion: bool = False
    economic_buyer_engaged: bool = False
    technical_evaluator_engaged: bool = False
    blockers_identified: int = Field(default=0, ge=0)
    decision_makers_count: int = Field(default=1, ge=1)
    deal_value_sar: float = Field(..., ge=0)


# ---------------------------------------------------------------------------
# Pure-function core
# ---------------------------------------------------------------------------


def _assess_stakeholder_map(inp: StakeholderAssessmentInput) -> dict[str, Any]:
    """Compute stakeholder coverage score and deal risk for an opportunity.

    Coverage score: +40 champion, +30 economic buyer, +20 technical evaluator,
    -10 per blocker (floor 0). Returns coverage label, missing archetypes,
    deal risk level, and recommended next contacts.
    Governance decision: ALLOW_WITH_REVIEW.
    """
    score: int = 0
    if inp.identified_champion:
        score += 40
    if inp.economic_buyer_engaged:
        score += 30
    if inp.technical_evaluator_engaged:
        score += 20
    score = max(0, score - inp.blockers_identified * 10)

    if score >= 70:
        coverage_label = "strong"
    elif score >= 40:
        coverage_label = "adequate"
    else:
        coverage_label = "weak"

    missing_archetypes: list[str] = []
    if not inp.identified_champion:
        missing_archetypes.append("champion")
    if not inp.economic_buyer_engaged:
        missing_archetypes.append("economic_buyer")
    if not inp.technical_evaluator_engaged:
        missing_archetypes.append("technical_evaluator")

    if score < 40:
        deal_risk_level = "high"
    elif score < 70:
        deal_risk_level = "medium"
    else:
        deal_risk_level = "low"

    recommended_next_contacts: list[str] = list(missing_archetypes)

    return {
        "prospect_company": inp.prospect_company,
        "coverage_score": score,
        "coverage_label": coverage_label,
        "missing_archetypes": missing_archetypes,
        "deal_risk_level": deal_risk_level,
        "recommended_next_contacts": recommended_next_contacts,
        "governance_decision": _GOV_REVIEW,
    }


# ---------------------------------------------------------------------------
# Router endpoints
# ---------------------------------------------------------------------------


@router.get("/archetypes", summary="All 5 stakeholder archetypes")
def get_archetypes() -> dict[str, Any]:
    """Return all stakeholder archetypes with motivations and engagement strategies."""
    return {
        "archetypes": _STAKEHOLDER_ARCHETYPES,
        "governance_decision": _GOV_REVIEW,
    }


@router.get("/decision-patterns", summary="All 4 Saudi decision-making patterns")
def get_decision_patterns() -> dict[str, Any]:
    """Return Saudi-specific decision-making patterns with deal implications."""
    return {
        "decision_patterns": _DECISION_MAKING_PATTERNS,
        "governance_decision": _GOV_REVIEW,
    }


@router.get("/influence-map", summary="Three-level influence map template")
def get_influence_map() -> dict[str, Any]:
    """Return the three-level organisational influence map with typical roles."""
    return {
        "influence_map": _INFLUENCE_MAP_TEMPLATE,
        "governance_decision": _GOV_REVIEW,
    }


@router.post("/assess", summary="Assess stakeholder map coverage for an opportunity")
def assess_stakeholder_map(body: StakeholderAssessmentInput) -> dict[str, Any]:
    """Accept stakeholder engagement flags and return coverage score and deal risk.

    Governance decision: ALLOW_WITH_REVIEW.
    """
    return _assess_stakeholder_map(body)
