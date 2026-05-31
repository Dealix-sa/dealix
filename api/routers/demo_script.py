"""
Demo script builder for Saudi B2B sales presentations.

Provides demo flow phases, demo type configurations, Saudi cultural rules,
and in-demo objection responses. Pure Python — no LLM calls, no external
API calls. Bilingual (EN/AR).

No guaranteed-outcome language. No cold WhatsApp or LinkedIn automation.
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter(prefix="/api/v1/demo-script", tags=["Sales"])

# ---------------------------------------------------------------------------
# Demo flow phases — 6 phases, total 50 minutes
# ---------------------------------------------------------------------------

_DEMO_FLOW: list[dict[str, Any]] = [
    {
        "id": "opening",
        "name_en": "Opening",
        "name_ar": "الافتتاح",
        "duration_minutes": 5,
        "purpose_en": "Establish context, confirm time, state agenda.",
        "purpose_ar": "تأسيس السياق، تأكيد الوقت، عرض جدول الأعمال.",
    },
    {
        "id": "pain_discovery",
        "name_en": "Pain Discovery",
        "name_ar": "اكتشاف الألم",
        "duration_minutes": 10,
        "purpose_en": "Ask 3 discovery questions before showing anything.",
        "purpose_ar": "طرح 3 أسئلة اكتشافية قبل عرض أي شيء.",
    },
    {
        "id": "solution_fit",
        "name_en": "Solution Fit",
        "name_ar": "ملاءمة الحل",
        "duration_minutes": 15,
        "purpose_en": "Show 3 features max that address stated pains.",
        "purpose_ar": "عرض 3 ميزات كحد أقصى تعالج الآلام المذكورة.",
    },
    {
        "id": "roi_moment",
        "name_en": "ROI Moment",
        "name_ar": "لحظة العائد",
        "duration_minutes": 10,
        "purpose_en": "Live ROI calculation using their numbers (ZATCA savings, time saved).",
        "purpose_ar": "حساب العائد الحي باستخدام أرقامهم (وفورات هيئة الزكاة، الوقت الموفر).",
    },
    {
        "id": "proof_point",
        "name_en": "Proof Point",
        "name_ar": "دليل الإثبات",
        "duration_minutes": 5,
        "purpose_en": "Show one relevant Saudi client outcome (anonymized if needed).",
        "purpose_ar": "عرض نتيجة واحدة لعميل سعودي ذات صلة (مجهولة الهوية إذا لزم).",
    },
    {
        "id": "next_step",
        "name_en": "Next Step",
        "name_ar": "الخطوة التالية",
        "duration_minutes": 5,
        "purpose_en": "End with a specific next step: diagnostic, pilot, proposal.",
        "purpose_ar": "الختام بخطوة تالية محددة: تشخيص، تجربة، عرض.",
    },
]

_DEMO_FLOW_TOTAL_MINUTES = sum(p["duration_minutes"] for p in _DEMO_FLOW)  # 50

# ---------------------------------------------------------------------------
# Demo types — 4 configurations
# ---------------------------------------------------------------------------

_DEMO_TYPES: dict[str, dict[str, Any]] = {
    "executive_overview": {
        "name_en": "Executive Overview",
        "name_ar": "نظرة عامة تنفيذية",
        "duration_minutes": 20,
        "audience_en": "C-level / VP",
        "audience_ar": "المستوى التنفيذي / نائب الرئيس",
        "max_slides": 3,
        "technical_detail": False,
        "notes_en": "Lead with business outcomes, not features. No technical detail.",
        "notes_ar": "ابدأ بنتائج الأعمال وليس الميزات. بدون تفاصيل تقنية.",
    },
    "champion_deep_dive": {
        "name_en": "Champion Deep Dive",
        "name_ar": "غوص عميق مع البطل",
        "duration_minutes": 50,
        "audience_en": "Operational / IT champion",
        "audience_ar": "البطل التشغيلي / تقنية المعلومات",
        "max_slides": None,
        "technical_detail": True,
        "notes_en": "Follow the full 6-phase demo flow. Show integration depth.",
        "notes_ar": "اتبع تدفق العرض الكامل المكون من 6 مراحل. اعرض عمق التكامل.",
    },
    "proposal_validation": {
        "name_en": "Proposal Validation",
        "name_ar": "التحقق من العرض",
        "duration_minutes": 30,
        "audience_en": "Mixed (champion + decision-maker)",
        "audience_ar": "مختلط (البطل + صانع القرار)",
        "max_slides": None,
        "technical_detail": False,
        "notes_en": "Confirms fit before proposal send. Address remaining objections.",
        "notes_ar": "يؤكد الملاءمة قبل إرسال العرض. عالج الاعتراضات المتبقية.",
    },
    "pilot_kickoff": {
        "name_en": "Pilot Kickoff",
        "name_ar": "انطلاق التجربة",
        "duration_minutes": 45,
        "audience_en": "Operational team",
        "audience_ar": "الفريق التشغيلي",
        "max_slides": None,
        "technical_detail": True,
        "notes_en": "Hands-on platform walkthrough. Assign champion tasks.",
        "notes_ar": "جولة تطبيقية على المنصة. أسند مهام للبطل.",
    },
}

# ---------------------------------------------------------------------------
# Cultural demo rules — 7 rules for Saudi demo context
# ---------------------------------------------------------------------------

_CULTURAL_DEMO_RULES: list[dict[str, Any]] = [
    {
        "id": "arabic_first_slide",
        "rule_en": "Start with an Arabic slide if the audience is primarily Arabic-speaking.",
        "rule_ar": "ابدأ بشريحة عربية إذا كان الجمهور في أغلبه ناطقاً بالعربية.",
    },
    {
        "id": "quran_verse_respect",
        "rule_en": "Never rush through a Quran verse if the counterpart opens with one.",
        "rule_ar": "لا تتعجل في تلاوة آية قرآنية إذا افتتح بها المقابل.",
    },
    {
        "id": "dates_and_coffee",
        "rule_en": "Offer dates and coffee before screen sharing (virtual: acknowledge the tradition).",
        "rule_ar": "قدّم التمر والقهوة قبل مشاركة الشاشة (افتراضي: اعترف بالتقليد).",
    },
    {
        "id": "sar_currency",
        "rule_en": "Use SAR not USD in all live calculations.",
        "rule_ar": "استخدم الريال السعودي وليس الدولار في جميع الحسابات الحية.",
    },
    {
        "id": "avoid_friday_afternoon",
        "rule_en": "Avoid Friday afternoon slots (Jumu'ah).",
        "rule_ar": "تجنب مواعيد بعد الظهر يوم الجمعة (صلاة الجمعة).",
    },
    {
        "id": "senior_person_first",
        "rule_en": "Address the most senior person first, even if not the decision-maker.",
        "rule_ar": "خاطب أكبر شخصاً في المرتبة أولاً حتى لو لم يكن صانع القرار.",
    },
    {
        "id": "allow_silence",
        "rule_en": "Allow silence after key points; do not interpret quiet as confusion.",
        "rule_ar": "اسمح بالصمت بعد النقاط الرئيسية؛ لا تفسر الهدوء على أنه ارتباك.",
    },
]

# ---------------------------------------------------------------------------
# In-demo objection responses — 5 objections with bilingual responses
# ---------------------------------------------------------------------------

_OBJECTION_RESPONSES: list[dict[str, Any]] = [
    {
        "id": "we_already_have_crm",
        "trigger_en": "We already have a CRM.",
        "trigger_ar": "لدينا CRM بالفعل.",
        "response_en": (
            "Dealix integrates with your CRM — it handles what CRMs can't: "
            "AI drafts, ZATCA validation, bilingual sequences."
        ),
        "response_ar": (
            "ديليكس يتكامل مع CRM الخاص بك — يتعامل مع ما لا تستطيع فعله أنظمة CRM: "
            "المسودات بالذكاء الاصطناعي، والتحقق من هيئة الزكاة، والتسلسلات ثنائية اللغة."
        ),
    },
    {
        "id": "our_it_team_can_build",
        "trigger_en": "Our IT team can build this.",
        "trigger_ar": "فريق تقنية المعلومات لدينا يستطيع بناء هذا.",
        "response_en": (
            "Your IT team is best for core systems — Dealix is live in 7 days "
            "so your revenue team does not wait 6-12 months."
        ),
        "response_ar": (
            "فريق تقنية المعلومات لديك هو الأمثل للأنظمة الأساسية — "
            "ديليكس يعمل في 7 أيام حتى لا ينتظر فريق الإيرادات 6-12 شهراً."
        ),
    },
    {
        "id": "show_me_the_price",
        "trigger_en": "Show me the price.",
        "trigger_ar": "أرني السعر.",
        "response_en": (
            "I will show pricing right after we confirm the fit — "
            "does what you have seen so far solve [stated pain]?"
        ),
        "response_ar": (
            "سأعرض التسعير مباشرة بعد أن نؤكد الملاءمة — "
            "هل ما رأيته حتى الآن يحل [الألم المذكور]؟"
        ),
    },
    {
        "id": "we_need_arabic_first",
        "trigger_en": "We need Arabic first.",
        "trigger_ar": "نحتاج العربية أولاً.",
        "response_en": (
            "Our platform is bilingual by design — let me switch to Arabic right now. "
            "Then demonstrate."
        ),
        "response_ar": (
            "منصتنا ثنائية اللغة بالتصميم — دعني أتحول إلى العربية الآن. "
            "ثم أقدم العرض."
        ),
    },
    {
        "id": "what_about_data_security",
        "trigger_en": "What about data security?",
        "trigger_ar": "ما مدى أمان البيانات؟",
        "response_en": (
            "We are PDPL-compliant and can share our Data Processing Agreement — "
            "who in your team should review it?"
        ),
        "response_ar": (
            "نحن متوافقون مع نظام حماية البيانات الشخصية ويمكننا مشاركة اتفاقية معالجة البيانات — "
            "من في فريقك يجب أن يراجعها؟"
        ),
    },
]

# ---------------------------------------------------------------------------
# Pydantic input model
# ---------------------------------------------------------------------------

_VALID_DEMO_TYPES = set(_DEMO_TYPES.keys())
_VALID_SENIORITY_LEVELS = {"c_level", "vp_director", "manager_team_lead"}


class DemoConfigInput(BaseModel):
    """Input for building a tailored demo configuration."""

    demo_type: str = Field(..., description="One of the 4 demo type keys.")
    audience_seniority: str = Field(
        ...,
        description="'c_level' | 'vp_director' | 'manager_team_lead'",
    )
    known_pains: list[str] = Field(
        ...,
        min_length=1,
        max_length=3,
        description="1-3 pain points from discovery.",
    )
    is_arabic_primary: bool = Field(
        ...,
        description="True if the audience primarily communicates in Arabic.",
    )


# ---------------------------------------------------------------------------
# Core business logic
# ---------------------------------------------------------------------------

def _configure_demo(inp: DemoConfigInput) -> dict[str, Any]:
    """
    Build a tailored demo configuration based on demo type, audience, and
    discovered pain points.

    Returns the filtered phase list to fit the demo duration, plus bilingual
    language guidance and a context-specific opening hook.
    """
    if inp.demo_type not in _VALID_DEMO_TYPES:
        raise ValueError(
            f"demo_type must be one of {sorted(_VALID_DEMO_TYPES)}, "
            f"got '{inp.demo_type}'"
        )
    if inp.audience_seniority not in _VALID_SENIORITY_LEVELS:
        raise ValueError(
            f"audience_seniority must be one of {sorted(_VALID_SENIORITY_LEVELS)}, "
            f"got '{inp.audience_seniority}'"
        )

    demo_meta = _DEMO_TYPES[inp.demo_type]
    target_minutes: int = demo_meta["duration_minutes"]

    # Select phases that fit the demo duration by including phases in order
    # until the total duration would be exceeded.
    recommended_flow: list[dict[str, Any]] = []
    running_total = 0
    for phase in _DEMO_FLOW:
        if running_total + phase["duration_minutes"] <= target_minutes:
            recommended_flow.append(phase)
            running_total += phase["duration_minutes"]

    # Language guidance
    if inp.is_arabic_primary:
        language_guidance_en = (
            "Open with an Arabic slide. Deliver key points in Arabic first, "
            "then offer English clarification on request."
        )
        language_guidance_ar = (
            "افتح بشريحة عربية. قدّم النقاط الرئيسية بالعربية أولاً، "
            "ثم اعرض التوضيح بالإنجليزية عند الطلب."
        )
    else:
        language_guidance_en = (
            "Lead in English. Offer Arabic equivalents for key terms and pricing."
        )
        language_guidance_ar = (
            "ابدأ بالإنجليزية. قدّم مقابلات عربية للمصطلحات الرئيسية والتسعير."
        )

    # Opening hook
    first_pain = inp.known_pains[0] if inp.known_pains else "your key business challenge"
    opening_hook_en = (
        f"Before I show you anything, I want to confirm we are solving the right problem. "
        f"You mentioned {first_pain} — let me show you exactly how we address that in the first 10 minutes."
    )

    return {
        "demo_type": inp.demo_type,
        "duration_minutes": target_minutes,
        "audience_en": demo_meta["audience_en"],
        "audience_ar": demo_meta["audience_ar"],
        "recommended_flow": recommended_flow,
        "language_guidance_en": language_guidance_en,
        "language_guidance_ar": language_guidance_ar,
        "opening_hook_en": opening_hook_en,
        "governance_decision": "ALLOW_WITH_REVIEW",
    }


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------


@router.get("/flow", summary="All 6 demo flow phases with durations")
async def get_demo_flow() -> dict[str, Any]:
    return {
        "phases": _DEMO_FLOW,
        "total_duration_minutes": _DEMO_FLOW_TOTAL_MINUTES,
        "governance_decision": "ALLOW_WITH_REVIEW",
    }


@router.get("/types", summary="All 4 demo types with audience and duration guidance")
async def get_demo_types() -> dict[str, Any]:
    return {
        "demo_types": _DEMO_TYPES,
        "governance_decision": "ALLOW_WITH_REVIEW",
    }


@router.get("/cultural-rules", summary="Saudi cultural rules for demo delivery")
async def get_cultural_rules() -> dict[str, Any]:
    return {
        "cultural_rules": _CULTURAL_DEMO_RULES,
        "governance_decision": "ALLOW_WITH_REVIEW",
    }


@router.get("/objections", summary="In-demo objection responses with bilingual scripts")
async def get_objection_responses() -> dict[str, Any]:
    return {
        "objection_responses": _OBJECTION_RESPONSES,
        "governance_decision": "ALLOW_WITH_REVIEW",
    }


@router.post("/configure", summary="Build a tailored demo configuration")
async def configure_demo(inp: DemoConfigInput) -> dict[str, Any]:
    """
    Returned governance_decision is ALLOW_WITH_REVIEW.
    Review the configuration with the sales team before delivering the demo.
    """
    if inp.demo_type not in _VALID_DEMO_TYPES:
        raise HTTPException(
            status_code=422,
            detail=f"demo_type must be one of {sorted(_VALID_DEMO_TYPES)}",
        )
    if inp.audience_seniority not in _VALID_SENIORITY_LEVELS:
        raise HTTPException(
            status_code=422,
            detail=f"audience_seniority must be one of {sorted(_VALID_SENIORITY_LEVELS)}",
        )
    return _configure_demo(inp)
