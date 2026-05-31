"""
Saudi B2B pricing psychology and ROI simulator for Dealix sales team.

Provides pricing conversation anchoring scripts, tier psychological
positioning, and an ROI simulation calculator to help prospects
justify Dealix's price against manual labour, ZATCA risk, and pipeline losses.
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

router = APIRouter(prefix="/api/v1/pricing-psychology", tags=["Sales"])

# ---------------------------------------------------------------------------
# Pricing psychology principles
# ---------------------------------------------------------------------------

_PRICING_PSYCHOLOGY: dict[str, Any] = {
    "anchor_high_first": {
        "principle_en": "Anchor High First",
        "principle_ar": "الارتساء العالي أولاً",
        "description_en": (
            "Always present the most premium Dealix option (Custom AI, SAR 5K–25K) first, "
            "then step down. The brain anchors to the first number it hears. "
            "Starting with SAR 499 Sprint makes it the anchor — and clients then negotiate down from nothing."
        ),
        "description_ar": (
            "قدّم دائماً الخيار الأعلى قيمة (الذكاء الاصطناعي المخصص، 5K–25K ريال) أولاً، ثم انزل. "
            "العقل يُثبّت الرقم الأول الذي يسمعه. البدء بسبرنت 499 ريال يجعله المرساة."
        ),
        "script_en": "We typically work with clients at SAR 25,000 for a full Custom AI buildout. "
                     "However, for a company at your stage, the Revenue Intelligence Sprint at SAR 499 "
                     "lets us prove value in 7 days before committing.",
        "avoid_en": "Never start with the free diagnostic price — it anchors the relationship as zero-value.",
    },
    "zatca_roi_anchor": {
        "principle_en": "ZATCA Fine Avoidance as ROI Anchor",
        "principle_ar": "تجنب غرامات الزكاة كمرساة عائد الاستثمار",
        "description_en": (
            "ZATCA non-compliance fines range from SAR 10,000 to SAR 50,000 per violation. "
            "Frame Dealix's Managed Ops (SAR 2,999–4,999/mo) against this risk."
        ),
        "description_ar": (
            "تتراوح غرامات عدم الامتثال لهيئة الزكاة من 10,000 إلى 50,000 ريال لكل مخالفة. "
            "ضع عمليات ديليكس المُدارة (2,999–4,999 ريال/شهر) في مواجهة هذا الخطر."
        ),
        "script_en": "One ZATCA fine covers 10 months of Dealix's managed service. "
                     "We help you avoid that risk entirely — what's the cost of the last audit issue you had?",
        "avoid_en": "Do not claim Dealix guarantees ZATCA compliance — say 'reduces risk' not 'eliminates'.",
    },
    "ramadan_sensitivity": {
        "principle_en": "Ramadan Price Sensitivity",
        "principle_ar": "الحساسية السعرية في رمضان",
        "description_en": (
            "Saudi executives are in reflection mode during Ramadan weeks 1–2. "
            "Pushing pricing discussions in this window damages trust and rarely closes. "
            "Plant seeds: 'After Eid, I'd love to show you what this looks like for [Company].' "
            "Then follow up in the first 3 business days post-Eid."
        ),
        "description_ar": (
            "المسؤولون السعوديون في وضع التأمل خلال أسبوعي رمضان الأول والثاني. "
            "دفع نقاشات التسعير في هذه النافذة يضر بالثقة ونادراً ما يُغلق. "
            "ازرع البذور: 'بعد العيد، أود أن أريك كيف يبدو هذا لـ [الشركة]'."
        ),
        "script_en": "I respect that Ramadan is a time for reflection. "
                     "I'll follow up after Eid to share what we've prepared for you — Eid Mubarak.",
        "avoid_en": "Never send pricing proposals or invoice during Eid break.",
    },
    "relationship_before_price": {
        "principle_en": "Relationship Before Price",
        "principle_ar": "العلاقة قبل السعر",
        "description_en": (
            "Saudi B2B buyers buy from people they trust, not from the best price. "
            "Run the free diagnostic first — it builds trust and creates a data-based conversation. "
            "Price is discussed only after the prospect has seen value."
        ),
        "description_ar": (
            "مشترو B2B السعوديون يشترون من الأشخاص الذين يثقون بهم، وليس من الأرخص. "
            "ابدأ بالتشخيص المجاني — فهو يبني الثقة ويخلق محادثة قائمة على البيانات. "
            "يُناقَش السعر فقط بعد أن يرى العميل قيمة."
        ),
        "script_en": "Before we talk about investment, let me show you what your pipeline looks like. "
                     "No cost, no commitment — just data you'll use regardless.",
        "avoid_en": "Never lead with pricing on the first call or meeting.",
    },
    "arabic_price_framing": {
        "principle_en": "Arabic Price Framing",
        "principle_ar": "صياغة السعر بالعربية",
        "description_en": (
            "When speaking Arabic, frame prices as 'استثمار' (investment) not 'تكلفة' (cost). "
            "Use Arabic numerals in written Arabic communications. "
            "Monthly framing is more digestible than annual: '4,999 ريال شهرياً' not '59,988 ريال سنوياً'."
        ),
        "description_ar": (
            "عند التحدث بالعربية، ضع الأسعار كـ'استثمار' لا 'تكلفة'. "
            "استخدم الأرقام العربية في الاتصالات المكتوبة باللغة العربية. "
            "الصياغة الشهرية أسهل هضماً من السنوية."
        ),
        "script_en": "هذا ليس تكلفة — هو استثمار بعائد مضمون على مؤشرات الأداء.",
        "avoid_en": "Avoid presenting annual totals in Arabic — it magnifies sticker shock.",
    },
    "competitor_price_anchoring": {
        "principle_en": "Competitor Price Anchoring",
        "principle_ar": "الارتساء بأسعار المنافسين",
        "description_en": (
            "Big 4 consulting engagements in Saudi cost SAR 100K–500K+ for a one-time report. "
            "Global CRMs (Salesforce) run SAR 3,000–15,000+/mo per seat with no Saudi customisation. "
            "Dealix delivers Saudi-native revenue intelligence for SAR 499–4,999/mo — frame accordingly."
        ),
        "description_ar": (
            "مشاريع مجموعات الكبار الأربعة في السعودية تكلف 100K–500K ريال+ للتقرير الواحد. "
            "أدوات CRM العالمية (Salesforce) تُكلّف 3,000–15,000+ ريال/شهر/مستخدم بدون تخصيص سعودي. "
            "ديليكس تُقدّم ذكاء الإيرادات السعودي الأصلي بـ 499–4,999 ريال/شهر — ضعه في هذا السياق."
        ),
        "script_en": "The alternative is SAR 300,000 for a Big 4 strategy project that delivers a PDF. "
                     "Dealix delivers live insights, in Arabic, updated weekly, for SAR 4,999/mo.",
        "avoid_en": "Do not name specific competitors directly in written proposals without founder approval.",
    },
}

# ---------------------------------------------------------------------------
# Price anchor conversation scripts
# ---------------------------------------------------------------------------

_PRICE_ANCHOR_SCRIPTS: list[dict[str, Any]] = [
    {
        "scenario_en": "Prospect says price is too high",
        "scenario_ar": "العميل يقول السعر مرتفع جداً",
        "script_en": (
            "I understand. Let's look at it differently: "
            "your team spends [HOURS]h/week on manual reporting — that's SAR [COST]/mo in salary cost alone. "
            "Dealix automates 70% of that at SAR [TIER_PRICE]/mo. "
            "The ROI starts in month 1."
        ),
        "script_ar": (
            "أفهم ذلك. دعنا ننظر إليه بطريقة مختلفة: "
            "فريقك يقضي [HOURS] ساعة/أسبوع في التقارير اليدوية — هذا [COST] ريال/شهر في رواتب وحدها. "
            "ديليكس تُؤتمت 70% من ذلك بـ [TIER_PRICE] ريال/شهر. "
            "عائد الاستثمار يبدأ في الشهر الأول."
        ),
        "trap_to_avoid_en": "Do not offer a discount immediately — reframe ROI first.",
    },
    {
        "scenario_en": "Prospect asks for a discount",
        "scenario_ar": "العميل يطلب خصماً",
        "script_en": (
            "Instead of discounting, let me offer you something more valuable: "
            "start with our SAR 499 Sprint. "
            "If we deliver the value we expect, you'll choose the engagement that fits your budget. "
            "No commitment, full insight."
        ),
        "script_ar": (
            "بدلاً من الخصم، دعني أقدم لك شيئاً أكثر قيمة: "
            "ابدأ بسبرنت 499 ريال. "
            "إذا أوصلنا القيمة المتوقعة، ستختار الباقة التي تناسب ميزانيتك. "
            "لا التزام، رؤية كاملة."
        ),
        "trap_to_avoid_en": "Never discount Managed Ops below SAR 2,999 — it signals lack of confidence in value.",
    },
    {
        "scenario_en": "Prospect compares to a cheaper tool",
        "scenario_ar": "العميل يقارن بأداة أرخص",
        "script_en": (
            "That tool is built for global markets. "
            "Does it speak Arabic? Does it understand Hijri calendar scheduling, ZATCA compliance phases, "
            "or Nitaqat Saudization bands? "
            "Dealix is built from the ground up for Saudi revenue operations — "
            "the difference isn't price, it's fit."
        ),
        "script_ar": (
            "تلك الأداة مصممة للأسواق العالمية. "
            "هل تتحدث العربية؟ هل تفهم جدولة التقويم الهجري، مراحل الامتثال لهيئة الزكاة، "
            "أو نطاقات السعودة؟ "
            "ديليكس مصممة من الأساس لعمليات الإيرادات السعودية — "
            "الفرق ليس في السعر، بل في الملاءمة."
        ),
        "trap_to_avoid_en": "Never attack the competitor by name. Focus on Saudi-specific differentiation.",
    },
    {
        "scenario_en": "CFO asks for ROI justification",
        "scenario_ar": "المدير المالي يطلب مبرر عائد الاستثمار",
        "script_en": (
            "Excellent question — let's build the ROI case together. "
            "Three numbers: "
            "1) Your team spends ~X hours/month on reporting at SAR Y/hour = SAR Z/month. "
            "2) ZATCA non-compliance risk: SAR 10,000–50,000 per finding. "
            "3) Deals lost to slow pipeline: X deals × SAR Y/deal. "
            "Dealix addresses all three. Want me to run the exact numbers for your context?"
        ),
        "script_ar": (
            "سؤال ممتاز — دعنا نبني حالة عائد الاستثمار معاً. "
            "ثلاثة أرقام: "
            "1) فريقك يقضي ~X ساعة/شهر في التقارير بـ Y ريال/ساعة = Z ريال/شهر. "
            "2) خطر عدم الامتثال لهيئة الزكاة: 10,000–50,000 ريال لكل مخالفة. "
            "3) الصفقات المفقودة بسبب بطء المسار: X صفقة × Y ريال/صفقة. "
            "ديليكس تعالج الثلاثة. هل تريد حساب الأرقام الدقيقة لسياقكم؟"
        ),
        "trap_to_avoid_en": "Do not use guaranteed return language — say 'typically see' not 'you will get'.",
    },
    {
        "scenario_en": "Prospect wants to start very small",
        "scenario_ar": "العميل يريد البدء بشيء صغير جداً",
        "script_en": (
            "Perfect — that's exactly what our Free Diagnostic is for. "
            "No cost, 7 days, and at the end you'll have a clear picture of your revenue gaps. "
            "Most clients then invest in the SAR 499 Sprint to act on what we find. "
            "Shall we schedule the diagnostic kickoff?"
        ),
        "script_ar": (
            "ممتاز — هذا بالضبط ما يُعنى به تشخيصنا المجاني. "
            "لا تكلفة، 7 أيام، وفي النهاية ستحصل على صورة واضحة لفجوات إيراداتك. "
            "معظم العملاء يستثمرون بعد ذلك في سبرنت 499 ريال للتصرف بناءً على ما نجده. "
            "هل نجدول بدء التشخيص؟"
        ),
        "trap_to_avoid_en": "Never push from 'free' directly to 'Managed Ops' in one call — respect the ladder.",
    },
]

# ---------------------------------------------------------------------------
# Tier psychology
# ---------------------------------------------------------------------------

_TIER_PSYCHOLOGY: dict[str, Any] = {
    "free_diagnostic": {
        "tier_en": "Free Diagnostic",
        "tier_ar": "التشخيص المجاني",
        "price_display": "SAR 0",
        "psychology_en": (
            "Zero risk entry — Saudi buyers need to feel value before committing. "
            "The free diagnostic removes the biggest barrier: trust. "
            "It's not charity — it's a 7-day sales call that pays for itself when 30% convert."
        ),
        "psychology_ar": (
            "دخول صفر مخاطرة — المشترون السعوديون يحتاجون إلى الشعور بالقيمة قبل الالتزام. "
            "التشخيص المجاني يزيل أكبر حاجز: الثقة."
        ),
        "ideal_for_en": "Cold-to-warm conversion, enterprise first touch, post-LEAP introductions",
    },
    "sprint_499": {
        "tier_en": "Revenue Intelligence Sprint",
        "tier_ar": "سبرنت ذكاء الإيرادات",
        "price_display": "SAR 499",
        "psychology_en": (
            "SAR 499 is a rounding error in any Saudi B2B budget. "
            "Frame it as: 'less than 4 hours of an analyst's time.' "
            "The psychological barrier isn't money — it's commitment. "
            "Position as: 'You're not paying for a service. You're buying data about your own business.'"
        ),
        "psychology_ar": (
            "499 ريال هو خطأ تقريب في أي ميزانية B2B سعودية. "
            "ضعه كـ: 'أقل من 4 ساعات من وقت محلل'. "
            "الحاجز النفسي ليس المال — بل الالتزام."
        ),
        "ideal_for_en": "SMEs, post-diagnostic conversion, ZATCA-triggered companies",
    },
    "data_pack_1500": {
        "tier_en": "Data Intelligence Pack",
        "tier_ar": "حزمة ذكاء البيانات",
        "price_display": "SAR 1,500",
        "psychology_en": (
            "Less than one employee's monthly basic salary (SAR 3,000+). "
            "Frame against the cost of a bad hire, a missed ZATCA filing, "
            "or 2 weeks of a consultant's time. "
            "'For the cost of fixing one reporting error, you get your entire data architecture assessed.'"
        ),
        "psychology_ar": (
            "أقل من راتب موظف شهري (3,000 ريال+). "
            "ضعه مقابل تكلفة توظيف خاطئ، أو تقديم هيئة زكاة فائت، أو أسبوعين من وقت مستشار."
        ),
        "ideal_for_en": "Data-mature SMEs, post-sprint upsell, FinTechs with data complexity",
    },
    "managed_ops_2999_4999": {
        "tier_en": "Managed Revenue Operations",
        "tier_ar": "عمليات الإيرادات المُدارة",
        "price_display": "SAR 2,999–4,999/mo",
        "psychology_en": (
            "CFO logic: Hiring a Saudi data analyst costs SAR 10,000–15,000/mo + benefits. "
            "Dealix Managed Ops delivers a full revenue intelligence function for SAR 4,999/mo. "
            "'You're not buying software. You're adding a revenue intelligence function without headcount.'"
        ),
        "psychology_ar": (
            "منطق المدير المالي: توظيف محلل بيانات سعودي يكلف 10,000–15,000 ريال/شهر + مزايا. "
            "عمليات ديليكس المُدارة تقدم وظيفة ذكاء إيرادات كاملة بـ 4,999 ريال/شهر."
        ),
        "ideal_for_en": "Growth-stage companies (50–500 employees), CFO champions, Vision 2030 KPI reporters",
    },
    "custom_ai_5k_25k": {
        "tier_en": "Custom AI Buildout",
        "tier_ar": "بناء الذكاء الاصطناعي المخصص",
        "price_display": "SAR 5,000–25,000",
        "psychology_en": (
            "Enterprise anchor. Present alongside Vision 2030 ROI, not just operational savings. "
            "'This is a strategic AI investment that positions your company as a digital leader in Vision 2030.' "
            "Compare to Big 4 strategy engagement (SAR 100K+) delivering a PDF — "
            "Dealix delivers working AI at 5–25% of that cost."
        ),
        "psychology_ar": (
            "مرساة المؤسسات. قدّمه جنباً إلى جنب مع عائد استثمار رؤية 2030، لا مجرد توفيرات تشغيلية. "
            "'هذا استثمار ذكاء اصطناعي استراتيجي يضع شركتك كقائد رقمي في رؤية 2030.'"
        ),
        "ideal_for_en": "Enterprises (300+ employees), CTO/CDO champions, NEOM/PIF portfolio companies",
    },
}


class PriceSimulatorInput(BaseModel):
    annual_manual_reporting_hours: float = Field(..., ge=0, description="Hours/year spent on manual reporting")
    hourly_fully_loaded_cost_sar: float = Field(default=75.0, ge=0, description="Fully-loaded hourly cost in SAR")
    zatca_non_compliance_risk_sar: float = Field(default=0.0, ge=0, description="Estimated annual ZATCA fine risk in SAR")
    missed_deals_per_year: int = Field(default=0, ge=0, description="Deals lost to slow pipeline visibility")
    avg_deal_size_sar: float = Field(default=3_500.0, ge=0, description="Average deal size in SAR")


def _simulate_price_roi(inp: PriceSimulatorInput) -> dict[str, Any]:
    annual_reporting_savings = inp.annual_manual_reporting_hours * inp.hourly_fully_loaded_cost_sar * 0.70
    compliance_savings = inp.zatca_non_compliance_risk_sar * 0.80
    pipeline_uplift = inp.missed_deals_per_year * inp.avg_deal_size_sar * 0.30
    total_annual_value = annual_reporting_savings + compliance_savings + pipeline_uplift

    sprint_cost = 499.0
    managed_ops_annual_cost = 4_999.0 * 12

    roi_at_sprint = round((total_annual_value - sprint_cost) / sprint_cost * 100, 1) if sprint_cost > 0 else 0.0
    roi_at_managed_ops = round((total_annual_value - managed_ops_annual_cost) / managed_ops_annual_cost * 100, 1) if managed_ops_annual_cost > 0 else 0.0

    payback_months_sprint = round(sprint_cost / (total_annual_value / 12), 1) if total_annual_value > 0 else 999.0
    payback_months_managed_ops = round(4_999.0 / (total_annual_value / 12), 1) if total_annual_value > 0 else 999.0

    if total_annual_value >= managed_ops_annual_cost * 3:
        recommended_tier = "custom_ai"
    elif total_annual_value >= 4_999 * 6:
        recommended_tier = "managed_ops_2999_4999"
    elif total_annual_value >= 1_500 * 3:
        recommended_tier = "data_pack_1500"
    elif total_annual_value >= 499:
        recommended_tier = "sprint_499"
    else:
        recommended_tier = "free_diagnostic"

    return {
        "annual_reporting_savings_sar": round(annual_reporting_savings, 0),
        "compliance_savings_sar": round(compliance_savings, 0),
        "pipeline_uplift_sar": round(pipeline_uplift, 0),
        "total_annual_value_sar": round(total_annual_value, 0),
        "roi_at_sprint_pct": roi_at_sprint,
        "roi_at_managed_ops_pct": roi_at_managed_ops,
        "payback_months_sprint": payback_months_sprint,
        "payback_months_managed_ops": payback_months_managed_ops,
        "recommended_tier": recommended_tier,
        "governance_decision": "ALLOW_WITH_REVIEW",
    }


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.get("/principles", summary="Saudi B2B pricing psychology principles")
async def get_principles() -> dict[str, Any]:
    return {
        "principles": _PRICING_PSYCHOLOGY,
        "total": len(_PRICING_PSYCHOLOGY),
        "governance_decision": "ALLOW_WITH_REVIEW",
    }


@router.get("/anchor-scripts", summary="Pricing conversation anchor scripts")
async def get_anchor_scripts() -> dict[str, Any]:
    return {
        "scripts": _PRICE_ANCHOR_SCRIPTS,
        "total": len(_PRICE_ANCHOR_SCRIPTS),
        "governance_decision": "ALLOW_WITH_REVIEW",
    }


@router.get("/tier-psychology", summary="Psychological positioning for each Dealix tier")
async def get_tier_psychology() -> dict[str, Any]:
    return {
        "tiers": _TIER_PSYCHOLOGY,
        "governance_decision": "ALLOW_WITH_REVIEW",
    }


@router.post("/simulate-roi", summary="Simulate ROI of Dealix vs. manual operations")
async def simulate_roi(inp: PriceSimulatorInput) -> dict[str, Any]:
    return _simulate_price_roi(inp)
