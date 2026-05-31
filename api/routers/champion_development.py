"""
Champion development framework for Dealix Saudi B2B sales team.

All data is static. No LLM calls, no external API calls. Bilingual (EN/AR).
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel, Field, model_validator

router = APIRouter(prefix="/api/v1/champion-development", tags=["Sales"])

_ALLOW = "ALLOW_WITH_REVIEW"

# ---------------------------------------------------------------------------
# Champion archetypes
# ---------------------------------------------------------------------------

_CHAMPION_PROFILES: dict[str, dict[str, Any]] = {
    "operational_owner": {
        "id": "operational_owner",
        "name_en": "Operational Owner",
        "name_ar": "صاحب العملية",
        "description_en": (
            "Runs day-to-day operations; cares about time savings and error reduction. "
            "Saudi context: typically a department manager or team lead."
        ),
        "description_ar": (
            "يُدير العمليات اليومية؛ يهتم بتوفير الوقت وتقليل الأخطاء. "
            "السياق السعودي: في الغالب مدير قسم أو قائد فريق."
        ),
        "primary_motivators_en": ["Time savings", "Error reduction", "Team productivity"],
        "primary_motivators_ar": ["توفير الوقت", "تقليل الأخطاء", "إنتاجية الفريق"],
        "engagement_tip_en": (
            "Lead with operational pain points and demonstrate how daily workflows improve. "
            "Show before-and-after process maps."
        ),
        "engagement_tip_ar": (
            "ابدأ بنقاط الألم التشغيلية وأظهر كيف تتحسن سير العمل اليومية. "
            "اعرض خرائط العمليات قبل وبعد."
        ),
    },
    "technology_lead": {
        "id": "technology_lead",
        "name_en": "Technology Lead",
        "name_ar": "قائد التقنية",
        "description_en": (
            "IT or IS director; cares about integration, security, and PDPL compliance. "
            "Will scrutinize data handling, API architecture, and audit trails."
        ),
        "description_ar": (
            "مدير تقنية المعلومات أو نظم المعلومات؛ يهتم بالتكامل والأمان وامتثال PDPL. "
            "يُدقق في التعامل مع البيانات وبنية API ومسارات التدقيق."
        ),
        "primary_motivators_en": ["System integration", "Security posture", "PDPL compliance"],
        "primary_motivators_ar": ["تكامل الأنظمة", "وضع الأمان", "امتثال PDPL"],
        "engagement_tip_en": (
            "Share technical architecture diagrams, PDPL data-processing agreements, "
            "and security certifications upfront."
        ),
        "engagement_tip_ar": (
            "شارك مخططات البنية التقنية واتفاقيات معالجة بيانات PDPL "
            "وشهادات الأمان مسبقاً."
        ),
    },
    "financial_buyer": {
        "id": "financial_buyer",
        "name_en": "Financial Buyer",
        "name_ar": "المشتري المالي",
        "description_en": (
            "CFO or finance director; cares about ROI, ZATCA compliance, and SAR cash flow. "
            "Decision framing must be in financial terms with clear payback periods."
        ),
        "description_ar": (
            "المدير المالي أو مدير المالية؛ يهتم بعائد الاستثمار وامتثال هيئة الزكاة والتدفق النقدي. "
            "يجب صياغة القرار بمصطلحات مالية مع فترات استرداد واضحة."
        ),
        "primary_motivators_en": ["ROI", "ZATCA compliance", "SAR cash-flow optimization"],
        "primary_motivators_ar": ["عائد الاستثمار", "امتثال هيئة الزكاة", "تحسين التدفق النقدي"],
        "engagement_tip_en": (
            "Present a structured ROI model showing payback period, NPV, and ZATCA fine avoidance. "
            "Use SAR figures; avoid USD or percentage-only framing."
        ),
        "engagement_tip_ar": (
            "قدّم نموذج عائد استثمار منظّم يُظهر فترة الاسترداد وصافي القيمة الحالية وتجنب غرامات هيئة الزكاة. "
            "استخدم أرقاماً بالريال؛ تجنب الدولار أو الصياغة بالنسبة المئوية فقط."
        ),
    },
    "executive_sponsor": {
        "id": "executive_sponsor",
        "name_en": "Executive Sponsor",
        "name_ar": "الراعي التنفيذي",
        "description_en": (
            "CEO or COO; cares about Vision 2030 alignment, Saudization, and strategic positioning. "
            "Engages at the level of macro outcomes, not feature details."
        ),
        "description_ar": (
            "الرئيس التنفيذي أو المدير التشغيلي؛ يهتم بتوافق رؤية 2030 والسعودة والتموضع الاستراتيجي. "
            "يتفاعل على مستوى النتائج الكلية وليس تفاصيل المميزات."
        ),
        "primary_motivators_en": ["Vision 2030 alignment", "Saudization", "Strategic positioning"],
        "primary_motivators_ar": ["توافق رؤية 2030", "السعودة", "التموضع الاستراتيجي"],
        "engagement_tip_en": (
            "Open with the Vision 2030 digital transformation narrative. "
            "Connect Dealix to Saudization KPIs and national competitiveness."
        ),
        "engagement_tip_ar": (
            "ابدأ بسردية التحول الرقمي لرؤية 2030. "
            "اربط ديليكس بمؤشرات السعودة والتنافسية الوطنية."
        ),
    },
}

_VALID_ARCHETYPES: frozenset[str] = frozenset(_CHAMPION_PROFILES.keys())

# ---------------------------------------------------------------------------
# Champion development stages
# ---------------------------------------------------------------------------

_CHAMPION_DEVELOPMENT_STAGES: list[dict[str, Any]] = [
    {
        "stage": "identify",
        "name_en": "Identify",
        "name_ar": "التعرف",
        "description_en": (
            "Find the internal person most affected by the problem, not the most senior."
        ),
        "description_ar": (
            "ابحث عن الشخص الداخلي الأكثر تأثراً بالمشكلة، وليس الأعلى مرتبة."
        ),
        "activities_en": [
            "Map the org chart to find the operational pain owner.",
            "Review job postings and LinkedIn bios for keywords matching your solution.",
            "Ask the inbound contact: 'Who loses the most time to this problem every day?'",
        ],
        "activities_ar": [
            "ارسم خريطة الهيكل التنظيمي للعثور على صاحب الألم التشغيلي.",
            "راجع إعلانات الوظائف وتعريفات LinkedIn بحثاً عن كلمات مفتاحية تتطابق مع حلك.",
            "اسأل جهة الاتصال الواردة: 'من يخسر أكثر وقت يومياً بسبب هذه المشكلة؟'",
        ],
    },
    {
        "stage": "educate",
        "name_en": "Educate",
        "name_ar": "التثقيف",
        "description_en": (
            "Share industry insights, Saudi B2B benchmarks, ZATCA and PDPL context."
        ),
        "description_ar": (
            "شارك رؤى الصناعة ومعايير الأعمال السعودية وسياق هيئة الزكاة وPDPL."
        ),
        "activities_en": [
            "Share a 1-page Saudi B2B benchmark report relevant to their sector.",
            "Explain ZATCA Phase 2 requirements and how peers are responding.",
            "Walk through the PDPL personal data framework and its operational implications.",
        ],
        "activities_ar": [
            "شارك تقرير معيار أعمال سعودي بصفحة واحدة يتعلق بقطاعهم.",
            "اشرح متطلبات المرحلة الثانية من هيئة الزكاة وكيف يتعامل معها الأقران.",
            "استعرض إطار بيانات PDPL الشخصية وتداعياته التشغيلية.",
        ],
    },
    {
        "stage": "arm",
        "name_en": "Arm",
        "name_ar": "التمكين",
        "description_en": (
            "Give them the internal pitch deck, ROI calculator, and proof pack."
        ),
        "description_ar": (
            "امنحهم العرض التقديمي الداخلي وحاسبة عائد الاستثمار وحزمة الإثبات."
        ),
        "activities_en": [
            "Provide a branded, editable internal presentation for their leadership review.",
            "Share a pre-filled ROI calculator with their industry benchmarks.",
            "Deliver a Proof Pack from a comparable Saudi client (anonymized as needed).",
        ],
        "activities_ar": [
            "قدّم عرضاً تقديمياً داخلياً قابلاً للتحرير لمراجعة قيادتهم.",
            "شارك حاسبة عائد الاستثمار مع معايير قطاعهم مُعبأة مسبقاً.",
            "سلّم حزمة إثبات من عميل سعودي مماثل (مُخفى عند الحاجة).",
        ],
    },
    {
        "stage": "test",
        "name_en": "Test",
        "name_ar": "الاختبار",
        "description_en": (
            "Ask them to arrange a senior sponsor meeting to gauge their real influence."
        ),
        "description_ar": (
            "اطلب منهم ترتيب اجتماع مع راعٍ أعلى لقياس نفوذهم الفعلي."
        ),
        "activities_en": [
            "Request an introduction to the economic buyer or executive sponsor.",
            "Ask the champion to present one internal concept before the formal pitch.",
        ],
        "activities_ar": [
            "اطلب تعريفاً بالمشتري الاقتصادي أو الراعي التنفيذي.",
            "اطلب من البطل تقديم مفهوم داخلي واحد قبل العرض الرسمي.",
        ],
    },
    {
        "stage": "elevate",
        "name_en": "Elevate",
        "name_ar": "الارتقاء",
        "description_en": (
            "Co-present at the QBR and create shared success visible to their leadership."
        ),
        "description_ar": (
            "شارك في تقديم مراجعة الربع السنوي وأنشئ نجاحاً مشتركاً مرئياً لقيادتهم."
        ),
        "activities_en": [
            "Co-present the 90-day ROI summary at the client's internal QBR.",
            "Nominate the champion for a joint case study or reference story.",
        ],
        "activities_ar": [
            "شارك في تقديم ملخص عائد الاستثمار لـ 90 يوماً في مراجعة الربع السنوي الداخلية للعميل.",
            "رشّح البطل لدراسة حالة مشتركة أو قصة مرجعية.",
        ],
    },
]

# ---------------------------------------------------------------------------
# Champion health indicators
# ---------------------------------------------------------------------------

_CHAMPION_HEALTH_INDICATORS: dict[str, list[str]] = {
    "strong": [
        "Responds within 24 hours to messages and meeting requests.",
        "Shares internal org chart and introduces relevant stakeholders.",
        "Facilitates an introduction to a senior sponsor or economic buyer.",
        "Provides or commits to providing data source access.",
        "Advocates for Dealix in meetings where Dealix is not present.",
    ],
    "weak": [
        "Filters all communication and blocks access to senior stakeholders.",
        "Cannot secure budget approval or confirm internal support.",
        "Senior stakeholder is never available despite repeated requests.",
        "Goes quiet after the proposal is submitted with no engagement.",
        "Introduces Dealix only to junior or non-decision-making contacts.",
    ],
}

# ---------------------------------------------------------------------------
# Pydantic models
# ---------------------------------------------------------------------------


class ChampionAssessmentInput(BaseModel):
    contact_name: str = Field(..., min_length=1, description="Full name of the champion contact")
    contact_title: str = Field(..., min_length=1, description="Job title of the champion contact")
    archetype_guess: str = Field(
        ...,
        description=(
            "One of: operational_owner | technology_lead | financial_buyer | executive_sponsor"
        ),
    )
    has_senior_access: bool = Field(
        ..., description="Has this contact arranged access to a senior stakeholder?"
    )
    data_access_committed: bool = Field(
        ..., description="Has this contact committed to connecting required data sources?"
    )
    response_time_hours: float = Field(
        ..., ge=0, description="Average response time to messages in hours"
    )
    introduced_senior: bool = Field(
        ...,
        description="Has this contact made a direct introduction to a senior or executive stakeholder?",
    )

    @model_validator(mode="after")
    def validate_archetype(self) -> "ChampionAssessmentInput":
        if self.archetype_guess not in _VALID_ARCHETYPES:
            raise ValueError(
                f"archetype_guess '{self.archetype_guess}' is not valid. "
                f"Valid values: {sorted(_VALID_ARCHETYPES)}"
            )
        return self


# ---------------------------------------------------------------------------
# Pure-function business logic
# ---------------------------------------------------------------------------


def _assess_champion(inp: ChampionAssessmentInput) -> dict[str, Any]:
    """
    Compute a champion health score 0-100 and return assessment results.

    Scoring:
      has_senior_access:       +25
      data_access_committed:   +20
      response_time_hours:
        <= 24h                 +20
        <= 48h                 +10
        > 48h                  +0
      introduced_senior:       +20
      max possible:            85 (normalized to 100 for output)

    Health labels:
      Strong   >= 70
      Moderate  40-69
      Weak      < 40
    """
    score = 0

    if inp.has_senior_access:
        score += 25
    if inp.data_access_committed:
        score += 20
    if inp.response_time_hours <= 24:
        score += 20
    elif inp.response_time_hours <= 48:
        score += 10
    if inp.introduced_senior:
        score += 20

    # Normalize to 100 (max raw = 85, but we keep the scale as-is for transparency)
    health_score = min(score, 100)

    if health_score >= 70:
        health_label = "Strong"
        health_label_ar = "قوي"
        recommended_actions_en = [
            "Schedule a co-presentation with the champion at the next senior leadership meeting.",
            "Provide an editable internal case study or win story the champion can circulate.",
            "Propose a shared success metric that makes the champion's contribution visible to their leadership.",
        ]
        recommended_actions_ar = [
            "جدوّل عرضاً مشتركاً مع البطل في اجتماع القيادة العليا التالي.",
            "قدّم دراسة حالة داخلية قابلة للتحرير أو قصة نجاح يمكن للبطل توزيعها.",
            "اقترح مقياس نجاح مشترك يجعل مساهمة البطل مرئية لقيادته.",
        ]
    elif health_score >= 40:
        health_label = "Moderate"
        health_label_ar = "متوسط"
        recommended_actions_en = [
            "Explicitly ask the champion to arrange a meeting with the economic buyer within 14 days.",
            "Share a pre-built internal briefing deck to lower the effort barrier for escalation.",
            "Confirm whether data source access is blocked by IT policy or personal hesitation.",
        ]
        recommended_actions_ar = [
            "اطلب صراحةً من البطل ترتيب اجتماع مع المشتري الاقتصادي خلال 14 يوماً.",
            "شارك عرضاً تقديمياً داخلياً جاهزاً لتقليل عائق الجهد للتصعيد.",
            "تأكد مما إذا كان الوصول إلى مصادر البيانات محجوباً بسبب سياسة تقنية أو تردد شخصي.",
        ]
    else:
        health_label = "Weak"
        health_label_ar = "ضعيف"
        recommended_actions_en = [
            "Pause commercial advancement and reassess whether this contact is the real champion.",
            "Map the organization independently to identify an alternative internal advocate.",
            "Set a 30-day re-engagement checkpoint; if senior access is not secured, revise the strategy.",
        ]
        recommended_actions_ar = [
            "أوقف التقدم التجاري وأعد تقييم ما إذا كان هذا الاتصال هو البطل الحقيقي.",
            "ارسم خريطة المنظمة باستقلالية لتحديد مناصر داخلي بديل.",
            "حدد نقطة إعادة تفاعل بعد 30 يوماً؛ إن لم يُؤمَّن الوصول للمستوى الأعلى، أعد النظر في الاستراتيجية.",
        ]

    archetype_profile = _CHAMPION_PROFILES[inp.archetype_guess]

    return {
        "contact_name": inp.contact_name,
        "contact_title": inp.contact_title,
        "archetype_guess": inp.archetype_guess,
        "archetype_profile": archetype_profile,
        "health_score": health_score,
        "health_label": health_label,
        "health_label_ar": health_label_ar,
        "score_breakdown": {
            "has_senior_access": 25 if inp.has_senior_access else 0,
            "data_access_committed": 20 if inp.data_access_committed else 0,
            "response_time_hours_points": (
                20 if inp.response_time_hours <= 24
                else 10 if inp.response_time_hours <= 48
                else 0
            ),
            "introduced_senior": 20 if inp.introduced_senior else 0,
        },
        "recommended_actions_en": recommended_actions_en,
        "recommended_actions_ar": recommended_actions_ar,
        "governance_decision": _ALLOW,
    }


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------


@router.get("/profiles", summary="All 4 champion archetypes with bilingual descriptions")
async def list_profiles() -> dict[str, Any]:
    return {
        "profiles": list(_CHAMPION_PROFILES.values()),
        "count": len(_CHAMPION_PROFILES),
        "governance_decision": _ALLOW,
    }


@router.get(
    "/development-stages",
    summary="All 5 champion development stages with activities",
)
async def list_development_stages() -> dict[str, Any]:
    return {
        "stages": _CHAMPION_DEVELOPMENT_STAGES,
        "count": len(_CHAMPION_DEVELOPMENT_STAGES),
        "governance_decision": _ALLOW,
    }


@router.get(
    "/health-indicators",
    summary="Strong and weak champion health indicator lists",
)
async def list_health_indicators() -> dict[str, Any]:
    return {
        "health_indicators": _CHAMPION_HEALTH_INDICATORS,
        "strong_count": len(_CHAMPION_HEALTH_INDICATORS["strong"]),
        "weak_count": len(_CHAMPION_HEALTH_INDICATORS["weak"]),
        "governance_decision": _ALLOW,
    }


@router.post("/assess", summary="Assess a champion's health and return recommended actions")
async def assess_champion(body: ChampionAssessmentInput) -> dict[str, Any]:
    return _assess_champion(body)
