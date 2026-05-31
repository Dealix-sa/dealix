"""Competitive battlecard builder for Dealix Saudi B2B sales.

All data is static; no LLM or external API calls are made.
All generated battlecards carry a mandatory governance decision and must be
reviewed before acting on them.

Prefix: /api/v1/competitive-battlecard
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter(
    prefix="/api/v1/competitive-battlecard",
    tags=["Sales"],
)

# ---------------------------------------------------------------------------
# Governance constants
# ---------------------------------------------------------------------------

_GOV_REVIEW = "ALLOW_WITH_REVIEW"
_GOV_APPROVAL = "APPROVAL_FIRST"

# ---------------------------------------------------------------------------
# Static data: battlecard sections
# ---------------------------------------------------------------------------

_BATTLECARD_SECTIONS: list[dict[str, Any]] = [
    {
        "order": 1,
        "section_name_en": "Positioning Statement",
        "section_name_ar": "بيان تحديد الموقع",
        "purpose_en": "Establish a clear, memorable one-sentence differentiation claim.",
        "purpose_ar": "إرساء ادعاء تمايز واضح ولا يُنسى في جملة واحدة.",
    },
    {
        "order": 2,
        "section_name_en": "Three Strengths",
        "section_name_ar": "ثلاث نقاط قوة",
        "purpose_en": "Highlight the three product or delivery advantages most relevant to this deal.",
        "purpose_ar": "إبراز المزايا الثلاث الأكثر صلة بهذه الصفقة سواء في المنتج أو التسليم.",
    },
    {
        "order": 3,
        "section_name_en": "Three Vulnerabilities",
        "section_name_ar": "ثلاث نقاط ضعف",
        "purpose_en": "Acknowledge honest weaknesses and pre-empt competitor attacks.",
        "purpose_ar": "الاعتراف بالضعف بصدق والتقدم على هجمات المنافسين.",
    },
    {
        "order": 4,
        "section_name_en": "Counter Objections",
        "section_name_ar": "الرد على الاعتراضات",
        "purpose_en": "Provide scripted, evidence-backed responses to the most common objections.",
        "purpose_ar": "تقديم ردود مدعومة بالأدلة على أكثر الاعتراضات شيوعاً.",
    },
    {
        "order": 5,
        "section_name_en": "Proof Points",
        "section_name_ar": "نقاط الإثبات",
        "purpose_en": "Reference specific case studies, metrics, or third-party validation.",
        "purpose_ar": "الإشارة إلى دراسات حالة محددة أو مقاييس أو تحقق من طرف ثالث.",
    },
]

# ---------------------------------------------------------------------------
# Static data: Dealix differentiators
# ---------------------------------------------------------------------------

_DEALIX_DIFFERENTIATORS: list[dict[str, Any]] = [
    {
        "differentiator_en": "Saudi-native compliance built in",
        "differentiator_ar": "امتثال سعودي أصيل مدمج",
        "proof_data_en": "ZATCA Phase 2, Arabic UI, and Hijri calendar support shipped on day one.",
        "applicable_competitors_en": "global SaaS vendors",
    },
    {
        "differentiator_en": "7-day sprint delivery model",
        "differentiator_ar": "نموذج تسليم بسباق سبعة أيام",
        "proof_data_en": "Clients receive first working prototype within one calendar week of contract sign.",
        "applicable_competitors_en": "enterprise integrators, boutique consultancies",
    },
    {
        "differentiator_en": "Price advantage versus global vendors",
        "differentiator_ar": "ميزة السعر مقارنة بالموردين العالميين",
        "proof_data_en": "Average 40% cost reduction versus comparable global SaaS contracts in Saudi market.",
        "applicable_competitors_en": "Salesforce, SAP, Oracle, HubSpot",
    },
    {
        "differentiator_en": "Vision 2030 alignment narrative",
        "differentiator_ar": "سرد التوافق مع رؤية 2030",
        "proof_data_en": "Mapped to Vision 2030 pillars in every deliverable for procurement justification.",
        "applicable_competitors_en": "all international competitors",
    },
    {
        "differentiator_en": "Founder-led delivery",
        "differentiator_ar": "تسليم يقوده المؤسس",
        "proof_data_en": "The founding team personally owns every pilot engagement, not a junior team.",
        "applicable_competitors_en": "enterprise integrators, large consulting firms",
    },
    {
        "differentiator_en": "Bilingual-first user experience",
        "differentiator_ar": "تجربة مستخدم ثنائية اللغة في المقام الأول",
        "proof_data_en": "100% of UI strings available in Arabic and English with right-to-left layout.",
        "applicable_competitors_en": "global SaaS vendors, regional non-Arabic tools",
    },
]

# ---------------------------------------------------------------------------
# Static data: objection counter scripts
# ---------------------------------------------------------------------------

_OBJECTION_COUNTER_SCRIPTS: list[dict[str, Any]] = [
    {
        "objection_en": "We already have a system",
        "objection_ar": "لدينا نظام بالفعل",
        "counter_en": (
            "Most clients who say this find their current system covers only part of the workflow. "
            "Can we map your current tool against these three specific gaps and see where it stands?"
        ),
        "counter_ar": (
            "معظم العملاء الذين يقولون ذلك يجدون أن نظامهم الحالي يغطي جزءاً من سير العمل فقط. "
            "هل يمكننا مقارنة أداتك الحالية بهذه الثغرات الثلاث المحددة؟"
        ),
    },
    {
        "objection_en": "Too expensive",
        "objection_ar": "السعر مرتفع",
        "counter_en": (
            "Compared to what alternative? When we factor in implementation cost, localisation, "
            "and time to value, our total cost of ownership is typically 40% below global vendors."
        ),
        "counter_ar": (
            "مقارنةً بأي بديل؟ عند احتساب تكاليف التنفيذ والتعريب والوقت اللازم لتحقيق القيمة، "
            "فإن تكلفة الملكية الإجمالية لدينا أقل عادةً بنسبة 40% من الموردين العالميين."
        ),
    },
    {
        "objection_en": "We need enterprise features",
        "objection_ar": "نحتاج إلى ميزات المؤسسات",
        "counter_en": (
            "Which specific enterprise features are mandatory for your rollout? "
            "We have shipped SSO, audit logs, role-based access, and API integrations. "
            "Let us walk through your checklist."
        ),
        "counter_ar": (
            "ما هي ميزات المؤسسة المحددة الإلزامية لطرح منتجك؟ "
            "لقد شحنّا الدخول الأحادي وسجلات التدقيق والوصول القائم على الأدوار وتكاملات API. "
            "دعنا نستعرض قائمتك."
        ),
    },
    {
        "objection_en": "No local support",
        "objection_ar": "لا يوجد دعم محلي",
        "counter_en": (
            "Our support team is Riyadh-based and operates in Arabic during Saudi business hours, "
            "including prayer-time-aware scheduling. Response SLA is four business hours."
        ),
        "counter_ar": (
            "فريق الدعم لدينا مقره الرياض ويعمل باللغة العربية خلال ساعات العمل السعودية "
            "مع جدول زمني يراعي أوقات الصلاة. اتفاقية مستوى الخدمة للاستجابة أربع ساعات عمل."
        ),
    },
    {
        "objection_en": "We prefer global brands",
        "objection_ar": "نفضل العلامات التجارية العالمية",
        "counter_en": (
            "Global brands are built for global markets. "
            "Vision 2030 mandates Saudi-first solutions for government-aligned procurement. "
            "We are purpose-built for this market and hold the local compliance references you need."
        ),
        "counter_ar": (
            "العلامات التجارية العالمية مبنية للأسواق العالمية. "
            "تُلزم رؤية 2030 بحلول سعودية أولاً في المشتريات المرتبطة بالحكومة. "
            "نحن مبنيون لهذا السوق تحديداً ونحمل مراجع الامتثال المحلية التي تحتاجها."
        ),
    },
]

# ---------------------------------------------------------------------------
# Valid contexts
# ---------------------------------------------------------------------------

_VALID_COMPETITIVE_CONTEXTS: set[str] = {
    "head_to_head",
    "rfp_response",
    "renewal_defense",
    "new_logo",
}

# ---------------------------------------------------------------------------
# Talk track templates per context
# ---------------------------------------------------------------------------

_TALK_TRACKS: dict[str, dict[str, str]] = {
    "head_to_head": {
        "en": (
            "We know you are evaluating alternatives and we welcome the comparison. "
            "Let me walk you through where we specifically outperform on Saudi compliance and speed to value."
        ),
        "ar": (
            "نعلم أنك تقيّم البدائل ونرحب بالمقارنة. "
            "دعني أوضح لك أين نتفوق تحديداً في الامتثال السعودي والسرعة في تحقيق القيمة."
        ),
    },
    "rfp_response": {
        "en": (
            "This response addresses each RFP criterion with verifiable evidence, "
            "not marketing claims. Every capability listed has a reference client in the Saudi market."
        ),
        "ar": (
            "يتناول هذا الرد كل معيار في طلب تقديم العروض بأدلة قابلة للتحقق، "
            "وليس ادعاءات تسويقية. كل قدرة مذكورة لها عميل مرجعي في السوق السعودي."
        ),
    },
    "renewal_defense": {
        "en": (
            "Before we discuss renewal terms, let me show you the verified business outcomes "
            "delivered since contract start and the roadmap items that deepen your ROI."
        ),
        "ar": (
            "قبل أن نناقش شروط التجديد، دعني أريك النتائج التجارية الموثقة "
            "منذ بداية العقد وعناصر خارطة الطريق التي تعزز عائدك على الاستثمار."
        ),
    },
    "new_logo": {
        "en": (
            "We have helped similar companies in your sector go live in Saudi Arabia within seven days. "
            "Let me share two specific proof points that are directly relevant to your situation."
        ),
        "ar": (
            "ساعدنا شركات مماثلة في قطاعك على الانطلاق في السعودية خلال سبعة أيام. "
            "دعني أشارككم نقطتَي إثبات محددتين تتعلقان مباشرة بوضعك."
        ),
    },
}

# ---------------------------------------------------------------------------
# Pydantic models
# ---------------------------------------------------------------------------


class BattlecardInput(BaseModel):
    competitive_context: str
    prospect_sector: str
    deal_value_sar: float = Field(..., ge=0)
    known_competitor_archetype: str = Field(default="unknown")


# ---------------------------------------------------------------------------
# Pure-function core
# ---------------------------------------------------------------------------


def _build_battlecard(inp: BattlecardInput) -> dict[str, Any]:
    """Build a competitive battlecard for a given sales context.

    Returns a structured dict with sections, differentiators,
    objection counters, a context-specific talk track, and governance decision.
    """
    if inp.competitive_context not in _VALID_COMPETITIVE_CONTEXTS:
        raise HTTPException(
            status_code=422,
            detail=(
                f"Invalid competitive_context '{inp.competitive_context}'. "
                f"Must be one of: {sorted(_VALID_COMPETITIVE_CONTEXTS)}"
            ),
        )

    tracks = _TALK_TRACKS[inp.competitive_context]

    return {
        "competitive_context": inp.competitive_context,
        "sections": _BATTLECARD_SECTIONS,
        "dealix_differentiators": _DEALIX_DIFFERENTIATORS,
        "objection_counters": _OBJECTION_COUNTER_SCRIPTS,
        "talk_track_en": tracks["en"],
        "talk_track_ar": tracks["ar"],
        "governance_decision": _GOV_APPROVAL,
    }


# ---------------------------------------------------------------------------
# Router endpoints
# ---------------------------------------------------------------------------


@router.get("/sections", summary="All 5 battlecard sections with bilingual labels")
def get_sections() -> dict[str, Any]:
    """Return all battlecard sections in order with bilingual names and purpose."""
    return {
        "sections": _BATTLECARD_SECTIONS,
        "total_sections": len(_BATTLECARD_SECTIONS),
        "governance_decision": _GOV_REVIEW,
    }


@router.get("/differentiators", summary="All 6 Dealix differentiators with proof data")
def get_differentiators() -> dict[str, Any]:
    """Return all Dealix differentiators with bilingual labels and proof claims."""
    return {
        "differentiators": _DEALIX_DIFFERENTIATORS,
        "total_differentiators": len(_DEALIX_DIFFERENTIATORS),
        "governance_decision": _GOV_REVIEW,
    }


@router.get("/objection-counters", summary="All 5 objection counter scripts")
def get_objection_counters() -> dict[str, Any]:
    """Return all objection counter scripts with bilingual objections and counters."""
    return {
        "objection_counters": _OBJECTION_COUNTER_SCRIPTS,
        "total_scripts": len(_OBJECTION_COUNTER_SCRIPTS),
        "governance_decision": _GOV_REVIEW,
    }


@router.post("/build", summary="Build a competitive battlecard for a given context")
def build_battlecard(body: BattlecardInput) -> dict[str, Any]:
    """Accept deal context and return a full competitive battlecard.

    Governance decision: APPROVAL_FIRST.
    """
    return _build_battlecard(body)
