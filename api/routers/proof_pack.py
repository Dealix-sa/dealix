"""Proof Pack Builder — evidence packages for proposals, renewals, and expansions.

Assembles structured proof packs from baseline/current metric pairs.
All built proof packs are commercial assets and require governance approval
before use in client-facing conversations.

Prefix: /api/v1/proof-pack
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

router = APIRouter(prefix="/api/v1/proof-pack", tags=["Sales"])

_GOV_READ = "ALLOW_WITH_REVIEW"
_GOV_BUILD = "APPROVAL_FIRST"

# ---------------------------------------------------------------------------
# Static reference data
# ---------------------------------------------------------------------------

_PROOF_CATEGORIES: dict[str, dict[str, Any]] = {
    "roi_evidence": {
        "category_id": "roi_evidence",
        "name_en": "ROI Evidence",
        "name_ar": "دليل العائد على الاستثمار",
        "description_en": "Financial proof: cost savings, revenue uplift, payback period",
        "description_ar": "إثبات مالي: توفير التكاليف، ورفع الإيرادات، وفترة الاسترداد",
        "required_data_en": [
            "Baseline cost or revenue figure (SAR)",
            "Post-engagement cost or revenue figure (SAR)",
            "Engagement investment amount (SAR)",
        ],
        "required_data_ar": [
            "رقم التكلفة أو الإيرادات الأساسي (ريال)",
            "رقم التكلفة أو الإيرادات بعد التعاقد (ريال)",
            "مبلغ الاستثمار في التعاقد (ريال)",
        ],
        "template_en": (
            "[CLIENT_NAME] reduced [COST_CATEGORY] from [BASELINE_SAR] to [CURRENT_SAR], "
            "recovering [DELTA_SAR] against a [INVESTMENT_SAR] engagement — "
            "a [ROI_MULTIPLE]x ROI within [TIMEFRAME]."
        ),
        "strength_rating": "high",
        "strength_note_en": "Financial proof is the most persuasive category for economic buyers.",
        "strength_note_ar": "الإثبات المالي هو الفئة الأكثر إقناعاً للمشترين الاقتصاديين.",
    },
    "process_improvement": {
        "category_id": "process_improvement",
        "name_en": "Process Improvement",
        "name_ar": "تحسين العمليات",
        "description_en": "Operational proof: time saved, errors reduced, team adoption",
        "description_ar": "إثبات تشغيلي: الوقت الموفَّر، تقليل الأخطاء، اعتماد الفريق",
        "required_data_en": [
            "Process name and baseline cycle time (hours or days)",
            "Post-engagement cycle time",
            "Error rate before and after",
        ],
        "required_data_ar": [
            "اسم العملية ووقت الدورة الأساسي (ساعات أو أيام)",
            "وقت الدورة بعد التعاقد",
            "معدل الخطأ قبل وبعد",
        ],
        "template_en": (
            "[CLIENT_NAME] reduced [PROCESS_NAME] cycle time from [BASELINE_TIME] "
            "to [CURRENT_TIME] — saving [HOURS_SAVED] hours per [PERIOD] — "
            "while cutting error rates by [ERROR_REDUCTION_PCT]%."
        ),
        "strength_rating": "medium-high",
        "strength_note_en": "Operational proof resonates with operations and IT buyers.",
        "strength_note_ar": "الإثبات التشغيلي يؤثر على مشتري العمليات وتقنية المعلومات.",
    },
    "compliance_improvement": {
        "category_id": "compliance_improvement",
        "name_en": "Compliance Improvement",
        "name_ar": "تحسين الامتثال",
        "description_en": "ZATCA, Nitaqat, PDPL posture improvement",
        "description_ar": "تحسين وضع الامتثال لزاتكا ونطاقات ونظام PDPL",
        "required_data_en": [
            "Compliance framework name (ZATCA / Nitaqat / PDPL)",
            "Baseline compliance score or percentage",
            "Post-engagement compliance score or percentage",
        ],
        "required_data_ar": [
            "اسم إطار الامتثال (زاتكا / نطاقات / PDPL)",
            "درجة الامتثال الأساسية أو النسبة المئوية",
            "درجة الامتثال أو النسبة المئوية بعد التعاقد",
        ],
        "template_en": (
            "[CLIENT_NAME] achieved [COMPLIANCE_FRAMEWORK] compliance improvement "
            "from [BASELINE_PCT]% to [CURRENT_PCT]%, "
            "reducing regulatory risk and potential penalties."
        ),
        "strength_rating": "high",
        "strength_note_en": "Compliance proof resonates strongly with CFOs and legal teams.",
        "strength_note_ar": "الإثبات التنظيمي يؤثر بقوة على المديرين الماليين والفرق القانونية.",
    },
    "competitive_win": {
        "category_id": "competitive_win",
        "name_en": "Competitive Win",
        "name_ar": "الفوز التنافسي",
        "description_en": "Proof that client won vs. competitor with Dealix insight",
        "description_ar": "إثبات أن العميل فاز على منافس بمساعدة رؤى Dealix",
        "required_data_en": [
            "Deal or contract that was won",
            "Competitor that was displaced or avoided",
            "Dealix contribution to the win (e.g. data insight, positioning)",
        ],
        "required_data_ar": [
            "الصفقة أو العقد الذي تم الفوز به",
            "المنافس الذي تم تجاوزه أو تفاديه",
            "مساهمة Dealix في الفوز (مثال: رؤية البيانات، التموضع)",
        ],
        "template_en": (
            "[CLIENT_NAME] secured [DEAL_VALUE_SAR] contract against [COMPETITOR_TYPE] "
            "by leveraging [DEALIX_INSIGHT] — "
            "a [WIN_DESCRIPTION] enabled by Dealix data positioning."
        ),
        "strength_rating": "high",
        "strength_note_en": "Peer comparison is powerful in Saudi B2B — reference wins build credibility.",
        "strength_note_ar": "المقارنة بين الأقران قوية في B2B السعودي — الانتصارات المرجعية تبني المصداقية.",
    },
    "vision_2030_contribution": {
        "category_id": "vision_2030_contribution",
        "name_en": "Vision 2030 Contribution",
        "name_ar": "الإسهام في رؤية 2030",
        "description_en": "How client KPIs aligned with Vision 2030 targets",
        "description_ar": "كيف توافقت مؤشرات العميل مع أهداف رؤية 2030",
        "required_data_en": [
            "Relevant Vision 2030 KPI (e.g. Saudization rate, digital transaction share)",
            "Baseline KPI value",
            "Post-engagement KPI value",
        ],
        "required_data_ar": [
            "مؤشر رؤية 2030 ذو الصلة (مثال: معدل السعودة، حصة المعاملات الرقمية)",
            "قيمة المؤشر الأساسية",
            "قيمة المؤشر بعد التعاقد",
        ],
        "template_en": (
            "[CLIENT_NAME] improved [VISION_2030_KPI] from [BASELINE] to [CURRENT], "
            "contributing to [RELEVANT_2030_PILLAR] targets "
            "and demonstrating alignment with the Kingdom's transformation agenda."
        ),
        "strength_rating": "medium",
        "strength_note_en": (
            "Relevant for government and quasi-government clients where "
            "Vision 2030 alignment is a procurement criterion."
        ),
        "strength_note_ar": (
            "مناسب للعملاء الحكوميين وشبه الحكوميين حيث يُعدّ "
            "التوافق مع رؤية 2030 معياراً في المشتريات."
        ),
    },
}

_PROOF_PACK_SECTIONS: list[dict[str, Any]] = [
    {
        "order": 1,
        "section_id": "client_context",
        "title_en": "Client Context",
        "title_ar": "سياق العميل",
        "purpose_en": "Who is the client, what stage are they at, and what challenge brought them to Dealix.",
        "purpose_ar": "من هو العميل، وما هو مرحلته، وما التحدي الذي قاده إلى Dealix.",
        "required_fields_en": ["Client name", "Sector", "Engagement type", "Engagement start date", "Primary challenge"],
    },
    {
        "order": 2,
        "section_id": "baseline_metrics",
        "title_en": "Baseline Metrics",
        "title_ar": "المقاييس الأساسية",
        "purpose_en": "State of key metrics BEFORE Dealix engagement — establishes the starting point for proof.",
        "purpose_ar": "حالة المقاييس الرئيسية قبل تعاقد Dealix — يُرسي نقطة البداية للإثبات.",
        "required_fields_en": ["Metric name", "Baseline value", "Unit", "Measurement date"],
    },
    {
        "order": 3,
        "section_id": "results_after_dealix",
        "title_en": "Results After Dealix",
        "title_ar": "النتائج بعد Dealix",
        "purpose_en": "State of metrics AFTER engagement, clearly attributed to Dealix work.",
        "purpose_ar": "حالة المقاييس بعد التعاقد، مع إسناد واضح لعمل Dealix.",
        "required_fields_en": ["Metric name", "Current value", "Delta vs baseline", "Attribution note"],
    },
    {
        "order": 4,
        "section_id": "client_testimonial",
        "title_en": "Client Testimonial",
        "title_ar": "شهادة العميل",
        "purpose_en": "Direct quote or NPS score from the internal champion validating the engagement.",
        "purpose_ar": "اقتباس مباشر أو درجة NPS من البطل الداخلي للتحقق من قيمة التعاقد.",
        "required_fields_en": ["Champion name", "Champion title", "NPS score (0–10)", "Testimonial quote (optional)"],
    },
    {
        "order": 5,
        "section_id": "investment_vs_return",
        "title_en": "Investment vs. Return",
        "title_ar": "الاستثمار مقابل العائد",
        "purpose_en": "Simple ROI table: engagement cost vs. quantified value delivered.",
        "purpose_ar": "جدول عائد الاستثمار البسيط: تكلفة التعاقد مقابل القيمة المُسلَّمة.",
        "required_fields_en": ["Engagement fee (SAR)", "Quantified value delivered (SAR)", "ROI multiple", "Payback period"],
    },
]

_PROOF_QUALITY_CHECKLIST: list[dict[str, Any]] = [
    {
        "check_id": 1,
        "check_en": "All 5 required sections are populated with client-specific data.",
        "check_ar": "جميع الأقسام الخمسة المطلوبة مملوءة ببيانات خاصة بالعميل.",
    },
    {
        "check_id": 2,
        "check_en": "Baseline metrics are sourced from a documented measurement, not estimates.",
        "check_ar": "المقاييس الأساسية مستمدة من قياس موثَّق وليس تقديرات.",
    },
    {
        "check_id": 3,
        "check_en": "No guaranteed-outcome language — use 'typically see' or 'target' framing.",
        "check_ar": "لا يوجد لغة ضمان نتائج — استخدم صياغة 'نستهدف' أو 'نرى عادةً'.",
    },
    {
        "check_id": 4,
        "check_en": "Financial figures are in SAR with comma separators (e.g. SAR 1,234,567).",
        "check_ar": "الأرقام المالية بالريال السعودي مع فاصلة الآلاف (مثال: 1,234,567 ريال).",
    },
    {
        "check_id": 5,
        "check_en": "Client testimonial or NPS score is included and attributed to a named champion.",
        "check_ar": "شهادة العميل أو درجة NPS مُدرَجة ومنسوبة إلى بطل داخلي مُسمَّى.",
    },
    {
        "check_id": 6,
        "check_en": "PDPL compliance: no personal data included without explicit client consent.",
        "check_ar": "الامتثال لـ PDPL: لا بيانات شخصية مُدرَجة دون موافقة صريحة من العميل.",
    },
    {
        "check_id": 7,
        "check_en": "Proof pack reviewed and approved by founder before use in client-facing conversation.",
        "check_ar": "تمت مراجعة الحزمة والموافقة عليها من المؤسس قبل استخدامها في محادثة تواجه العميل.",
    },
]

# ---------------------------------------------------------------------------
# Request model
# ---------------------------------------------------------------------------


class ProofPackInput(BaseModel):
    client_name: str = Field(min_length=1)
    client_sector: str = Field(min_length=1)
    engagement_type: str = Field(
        description="One of: sprint | data_pack | managed_ops | custom_ai"
    )
    engagement_start_date: str = Field(
        description="ISO date format, e.g. '2025-01-15'"
    )
    baseline_metrics: dict[str, float] = Field(
        description="Metric name mapped to before-value, e.g. {'reporting_hours_per_week': 20}"
    )
    current_metrics: dict[str, float] = Field(
        description="Metric name mapped to after-value"
    )
    champion_name: str = Field(min_length=1)
    champion_title: str = Field(min_length=1)
    nps_score: float = Field(ge=0, le=10)
    testimonial_quote: str = ""


# ---------------------------------------------------------------------------
# Pure-function business logic
# ---------------------------------------------------------------------------

_VALID_ENGAGEMENT_TYPES = frozenset({"sprint", "data_pack", "managed_ops", "custom_ai"})


def _compute_metric_deltas(
    baseline: dict[str, float],
    current: dict[str, float],
) -> list[dict[str, Any]]:
    """Compute delta and percentage change for each metric present in both dicts."""
    deltas: list[dict[str, Any]] = []
    for metric, baseline_val in baseline.items():
        if metric not in current:
            continue
        current_val = current[metric]
        delta = current_val - baseline_val
        if baseline_val != 0.0:
            pct_change = round((delta / abs(baseline_val)) * 100.0, 2)
        else:
            pct_change = 0.0 if current_val == 0.0 else 100.0
        deltas.append(
            {
                "metric": metric,
                "before": baseline_val,
                "after": current_val,
                "delta": round(delta, 4),
                "pct_change": pct_change,
            }
        )
    return deltas


def _top_improvements(
    deltas: list[dict[str, Any]],
    n: int = 2,
) -> list[dict[str, Any]]:
    """Return the n metrics with the largest absolute percentage change."""
    ranked = sorted(deltas, key=lambda d: abs(d["pct_change"]), reverse=True)
    return ranked[:n]


def _fmt_sar(value: float) -> str:
    """Format a float as a SAR figure with comma separators."""
    return f"SAR {value:,.0f}"


def _nps_label(score: float) -> str:
    """Return a plain-English NPS category label."""
    if score >= 9:
        return "Promoter"
    if score >= 7:
        return "Passive"
    return "Detractor"


def _build_proof_pack(inp: ProofPackInput) -> dict[str, Any]:
    """Assemble a structured proof pack from the supplied inputs.

    Computes deltas for each shared metric, identifies the top 2 improvements,
    and populates all 5 required sections with client-specific content.
    Returns governance_decision APPROVAL_FIRST — proof packs are commercial
    assets and must be reviewed before use.
    """
    if inp.engagement_type not in _VALID_ENGAGEMENT_TYPES:
        raise HTTPException(
            status_code=422,
            detail={
                "en": (
                    f"Invalid engagement_type '{inp.engagement_type}'. "
                    "Valid values: sprint, data_pack, managed_ops, custom_ai"
                ),
                "ar": (
                    f"نوع التعاقد '{inp.engagement_type}' غير صالح. "
                    "القيم الصحيحة: sprint, data_pack, managed_ops, custom_ai"
                ),
            },
        )

    deltas = _compute_metric_deltas(inp.baseline_metrics, inp.current_metrics)
    top_two = _top_improvements(deltas)
    nps_label = _nps_label(inp.nps_score)

    # Build the 5 required sections
    sections: list[dict[str, Any]] = []

    # Section 1 — Client Context
    sections.append(
        {
            "order": 1,
            "section_id": "client_context",
            "title_en": "Client Context",
            "title_ar": "سياق العميل",
            "content_en": (
                f"{inp.client_name} is a {inp.client_sector} organisation "
                f"that engaged Dealix on a {inp.engagement_type} starting {inp.engagement_start_date}. "
                "The engagement was initiated to address measurable operational and revenue challenges."
            ),
            "content_ar": (
                f"{inp.client_name} منظمة في قطاع {inp.client_sector} "
                f"بدأت التعاقد مع Dealix على شكل {inp.engagement_type} "
                f"اعتباراً من {inp.engagement_start_date}. "
                "جاء التعاقد لمعالجة تحديات تشغيلية وإيرادية قابلة للقياس."
            ),
        }
    )

    # Section 2 — Baseline Metrics
    baseline_lines_en: list[str] = [
        f"{metric}: {value}" for metric, value in inp.baseline_metrics.items()
    ]
    baseline_lines_ar: list[str] = [
        f"{metric}: {value}" for metric, value in inp.baseline_metrics.items()
    ]
    sections.append(
        {
            "order": 2,
            "section_id": "baseline_metrics",
            "title_en": "Baseline Metrics",
            "title_ar": "المقاييس الأساسية",
            "content_en": (
                f"Before the Dealix {inp.engagement_type} engagement, "
                f"{inp.client_name} recorded the following metrics: "
                + "; ".join(baseline_lines_en)
                + "."
            ),
            "content_ar": (
                f"قبل تعاقد {inp.engagement_type} مع Dealix، "
                f"سجّلت {inp.client_name} المقاييس التالية: "
                + "؛ ".join(baseline_lines_ar)
                + "."
            ),
            "raw_metrics": inp.baseline_metrics,
        }
    )

    # Section 3 — Results After Dealix
    current_lines_en: list[str] = [
        f"{d['metric']}: {d['before']} → {d['after']} ({d['pct_change']:+.1f}%)"
        for d in deltas
    ]
    current_lines_ar: list[str] = [
        f"{d['metric']}: {d['before']} → {d['after']} ({d['pct_change']:+.1f}%)"
        for d in deltas
    ]
    sections.append(
        {
            "order": 3,
            "section_id": "results_after_dealix",
            "title_en": "Results After Dealix",
            "title_ar": "النتائج بعد Dealix",
            "content_en": (
                f"Following the Dealix engagement, {inp.client_name} achieved: "
                + "; ".join(current_lines_en)
                + ". Results are attributed to the Dealix engagement scope."
            )
            if current_lines_en
            else (
                f"Following the Dealix engagement, {inp.client_name} reported "
                "improved operational performance. Provide current metrics to quantify results."
            ),
            "content_ar": (
                f"بعد تعاقد Dealix، حققت {inp.client_name}: "
                + "؛ ".join(current_lines_ar)
                + ". تُنسب النتائج إلى نطاق تعاقد Dealix."
            )
            if current_lines_ar
            else (
                f"بعد تعاقد Dealix، أفادت {inp.client_name} بتحسُّن الأداء التشغيلي. "
                "أضف المقاييس الحالية لقياس النتائج."
            ),
            "metric_deltas": deltas,
        }
    )

    # Section 4 — Client Testimonial
    testimonial_text = (
        inp.testimonial_quote
        if inp.testimonial_quote
        else "[No quote provided — request written quote or NPS follow-up from champion]"
    )
    sections.append(
        {
            "order": 4,
            "section_id": "client_testimonial",
            "title_en": "Client Testimonial",
            "title_ar": "شهادة العميل",
            "content_en": (
                f"Champion: {inp.champion_name}, {inp.champion_title}. "
                f"NPS Score: {inp.nps_score}/10 ({nps_label}). "
                f'Quote: "{testimonial_text}"'
            ),
            "content_ar": (
                f"البطل الداخلي: {inp.champion_name}، {inp.champion_title}. "
                f"درجة NPS: {inp.nps_score}/10 ({nps_label}). "
                f'الاقتباس: "{testimonial_quote_ar(inp.testimonial_quote)}"'
            ),
            "nps_score": inp.nps_score,
            "nps_label": nps_label,
            "champion_name": inp.champion_name,
            "champion_title": inp.champion_title,
        }
    )

    # Section 5 — Investment vs. Return
    sections.append(
        {
            "order": 5,
            "section_id": "investment_vs_return",
            "title_en": "Investment vs. Return",
            "title_ar": "الاستثمار مقابل العائد",
            "content_en": (
                "Investment vs. Return table: populate with engagement fee (SAR), "
                "total quantified value delivered (SAR), ROI multiple, and payback period. "
                "Use only verified figures. Do not use guaranteed-outcome language."
            ),
            "content_ar": (
                "جدول الاستثمار مقابل العائد: أضف رسوم التعاقد (ريال)، "
                "وإجمالي القيمة المُسلَّمة والموثَّقة (ريال)، ومضاعف العائد، وفترة الاسترداد. "
                "استخدم الأرقام الموثَّقة فقط. لا تستخدم لغة ضمان النتائج."
            ),
            "placeholder_fields": {
                "engagement_fee_sar": "TBC",
                "quantified_value_sar": "TBC",
                "roi_multiple": "TBC",
                "payback_period": "TBC",
            },
        }
    )

    # ROI summary (narrative, not a guarantee)
    if top_two:
        top = top_two[0]
        roi_summary_en = (
            f"{inp.client_name} typically saw improvements across {len(deltas)} measured metrics. "
            f"The largest improvement was in '{top['metric']}' "
            f"({top['before']} → {top['after']}, {top['pct_change']:+.1f}%)."
        )
        roi_summary_ar = (
            f"شهدت {inp.client_name} عادةً تحسينات في {len(deltas)} مقياساً مقاساً. "
            f"أكبر تحسين كان في '{top['metric']}' "
            f"({top['before']} → {top['after']}, {top['pct_change']:+.1f}%)."
        )
    else:
        roi_summary_en = (
            f"{inp.client_name} completed a Dealix {inp.engagement_type} engagement. "
            "Populate baseline and current metrics to generate a quantified ROI summary."
        )
        roi_summary_ar = (
            f"أكملت {inp.client_name} تعاقد {inp.engagement_type} مع Dealix. "
            "أضف المقاييس الأساسية والحالية لتوليد ملخص عائد الاستثمار."
        )

    return {
        "governance_decision": _GOV_BUILD,
        "client_name": inp.client_name,
        "client_sector": inp.client_sector,
        "engagement_type": inp.engagement_type,
        "engagement_start_date": inp.engagement_start_date,
        "sections": sections,
        "top_improvements": top_two,
        "roi_summary_en": roi_summary_en,
        "roi_summary_ar": roi_summary_ar,
        "quality_checklist_reminder_en": (
            "Run the /quality-checklist items before using this proof pack in any client conversation."
        ),
        "quality_checklist_reminder_ar": (
            "نفّذ بنود /quality-checklist قبل استخدام هذه الحزمة في أي محادثة مع العميل."
        ),
        "disclaimer_en": (
            "This proof pack is a draft framework. All figures must be verified "
            "and approved by the founder before client-facing use."
        ),
        "disclaimer_ar": (
            "هذه الحزمة مسودة أولية. يجب التحقق من جميع الأرقام والموافقة عليها "
            "من المؤسس قبل الاستخدام أمام العميل."
        ),
    }


def testimonial_quote_ar(quote: str) -> str:
    """Return the testimonial quote as-is, or a placeholder if empty."""
    return quote if quote else "[لم يُقدَّم اقتباس — اطلب اقتباساً مكتوباً أو متابعة NPS من البطل الداخلي]"


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------


@router.get("/categories")
async def get_proof_categories() -> dict[str, Any]:
    """Return all proof categories with strength ratings and data requirements."""
    return {
        "governance_decision": _GOV_READ,
        "category_count": len(_PROOF_CATEGORIES),
        "categories": list(_PROOF_CATEGORIES.values()),
    }


@router.get("/required-sections")
async def get_required_sections() -> dict[str, Any]:
    """Return the 5 required sections that every proof pack must include."""
    return {
        "governance_decision": _GOV_READ,
        "section_count": len(_PROOF_PACK_SECTIONS),
        "sections": _PROOF_PACK_SECTIONS,
    }


@router.get("/quality-checklist")
async def get_quality_checklist() -> dict[str, Any]:
    """Return the 7-item quality checklist every proof pack must pass before use."""
    return {
        "governance_decision": _GOV_READ,
        "checklist_count": len(_PROOF_QUALITY_CHECKLIST),
        "checklist": _PROOF_QUALITY_CHECKLIST,
        "note_en": (
            "All 7 checks must pass before a proof pack is used "
            "in any client-facing proposal or renewal conversation."
        ),
        "note_ar": (
            "يجب اجتياز جميع البنود السبعة قبل استخدام الحزمة "
            "في أي محادثة مقترح أو تجديد تواجه العميل."
        ),
    }


@router.post("/build")
async def build_proof_pack(inp: ProofPackInput) -> dict[str, Any]:
    """Build a structured proof pack from baseline and current metric pairs.

    Computes deltas for each shared metric, identifies top 2 improvements,
    and populates all 5 required sections with client-specific content.
    Governance decision is APPROVAL_FIRST — proof packs are commercial assets
    that require founder review before use.
    """
    return _build_proof_pack(inp)
