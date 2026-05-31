"""
Negotiation Playbook API Router.

Saudi-specific negotiation principles, concession framework, walk-away signals,
and scenario playbooks for B2B commercial engagements.

Prefix: /api/v1/negotiation-playbook
"""

from __future__ import annotations

from typing import Any, Literal

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, model_validator

router = APIRouter(
    prefix="/api/v1/negotiation-playbook",
    tags=["Sales"],
)

_ALLOW = "ALLOW_WITH_REVIEW"
_APPROVE = "APPROVAL_FIRST"

# ---------------------------------------------------------------------------
# Static data
# ---------------------------------------------------------------------------

_SAUDI_NEGOTIATION_PRINCIPLES: list[dict[str, Any]] = [
    {
        "id": "face_saving",
        "name_en": "Face Saving",
        "name_ar": "حفظ ماء الوجه",
        "description_en": "Never publicly corner a counterpart; offer a graceful exit.",
        "description_ar": "لا تضع الطرف الآخر في موقف حرج علنياً؛ قدّم له مخرجاً كريماً.",
    },
    {
        "id": "relationship_first",
        "name_en": "Relationship First",
        "name_ar": "العلاقة أولاً",
        "description_en": "Build trust across 3+ meetings before commercial terms.",
        "description_ar": "ابنِ الثقة عبر 3 اجتماعات أو أكثر قبل الخوض في الشروط التجارية.",
    },
    {
        "id": "authority_clarity",
        "name_en": "Authority Clarity",
        "name_ar": "وضوح الصلاحية",
        "description_en": "Confirm decision-maker is present; Saudis may defer to seniors.",
        "description_ar": "تأكد من حضور صاحب القرار؛ قد يُحيل السعوديون الأمر للمسؤولين الأعلى.",
    },
    {
        "id": "silence_as_strength",
        "name_en": "Silence as Strength",
        "name_ar": "الصمت قوة",
        "description_en": "Comfortable silence signals confidence; don't fill it with concessions.",
        "description_ar": "الصمت المريح يدل على الثقة؛ لا تملأه بتنازلات.",
    },
    {
        "id": "halal_commercial_terms",
        "name_en": "Halal Commercial Terms",
        "name_ar": "الشروط التجارية الحلال",
        "description_en": (
            "Avoid interest-based framing; use fee-for-service or Murabaha language."
        ),
        "description_ar": "تجنب الصياغة القائمة على الفائدة؛ استخدم لغة الرسوم مقابل الخدمة أو المرابحة.",
    },
    {
        "id": "patience_timeline",
        "name_en": "Patience Timeline",
        "name_ar": "الصبر في التفاوض",
        "description_en": (
            "Rushing signals desperation; budget cycles are Q1 Jan and Q4 Oct."
        ),
        "description_ar": "التسرع يدل على اليأس؛ دورات الميزانية هي الربع الأول في يناير والربع الرابع في أكتوبر.",
    },
]

_CONCESSION_FRAMEWORK: list[dict[str, Any]] = [
    {
        "id": "anchor_high",
        "name_en": "Anchor High",
        "name_ar": "ابدأ بسقف عالٍ",
        "description_en": "Start 20-30% above walk-away; gives room to concede with dignity.",
        "description_ar": "ابدأ بنسبة 20-30% فوق حد الانسحاب؛ يمنحك مجالاً للتنازل باحترام.",
    },
    {
        "id": "bundle_concession",
        "name_en": "Bundle Concession",
        "name_ar": "التنازل الحزمي",
        "description_en": (
            "Trade implementation time for price reduction (never pure discount)."
        ),
        "description_ar": "قايض وقت التنفيذ مقابل خفض السعر (لا خصماً صريحاً أبداً).",
    },
    {
        "id": "scope_reduction",
        "name_en": "Scope Reduction",
        "name_ar": "تقليص النطاق",
        "description_en": "Reduce deliverables rather than rate — protects value anchor.",
        "description_ar": "قلّل المخرجات بدلاً من السعر — يحمي مرساة القيمة.",
    },
    {
        "id": "payment_terms",
        "name_en": "Payment Terms",
        "name_ar": "شروط الدفع",
        "description_en": (
            "Extend payment timeline instead of reducing price (SAR cash-flow benefit)."
        ),
        "description_ar": "مدّد الجدول الزمني للدفع بدلاً من تخفيض السعر (فائدة في التدفق النقدي بالريال).",
    },
    {
        "id": "pilot_first",
        "name_en": "Pilot First",
        "name_ar": "ابدأ بتجربة",
        "description_en": "Offer a paid pilot (SAR 499–999) to reduce perceived risk.",
        "description_ar": "قدّم تجربة مدفوعة (499–999 ريال) لتقليل المخاطر المتصوَّرة.",
    },
]

_WALK_AWAY_SIGNALS: list[dict[str, Any]] = [
    {
        "id": "persistent_below_cost_pressure",
        "signal_en": "Persistent Below-Cost Pressure",
        "signal_ar": "ضغط متواصل تحت التكلفة",
        "description_en": "Asking below SAR 2,000/mo for managed ops.",
        "description_ar": "الطلب بأقل من 2,000 ريال شهرياً للعمليات المُدارة.",
    },
    {
        "id": "single_decision_maker_absent",
        "signal_en": "Single Decision-Maker Absent",
        "signal_ar": "غياب صاحب القرار المنفرد",
        "description_en": (
            "Champion keeps saying 'I need to check with management' repeatedly."
        ),
        "description_ar": "البطل يكرر 'أحتاج للرجوع إلى الإدارة' مراراً وتكراراً.",
    },
    {
        "id": "scope_creep_before_signing",
        "signal_en": "Scope Creep Before Signing",
        "signal_ar": "توسع النطاق قبل التوقيع",
        "description_en": "Adding requirements after proposal without price discussion.",
        "description_ar": "إضافة متطلبات بعد العرض دون مناقشة السعر.",
    },
    {
        "id": "payment_terms_over_90_days",
        "signal_en": "Payment Terms Over 90 Days",
        "signal_ar": "شروط دفع تتجاوز 90 يوماً",
        "description_en": (
            "Requesting >90-day payment terms without strategic justification."
        ),
        "description_ar": "طلب شروط دفع تتجاوز 90 يوماً دون مبرر استراتيجي.",
    },
    {
        "id": "no_data_access_commitment",
        "signal_en": "No Data Access Commitment",
        "signal_ar": "لا التزام بالوصول إلى البيانات",
        "description_en": (
            "Refusing to connect data sources required for the engagement."
        ),
        "description_ar": "الامتناع عن توصيل مصادر البيانات اللازمة للمشاركة.",
    },
]

_SCENARIO_PLAYBOOKS: dict[str, dict[str, Any]] = {
    "price_objection": {
        "scenario_type": "price_objection",
        "name_en": "Price Objection",
        "name_ar": "اعتراض السعر",
        "recommended_response_en": (
            "Acknowledge the concern without immediately reducing the price. "
            "Anchor the conversation on verified outcomes rather than fee level. "
            "Offer to adjust scope or payment terms before touching the rate."
        ),
        "recommended_response_ar": (
            "اعترف بالمخاوف دون تخفيض السعر فوراً. "
            "أرسِ المحادثة على النتائج الموثقة بدلاً من مستوى الرسوم. "
            "عرض تعديل النطاق أو شروط الدفع قبل تغيير السعر."
        ),
        "trap_to_avoid_en": "Do not offer an immediate discount; it devalues the anchor.",
        "trap_to_avoid_ar": "لا تقدم خصماً فورياً؛ فذلك يُضعف مرساة القيمة.",
        "example_script_en": (
            "I hear your concern on price. "
            "Before we revisit the number, let me confirm what is included: "
            "a verified Proof Pack, ZATCA-ready data pipeline, and bilingual approval workflows. "
            "If scope is the issue, we can narrow the pilot and protect the rate."
        ),
    },
    "timeline_objection": {
        "scenario_type": "timeline_objection",
        "name_en": "Timeline Objection",
        "name_ar": "اعتراض الجدول الزمني",
        "recommended_response_en": (
            "Validate the timeline concern and ask what event is driving the target date. "
            "Separate discovery work from full commitment to reduce the perceived risk. "
            "Surface any regulatory deadline (ZATCA Phase 2) that creates natural urgency."
        ),
        "recommended_response_ar": (
            "أقرّ بمخاوف الجدول الزمني واسأل عن الحدث الذي يحرك الموعد المستهدف. "
            "افصل عمل الاستكشاف عن الالتزام الكامل لتقليل المخاطر المتصوَّرة. "
            "أظهر أي موعد تنظيمي (مرحلة زاتكا 2) يخلق إلحاحاً طبيعياً."
        ),
        "trap_to_avoid_en": "Avoid pressuring a decision during Ramadan or national holidays.",
        "trap_to_avoid_ar": "تجنب الضغط على قرار خلال رمضان أو الأعياد الوطنية.",
        "example_script_en": (
            "Understood — timing matters. "
            "What changes in Q3 that makes it a better window? "
            "I ask because ZATCA Phase 2 deadlines are fixed; a scoped 2-week pilot now "
            "would give you documented evidence before any Q3 review."
        ),
    },
    "scope_creep": {
        "scenario_type": "scope_creep",
        "name_en": "Scope Creep",
        "name_ar": "توسع النطاق",
        "recommended_response_en": (
            "Log the new requirement in writing immediately. "
            "Frame the conversation as a change-order discussion, not a negotiation. "
            "Present the cost and timeline impact of the addition before agreeing."
        ),
        "recommended_response_ar": (
            "سجّل المتطلب الجديد كتابياً فوراً. "
            "أطّر المحادثة كنقاش لطلب تغيير، لا كتفاوض. "
            "اعرض تأثير الإضافة على التكلفة والجدول الزمني قبل الموافقة."
        ),
        "trap_to_avoid_en": "Never absorb new requirements silently; it signals unlimited flexibility.",
        "trap_to_avoid_ar": "لا تستوعب المتطلبات الجديدة بصمت أبداً؛ ذلك يوحي بمرونة غير محدودة.",
        "example_script_en": (
            "Thank you for raising this. "
            "The original proposal covered [original scope]. "
            "This addition is outside that boundary and will affect delivery time and cost. "
            "Let me document it and come back with a change-order figure within 24 hours."
        ),
    },
    "competitor_comparison": {
        "scenario_type": "competitor_comparison",
        "name_en": "Competitor Comparison",
        "name_ar": "المقارنة مع المنافس",
        "recommended_response_en": (
            "Ask specifically what the competitor is offering and at what price point. "
            "Differentiate on Saudi-specific capabilities: ZATCA integration, bilingual workflows, PDPL compliance. "
            "Offer a Proof Pack comparison rather than a verbal feature list."
        ),
        "recommended_response_ar": (
            "اسأل تحديداً عما يقدمه المنافس وبأي سعر. "
            "ميّز بالقدرات السعودية المحددة: تكامل زاتكا، سير العمل ثنائي اللغة، امتثال PDPL. "
            "اعرض مقارنة حزمة الإثبات بدلاً من قائمة مزايا شفهية."
        ),
        "trap_to_avoid_en": "Never criticize the competitor directly; let the evidence speak.",
        "trap_to_avoid_ar": "لا تنتقد المنافس مباشرة أبداً؛ دع الأدلة تتكلم.",
        "example_script_en": (
            "I appreciate the transparency. "
            "A few questions about their offer: does it include ZATCA Phase 2 certification? "
            "Does it handle PDPL consent workflows in Arabic natively? "
            "Our Proof Pack at the end of every engagement documents exactly what changed — "
            "we can put both offers side by side on verified outcomes."
        ),
    },
    "approval_delay": {
        "scenario_type": "approval_delay",
        "name_en": "Approval Delay",
        "name_ar": "تأخر الموافقة",
        "recommended_response_en": (
            "Confirm who the approver is and what they need to see to decide. "
            "Offer to co-create the internal business case for the champion. "
            "Set a concrete follow-up date tied to a specific internal milestone."
        ),
        "recommended_response_ar": (
            "أكّد هوية المعتمِد وما يحتاج رؤيته للقرار. "
            "عرض المشاركة في بناء مسوّغ العمل الداخلي للبطل. "
            "حدد تاريخ متابعة ملموساً مرتبطاً بحدث داخلي محدد."
        ),
        "trap_to_avoid_en": (
            "Do not follow up more than once per week; over-contacting reads as desperation."
        ),
        "trap_to_avoid_ar": (
            "لا تتابع أكثر من مرة في الأسبوع؛ الاتصال المفرط يُقرأ كيأس."
        ),
        "example_script_en": (
            "Understood — internal approvals take time. "
            "To help move this forward, I can prepare a one-page executive summary "
            "tailored to what your CFO or CEO needs to see. "
            "What is the next scheduled leadership review where this could be on the agenda?"
        ),
    },
}

_VALID_SCENARIO_TYPES = list(_SCENARIO_PLAYBOOKS.keys())

_CONCESSION_BY_TIER: dict[str, list[str]] = {
    "small": ["pilot_first", "payment_terms"],
    "medium": ["bundle_concession", "payment_terms", "scope_reduction"],
    "large": ["anchor_high", "bundle_concession", "scope_reduction"],
}

# ---------------------------------------------------------------------------
# Pydantic models
# ---------------------------------------------------------------------------

ScenarioType = Literal[
    "price_objection",
    "timeline_objection",
    "scope_creep",
    "competitor_comparison",
    "approval_delay",
]


class NegotiationScenarioInput(BaseModel):
    scenario_type: ScenarioType
    deal_value_sar: float = Field(..., ge=0, description="Deal value in SAR")
    stage: Literal["proposal", "negotiation", "close"]

    @model_validator(mode="after")
    def validate_deal_value_has_context(self) -> NegotiationScenarioInput:
        if self.deal_value_sar == 0 and self.stage == "close":
            raise ValueError(
                "deal_value_sar must be greater than 0 when stage is 'close'."
            )
        return self


# ---------------------------------------------------------------------------
# Pure function
# ---------------------------------------------------------------------------


def _build_negotiation_brief(inp: NegotiationScenarioInput) -> dict[str, Any]:
    """
    Return matching scenario playbook + concession recommendations.

    Raises HTTPException 422 if scenario_type is not recognized.
    """
    playbook = _SCENARIO_PLAYBOOKS.get(inp.scenario_type)
    if playbook is None:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "unknown_scenario_type",
                "received": inp.scenario_type,
                "valid": _VALID_SCENARIO_TYPES,
            },
        )

    if inp.deal_value_sar < 5_000:
        tier_key = "small"
    elif inp.deal_value_sar < 50_000:
        tier_key = "medium"
    else:
        tier_key = "large"

    concession_ids = _CONCESSION_BY_TIER[tier_key]
    recommended_concessions = [
        c for c in _CONCESSION_FRAMEWORK if c["id"] in concession_ids
    ]

    return {
        "governance_decision": _APPROVE,
        "scenario_type": inp.scenario_type,
        "deal_value_sar": inp.deal_value_sar,
        "stage": inp.stage,
        "playbook": playbook,
        "recommended_concessions": recommended_concessions,
        "concession_tier": tier_key,
        "note_en": (
            "All negotiation actions require human review before execution. "
            "No guaranteed outcomes."
        ),
        "note_ar": (
            "جميع إجراءات التفاوض تتطلب مراجعة بشرية قبل التنفيذ. "
            "لا نتائج مضمونة."
        ),
    }


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------


@router.get("/principles")
async def list_principles() -> dict[str, Any]:
    """Return all 6 Saudi negotiation principles with bilingual content."""
    return {
        "governance_decision": _ALLOW,
        "total": len(_SAUDI_NEGOTIATION_PRINCIPLES),
        "principles": _SAUDI_NEGOTIATION_PRINCIPLES,
    }


@router.get("/concession-framework")
async def list_concession_framework() -> dict[str, Any]:
    """Return all 5 concession types with bilingual descriptions."""
    return {
        "governance_decision": _ALLOW,
        "total": len(_CONCESSION_FRAMEWORK),
        "concessions": _CONCESSION_FRAMEWORK,
    }


@router.get("/walk-away-signals")
async def list_walk_away_signals() -> dict[str, Any]:
    """Return all 5 walk-away signals with bilingual descriptions."""
    return {
        "governance_decision": _ALLOW,
        "total": len(_WALK_AWAY_SIGNALS),
        "signals": _WALK_AWAY_SIGNALS,
    }


@router.post("/scenario-brief")
async def scenario_brief(body: NegotiationScenarioInput) -> dict[str, Any]:
    """Return scenario playbook and concession recommendations. Requires approval."""
    return _build_negotiation_brief(body)
