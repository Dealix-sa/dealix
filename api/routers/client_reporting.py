"""Client Reporting — templates and outline generation for Saudi B2B engagements.

Covers weekly brief, monthly intelligence report, and QBR deck formats.
All generated outlines require approval before distribution to clients.

Prefix: /api/v1/client-reporting
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

router = APIRouter(prefix="/api/v1/client-reporting", tags=["Analytics"])

_GOV_READ = "ALLOW_WITH_REVIEW"
_GOV_GENERATE = "APPROVAL_FIRST"

# ---------------------------------------------------------------------------
# Static reference data
# ---------------------------------------------------------------------------

_REPORT_TEMPLATES: dict[str, dict[str, Any]] = {
    "weekly_brief": {
        "report_type": "weekly_brief",
        "name_en": "Weekly Revenue Brief",
        "name_ar": "ملخص الإيرادات الأسبوعي",
        "page_range": "1-2",
        "cadence_en": "Every Monday",
        "cadence_ar": "كل يوم الاثنين",
        "sections": [
            "Pipeline movement (wins/losses/stalls)",
            "Top 3 accounts to focus",
            "Key metric deltas (MRR, CAC, churn)",
            "Action items for the week",
        ],
        "kpis_included": [
            "MRR delta",
            "new deals",
            "churned deals",
            "pipeline value",
        ],
        "audience_en": "Champion + sales team",
        "audience_ar": "البطل الداخلي وفريق المبيعات",
        "bilingual_required": True,
    },
    "monthly_intelligence_report": {
        "report_type": "monthly_intelligence_report",
        "name_en": "Monthly Revenue Intelligence Report",
        "name_ar": "تقرير استخبارات الإيرادات الشهري",
        "page_range": "4-6",
        "cadence_en": "Monthly",
        "cadence_ar": "شهري",
        "sections": [
            "Executive summary",
            "Revenue performance vs. target",
            "Pipeline health score",
            "Account health matrix",
            "ZATCA/compliance status",
            "Data quality score",
            "Recommended actions",
            "Vision 2030 alignment update",
        ],
        "kpis_included": [
            "MRR",
            "NRR",
            "CAC",
            "churn rate",
            "pipeline coverage",
            "data quality score",
            "saudization rate",
        ],
        "audience_en": "Economic buyer + C-suite",
        "audience_ar": "المشتري الاقتصادي والمستوى التنفيذي",
        "bilingual_required": True,
    },
    "qbr_deck": {
        "report_type": "qbr_deck",
        "name_en": "Quarterly Business Review Deck",
        "name_ar": "عرض مراجعة الأعمال الفصلية",
        "page_range": "12-16 slides",
        "cadence_en": "Quarterly",
        "cadence_ar": "فصلي",
        "sections": [
            "QoQ comparison",
            "ROI proof",
            "Market benchmarks",
            "Roadmap vs. delivery",
            "Expansion opportunities",
            "Competitive landscape",
            "Renewal recommendation",
        ],
        "kpis_included": [
            "All standard KPIs + ROI multiple",
        ],
        "audience_en": "Executive sponsor + economic buyer",
        "audience_ar": "الراعي التنفيذي والمشتري الاقتصادي",
        "bilingual_required": True,
    },
}

_REPORT_DELIVERY_STANDARDS: list[dict[str, Any]] = [
    {
        "standard_id": 1,
        "standard_en": (
            "Arabic-first for executive summaries in Arabic-speaking client organizations"
        ),
        "standard_ar": (
            "تقديم الملخصات التنفيذية بالعربية أولاً في المؤسسات العربية"
        ),
    },
    {
        "standard_id": 2,
        "standard_en": (
            "No guaranteed-outcome language — use 'typically see' / 'target' language"
        ),
        "standard_ar": (
            "لا يُستخدم لغة ضمان النتائج — استخدم عبارات 'نستهدف' أو 'نرى عادةً'"
        ),
    },
    {
        "standard_id": 3,
        "standard_en": (
            "All financial figures in SAR with comma separators (e.g. SAR 1,234,567)"
        ),
        "standard_ar": (
            "جميع الأرقام المالية بالريال السعودي مع فاصلة الآلاف (مثال: 1,234,567 ريال)"
        ),
    },
    {
        "standard_id": 4,
        "standard_en": (
            "PDPL compliance: no personal data in shareable reports without consent"
        ),
        "standard_ar": (
            "الامتثال لنظام حماية البيانات الشخصية: لا بيانات شخصية في التقارير القابلة للمشاركة دون موافقة"
        ),
    },
    {
        "standard_id": 5,
        "standard_en": (
            "All reports must include a 'What's next' section with 3 specific action items"
        ),
        "standard_ar": (
            "يجب أن يتضمن كل تقرير قسم 'الخطوات التالية' بثلاثة إجراءات محددة"
        ),
    },
]

# ---------------------------------------------------------------------------
# Request / response models
# ---------------------------------------------------------------------------


class ReportGenerateInput(BaseModel):
    report_type: str = Field(
        description="One of: weekly_brief | monthly_intelligence_report | qbr_deck"
    )
    client_name: str = Field(min_length=1)
    client_sector: str = Field(min_length=1)
    reporting_period_en: str = Field(
        description="Human-readable period, e.g. 'Week of 26 May 2025'"
    )
    current_mrr_sar: float = Field(ge=0)
    prior_period_mrr_sar: float = Field(ge=0)
    pipeline_value_sar: float = Field(ge=0)
    key_wins: list[str] = Field(default_factory=list)
    key_challenges: list[str] = Field(default_factory=list)
    action_items: list[str] = Field(default_factory=list, max_length=5)


# ---------------------------------------------------------------------------
# Pure-function business logic
# ---------------------------------------------------------------------------


def _compute_mrr_growth_pct(current: float, prior: float) -> float:
    """Return MRR growth percentage. Returns 0.0 when prior is zero."""
    if prior == 0.0:
        return 0.0
    return round((current - prior) / prior * 100.0, 2)


def _fmt_sar(value: float) -> str:
    """Format a float as a SAR figure with comma separators."""
    return f"SAR {value:,.0f}"


def _generate_report_outline(inp: ReportGenerateInput) -> dict[str, Any]:
    """Build a structured report outline from the supplied inputs.

    Looks up the template, computes MRR metrics, and populates per-section
    draft content in both English and Arabic. Returns a dict with
    governance_decision set to APPROVAL_FIRST — all client-facing output
    requires review before distribution.
    """
    template = _REPORT_TEMPLATES.get(inp.report_type)
    if template is None:
        raise HTTPException(
            status_code=404,
            detail={
                "en": (
                    f"Unknown report_type '{inp.report_type}'. "
                    "Valid values: weekly_brief, monthly_intelligence_report, qbr_deck"
                ),
                "ar": (
                    f"نوع التقرير '{inp.report_type}' غير معروف. "
                    "القيم الصحيحة: weekly_brief, monthly_intelligence_report, qbr_deck"
                ),
            },
        )

    mrr_delta = inp.current_mrr_sar - inp.prior_period_mrr_sar
    growth_pct = _compute_mrr_growth_pct(inp.current_mrr_sar, inp.prior_period_mrr_sar)
    growth_direction_en = "increase" if mrr_delta >= 0 else "decrease"
    growth_direction_ar = "ارتفاع" if mrr_delta >= 0 else "انخفاض"

    computed_metrics: dict[str, Any] = {
        "current_mrr_sar": inp.current_mrr_sar,
        "prior_period_mrr_sar": inp.prior_period_mrr_sar,
        "mrr_delta_sar": round(mrr_delta, 2),
        "mrr_delta_formatted": _fmt_sar(abs(mrr_delta)),
        "growth_pct": growth_pct,
        "pipeline_value_sar": inp.pipeline_value_sar,
        "pipeline_value_formatted": _fmt_sar(inp.pipeline_value_sar),
    }

    # Build per-section draft content using the template's section list
    section_outlines: list[dict[str, str]] = []
    for section_title in template["sections"]:
        section_lower = section_title.lower()

        if "executive summary" in section_lower or "pipeline movement" in section_lower:
            draft_en = (
                f"During {inp.reporting_period_en}, {inp.client_name} "
                f"({inp.client_sector}) recorded MRR of {_fmt_sar(inp.current_mrr_sar)}, "
                f"a {growth_direction_en} of {_fmt_sar(abs(mrr_delta))} "
                f"({abs(growth_pct)}%) vs. prior period."
            )
            draft_ar = (
                f"خلال {inp.reporting_period_en}، سجّلت {inp.client_name} "
                f"({inp.client_sector}) إيرادات متكررة شهرية بلغت "
                f"{_fmt_sar(inp.current_mrr_sar)}، "
                f"بـ{growth_direction_ar} قدره {_fmt_sar(abs(mrr_delta))} "
                f"({abs(growth_pct)}%) مقارنةً بالفترة السابقة."
            )

        elif "pipeline" in section_lower:
            draft_en = (
                f"Pipeline value stands at {_fmt_sar(inp.pipeline_value_sar)}. "
                f"Key wins this period: {', '.join(inp.key_wins) if inp.key_wins else 'None recorded'}."
            )
            draft_ar = (
                f"تبلغ قيمة خط الأعمال {_fmt_sar(inp.pipeline_value_sar)}. "
                f"الانتصارات الرئيسية هذه الفترة: "
                f"{', '.join(inp.key_wins) if inp.key_wins else 'لا يوجد'}."
            )

        elif "revenue performance" in section_lower or "roi" in section_lower:
            draft_en = (
                f"MRR target tracking: current {_fmt_sar(inp.current_mrr_sar)} "
                f"vs. prior {_fmt_sar(inp.prior_period_mrr_sar)}. "
                f"Growth: {growth_pct:+.1f}%."
            )
            draft_ar = (
                f"تتبع هدف الإيرادات المتكررة: الحالي {_fmt_sar(inp.current_mrr_sar)} "
                f"مقابل السابق {_fmt_sar(inp.prior_period_mrr_sar)}. "
                f"النمو: {growth_pct:+.1f}%."
            )

        elif "metric" in section_lower or "kpi" in section_lower:
            delta_sign = "+" if mrr_delta >= 0 else ""
            draft_en = (
                f"MRR delta: {delta_sign}{_fmt_sar(mrr_delta)} ({growth_pct:+.1f}%). "
                f"Pipeline value: {_fmt_sar(inp.pipeline_value_sar)}. "
                "CAC and churn data to be added from CRM."
            )
            draft_ar = (
                f"تغيّر الإيرادات المتكررة: {delta_sign}{_fmt_sar(mrr_delta)} ({growth_pct:+.1f}%). "
                f"قيمة خط الأعمال: {_fmt_sar(inp.pipeline_value_sar)}. "
                "بيانات CAC والاضطراب تُضاف من نظام CRM."
            )

        elif "action" in section_lower:
            items_en = inp.action_items if inp.action_items else ["To be defined with client champion."]
            items_ar = inp.action_items if inp.action_items else ["يُحدَّد مع البطل الداخلي للعميل."]
            draft_en = "Action items: " + "; ".join(items_en)
            draft_ar = "بنود العمل: " + "؛ ".join(items_ar)

        elif "challenge" in section_lower or "risk" in section_lower:
            draft_en = (
                "Challenges noted: "
                + (", ".join(inp.key_challenges) if inp.key_challenges else "None flagged this period.")
            )
            draft_ar = (
                "التحديات المُرصودة: "
                + (", ".join(inp.key_challenges) if inp.key_challenges else "لا يوجد تحديات مُبلَّغ عنها.")
            )

        elif "vision 2030" in section_lower:
            draft_en = (
                f"{inp.client_name} ({inp.client_sector}) alignment update: "
                "review saudization rate, digital transformation KPIs, and SME support metrics."
            )
            draft_ar = (
                f"تحديث توافق {inp.client_name} ({inp.client_sector}) مع رؤية 2030: "
                "راجع معدل السعودة ومؤشرات التحول الرقمي ومقاييس دعم المنشآت الصغيرة."
            )

        elif "zatca" in section_lower or "compliance" in section_lower:
            draft_en = (
                "ZATCA/compliance status: confirm Phase 2 e-invoicing integration. "
                "PDPL data handling posture to be reviewed."
            )
            draft_ar = (
                "حالة زاتكا والامتثال: تأكيد تكامل الفوترة الإلكترونية المرحلة الثانية. "
                "مراجعة وضع معالجة البيانات وفق نظام PDPL."
            )

        elif "expansion" in section_lower or "renewal" in section_lower:
            draft_en = (
                f"Renewal and expansion opportunities for {inp.client_name}: "
                "identify upsell potential and contract renewal timeline."
            )
            draft_ar = (
                f"فرص التجديد والتوسع لدى {inp.client_name}: "
                "تحديد إمكانات البيع الإضافي والجدول الزمني لتجديد العقد."
            )

        elif "account" in section_lower:
            draft_en = (
                f"Account health matrix for {inp.client_name}: "
                "populate health score, adoption rate, and open support tickets."
            )
            draft_ar = (
                f"مصفوفة صحة الحساب لـ {inp.client_name}: "
                "أضف درجة الصحة ومعدل التبني وتذاكر الدعم المفتوحة."
            )

        elif "data quality" in section_lower:
            draft_en = (
                "Data quality score this period: pull latest DQ score from data_os. "
                "Target score: 80+."
            )
            draft_ar = (
                "درجة جودة البيانات لهذه الفترة: اسحب أحدث درجة من data_os. "
                "الهدف: 80 نقطة أو أكثر."
            )

        elif "top 3" in section_lower or "focus" in section_lower:
            draft_en = (
                f"Top 3 accounts to focus this week for {inp.client_name}: "
                "to be populated from CRM pipeline data."
            )
            draft_ar = (
                f"أهم 3 حسابات للتركيز عليها هذا الأسبوع لـ {inp.client_name}: "
                "يُستكمل من بيانات خط الأعمال في CRM."
            )

        elif "market benchmark" in section_lower or "competitive" in section_lower:
            draft_en = (
                f"Market benchmarks for {inp.client_sector}: "
                "typical MRR growth and pipeline coverage ratios for the sector."
            )
            draft_ar = (
                f"معايير السوق لقطاع {inp.client_sector}: "
                "معدلات نمو الإيرادات المتكررة ونسب تغطية خط الأعمال المعتادة في القطاع."
            )

        elif "roadmap" in section_lower:
            draft_en = (
                "Roadmap vs. delivery: compare committed milestones against delivered outcomes. "
                "Flag any deferred items."
            )
            draft_ar = (
                "خارطة الطريق مقابل التسليم: قارن المعالم المُلتزَم بها مع المخرجات الفعلية. "
                "أبرز أي بنود مؤجَّلة."
            )

        elif "qoq" in section_lower or "comparison" in section_lower:
            draft_en = (
                f"QoQ comparison for {inp.client_name}: "
                f"current period MRR {_fmt_sar(inp.current_mrr_sar)} vs. "
                f"prior {_fmt_sar(inp.prior_period_mrr_sar)}. "
                f"Change: {growth_pct:+.1f}%."
            )
            draft_ar = (
                f"المقارنة ربع السنوية لـ {inp.client_name}: "
                f"الإيرادات المتكررة الحالية {_fmt_sar(inp.current_mrr_sar)} "
                f"مقابل السابقة {_fmt_sar(inp.prior_period_mrr_sar)}. "
                f"التغيير: {growth_pct:+.1f}%."
            )

        else:
            # Generic fallback for any section not matched above
            draft_en = (
                f"{section_title} — populate with {inp.client_name} data "
                f"for {inp.reporting_period_en}."
            )
            draft_ar = (
                f"{section_title} — أضف بيانات {inp.client_name} "
                f"للفترة {inp.reporting_period_en}."
            )

        section_outlines.append(
            {
                "section_title_en": section_title,
                "section_title_ar": section_title,
                "draft_content_en": draft_en,
                "draft_content_ar": draft_ar,
            }
        )

    return {
        "governance_decision": _GOV_GENERATE,
        "report_type": inp.report_type,
        "report_name_en": template["name_en"],
        "report_name_ar": template["name_ar"],
        "client_name": inp.client_name,
        "client_sector": inp.client_sector,
        "period": inp.reporting_period_en,
        "computed_metrics": computed_metrics,
        "section_outlines": section_outlines,
        "next_steps_en": (
            "1. Review each section draft and replace placeholder text with verified data. "
            "2. Confirm all financial figures are in SAR with comma separators. "
            "3. Submit for founder approval before sharing with client."
        ),
        "next_steps_ar": (
            "1. راجع مسودة كل قسم واستبدل النصوص التجريبية بالبيانات الموثَّقة. "
            "2. تأكد من أن جميع الأرقام المالية بالريال السعودي مع فاصلة الآلاف. "
            "3. قدّم للمؤسس للموافقة قبل مشاركة التقرير مع العميل."
        ),
        "disclaimer_en": (
            "This outline is a draft framework. All figures must be verified "
            "before client distribution. Do not use guaranteed-outcome language."
        ),
        "disclaimer_ar": (
            "هذا المخطط مسودة أولية. يجب التحقق من جميع الأرقام قبل توزيعها على العميل. "
            "لا تستخدم لغة ضمان النتائج."
        ),
    }


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------


@router.get("/templates")
async def list_report_templates() -> dict[str, Any]:
    """Return all available report templates with metadata."""
    return {
        "governance_decision": _GOV_READ,
        "template_count": len(_REPORT_TEMPLATES),
        "templates": list(_REPORT_TEMPLATES.values()),
    }


@router.get("/templates/{report_type}")
async def get_report_template(report_type: str) -> dict[str, Any]:
    """Return a single report template by type. Returns 404 if not found."""
    template = _REPORT_TEMPLATES.get(report_type)
    if template is None:
        raise HTTPException(
            status_code=404,
            detail={
                "en": (
                    f"Report type '{report_type}' not found. "
                    "Valid types: weekly_brief, monthly_intelligence_report, qbr_deck"
                ),
                "ar": (
                    f"نوع التقرير '{report_type}' غير موجود. "
                    "الأنواع الصحيحة: weekly_brief, monthly_intelligence_report, qbr_deck"
                ),
            },
        )
    return {
        "governance_decision": _GOV_READ,
        "template": template,
    }


@router.get("/delivery-standards")
async def get_delivery_standards() -> dict[str, Any]:
    """Return the delivery quality standards that all Dealix reports must meet."""
    return {
        "governance_decision": _GOV_READ,
        "standard_count": len(_REPORT_DELIVERY_STANDARDS),
        "standards": _REPORT_DELIVERY_STANDARDS,
    }


@router.post("/generate-outline")
async def generate_report_outline(inp: ReportGenerateInput) -> dict[str, Any]:
    """Generate a structured bilingual report outline from client inputs.

    The outline includes per-section draft content in English and Arabic,
    computed MRR metrics, and next-step guidance.
    Governance decision is APPROVAL_FIRST — all client-facing output requires
    founder review before distribution.
    """
    return _generate_report_outline(inp)
