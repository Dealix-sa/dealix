"""Annual Business Review (ABR) framework for Dealix enterprise Saudi clients.

Structures the annual review meeting and generates a bilingual ABR report.
All data is static; no LLM or external API calls are made.
All generated content carries a mandatory draft disclaimer and must be
reviewed and approved before sharing with any client.

Prefix: /api/v1/annual-business-review
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter(
    prefix="/api/v1/annual-business-review",
    tags=["Analytics"],
)

# ---------------------------------------------------------------------------
# Governance constants
# ---------------------------------------------------------------------------

_GOV_REVIEW = "ALLOW_WITH_REVIEW"
_GOV_APPROVAL = "APPROVAL_FIRST"

_DISCLAIMER_EN = (
    "This ABR report is a draft generated from inputs provided. "
    "All metrics, narratives, and recommendations must be reviewed and "
    "approved by an account manager before sharing with the client."
)
_DISCLAIMER_AR = (
    "هذا التقرير السنوي مسودة أُنشئت استناداً إلى المدخلات المقدمة. "
    "يجب على مدير الحساب مراجعة جميع المقاييس والروايات والتوصيات "
    "والموافقة عليها قبل مشاركتها مع العميل."
)

# ---------------------------------------------------------------------------
# Static data: ABR sections
# ---------------------------------------------------------------------------

_ABR_SECTIONS: list[dict[str, Any]] = [
    {
        "order": 1,
        "title_en": "Executive Summary",
        "title_ar": "الملخص التنفيذي",
        "description_en": (
            "High-level strategic highlights for the review year, "
            "covering the top three wins and top three challenges."
        ),
        "description_ar": (
            "أبرز النقاط الاستراتيجية للسنة المراجَعة، "
            "تشمل أهم ثلاثة إنجازات وأبرز ثلاثة تحديات."
        ),
        "key_questions_en": [
            "What were the three biggest strategic wins this year?",
            "What were the three most significant challenges and how were they addressed?",
            "How does this year's overall performance compare to the objectives set at the start of the year?",
        ],
        "data_required_en": [
            "Year-start strategic objectives and OKRs",
            "Summary of major project completions and outcomes",
            "Executive narrative from account sponsor",
        ],
    },
    {
        "order": 2,
        "title_en": "Revenue Performance",
        "title_ar": "أداء الإيرادات",
        "description_en": (
            "Analysis of MRR trend, net revenue retention, and deal velocity "
            "compared to the prior year."
        ),
        "description_ar": (
            "تحليل اتجاه الإيرادات الشهرية المتكررة، الاحتفاظ بالإيرادات الصافية، "
            "وسرعة الصفقات مقارنةً بالسنة السابقة."
        ),
        "key_questions_en": [
            "What was the MRR trend from start to end of year, and what drove key inflection points?",
            "What is the net revenue retention rate, and how does it compare to the Saudi B2B median?",
            "How did deal velocity (average days to close) change versus the prior year?",
        ],
        "data_required_en": [
            "Monthly MRR figures for the full review year",
            "NRR calculation: (starting MRR + expansion - contraction - churn) / starting MRR",
            "Deal-level close data with stage timestamps",
        ],
    },
    {
        "order": 3,
        "title_en": "AI and Data ROI",
        "title_ar": "عائد الاستثمار في الذكاء الاصطناعي والبيانات",
        "description_en": (
            "Quantified return from AI and data initiatives: automation savings, "
            "ZATCA compliance improvement, and data quality score change."
        ),
        "description_ar": (
            "العائد الكمي من مبادرات الذكاء الاصطناعي والبيانات: "
            "وفورات الأتمتة، تحسين الامتثال لهيئة الزكاة والضريبة والجمارك، "
            "والتغيير في درجة جودة البيانات."
        ),
        "key_questions_en": [
            "What measurable cost or time savings were achieved through AI automation this year?",
            "How much did ZATCA Phase 2 e-invoicing compliance improve as a result of Dealix solutions?",
            "What was the change in data quality score from the start to the end of the year?",
        ],
        "data_required_en": [
            "Automation savings log (hours saved, error rates before and after)",
            "ZATCA compliance audit results at start and end of year",
            "Data quality score measurement (DQ score from data_os compute_dq)",
        ],
    },
    {
        "order": 4,
        "title_en": "Vision 2030 Alignment",
        "title_ar": "التوافق مع رؤية 2030",
        "description_en": (
            "Which Vision 2030 KPIs the client improved during the year, "
            "including GDP non-oil contribution, Saudization rate, "
            "tourism revenue, and digital transaction share."
        ),
        "description_ar": (
            "مؤشرات أداء رؤية 2030 التي حسّنها العميل خلال السنة، "
            "بما فيها مساهمة الناتج المحلي غير النفطي، نسبة التوطين، "
            "إيرادات السياحة، وحصة المعاملات الرقمية."
        ),
        "key_questions_en": [
            "Which Vision 2030 national KPIs did the client's operations directly contribute to this year?",
            "What is the client's current Saudization (Nitaqat) rate, and how has it changed year-on-year?",
            "How can Dealix's roadmap be better aligned with upcoming Vision 2030 program deadlines?",
        ],
        "data_required_en": [
            "Client Saudization (Nitaqat) rate at year-start and year-end",
            "List of Vision 2030 programs or national initiatives the client participates in",
            "Any government recognition, certifications, or compliance badges received",
        ],
    },
    {
        "order": 5,
        "title_en": "Competitive Positioning",
        "title_ar": "التموضع التنافسي",
        "description_en": (
            "How the client is positioned versus sector peers, "
            "and the role Dealix plays in strengthening that position."
        ),
        "description_ar": (
            "كيفية تموضع العميل مقارنةً بمنافسيه في القطاع، "
            "والدور الذي تضطلع به ديليكس في تعزيز ذلك التموضع."
        ),
        "key_questions_en": [
            "In which capability areas is the client ahead of sector peers, and how has Dealix contributed?",
            "Where do competitors pose the greatest threat, and what is the plan to close the gap?",
            "What Dealix capabilities remain unused that could provide a near-term competitive advantage?",
        ],
        "data_required_en": [
            "Sector benchmark data for the client's primary KPIs",
            "Competitive intelligence notes from sales and CS teams",
            "Usage data for Dealix features by the client (feature adoption report)",
        ],
    },
    {
        "order": 6,
        "title_en": "Strategic Roadmap",
        "title_ar": "خارطة الطريق الاستراتيجية",
        "description_en": (
            "The three strategic priorities for the next 12 months "
            "and how the Dealix product roadmap aligns with them."
        ),
        "description_ar": (
            "الأولويات الاستراتيجية الثلاث للاثني عشر شهراً القادمة "
            "وكيف تتوافق خارطة طريق ديليكس المنتجية معها."
        ),
        "key_questions_en": [
            "What are the client's top three strategic priorities for the next 12 months?",
            "Which upcoming Dealix product releases or features directly address those priorities?",
            "What dependencies or prerequisites must be resolved for the roadmap to succeed?",
        ],
        "data_required_en": [
            "Client's internal strategic plan or board-approved objectives for next year",
            "Dealix product roadmap (filtered to client-relevant items)",
            "Outstanding implementation items or technical debt that must be resolved",
        ],
    },
    {
        "order": 7,
        "title_en": "Commercial Renewal",
        "title_ar": "التجديد التجاري",
        "description_en": (
            "Renewal terms, pricing review, expansion opportunities, "
            "and contract extension options."
        ),
        "description_ar": (
            "شروط التجديد، مراجعة الأسعار، فرص التوسع، "
            "وخيارات تمديد العقد."
        ),
        "key_questions_en": [
            "What is the recommended renewal term and pricing adjustment based on usage and value delivered?",
            "Which expansion modules or seats represent the highest-value upsell opportunity for this client?",
            "Are there multi-year contract options that would benefit both the client and Dealix's revenue predictability?",
        ],
        "data_required_en": [
            "Current contract terms: start date, end date, MRR, and committed usage",
            "Usage data and feature adoption percentages",
            "Expansion revenue history and pipeline for this account",
        ],
    },
]

# ---------------------------------------------------------------------------
# Static data: Saudi B2B SaaS benchmarks for ABR
# ---------------------------------------------------------------------------

_ABR_BENCHMARKS: dict[str, Any] = {
    "world_class_nrr_pct": 120,
    "saudi_median_revenue_growth_pct": 18,
    "top_quartile_data_quality_score": 85,
    "acceptable_churn_rate_monthly_pct": 2.5,
    "vision_2030_saudization_target_pct": 50,
    "benchmark_source_note_en": (
        "Benchmarks derived from Saudi B2B SaaS market data and Vision 2030 program targets. "
        "Indicative only — actual targets vary by sector and company size."
    ),
    "benchmark_source_note_ar": (
        "مستقاة من بيانات سوق B2B SaaS السعودي وأهداف برامج رؤية 2030. "
        "استرشادية فقط — تتفاوت الأهداف الفعلية بحسب القطاع وحجم الشركة."
    ),
}

# ---------------------------------------------------------------------------
# Preparation guide
# ---------------------------------------------------------------------------

_PREPARATION_GUIDE: dict[str, Any] = {
    "title_en": "How to Prepare for an Annual Business Review",
    "title_ar": "كيفية التحضير للمراجعة التجارية السنوية",
    "recommended_timing_en": (
        "Schedule the ABR 30–45 days before contract renewal. "
        "Avoid Ramadan period and the first week after Eid. "
        "Q4 (October–November) is the optimal window for strategic clients in Saudi Arabia."
    ),
    "recommended_timing_ar": (
        "جدول المراجعة قبل 30 إلى 45 يوماً من تجديد العقد. "
        "تجنب شهر رمضان والأسبوع الأول بعد العيد. "
        "الربع الرابع (أكتوبر–نوفمبر) هو النافذة المثلى للعملاء الاستراتيجيين في المملكة العربية السعودية."
    ),
    "who_to_invite_en": [
        "Client executive sponsor (C-level or VP)",
        "Client operational owner (the day-to-day champion)",
        "Client finance lead if renewal discussion is included",
        "Dealix account manager",
        "Dealix customer success manager",
        "Dealix executive sponsor for strategic accounts",
    ],
    "who_to_invite_ar": [
        "راعي التنفيذ من جانب العميل (على مستوى C أو نائب الرئيس)",
        "المسؤول التشغيلي لدى العميل (البطل اليومي)",
        "قائد التمويل لدى العميل إذا كانت مناقشة التجديد مدرجة",
        "مدير حساب ديليكس",
        "مدير نجاح العميل في ديليكس",
        "الراعي التنفيذي لديليكس للحسابات الاستراتيجية",
    ],
    "data_collection_checklist_en": [
        "Pull full MRR history for the review year from billing system",
        "Export feature adoption report from Dealix platform",
        "Collect ZATCA compliance audit results (before and after)",
        "Request Saudization rate from client HR team",
        "Compile notable wins and challenge narratives from CS notes",
        "Prepare renewal commercial proposal (separate approval required)",
    ],
    "data_collection_checklist_ar": [
        "استخراج سجل الإيرادات الشهرية كاملاً لسنة المراجعة من نظام الفوترة",
        "تصدير تقرير تبني الميزات من منصة ديليكس",
        "جمع نتائج تدقيق الامتثال لهيئة الزكاة (قبل وبعد)",
        "طلب نسبة التوطين من فريق الموارد البشرية لدى العميل",
        "تجميع روايات الإنجازات البارزة والتحديات من ملاحظات نجاح العملاء",
        "إعداد اقتراح التجديد التجاري (يتطلب موافقة منفصلة)",
    ],
    "meeting_format_en": {
        "duration_minutes": 90,
        "language_recommendation": (
            "Use Arabic slides with English speaking notes for mixed-language rooms. "
            "Present executive summary slide in Arabic first."
        ),
        "agenda_structure": [
            "Welcome and relationship acknowledgement (5 min)",
            "Year in review: wins and challenges (20 min)",
            "Metrics deep-dive: revenue, AI ROI, data quality (25 min)",
            "Vision 2030 alignment and competitive positioning (15 min)",
            "Strategic roadmap for next year (15 min)",
            "Commercial renewal discussion (10 min)",
        ],
    },
    "governance_decision": _GOV_REVIEW,
}

# ---------------------------------------------------------------------------
# Pydantic models
# ---------------------------------------------------------------------------


class ABRGenerateInput(BaseModel):
    client_name: str = Field(..., min_length=1, max_length=150)
    client_sector: str = Field(..., min_length=2, max_length=80)
    account_tier: str = Field(
        ...,
        description="Account tier: strategic | growth | standard",
    )
    year: int = Field(..., ge=2024, le=2030)
    mrr_start_sar: float = Field(..., ge=0, description="MRR at the start of the review year in SAR")
    mrr_end_sar: float = Field(..., ge=0, description="MRR at the end of the review year in SAR")
    nrr_pct: float = Field(..., ge=0, le=300, description="Net Revenue Retention percentage")
    churn_rate_pct: float = Field(..., ge=0, le=100, description="Monthly churn rate percentage")
    data_quality_score: float = Field(..., ge=0, le=100, description="Data quality score (0–100)")
    saudization_pct: float = Field(..., ge=0, le=100, description="Saudization (Nitaqat) rate percentage")
    notable_wins: list[str] = Field(default_factory=list, description="List of notable wins during the year")
    challenges: list[str] = Field(default_factory=list, description="List of challenges encountered")


# ---------------------------------------------------------------------------
# Pure-function core
# ---------------------------------------------------------------------------

_VALID_ACCOUNT_TIERS = {"strategic", "growth", "standard"}


def _generate_abr(inp: ABRGenerateInput) -> dict[str, Any]:
    """Generate a structured ABR dict from validated input.

    Computes key metrics, benchmarks them against Saudi B2B standards,
    and produces draft section content with renewal recommendation.
    All output must be reviewed and approved before client delivery.
    """
    # Computed metrics
    mrr_growth_pct = (
        round((inp.mrr_end_sar - inp.mrr_start_sar) / inp.mrr_start_sar * 100, 1)
        if inp.mrr_start_sar > 0
        else 0.0
    )

    # Benchmark comparisons
    vs_revenue_growth = (
        "above_median"
        if mrr_growth_pct >= _ABR_BENCHMARKS["saudi_median_revenue_growth_pct"]
        else "below_median"
    )
    vs_nrr = (
        "world_class"
        if inp.nrr_pct >= _ABR_BENCHMARKS["world_class_nrr_pct"]
        else "below_world_class"
    )
    vs_data_quality = (
        "top_quartile"
        if inp.data_quality_score >= _ABR_BENCHMARKS["top_quartile_data_quality_score"]
        else "below_top_quartile"
    )
    vs_churn = (
        "acceptable"
        if inp.churn_rate_pct <= _ABR_BENCHMARKS["acceptable_churn_rate_monthly_pct"]
        else "above_acceptable"
    )
    vs_saudization = (
        "meets_target"
        if inp.saudization_pct >= _ABR_BENCHMARKS["vision_2030_saudization_target_pct"]
        else "below_target"
    )

    # Renewal recommendation
    if inp.nrr_pct >= 110 and vs_churn == "acceptable" and mrr_growth_pct >= 0:
        renewal_recommendation = "expand"
        renewal_recommendation_ar = "توسيع"
        renewal_rationale_en = (
            f"{inp.client_name} demonstrates strong retention (NRR {inp.nrr_pct}%) "
            "and healthy churn. Expansion conversation is warranted."
        )
        renewal_rationale_ar = (
            f"يُظهر {inp.client_name} احتفاظاً قوياً بالإيرادات (NRR {inp.nrr_pct}%) "
            "ومعدل تراجع صحياً. محادثة التوسع مبررة."
        )
    elif inp.nrr_pct >= 90 and vs_churn == "acceptable":
        renewal_recommendation = "renew"
        renewal_recommendation_ar = "تجديد"
        renewal_rationale_en = (
            f"{inp.client_name} is stable with adequate retention. "
            "Standard renewal at current terms is recommended."
        )
        renewal_rationale_ar = (
            f"{inp.client_name} مستقر مع احتفاظ كافٍ بالإيرادات. "
            "يُوصى بالتجديد القياسي بالشروط الحالية."
        )
    else:
        renewal_recommendation = "at_risk"
        renewal_recommendation_ar = "في خطر"
        renewal_rationale_en = (
            f"{inp.client_name} shows signals of churn risk "
            f"(NRR {inp.nrr_pct}%, churn {inp.churn_rate_pct}%/mo). "
            "A recovery plan should be agreed before renewal discussions."
        )
        renewal_rationale_ar = (
            f"يُظهر {inp.client_name} إشارات خطر تراجع "
            f"(NRR {inp.nrr_pct}%، تراجع {inp.churn_rate_pct}%/شهر). "
            "يجب الاتفاق على خطة تعافٍ قبل مناقشات التجديد."
        )

    # Executive highlights
    executive_highlights: list[str] = []
    if inp.notable_wins:
        executive_highlights.append(
            f"Top win: {inp.notable_wins[0]}"
        )
    executive_highlights.append(
        f"MRR grew {mrr_growth_pct}% year-on-year "
        f"(Saudi B2B median: {_ABR_BENCHMARKS['saudi_median_revenue_growth_pct']}%)."
    )
    executive_highlights.append(
        f"NRR of {inp.nrr_pct}% — "
        f"{'at or above' if vs_nrr == 'world_class' else 'below'} the world-class threshold of "
        f"{_ABR_BENCHMARKS['world_class_nrr_pct']}%."
    )
    if inp.saudization_pct > 0:
        executive_highlights.append(
            f"Saudization at {inp.saudization_pct}% — "
            f"{'meets' if vs_saudization == 'meets_target' else 'below'} "
            f"Vision 2030 target of {_ABR_BENCHMARKS['vision_2030_saudization_target_pct']}%."
        )

    # Section content (draft only)
    sections_content: list[dict[str, Any]] = []
    for section in _ABR_SECTIONS:
        draft_content_en = f"[DRAFT] Section {section['order']}: {section['title_en']} — content to be populated by account manager using client data."
        draft_content_ar = f"[مسودة] القسم {section['order']}: {section['title_ar']} — يُكمل مدير الحساب المحتوى باستخدام بيانات العميل."

        if section["order"] == 1:
            wins_str = "; ".join(inp.notable_wins[:3]) if inp.notable_wins else "Not provided"
            challenges_str = "; ".join(inp.challenges[:3]) if inp.challenges else "Not provided"
            draft_content_en = (
                f"Review year {inp.year} for {inp.client_name} ({inp.client_sector}). "
                f"Top wins: {wins_str}. "
                f"Key challenges: {challenges_str}."
            )
            draft_content_ar = (
                f"سنة المراجعة {inp.year} لـ{inp.client_name} ({inp.client_sector}). "
                f"أبرز الإنجازات: {wins_str}. "
                f"أبرز التحديات: {challenges_str}."
            )
        elif section["order"] == 2:
            draft_content_en = (
                f"MRR moved from SAR {inp.mrr_start_sar:,.0f} to SAR {inp.mrr_end_sar:,.0f} "
                f"({mrr_growth_pct:+.1f}% growth, Saudi median: "
                f"{_ABR_BENCHMARKS['saudi_median_revenue_growth_pct']}%). "
                f"NRR: {inp.nrr_pct}% ({vs_nrr.replace('_', ' ')}). "
                f"Monthly churn: {inp.churn_rate_pct}% ({vs_churn.replace('_', ' ')})."
            )
            draft_content_ar = (
                f"انتقلت الإيرادات الشهرية من {inp.mrr_start_sar:,.0f} ريال إلى "
                f"{inp.mrr_end_sar:,.0f} ريال "
                f"(نمو {mrr_growth_pct:+.1f}%، وسيط السوق السعودي: "
                f"{_ABR_BENCHMARKS['saudi_median_revenue_growth_pct']}%). "
                f"NRR: {inp.nrr_pct}%. "
                f"التراجع الشهري: {inp.churn_rate_pct}%."
            )
        elif section["order"] == 3:
            draft_content_en = (
                f"Data quality score: {inp.data_quality_score}/100 "
                f"(top-quartile threshold: {_ABR_BENCHMARKS['top_quartile_data_quality_score']}; "
                f"status: {vs_data_quality.replace('_', ' ')}). "
                "ZATCA compliance improvement and automation savings to be populated from client records."
            )
            draft_content_ar = (
                f"درجة جودة البيانات: {inp.data_quality_score}/100 "
                f"(عتبة الربع الأعلى: {_ABR_BENCHMARKS['top_quartile_data_quality_score']}; "
                f"الحالة: {vs_data_quality.replace('_', ' ')}). "
                "تحسين الامتثال لهيئة الزكاة ووفورات الأتمتة تُستكمل من سجلات العميل."
            )
        elif section["order"] == 4:
            draft_content_en = (
                f"Saudization rate: {inp.saudization_pct}% "
                f"(Vision 2030 target: {_ABR_BENCHMARKS['vision_2030_saudization_target_pct']}%; "
                f"status: {vs_saudization.replace('_', ' ')}). "
                "Additional Vision 2030 KPI contributions to be documented by account manager."
            )
            draft_content_ar = (
                f"نسبة التوطين: {inp.saudization_pct}% "
                f"(هدف رؤية 2030: {_ABR_BENCHMARKS['vision_2030_saudization_target_pct']}%; "
                f"الحالة: {vs_saudization.replace('_', ' ')}). "
                "مساهمات مؤشرات رؤية 2030 الإضافية يوثّقها مدير الحساب."
            )
        elif section["order"] == 7:
            draft_content_en = (
                f"Renewal recommendation: {renewal_recommendation}. "
                f"{renewal_rationale_en} "
                "Specific commercial terms require separate approval before presentation."
            )
            draft_content_ar = (
                f"توصية التجديد: {renewal_recommendation_ar}. "
                f"{renewal_rationale_ar} "
                "الشروط التجارية المحددة تتطلب موافقة منفصلة قبل التقديم."
            )

        sections_content.append(
            {
                "order": section["order"],
                "title_en": section["title_en"],
                "title_ar": section["title_ar"],
                "draft_content_en": draft_content_en,
                "draft_content_ar": draft_content_ar,
                "key_questions_en": section["key_questions_en"],
            }
        )

    return {
        "client_name": inp.client_name,
        "client_sector": inp.client_sector,
        "account_tier": inp.account_tier,
        "year": inp.year,
        "computed_metrics": {
            "mrr_start_sar": inp.mrr_start_sar,
            "mrr_end_sar": inp.mrr_end_sar,
            "mrr_growth_pct": mrr_growth_pct,
            "vs_saudi_median_revenue_growth": vs_revenue_growth,
            "nrr_pct": inp.nrr_pct,
            "vs_world_class_nrr": vs_nrr,
            "churn_rate_monthly_pct": inp.churn_rate_pct,
            "vs_acceptable_churn": vs_churn,
            "data_quality_score": inp.data_quality_score,
            "vs_top_quartile_dq": vs_data_quality,
            "saudization_pct": inp.saudization_pct,
            "vs_vision2030_saudization_target": vs_saudization,
        },
        "executive_highlights": executive_highlights,
        "renewal_recommendation": renewal_recommendation,
        "renewal_recommendation_ar": renewal_recommendation_ar,
        "renewal_rationale_en": renewal_rationale_en,
        "renewal_rationale_ar": renewal_rationale_ar,
        "sections": sections_content,
        "disclaimer_en": _DISCLAIMER_EN,
        "disclaimer_ar": _DISCLAIMER_AR,
        "governance_decision": _GOV_APPROVAL,
    }


# ---------------------------------------------------------------------------
# Router endpoints
# ---------------------------------------------------------------------------


@router.get("/sections", summary="All 7 ABR section templates")
def get_sections() -> dict[str, Any]:
    """Return all seven ABR section templates including key questions and data requirements."""
    return {
        "sections": _ABR_SECTIONS,
        "total_sections": len(_ABR_SECTIONS),
        "note_en": "Use these sections to structure the annual business review meeting agenda.",
        "note_ar": "استخدم هذه الأقسام لهيكلة جدول أعمال اجتماع المراجعة التجارية السنوية.",
        "governance_decision": _GOV_REVIEW,
    }


@router.get("/benchmarks", summary="Saudi B2B SaaS benchmarks for ABR")
def get_benchmarks() -> dict[str, Any]:
    """Return Saudi B2B SaaS benchmark metrics used to evaluate ABR performance."""
    return {
        "benchmarks": _ABR_BENCHMARKS,
        "governance_decision": _GOV_REVIEW,
    }


@router.post("/generate", summary="Generate a full bilingual ABR report")
def generate_abr(body: ABRGenerateInput) -> dict[str, Any]:
    """Accept ABR input data and return a structured draft ABR report.

    All output carries a mandatory draft disclaimer and requires account
    manager review and approval before sharing with the client.
    Governance decision: APPROVAL_FIRST.
    """
    if body.account_tier not in _VALID_ACCOUNT_TIERS:
        raise HTTPException(
            status_code=422,
            detail={
                "error": f"Invalid account_tier '{body.account_tier}'.",
                "valid_values": sorted(_VALID_ACCOUNT_TIERS),
                "governance_decision": _GOV_REVIEW,
            },
        )
    return _generate_abr(body)


@router.get("/preparation-guide", summary="How to prepare for an ABR meeting")
def get_preparation_guide() -> dict[str, Any]:
    """Return guidance on preparing for an ABR: data to collect, who to invite, and timing."""
    return _PREPARATION_GUIDE
