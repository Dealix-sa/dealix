"""Meeting intelligence for Saudi B2B sales engagements.

Provides meeting type metadata, Saudi cultural etiquette rules, outcome
templates, and a meeting brief builder. All data is static; no LLM or
external API calls are made.

Prefix: /api/v1/meeting-intelligence
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter(
    prefix="/api/v1/meeting-intelligence",
    tags=["Sales"],
)

# ---------------------------------------------------------------------------
# Governance constants
# ---------------------------------------------------------------------------

_GOV_REVIEW = "ALLOW_WITH_REVIEW"
_GOV_APPROVAL = "APPROVAL_FIRST"

# ---------------------------------------------------------------------------
# Static data: meeting types
# ---------------------------------------------------------------------------

_MEETING_TYPES: dict[str, Any] = {
    "discovery": {
        "name_en": "Discovery",
        "name_ar": "الاكتشاف",
        "duration_minutes": 60,
        "agenda_items_en": [
            "Introductions and relationship building",
            "Understand current reporting and data workflows",
            "Identify key pain points and business priorities",
            "Align on evaluation criteria and next steps",
        ],
        "agenda_items_ar": [
            "التعارف وبناء العلاقة",
            "فهم التقارير وسير عمل البيانات الحالية",
            "تحديد نقاط الألم الرئيسية والأولويات التجارية",
            "التوافق على معايير التقييم والخطوات التالية",
        ],
        "success_criteria_en": "Prospect shares current challenges openly and agrees to a follow-up demo",
        "success_criteria_ar": "يشارك العميل المحتمل تحدياته الحالية بصراحة ويوافق على عرض توضيحي لاحق",
    },
    "demo": {
        "name_en": "Product Demo",
        "name_ar": "العرض التوضيحي",
        "duration_minutes": 75,
        "agenda_items_en": [
            "Recap of discovery findings and agreed pain points",
            "Tailored platform walkthrough addressing specific use cases",
            "Live Q&A on features and integrations",
            "Agree on proof-of-concept or proposal review next step",
        ],
        "agenda_items_ar": [
            "مراجعة نتائج الاكتشاف ونقاط الألم المتفق عليها",
            "جولة مخصصة في المنصة تعالج حالات الاستخدام المحددة",
            "أسئلة وأجوبة مباشرة حول الميزات والتكاملات",
            "الاتفاق على إثبات المفهوم أو الخطوة التالية لمراجعة الاقتراح",
        ],
        "success_criteria_en": "Prospect confirms the platform addresses their top three use cases",
        "success_criteria_ar": "يؤكد العميل المحتمل أن المنصة تعالج حالات الاستخدام الثلاث الرئيسية لديه",
    },
    "proposal_review": {
        "name_en": "Proposal Review",
        "name_ar": "مراجعة الاقتراح",
        "duration_minutes": 60,
        "agenda_items_en": [
            "Walk through the commercial proposal and pricing structure",
            "Review scope, deliverables, and implementation timeline",
            "Address objections and negotiate terms",
            "Align on decision-making process and approvers",
        ],
        "agenda_items_ar": [
            "استعراض الاقتراح التجاري وهيكل التسعير",
            "مراجعة النطاق والمخرجات والجدول الزمني للتنفيذ",
            "معالجة الاعتراضات والتفاوض على الشروط",
            "التوافق على عملية اتخاذ القرار والمعتمدين",
        ],
        "success_criteria_en": "All decision-maker objections addressed; verbal agreement on commercial terms",
        "success_criteria_ar": "معالجة جميع اعتراضات صانعي القرار؛ اتفاق شفهي على الشروط التجارية",
    },
    "qbr": {
        "name_en": "Quarterly Business Review",
        "name_ar": "مراجعة الأعمال الربعية",
        "duration_minutes": 90,
        "agenda_items_en": [
            "Review KPIs and platform utilization versus targets",
            "Showcase value delivered and milestones achieved",
            "Discuss roadmap priorities and upcoming features",
            "Agree on expansion opportunities and renewal plan",
        ],
        "agenda_items_ar": [
            "مراجعة المؤشرات الرئيسية واستخدام المنصة مقارنةً بالأهداف",
            "إبراز القيمة المحققة والمعالم المُنجزة",
            "مناقشة أولويات خارطة الطريق والميزات القادمة",
            "الاتفاق على فرص التوسع وخطة التجديد",
        ],
        "success_criteria_en": "Client affirms value and verbal commitment to renewal or expansion",
        "success_criteria_ar": "يؤكد العميل القيمة والالتزام الشفهي بالتجديد أو التوسع",
    },
}

# ---------------------------------------------------------------------------
# Static data: Saudi meeting etiquette
# ---------------------------------------------------------------------------

_SAUDI_MEETING_ETIQUETTE: list[dict[str, Any]] = [
    {
        "rule_en": "Greet the most senior person first by their correct title",
        "rule_ar": "ابدأ بتحية الشخص الأعلى رتبةً باللقب الصحيح",
        "applies_to": "all",
    },
    {
        "rule_en": "Allow time for small talk and relationship building before discussing business",
        "rule_ar": "خصص وقتاً للحديث الاجتماعي وبناء العلاقة قبل الدخول في صلب الأعمال",
        "applies_to": "all",
    },
    {
        "rule_en": "Do not schedule meetings on Fridays or Saturdays",
        "rule_ar": "تجنب جدولة الاجتماعات أيام الجمعة والسبت",
        "applies_to": "all",
    },
    {
        "rule_en": "Accepting offered coffee or tea is expected and a sign of respect",
        "rule_ar": "يُتوقع قبول القهوة أو الشاي المُقدَّم وهو علامة احترام",
        "applies_to": "all",
    },
    {
        "rule_en": "Allow the most senior person to speak first and set the pace of discussion",
        "rule_ar": "دع الشخص الأعلى رتبةً يتحدث أولاً ويحدد وتيرة النقاش",
        "applies_to": "formal",
    },
    {
        "rule_en": "Avoid direct refusals; use indirect language to decline or redirect",
        "rule_ar": "تجنب الرفض المباشر؛ استخدم لغةً غير مباشرة للرفض أو إعادة التوجيه",
        "applies_to": "all",
    },
]

# ---------------------------------------------------------------------------
# Static data: meeting outcome templates
# ---------------------------------------------------------------------------

_MEETING_OUTCOME_TEMPLATES: dict[str, Any] = {
    "positive": {
        "label_en": "Positive — Strong Progress",
        "label_ar": "إيجابي — تقدم ملحوظ",
        "next_step_en": "Send a written summary within 24 hours and schedule the next milestone meeting",
        "next_step_ar": "أرسل ملخصاً كتابياً خلال 24 ساعة وجدول اجتماع المرحلة التالية",
    },
    "neutral": {
        "label_en": "Neutral — Further Information Needed",
        "label_ar": "محايد — معلومات إضافية مطلوبة",
        "next_step_en": "Send additional materials addressing open questions within 48 hours",
        "next_step_ar": "أرسل مواد إضافية تعالج الأسئلة المفتوحة خلال 48 ساعة",
    },
    "needs_follow_up": {
        "label_en": "Needs Follow-Up — Objections Unresolved",
        "label_ar": "يتطلب متابعة — اعتراضات لم تُحسم",
        "next_step_en": "Arrange a focused call with the economic buyer to resolve outstanding objections",
        "next_step_ar": "رتب مكالمة مركزة مع صانع القرار الاقتصادي لحل الاعتراضات القائمة",
    },
}

# ---------------------------------------------------------------------------
# Valid options
# ---------------------------------------------------------------------------

_VALID_MEETING_TYPES: set[str] = {"discovery", "demo", "proposal_review", "qbr"}

# ---------------------------------------------------------------------------
# Pydantic models
# ---------------------------------------------------------------------------


class MeetingBriefInput(BaseModel):
    meeting_type: str
    prospect_company: str
    prospect_name: str
    prospect_title: str
    known_pain_points: list[str] = Field(default_factory=list)
    is_first_meeting: bool = True
    arabic_primary: bool = False


# ---------------------------------------------------------------------------
# Pure-function core
# ---------------------------------------------------------------------------


def _build_meeting_brief(inp: MeetingBriefInput) -> dict[str, Any]:
    """Build a structured meeting brief for a Saudi B2B sales engagement.

    Returns agenda, etiquette rules, success criteria, and bilingual
    opening hooks tailored to the prospect.
    Governance decision: APPROVAL_FIRST.
    """
    if inp.meeting_type not in _VALID_MEETING_TYPES:
        raise HTTPException(
            status_code=422,
            detail=(
                f"Invalid meeting_type '{inp.meeting_type}'. "
                f"Valid values: {sorted(_VALID_MEETING_TYPES)}"
            ),
        )

    meeting_data = _MEETING_TYPES[inp.meeting_type]

    primary_pain = inp.known_pain_points[0] if inp.known_pain_points else "your operational priorities"

    opening_hook_en: str = (
        f"{inp.prospect_name}, based on our understanding of {inp.prospect_company}'s "
        f"current focus on {primary_pain}, we want to show you exactly how Dealix "
        f"addresses that challenge."
    )
    opening_hook_ar: str = (
        f"{inp.prospect_name}، بناءً على فهمنا لأولويات {inp.prospect_company} الحالية "
        f"المتعلقة بـ {primary_pain}، نريد أن نُريك بالضبط كيف تعالج ديلكس هذا التحدي."
    )

    return {
        "meeting_type": inp.meeting_type,
        "prospect_company": inp.prospect_company,
        "prospect_name": inp.prospect_name,
        "prospect_title": inp.prospect_title,
        "duration_minutes": meeting_data["duration_minutes"],
        "agenda_items_en": meeting_data["agenda_items_en"],
        "agenda_items_ar": meeting_data["agenda_items_ar"],
        "success_criteria_en": meeting_data["success_criteria_en"],
        "success_criteria_ar": meeting_data["success_criteria_ar"],
        "etiquette_rules": _SAUDI_MEETING_ETIQUETTE,
        "opening_hook_en": opening_hook_en,
        "opening_hook_ar": opening_hook_ar,
        "is_first_meeting": inp.is_first_meeting,
        "governance_decision": _GOV_APPROVAL,
    }


# ---------------------------------------------------------------------------
# Router endpoints
# ---------------------------------------------------------------------------


@router.get("/types", summary="All 4 meeting type definitions")
def get_meeting_types() -> dict[str, Any]:
    """Return all meeting types with agenda items, duration, and success criteria."""
    return {
        "meeting_types": _MEETING_TYPES,
        "governance_decision": _GOV_REVIEW,
    }


@router.get("/etiquette", summary="All 6 Saudi meeting etiquette rules")
def get_etiquette() -> dict[str, Any]:
    """Return Saudi cultural etiquette rules for B2B meetings."""
    return {
        "etiquette_rules": _SAUDI_MEETING_ETIQUETTE,
        "governance_decision": _GOV_REVIEW,
    }


@router.get("/outcome-templates", summary="All 3 meeting outcome templates")
def get_outcome_templates() -> dict[str, Any]:
    """Return bilingual outcome templates with recommended next steps."""
    return {
        "outcome_templates": _MEETING_OUTCOME_TEMPLATES,
        "governance_decision": _GOV_REVIEW,
    }


@router.post("/build-brief", summary="Build a meeting brief for a prospect")
def build_meeting_brief(body: MeetingBriefInput) -> dict[str, Any]:
    """Accept meeting context and return a tailored meeting brief.

    Governance decision: APPROVAL_FIRST.
    """
    return _build_meeting_brief(body)
