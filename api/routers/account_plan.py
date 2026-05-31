"""
Strategic account planning framework for Dealix Saudi B2B enterprise deals.

All data is static. No LLM calls, no external API calls. Bilingual (EN/AR).
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter(prefix="/api/v1/account-plan", tags=["Sales"])

# ---------------------------------------------------------------------------
# Account plan template — blank skeleton with section descriptions
# ---------------------------------------------------------------------------

_ACCOUNT_PLAN_TEMPLATE: dict[str, Any] = {
    "executive_summary": {
        "description_en": "Client overview, strategic objective, and 12-month revenue target.",
        "description_ar": "نظرة عامة على العميل، الهدف الاستراتيجي، وهدف الإيرادات لـ 12 شهراً.",
        "fields": [
            "client_name",
            "client_sector",
            "strategic_objective_en",
            "strategic_objective_ar",
            "revenue_target_12mo_sar",
            "account_owner",
            "plan_date",
        ],
    },
    "stakeholder_map": {
        "description_en": (
            "Map the four key stakeholder roles: economic buyer, champion, influencer, and blocker. "
            "Each role requires a tailored engagement strategy."
        ),
        "description_ar": (
            "رسم خريطة الأدوار الأربعة للمعنيين: المشتري الاقتصادي، البطل، المؤثر، والمعرقل. "
            "كل دور يتطلب استراتيجية تفاعل مخصصة."
        ),
        "roles": {
            "economic_buyer": {
                "description_en": "Decision-maker with budget authority.",
                "description_ar": "صاحب القرار الذي يملك صلاحية الميزانية.",
                "engagement_strategy_en": "Speak ROI, compliance, and Vision 2030 KPIs.",
                "engagement_strategy_ar": "تحدث بلغة العائد على الاستثمار، الامتثال، ومؤشرات رؤية 2030.",
            },
            "champion": {
                "description_en": "Internal advocate who believes in Dealix's value.",
                "description_ar": "المدافع الداخلي الذي يؤمن بقيمة ديليكس.",
                "engagement_strategy_en": (
                    "Enable with demos, data, and ready-to-present decks. "
                    "Make the champion the hero of the internal story."
                ),
                "engagement_strategy_ar": (
                    "دعّمه بالعروض التوضيحية والبيانات والعروض الجاهزة للتقديم. "
                    "اجعل البطل هو بطل القصة الداخلية."
                ),
            },
            "influencer": {
                "description_en": "Subject-matter expert or department head who shapes opinion.",
                "description_ar": "خبير متخصص أو رئيس قسم يصوغ الرأي.",
                "engagement_strategy_en": "Address technical or compliance-specific concerns directly.",
                "engagement_strategy_ar": "تعامل مع المخاوف التقنية أو المتعلقة بالامتثال مباشرة.",
            },
            "blocker": {
                "description_en": "Stakeholder with incentive to resist adoption.",
                "description_ar": "معني لديه حافز لمقاومة التبني.",
                "engagement_strategy_en": (
                    "Understand root concern (job security, vendor preference, risk aversion). "
                    "Involve early; give them a visible role in the success metric."
                ),
                "engagement_strategy_ar": (
                    "افهم المخاوف الجذرية (أمان الوظيفة، تفضيل مورد، تجنب المخاطر). "
                    "اشركه مبكراً؛ امنحه دوراً واضحاً في مقياس النجاح."
                ),
            },
        },
    },
    "value_hypothesis": {
        "description_en": (
            "Document the pain identified, how Dealix fits as a solution, "
            "the estimated ROI, and the link to Vision 2030 objectives."
        ),
        "description_ar": (
            "وثّق الألم المحدد، وكيف يناسب ديليكس كحل، "
            "وعائد الاستثمار المقدر، والارتباط بأهداف رؤية 2030."
        ),
        "fields": [
            "pain_identified",
            "solution_fit_en",
            "solution_fit_ar",
            "roi_estimate_sar",
            "roi_timeframe_days",
            "vision_2030_link_en",
            "vision_2030_link_ar",
        ],
    },
    "milestones": {
        "description_en": "30/60/90-day action plan with specific deliverables per phase.",
        "description_ar": "خطة عمل 30/60/90 يوماً مع مخرجات محددة لكل مرحلة.",
        "phases": {
            "day_30": {
                "label_en": "Foundation",
                "label_ar": "التأسيس",
                "focus_en": "Onboarding, baseline data capture, first value demonstration.",
                "focus_ar": "الإعداد، التقاط البيانات الأساسية، أول إثبات للقيمة.",
            },
            "day_60": {
                "label_en": "Activation",
                "label_ar": "التفعيل",
                "focus_en": "Full feature adoption, stakeholder alignment, first ROI measurement.",
                "focus_ar": "تبني الميزات الكاملة، محاذاة أصحاب المصلحة، أول قياس لعائد الاستثمار.",
            },
            "day_90": {
                "label_en": "Value Realization",
                "label_ar": "تحقيق القيمة",
                "focus_en": "Documented ROI, expansion conversation, renewal path confirmed.",
                "focus_ar": "عائد استثمار موثق، محادثة التوسع، مسار التجديد مؤكد.",
            },
        },
    },
    "risk_register": {
        "description_en": "Four standard risks tracked for every enterprise account.",
        "description_ar": "أربعة مخاطر قياسية يتم تتبعها لكل حساب مؤسسي.",
    },
    "success_metrics": {
        "description_en": "Five KPIs used to measure account health and Dealix ROI.",
        "description_ar": "خمسة مؤشرات أداء رئيسية لقياس صحة الحساب وعائد استثمار ديليكس.",
        "kpis": [
            {
                "name_en": "Pipeline Velocity",
                "name_ar": "سرعة خط الأنابيب",
                "definition_en": "Average days from lead creation to closed-won.",
                "definition_ar": "متوسط الأيام من إنشاء العميل المحتمل إلى الإغلاق.",
                "target": "Reduce by 20% within 90 days",
            },
            {
                "name_en": "Net Promoter Score (NPS)",
                "name_ar": "مؤشر صافي الترويج",
                "definition_en": "Client likelihood to recommend Dealix (0–10 scale).",
                "definition_ar": "احتمالية توصية العميل بديليكس (مقياس 0–10).",
                "target": "NPS >= 8 at 60-day mark",
            },
            {
                "name_en": "Product Adoption %",
                "name_ar": "نسبة تبني المنتج",
                "definition_en": "Percentage of licensed users active in the last 30 days.",
                "definition_ar": "نسبة المستخدمين المرخصين النشطين خلال آخر 30 يوماً.",
                "target": ">= 80% by day 60",
            },
            {
                "name_en": "ZATCA Compliance %",
                "name_ar": "نسبة الامتثال لهيئة الزكاة",
                "definition_en": "Percentage of invoices/transactions processed through ZATCA-compliant flow.",
                "definition_ar": "نسبة الفواتير/المعاملات المعالجة عبر التدفق المتوافق مع هيئة الزكاة.",
                "target": "100% by day 30",
            },
            {
                "name_en": "ROI Realized",
                "name_ar": "عائد الاستثمار المحقق",
                "definition_en": "Documented revenue impact or cost savings attributable to Dealix.",
                "definition_ar": "أثر الإيرادات الموثق أو توفير التكاليف المنسوب لديليكس.",
                "target": "3x annual contract value within 12 months",
            },
        ],
    },
}

# ---------------------------------------------------------------------------
# Standard risk register entries
# ---------------------------------------------------------------------------

_STANDARD_RISKS: list[dict[str, Any]] = [
    {
        "id": "risk_champion_leaves",
        "risk_en": "Champion leaves the organization",
        "risk_ar": "مغادرة البطل الداخلي للمؤسسة",
        "probability": "medium",
        "impact": "high",
        "mitigation_en": (
            "Map at least two internal champions before the 30-day mark. "
            "Ensure the economic buyer has direct visibility into Dealix value metrics. "
            "Document wins early so institutional knowledge survives personnel changes."
        ),
        "mitigation_ar": (
            "حدد اثنين على الأقل من الأبطال الداخليين قبل اليوم الثلاثين. "
            "تأكد من أن المشتري الاقتصادي لديه رؤية مباشرة لمقاييس قيمة ديليكس. "
            "وثّق الإنجازات مبكراً حتى تبقى المعرفة المؤسسية عند تغيير الأفراد."
        ),
    },
    {
        "id": "risk_budget_freeze",
        "risk_en": "Budget freeze or procurement hold",
        "risk_ar": "تجميد الميزانية أو وقف المشتريات",
        "probability": "medium",
        "impact": "high",
        "mitigation_en": (
            "Secure a signed multi-year contract before Q4. "
            "Align renewal timing with the client's fiscal year start (often Q1 or post-Ramadan). "
            "Pre-position Dealix as a cost-saving tool, not an additional expense."
        ),
        "mitigation_ar": (
            "احصل على عقد متعدد السنوات موقّع قبل الربع الرابع. "
            "اجعل توقيت التجديد متوافقاً مع بداية السنة المالية للعميل (غالباً الربع الأول أو ما بعد رمضان). "
            "ضع ديليكس مسبقاً كأداة لتوفير التكاليف، وليس نفقة إضافية."
        ),
    },
    {
        "id": "risk_competitor_poc",
        "risk_en": "Competitor initiates a competing proof of concept",
        "risk_ar": "قيام منافس بإطلاق إثبات مفهوم منافس",
        "probability": "low",
        "impact": "high",
        "mitigation_en": (
            "Accelerate time-to-value: deliver first measurable result within 7 days of go-live. "
            "Lock in the champion with a documented wins log. "
            "Run a competitive positioning brief before the competitor POC begins."
        ),
        "mitigation_ar": (
            "سرّع الوصول إلى القيمة: حقق أول نتيجة قابلة للقياس خلال 7 أيام من الإطلاق. "
            "احتفظ بالبطل من خلال سجل إنجازات موثق. "
            "نفّذ موجز التموضع التنافسي قبل أن يبدأ إثبات المفهوم المنافس."
        ),
    },
    {
        "id": "risk_ramadan_timing",
        "risk_en": "Ramadan timing slows decision-making or onboarding",
        "risk_ar": "توقيت رمضان يبطئ اتخاذ القرار أو الإعداد",
        "probability": "high",
        "impact": "medium",
        "mitigation_en": (
            "Avoid scheduling go-live or major milestones in the last two weeks of Shaban or the first week of Ramadan. "
            "Use Ramadan as a relationship-deepening period — no hard selling. "
            "Plan for an 18-day effective working window inside Ramadan (reduced hours). "
            "Target contract signature and kickoff before the 15th of Shaban."
        ),
        "mitigation_ar": (
            "تجنب جدولة الإطلاق أو المعالم الرئيسية في الأسبوعين الأخيرين من شعبان أو الأسبوع الأول من رمضان. "
            "استخدم رمضان فترة لتعميق العلاقة — لا بيع قسري. "
            "خطط لنافذة عمل فعلية مدتها 18 يوماً داخل رمضان (ساعات عمل مخفضة). "
            "استهدف توقيع العقد والانطلاق قبل الخامس عشر من شعبان."
        ),
    },
]

# ---------------------------------------------------------------------------
# Account tiers
# ---------------------------------------------------------------------------

_ACCOUNT_TIERS: dict[str, dict[str, Any]] = {
    "strategic": {
        "tier_id": "strategic",
        "name_en": "Strategic",
        "name_ar": "الاستراتيجي",
        "annual_revenue_sar_min": 50_000,
        "annual_revenue_sar_max": None,
        "criteria_en": "SAR 50,000+ per year",
        "criteria_ar": "أكثر من 50,000 ريال سنوياً",
        "benefits_en": [
            "Quarterly executive reviews",
            "Dedicated Customer Success Manager",
            "Custom AI roadmap aligned to client goals",
            "Priority support SLA (4-hour response)",
            "Co-marketing opportunities",
        ],
        "benefits_ar": [
            "مراجعات تنفيذية ربع سنوية",
            "مدير نجاح عملاء مخصص",
            "خارطة طريق AI مخصصة تتوافق مع أهداف العميل",
            "SLA دعم ذو أولوية (استجابة خلال 4 ساعات)",
            "فرص التسويق المشترك",
        ],
        "cadence_en": "Quarterly executive review + monthly CSM check-in",
        "cadence_ar": "مراجعة تنفيذية ربع سنوية + متابعة شهرية مع مدير نجاح العملاء",
    },
    "growth": {
        "tier_id": "growth",
        "name_en": "Growth",
        "name_ar": "النمو",
        "annual_revenue_sar_min": 20_000,
        "annual_revenue_sar_max": 50_000,
        "criteria_en": "SAR 20,000–50,000 per year",
        "criteria_ar": "من 20,000 إلى 50,000 ريال سنوياً",
        "benefits_en": [
            "Monthly check-ins with CSM",
            "Standard playbooks and templates",
            "Expansion path planning",
            "Business review at 6 and 12 months",
        ],
        "benefits_ar": [
            "متابعة شهرية مع مدير نجاح العملاء",
            "أدلة وقوالب قياسية",
            "تخطيط مسار التوسع",
            "مراجعة أعمال في الشهر السادس والثاني عشر",
        ],
        "cadence_en": "Monthly CSM check-in + bi-annual business review",
        "cadence_ar": "متابعة شهرية مع مدير نجاح العملاء + مراجعة أعمال نصف سنوية",
    },
    "standard": {
        "tier_id": "standard",
        "name_en": "Standard",
        "name_ar": "القياسي",
        "annual_revenue_sar_min": 5_000,
        "annual_revenue_sar_max": 20_000,
        "criteria_en": "SAR 5,000–20,000 per year",
        "criteria_ar": "من 5,000 إلى 20,000 ريال سنوياً",
        "benefits_en": [
            "Automated health scoring",
            "Self-serve knowledge base and onboarding content",
            "Upsell triggers based on usage signals",
            "Email support with 24-hour SLA",
        ],
        "benefits_ar": [
            "تقييم صحة تلقائي",
            "قاعدة معرفة ومحتوى إعداد ذاتي الخدمة",
            "محفزات البيع الإضافي بناءً على إشارات الاستخدام",
            "دعم بريد إلكتروني مع SLA خلال 24 ساعة",
        ],
        "cadence_en": "Automated health alerts + quarterly email touchpoint",
        "cadence_ar": "تنبيهات صحة تلقائية + نقطة تواصل بريدية ربع سنوية",
    },
}

# ---------------------------------------------------------------------------
# Stage-specific milestone templates
# ---------------------------------------------------------------------------

_STAGE_MILESTONES: dict[str, dict[str, list[str]]] = {
    "onboarding": {
        "day_30": [
            "Complete data integration and source configuration",
            "Train all primary users on core workflows",
            "Capture baseline KPIs for pipeline velocity and adoption",
            "Confirm ZATCA compliance configuration",
        ],
        "day_60": [
            "Full team active on platform (adoption >= 80%)",
            "First AI-generated pipeline report reviewed with champion",
            "Stakeholder alignment meeting with economic buyer",
            "Identify expansion use cases",
        ],
        "day_90": [
            "Document first measurable ROI outcome",
            "Present value summary to economic buyer",
            "Confirm renewal intent and expansion scope",
            "Introduce account tier benefits",
        ],
    },
    "value_realization": {
        "day_30": [
            "Review pipeline velocity improvement vs. baseline",
            "Identify underutilized features with champion",
            "Schedule executive briefing on ROI metrics",
        ],
        "day_60": [
            "Publish internal case study or win story with champion",
            "Expand usage to second department or business unit",
            "Conduct NPS survey",
        ],
        "day_90": [
            "Present 6-month ROI report to economic buyer",
            "Discuss multi-year contract or expansion tier",
            "Co-create Vision 2030 alignment narrative",
        ],
    },
    "expansion": {
        "day_30": [
            "Map new department or product use case requirements",
            "Introduce new stakeholders to Dealix",
            "Confirm expanded data source integrations",
        ],
        "day_60": [
            "Launch expanded module with new team",
            "Update account plan with revised revenue target",
            "Schedule cross-sell demo for additional capabilities",
        ],
        "day_90": [
            "Measure incremental ROI from expansion",
            "Formalize expanded contract scope",
            "Nominate account as strategic tier if revenue qualifies",
        ],
    },
    "renewal": {
        "day_30": [
            "Run full account health review",
            "Resolve any open support or adoption issues",
            "Prepare renewal proposal with updated ROI figures",
        ],
        "day_60": [
            "Present renewal proposal to economic buyer",
            "Address objections with documented value evidence",
            "Identify expansion or upsell opportunity to include in renewal",
        ],
        "day_90": [
            "Close renewal and execute updated contract",
            "Celebrate renewal with champion (internal recognition)",
            "Set 12-month plan for next cycle",
        ],
    },
}


# ---------------------------------------------------------------------------
# Pydantic models
# ---------------------------------------------------------------------------


class AccountPlanInput(BaseModel):
    client_name: str = Field(..., max_length=120)
    client_sector: str = Field(..., max_length=120)
    estimated_annual_revenue_sar: float = Field(..., gt=0)
    champion_name: str = Field(..., max_length=120)
    champion_title: str = Field(..., max_length=120)
    identified_pains: list[str] = Field(..., min_length=1, max_length=10)
    current_stage: str = Field(
        ...,
        description="One of: onboarding, value_realization, expansion, renewal",
    )
    months_as_client: int = Field(..., ge=0)


# ---------------------------------------------------------------------------
# Pure-function business logic
# ---------------------------------------------------------------------------

_VALID_STAGES: frozenset[str] = frozenset(
    {"onboarding", "value_realization", "expansion", "renewal"}
)


def _determine_tier(annual_revenue_sar: float) -> str:
    """Return the account tier ID for a given annual revenue figure."""
    if annual_revenue_sar >= 50_000:
        return "strategic"
    if annual_revenue_sar >= 20_000:
        return "growth"
    return "standard"


def _build_account_plan(inp: AccountPlanInput) -> dict[str, Any]:
    """
    Build a structured account plan dict from AccountPlanInput.

    Determines account tier, populates stage-specific milestones,
    generates a risk register with client-specific mitigation context,
    and returns all plan sections.
    """
    tier_id = _determine_tier(inp.estimated_annual_revenue_sar)
    tier = _ACCOUNT_TIERS[tier_id]

    stage = inp.current_stage
    milestone_actions = _STAGE_MILESTONES.get(stage, _STAGE_MILESTONES["onboarding"])

    pain_summary = "; ".join(inp.identified_pains[:5])

    plan: dict[str, Any] = {
        "executive_summary": {
            "client_name": inp.client_name,
            "client_sector": inp.client_sector,
            "account_tier": tier_id,
            "account_tier_name_en": tier["name_en"],
            "account_tier_name_ar": tier["name_ar"],
            "months_as_client": inp.months_as_client,
            "estimated_annual_revenue_sar": inp.estimated_annual_revenue_sar,
            "strategic_objective_en": (
                f"Grow {inp.client_name} to full platform adoption within 90 days, "
                f"demonstrate measurable ROI, and secure the next contract cycle."
            ),
            "strategic_objective_ar": (
                f"تنمية {inp.client_name} إلى تبني المنصة الكاملة خلال 90 يوماً، "
                f"وإثبات عائد استثمار ملموس، وتأمين دورة العقد التالية."
            ),
            "revenue_target_12mo_sar": round(inp.estimated_annual_revenue_sar * 1.25, 2),
        },
        "stakeholder_map": {
            "champion": {
                "name": inp.champion_name,
                "title": inp.champion_title,
                "role": "champion",
                "engagement_strategy_en": (
                    f"Enable {inp.champion_name} with demos, data, and ready-to-present decks. "
                    f"Make {inp.champion_name} the internal hero of the Dealix story."
                ),
                "engagement_strategy_ar": (
                    f"دعّم {inp.champion_name} بالعروض التوضيحية والبيانات والعروض الجاهزة للتقديم. "
                    f"اجعل {inp.champion_name} البطل الداخلي لقصة ديليكس."
                ),
            },
            "economic_buyer": {
                "name": None,
                "title": None,
                "role": "economic_buyer",
                "engagement_strategy_en": (
                    "Present ROI metrics, ZATCA compliance status, and Vision 2030 KPI alignment "
                    "in every executive touchpoint."
                ),
                "engagement_strategy_ar": (
                    "قدّم مقاييس عائد الاستثمار وحالة الامتثال لهيئة الزكاة وتوافق مؤشرات رؤية 2030 "
                    "في كل نقطة تواصل تنفيذية."
                ),
                "note_en": "Identify and map before 30-day mark.",
                "note_ar": "حدد ورسم الخريطة قبل اليوم الثلاثين.",
            },
            "influencer": {
                "name": None,
                "title": None,
                "role": "influencer",
                "engagement_strategy_en": (
                    "Address technical and compliance concerns directly. "
                    "Involve in ZATCA configuration review."
                ),
                "engagement_strategy_ar": (
                    "تعامل مع المخاوف التقنية والامتثال مباشرة. "
                    "اشرك في مراجعة إعداد هيئة الزكاة."
                ),
                "note_en": "Identify and map before 30-day mark.",
                "note_ar": "حدد ورسم الخريطة قبل اليوم الثلاثين.",
            },
            "blocker": {
                "name": None,
                "title": None,
                "role": "blocker",
                "engagement_strategy_en": (
                    "Identify root concern early. Assign a visible role in the success metric process."
                ),
                "engagement_strategy_ar": (
                    "حدد المخاوف الجذرية مبكراً. امنح دوراً واضحاً في عملية قياس النجاح."
                ),
                "note_en": "Identify and map before 30-day mark.",
                "note_ar": "حدد ورسم الخريطة قبل اليوم الثلاثين.",
            },
        },
        "value_hypothesis": {
            "pain_identified": inp.identified_pains,
            "pain_summary": pain_summary,
            "solution_fit_en": (
                f"Dealix addresses the core pains at {inp.client_name} — {pain_summary} — "
                f"through native Arabic NLP, Hijri calendar support, ZATCA compliance, "
                f"and automated pipeline intelligence."
            ),
            "solution_fit_ar": (
                f"ديليكس يعالج الآلام الجوهرية في {inp.client_name} — {pain_summary} — "
                f"من خلال معالجة اللغة العربية الأصلية، ودعم التقويم الهجري، "
                f"وامتثال هيئة الزكاة، وذكاء خط الأنابيب التلقائي."
            ),
            "roi_estimate_sar": round(inp.estimated_annual_revenue_sar * 3.0, 2),
            "roi_timeframe_days": 90,
            "vision_2030_link_en": (
                "Dealix supports Vision 2030's digital transformation pillar by digitizing "
                "revenue operations, enabling data-driven decisions, and building Saudi-native "
                "AI capabilities for the {sector} sector.".format(sector=inp.client_sector)
            ),
            "vision_2030_link_ar": (
                "يدعم ديليكس ركيزة التحول الرقمي لرؤية 2030 من خلال رقمنة عمليات الإيرادات، "
                "وتمكين القرارات المبنية على البيانات، وبناء قدرات الذكاء الاصطناعي السعودية الأصلية "
                f"لقطاع {inp.client_sector}."
            ),
        },
        "milestones": {
            "current_stage": stage,
            "day_30": {
                "label_en": "Foundation",
                "label_ar": "التأسيس",
                "actions": milestone_actions["day_30"],
            },
            "day_60": {
                "label_en": "Activation",
                "label_ar": "التفعيل",
                "actions": milestone_actions["day_60"],
            },
            "day_90": {
                "label_en": "Value Realization",
                "label_ar": "تحقيق القيمة",
                "actions": milestone_actions["day_90"],
            },
        },
        "risk_register": [
            {
                **risk,
                "client_context_en": (
                    f"For {inp.client_name}: {risk['mitigation_en']}"
                ),
                "client_context_ar": (
                    f"بالنسبة لـ {inp.client_name}: {risk['mitigation_ar']}"
                ),
            }
            for risk in _STANDARD_RISKS
        ],
        "success_metrics": _ACCOUNT_PLAN_TEMPLATE["success_metrics"]["kpis"],
        "account_tier_detail": tier,
        "plan_meta": {
            "generated_for": inp.client_name,
            "stage": stage,
            "months_as_client": inp.months_as_client,
            "tier": tier_id,
        },
    }

    return plan


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------


@router.get("/template", summary="Blank account plan template with section descriptions")
async def get_template() -> dict[str, Any]:
    return {
        "template": _ACCOUNT_PLAN_TEMPLATE,
        "usage_note_en": (
            "This is a blank framework. POST /generate with client data to receive "
            "a fully populated account plan."
        ),
        "usage_note_ar": (
            "هذا إطار فارغ. أرسل POST /generate مع بيانات العميل للحصول على "
            "خطة حساب مكتملة."
        ),
        "governance_decision": "ALLOW_WITH_REVIEW",
    }


@router.get("/tiers", summary="All account tiers with criteria and benefits")
async def list_tiers() -> dict[str, Any]:
    return {
        "tiers": list(_ACCOUNT_TIERS.values()),
        "governance_decision": "ALLOW_WITH_REVIEW",
    }


@router.get("/tiers/{tier_id}", summary="Single account tier detail")
async def get_tier(tier_id: str) -> dict[str, Any]:
    tier = _ACCOUNT_TIERS.get(tier_id)
    if not tier:
        raise HTTPException(
            status_code=404,
            detail=f"Tier '{tier_id}' not found. Valid: {list(_ACCOUNT_TIERS.keys())}",
        )
    return {
        **tier,
        "governance_decision": "ALLOW_WITH_REVIEW",
    }


@router.post("/generate", summary="Generate a full strategic account plan")
async def generate_account_plan(body: AccountPlanInput) -> dict[str, Any]:
    if body.current_stage not in _VALID_STAGES:
        raise HTTPException(
            status_code=422,
            detail=(
                f"current_stage '{body.current_stage}' is not valid. "
                f"Valid values: {sorted(_VALID_STAGES)}"
            ),
        )
    plan = _build_account_plan(body)
    return {
        **plan,
        "governance_decision": "APPROVAL_FIRST",
    }


@router.get("/risk-register-guide", summary="Standard risk register with mitigation strategies")
async def get_risk_register_guide() -> dict[str, Any]:
    return {
        "risks": _STANDARD_RISKS,
        "usage_note_en": (
            "These four risks apply to every enterprise account. "
            "Tailor the mitigation steps to the specific client context before presenting."
        ),
        "usage_note_ar": (
            "هذه المخاطر الأربعة تنطبق على كل حساب مؤسسي. "
            "خصّص خطوات التخفيف لسياق العميل المحدد قبل التقديم."
        ),
        "governance_decision": "ALLOW_WITH_REVIEW",
    }
