"""
Competitive positioning data for Dealix Saudi B2B sales team.

All data is static. No LLM calls, no external API calls. Bilingual (EN/AR).
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter(prefix="/api/v1/competitive-positioning", tags=["Sales"])

# ---------------------------------------------------------------------------
# Competitor category definitions
# ---------------------------------------------------------------------------

_COMPETITOR_CATEGORIES: dict[str, dict[str, Any]] = {
    "generic_crm": {
        "name_en": "Generic Global CRM",
        "name_ar": "منصات CRM العالمية العامة",
        "examples": "Salesforce / HubSpot / Zoho",
        "weakness_summary": "No Saudi customization, no Arabic NLP, no Hijri support, PDPL non-compliant",
        "dealix_advantage_en": (
            "Dealix is built for Saudi B2B: native Arabic NLP, Hijri calendar, "
            "ZATCA compliance, Vision 2030 KPI alignment"
        ),
        "dealix_advantage_ar": (
            "ديليكس مصمم للأعمال السعودية: معالجة عربية طبيعية، تقويم هجري، "
            "امتثال هيئة الزكاة، توافق مؤشرات رؤية 2030"
        ),
        "objection_response_en": (
            "A generic CRM won't understand your Arabic pipeline or map to ZATCA phases. "
            "Dealix is purpose-built for Saudi revenue intelligence."
        ),
        "price_comparison_en": (
            "Global CRMs cost SAR 3,000–15,000+/mo per seat. "
            "Dealix delivers faster ROI at SAR 2,999–4,999/mo all-in."
        ),
        "win_conditions": [
            "Saudi-only team",
            "ZATCA compliance need",
            "Arabic-first pipeline",
        ],
    },
    "big_4_consulting": {
        "name_en": "Big 4 / Strategy Consultants",
        "name_ar": "شركات الاستشارات الكبرى",
        "examples": "McKinsey / Deloitte / KPMG / PwC",
        "weakness_summary": "High cost, long timelines, no software, no recurring value",
        "dealix_advantage_en": (
            "Dealix delivers AI-powered revenue intelligence in 7 days, not 6 months. "
            "SAR 499 sprint vs. SAR 100K+ consulting engagements."
        ),
        "dealix_advantage_ar": (
            "ديليكس يوفر استخبارات إيرادات مدعومة بالذكاء الاصطناعي في 7 أيام وليس 6 أشهر. "
            "499 ريال مقابل تعاقدات استشارية بأكثر من 100,000 ريال."
        ),
        "objection_response_en": (
            "Consulting firms deliver strategy decks; Dealix delivers running systems. "
            "Position Dealix as the execution layer."
        ),
        "price_comparison_en": (
            "Big 4 engagements start at SAR 100K+ for a single project. "
            "Dealix at SAR 2,999/mo delivers monthly recurring intelligence."
        ),
        "win_conditions": [
            "Speed requirement",
            "Budget constraint",
            "Recurring need > one-time report",
        ],
    },
    "local_it_integrators": {
        "name_en": "Local IT Integrators",
        "name_ar": "شركات تكامل الأنظمة المحلية",
        "examples": "STC Solutions / Mobily Business / local system integrators",
        "weakness_summary": "Infrastructure focus, not revenue intelligence",
        "dealix_advantage_en": (
            "IT integrators wire systems together — Dealix turns those systems "
            "into revenue intelligence and sales action."
        ),
        "dealix_advantage_ar": (
            "شركات تكامل الأنظمة تربط الأنظمة ببعضها — ديليكس يحول تلك الأنظمة "
            "إلى استخبارات إيرادات وإجراءات مبيعات."
        ),
        "objection_response_en": (
            "Infrastructure is a prerequisite, not the outcome. "
            "Dealix is the revenue layer on top of your existing IT investment."
        ),
        "price_comparison_en": (
            "IT integration projects run SAR 50K–500K with long delivery cycles. "
            "Dealix deploys in 7 days on existing infrastructure."
        ),
        "win_conditions": [
            "Revenue focus vs. infrastructure",
            "Go-to-market need",
            "Sales productivity goal",
        ],
    },
    "in_house_team": {
        "name_en": "In-House Analytics / Excel",
        "name_ar": "فريق التحليل الداخلي / إكسل",
        "examples": "Internal analytics / BI team or Excel",
        "weakness_summary": "Manual, slow, no Saudi market benchmarks",
        "dealix_advantage_en": (
            "In-house teams spend 3 days/week on reporting. "
            "Dealix automates this in hours, freeing your team for strategy."
        ),
        "dealix_advantage_ar": (
            "الفرق الداخلية تقضي 3 أيام أسبوعياً في التقارير. "
            "ديليكس يؤتمت هذا في ساعات، محرراً فريقك للاستراتيجية."
        ),
        "objection_response_en": (
            "Your team is valuable — redirect them from reporting to decision-making. "
            "Dealix handles the data work so your analysts handle the insights."
        ),
        "price_comparison_en": (
            "3 analyst-days/week = SAR 15K+/mo in labor cost. "
            "Dealix at SAR 2,999/mo delivers faster reports and Saudi benchmarks."
        ),
        "win_conditions": [
            "Team capacity constraints",
            "Reporting backlog",
            "Board-ready dashboards needed",
        ],
    },
    "do_nothing": {
        "name_en": "Status Quo / No Decision",
        "name_ar": "الوضع الراهن / عدم اتخاذ قرار",
        "examples": "No decision: status quo, budget fear, timing",
        "weakness_summary": "Status quo, budget fear, timing",
        "dealix_advantage_en": (
            "Every month without Revenue Intelligence is a month of missed pipeline. "
            "The cost of inaction at SAR 10K pipeline lost/mo exceeds Dealix's annual fee."
        ),
        "dealix_advantage_ar": (
            "كل شهر بدون استخبارات الإيرادات هو شهر من فرص المبيعات الضائعة. "
            "تكلفة التقاعس بـ 10,000 ريال خسارة شهرية تتجاوز رسوم ديليكس السنوية."
        ),
        "objection_response_en": (
            "The real risk is inaction. Let's calculate what your current pipeline "
            "gaps cost per month — then compare that to SAR 499 sprint."
        ),
        "price_comparison_en": (
            "Inaction costs SAR 10K–100K/mo in missed pipeline. "
            "SAR 499 sprint proves ROI in 7 days with zero long-term commitment."
        ),
        "win_conditions": [
            "ZATCA deadline urgency",
            "Q4 budget pressure",
            "Competitor threat",
        ],
    },
}

# ---------------------------------------------------------------------------
# Battle cards
# ---------------------------------------------------------------------------

_BATTLE_CARDS: list[dict[str, Any]] = [
    {
        "id": "bc_salesforce",
        "scenario": "Prospect says: 'We're already using Salesforce'",
        "scenario_ar": "يقول العميل: 'نحن نستخدم Salesforce بالفعل'",
        "context_en": (
            "Prospect has an existing CRM investment and may see Dealix as redundant "
            "or as a reason to disqualify."
        ),
        "context_ar": (
            "العميل لديه استثمار قائم في CRM وقد يرى ديليكس مكرراً "
            "أو سبباً للاستبعاد."
        ),
        "dealix_response_en": (
            "Acknowledge the Salesforce investment — it is a solid system for US-market workflows. "
            "Bridge to Saudi-specific gaps: Salesforce does not support Hijri calendar natively, "
            "lacks Arabic NLP for pipeline notes, and requires expensive customization for ZATCA Phase 2. "
            "Offer a free 30-minute diagnostic to surface these gaps against their actual pipeline data."
        ),
        "dealix_response_ar": (
            "أقرّ باستثمار Salesforce — نظام متين لسير عمل السوق الأمريكي. "
            "انتقل إلى الفجوات الخاصة بالسوق السعودي: Salesforce لا يدعم التقويم الهجري بشكل أصلي، "
            "ويفتقر إلى معالجة اللغة العربية لملاحظات المبيعات، ويتطلب تخصيصاً مكلفاً لهيئة الزكاة. "
            "اعرض تشخيصاً مجانياً لمدة 30 دقيقة لإظهار هذه الفجوات على بيانات مبيعاتهم الفعلية."
        ),
        "trap_to_avoid_en": (
            "Do not position Dealix as a Salesforce replacement. "
            "Position as a Saudi-specific intelligence layer on top of their existing CRM investment."
        ),
    },
    {
        "id": "bc_big4",
        "scenario": "Prospect says: 'We're hiring a Big 4 firm'",
        "scenario_ar": "يقول العميل: 'نحن نوظف شركة من الكبرى الأربع'",
        "context_en": (
            "Prospect is in active procurement for a strategy engagement. "
            "Dealix could be seen as competing or overlapping."
        ),
        "context_ar": (
            "العميل في مرحلة شراء نشطة لتعاقد استراتيجي. "
            "قد يُنظر إلى ديليكس على أنه منافس أو متداخل."
        ),
        "dealix_response_en": (
            "Respect the Big 4 decision — strategy engagements have their place. "
            "Position Dealix as the execution layer that operationalizes their recommendations. "
            "The consulting firm will deliver a deck in 6 months; Dealix turns that deck into "
            "a running revenue intelligence system in 7 days. "
            "Recommend timing the Dealix sprint to begin when the consulting engagement ends."
        ),
        "dealix_response_ar": (
            "احترم قرار الاستشارات الكبرى — للتعاقدات الاستراتيجية مكانها. "
            "ضع ديليكس كطبقة تنفيذ تُشغّل توصياتهم. "
            "ستسلم شركة الاستشارات عرضاً بعد 6 أشهر؛ ديليكس يحول ذلك العرض إلى "
            "نظام استخبارات إيرادات يعمل في 7 أيام. "
            "أوصِ بأن يبدأ سبرينت ديليكس عند انتهاء تعاقد الاستشارات."
        ),
        "trap_to_avoid_en": (
            "Do not criticize the Big 4 firm directly. "
            "Consultants and Dealix serve different jobs — strategy vs. execution. "
            "Attacking the consulting choice damages trust."
        ),
    },
    {
        "id": "bc_build_internally",
        "scenario": "Prospect says: 'Our IT team can build this'",
        "scenario_ar": "يقول العميل: 'فريق تقنية المعلومات لدينا يستطيع بناء هذا'",
        "context_en": (
            "Prospect is evaluating a build-vs-buy decision. "
            "Internal technical confidence is high but timeline and maintenance risks are underestimated."
        ),
        "context_ar": (
            "العميل يقيّم قرار البناء مقابل الشراء. "
            "الثقة التقنية الداخلية عالية لكن مخاطر الجدول الزمني والصيانة مقللة."
        ),
        "dealix_response_en": (
            "Validate the technical capability — a skilled IT team can absolutely build this. "
            "Redirect focus to time cost: building a Saudi-grade revenue intelligence platform "
            "takes 6–18 months of engineering time, requires Arabic NLP expertise, "
            "ZATCA API integration, and ongoing maintenance. "
            "Dealix is live in 7 days. The IT team's time is better spent on core product. "
            "Offer the SAR 499 sprint to demonstrate capability before any long-term commitment."
        ),
        "dealix_response_ar": (
            "أكّد الكفاءة التقنية — الفريق الموهوب قادر بالتأكيد على البناء. "
            "أعد التركيز على تكلفة الوقت: بناء منصة استخبارات إيرادات بمستوى سعودي "
            "يستغرق 6–18 شهراً من وقت الهندسة، ويتطلب خبرة معالجة اللغة العربية، "
            "وتكامل API هيئة الزكاة، وصيانة مستمرة. "
            "ديليكس يعمل في 7 أيام. وقت فريق تقنية المعلومات أفضل استثماراً في المنتج الأساسي. "
            "اعرض سبرينت 499 ريال لإثبات الكفاءة قبل أي التزام طويل الأمد."
        ),
        "trap_to_avoid_en": (
            "Do not dismiss the IT team's capability — they may be your champion's allies. "
            "Agree on capability but redirect to opportunity cost and speed-to-value."
        ),
    },
    {
        "id": "bc_no_budget",
        "scenario": "Prospect says: 'We don't have budget right now'",
        "scenario_ar": "يقول العميل: 'ليس لدينا ميزانية الآن'",
        "context_en": (
            "Prospect is in a budget freeze or is deflecting with timing. "
            "Real objection may be risk aversion or unclear ROI."
        ),
        "context_ar": (
            "العميل في تجميد للميزانية أو يؤجل بالتوقيت. "
            "قد يكون الاعتراض الحقيقي تجنب المخاطرة أو عائد استثمار غير واضح."
        ),
        "dealix_response_en": (
            "Reframe: every month without revenue intelligence costs money. "
            "Calculate the pipeline gap at SAR 10K lost per month — "
            "that is SAR 120K/year in missed revenue vs. SAR 2,999/mo for Dealix. "
            "Offer the SAR 499 sprint as a low-risk entry point: "
            "7 days, full refund if no value demonstrated, requires no annual commitment. "
            "Position the sprint as a budget-neutral diagnostic, not a software purchase."
        ),
        "dealix_response_ar": (
            "أعد الإطار: كل شهر بدون استخبارات الإيرادات يكلف مالاً. "
            "احسب فجوة المبيعات بـ 10,000 ريال خسارة شهرياً — "
            "هذا 120,000 ريال سنوياً من الإيرادات الضائعة مقابل 2,999 ريال شهرياً لديليكس. "
            "اعرض سبرينت 499 ريال كنقطة دخول منخفضة المخاطر: "
            "7 أيام، استرداد كامل إذا لم تُثبت قيمة، لا يتطلب التزاماً سنوياً. "
            "ضع السبرينت كتشخيص محايد للميزانية، لا شراء برمجيات."
        ),
        "trap_to_avoid_en": (
            "Do not offer large discounts on the monthly plan — it devalues positioning. "
            "The SAR 499 sprint is the standard low-commitment entry point. "
            "Do not agree to revisit in 6 months without a specific follow-up date."
        ),
    },
]

# ---------------------------------------------------------------------------
# Pydantic models
# ---------------------------------------------------------------------------


class PositioningBriefRequest(BaseModel):
    competitor_category: str = Field(..., description="Category ID from GET /categories")
    client_name: str = Field(..., max_length=120)
    client_pain_points: list[str] = Field(..., min_length=1, max_length=10)
    deal_size_sar: float = Field(..., gt=0, description="Estimated deal size in SAR")


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------


@router.get("/categories", summary="All competitor categories with Dealix positioning")
async def list_categories() -> dict[str, Any]:
    return {
        "categories": [
            {"id": k, **v}
            for k, v in _COMPETITOR_CATEGORIES.items()
        ],
        "governance_decision": "ALLOW_WITH_REVIEW",
    }


@router.get("/categories/{category_id}", summary="Single competitor category detail")
async def get_category(category_id: str) -> dict[str, Any]:
    category = _COMPETITOR_CATEGORIES.get(category_id)
    if not category:
        raise HTTPException(
            status_code=404,
            detail=f"Category '{category_id}' not found. Valid: {list(_COMPETITOR_CATEGORIES.keys())}",
        )
    return {
        "id": category_id,
        **category,
        "governance_decision": "ALLOW_WITH_REVIEW",
    }


@router.get("/battle-cards", summary="All battle cards for competitive conversations")
async def list_battle_cards() -> dict[str, Any]:
    return {
        "battle_cards": _BATTLE_CARDS,
        "usage_note_en": (
            "These are structured talking points for 1-on-1 competitive conversations. "
            "Adapt to the specific prospect context before use."
        ),
        "usage_note_ar": (
            "هذه نقاط نقاش منظمة للمحادثات التنافسية الفردية. "
            "تكيّفها مع سياق العميل المحدد قبل الاستخدام."
        ),
        "governance_decision": "ALLOW_WITH_REVIEW",
    }


@router.post("/positioning-brief", summary="Generate tailored competitive positioning brief")
async def generate_positioning_brief(body: PositioningBriefRequest) -> dict[str, Any]:
    category = _COMPETITOR_CATEGORIES.get(body.competitor_category)
    if not category:
        raise HTTPException(
            status_code=404,
            detail=(
                f"Competitor category '{body.competitor_category}' not found. "
                f"Valid: {list(_COMPETITOR_CATEGORIES.keys())}"
            ),
        )

    pain_summary = "; ".join(body.client_pain_points[:5])

    tailored_pitch_en = (
        f"For {body.client_name}, the core argument against {category['name_en']} is clear: "
        f"{category['dealix_advantage_en']} "
        f"Given your identified challenges — {pain_summary} — "
        f"and a deal size of SAR {body.deal_size_sar:,.0f}, "
        f"Dealix delivers measurable ROI within the first 30 days. "
        f"Start with a SAR 499 sprint to prove value before any long-term commitment."
    )

    key_differentiators = [
        "Native Arabic NLP — no translation layer",
        "Hijri calendar support built-in",
        "ZATCA Phase 1 and Phase 2 compliance",
        "Vision 2030 KPI alignment out of the box",
        "7-day deployment vs. months for alternatives",
        "PDPL-compliant Saudi data residency",
    ]

    next_action_en = (
        f"Book a 30-minute diagnostic call with {body.client_name} to surface "
        f"the specific gaps the current solution leaves unaddressed. "
        f"Come prepared with the win conditions: {', '.join(category['win_conditions'])}."
    )
    next_action_ar = (
        f"احجز مكالمة تشخيص لمدة 30 دقيقة مع {body.client_name} لكشف "
        f"الفجوات المحددة التي يتركها الحل الحالي دون معالجة. "
        f"استعد بشروط الفوز: {', '.join(category['win_conditions'])}."
    )

    return {
        "competitor_category": body.competitor_category,
        "competitor_name_en": category["name_en"],
        "competitor_name_ar": category["name_ar"],
        "client_name": body.client_name,
        "deal_size_sar": body.deal_size_sar,
        "advantage_summary_en": category["dealix_advantage_en"],
        "advantage_summary_ar": category["dealix_advantage_ar"],
        "tailored_pitch_en": tailored_pitch_en,
        "key_differentiators": key_differentiators,
        "objection_response_en": category.get("objection_response_en", ""),
        "win_conditions": category["win_conditions"],
        "next_action_en": next_action_en,
        "next_action_ar": next_action_ar,
        "disclaimer_en": (
            "This brief is a starting point for conversation preparation. "
            "Adapt all figures and claims to verified client data before presenting."
        ),
        "disclaimer_ar": (
            "هذا الموجز نقطة انطلاق للتحضير للمحادثة. "
            "تكيّف جميع الأرقام والادعاءات ببيانات العميل الموثقة قبل التقديم."
        ),
        "governance_decision": "APPROVAL_FIRST",
    }
