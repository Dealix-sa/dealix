"""Value realization milestones, metrics, and value case builder.

Provides milestone tracking, value metric definitions, value frameworks,
and a value case computation function. All data is static; no LLM or
external API calls are made.

Prefix: /api/v1/value-realization
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter(
    prefix="/api/v1/value-realization",
    tags=["Analytics"],
)

# ---------------------------------------------------------------------------
# Governance constants
# ---------------------------------------------------------------------------

_GOV_REVIEW = "ALLOW_WITH_REVIEW"
_GOV_APPROVAL = "APPROVAL_FIRST"

# ---------------------------------------------------------------------------
# Static data: value milestones
# ---------------------------------------------------------------------------

_VALUE_MILESTONES: list[dict[str, Any]] = [
    {
        "order": 1,
        "milestone_id": "first_login",
        "milestone_name_en": "First Login",
        "milestone_name_ar": "تسجيل الدخول الأول",
        "typical_days_to_achieve": 7,
        "proof_metric_en": "User account activated and first session recorded",
        "proof_metric_ar": "تفعيل حساب المستخدم وتسجيل أول جلسة",
    },
    {
        "order": 2,
        "milestone_id": "first_report_generated",
        "milestone_name_en": "First Report Generated",
        "milestone_name_ar": "أول تقرير يتم إنشاؤه",
        "typical_days_to_achieve": 14,
        "proof_metric_en": "At least one automated report produced by the platform",
        "proof_metric_ar": "إنتاج تقرير آلي واحد على الأقل من المنصة",
    },
    {
        "order": 3,
        "milestone_id": "first_insight_actioned",
        "milestone_name_en": "First Insight Actioned",
        "milestone_name_ar": "أول رؤية يتم تطبيقها",
        "typical_days_to_achieve": 30,
        "proof_metric_en": "Client documents a business decision driven by a platform insight",
        "proof_metric_ar": "يوثق العميل قراراً تجارياً مستنداً إلى رؤية من المنصة",
    },
    {
        "order": 4,
        "milestone_id": "team_adoption",
        "milestone_name_en": "Team Adoption",
        "milestone_name_ar": "اعتماد الفريق",
        "typical_days_to_achieve": 60,
        "proof_metric_en": "Three or more team members actively using the platform weekly",
        "proof_metric_ar": "ثلاثة أعضاء أو أكثر من الفريق يستخدمون المنصة بشكل أسبوعي",
    },
    {
        "order": 5,
        "milestone_id": "roi_demonstrated",
        "milestone_name_en": "ROI Demonstrated",
        "milestone_name_ar": "إثبات العائد على الاستثمار",
        "typical_days_to_achieve": 90,
        "proof_metric_en": "Client confirms measurable return on investment versus pre-deployment baseline",
        "proof_metric_ar": "يؤكد العميل عائداً قابلاً للقياس على الاستثمار مقارنةً بخط الأساس قبل النشر",
    },
]

# ---------------------------------------------------------------------------
# Static data: value metrics
# ---------------------------------------------------------------------------

_VALUE_METRICS: list[dict[str, Any]] = [
    {
        "metric_id": "time_saved_hours",
        "metric_name_en": "Time Saved",
        "metric_name_ar": "الوقت الموفر",
        "unit": "hours/week",
        "calculation_method_en": "Baseline reporting hours per week minus current reporting hours per week",
    },
    {
        "metric_id": "errors_reduced_pct",
        "metric_name_en": "Errors Reduced",
        "metric_name_ar": "الأخطاء المُخفَّضة",
        "unit": "percentage points",
        "calculation_method_en": "Baseline error rate percentage minus current error rate percentage",
    },
    {
        "metric_id": "report_automation_pct",
        "metric_name_en": "Report Automation",
        "metric_name_ar": "نسبة أتمتة التقارير",
        "unit": "percent",
        "calculation_method_en": "Share of previously manual reports now generated automatically by the platform",
    },
    {
        "metric_id": "decision_speed_days",
        "metric_name_en": "Decision Speed",
        "metric_name_ar": "سرعة اتخاذ القرار",
        "unit": "days",
        "calculation_method_en": "Average calendar days from data request to approved business decision, before versus after",
    },
    {
        "metric_id": "cost_avoided_sar",
        "metric_name_en": "Cost Avoided",
        "metric_name_ar": "التكاليف المُتجنَّبة",
        "unit": "SAR",
        "calculation_method_en": "Annualized hours saved multiplied by blended analyst hourly cost in SAR",
    },
    {
        "metric_id": "revenue_influenced_sar",
        "metric_name_en": "Revenue Influenced",
        "metric_name_ar": "الإيرادات المتأثرة بالمنصة",
        "unit": "SAR",
        "calculation_method_en": "Incremental revenue attributed to decisions made using platform insights",
    },
]

# ---------------------------------------------------------------------------
# Static data: value frameworks
# ---------------------------------------------------------------------------

_VALUE_FRAMEWORKS: dict[str, Any] = {
    "efficiency": {
        "name_en": "Efficiency",
        "name_ar": "الكفاءة التشغيلية",
        "primary_metrics": ["time_saved_hours", "report_automation_pct", "cost_avoided_sar"],
        "headline_formula_en": "Annualized hours saved × SAR 75/hour analyst cost",
    },
    "compliance": {
        "name_en": "Compliance",
        "name_ar": "الامتثال والحوكمة",
        "primary_metrics": ["errors_reduced_pct", "report_automation_pct", "decision_speed_days"],
        "headline_formula_en": "Error rate reduction × estimated rework cost per incident",
    },
    "growth": {
        "name_en": "Growth",
        "name_ar": "النمو والتوسع",
        "primary_metrics": ["decision_speed_days", "revenue_influenced_sar", "time_saved_hours"],
        "headline_formula_en": "Revenue influenced by platform insights over the measurement period",
    },
}

# ---------------------------------------------------------------------------
# Valid options
# ---------------------------------------------------------------------------

_VALID_FRAMEWORKS: set[str] = {"efficiency", "compliance", "growth"}

# ---------------------------------------------------------------------------
# Pydantic models
# ---------------------------------------------------------------------------


class ValueCaseInput(BaseModel):
    client_name: str
    framework: str
    baseline_reporting_hours_per_week: float = Field(..., ge=0)
    current_reporting_hours_per_week: float = Field(..., ge=0)
    baseline_error_rate_pct: float = Field(..., ge=0, le=100)
    current_error_rate_pct: float = Field(..., ge=0, le=100)
    months_since_go_live: int = Field(..., ge=0)


# ---------------------------------------------------------------------------
# Pure-function core
# ---------------------------------------------------------------------------


def _build_value_case(inp: ValueCaseInput) -> dict[str, Any]:
    """Compute a quantified value case from client baseline and current metrics.

    Returns hours saved, error reduction, annualized SAR value, milestones
    likely achieved, and the selected framework data.
    Governance decision: APPROVAL_FIRST.
    """
    if inp.framework not in _VALID_FRAMEWORKS:
        raise HTTPException(
            status_code=422,
            detail=(
                f"Invalid framework '{inp.framework}'. "
                f"Valid values: {sorted(_VALID_FRAMEWORKS)}"
            ),
        )

    hours_saved_per_week: float = max(
        0.0,
        inp.baseline_reporting_hours_per_week - inp.current_reporting_hours_per_week,
    )

    hours_saved_pct: float = (
        hours_saved_per_week / inp.baseline_reporting_hours_per_week * 100
        if inp.baseline_reporting_hours_per_week > 0
        else 0.0
    )

    error_reduction_pct: float = max(
        0.0,
        inp.baseline_error_rate_pct - inp.current_error_rate_pct,
    )

    annualized_hours_saved: float = hours_saved_per_week * 52
    estimated_sar_value: float = annualized_hours_saved * 75

    days_active: int = inp.months_since_go_live * 30
    milestones_likely_achieved: list[str] = [
        m["milestone_id"]
        for m in _VALUE_MILESTONES
        if m["typical_days_to_achieve"] <= days_active
    ]

    return {
        "client_name": inp.client_name,
        "framework": inp.framework,
        "hours_saved_per_week": hours_saved_per_week,
        "hours_saved_pct": hours_saved_pct,
        "error_reduction_pct": error_reduction_pct,
        "annualized_hours_saved": annualized_hours_saved,
        "estimated_sar_value": estimated_sar_value,
        "milestones_likely_achieved": milestones_likely_achieved,
        "framework_data": _VALUE_FRAMEWORKS[inp.framework],
        "disclaimer_en": (
            "Estimates are based on client-supplied baseline figures and "
            "standard industry assumptions. Actual results may vary."
        ),
        "disclaimer_ar": (
            "التقديرات مبنية على أرقام الأساس التي قدمها العميل وافتراضات "
            "صناعية معيارية. قد تختلف النتائج الفعلية."
        ),
        "governance_decision": _GOV_APPROVAL,
    }


# ---------------------------------------------------------------------------
# Router endpoints
# ---------------------------------------------------------------------------


@router.get("/milestones", summary="All 5 value realization milestones")
def get_milestones() -> dict[str, Any]:
    """Return all milestones in sequence order with bilingual labels."""
    return {
        "milestones": _VALUE_MILESTONES,
        "governance_decision": _GOV_REVIEW,
    }


@router.get("/metrics", summary="All 6 value metrics")
def get_metrics() -> dict[str, Any]:
    """Return all value metrics with units and calculation methods."""
    return {
        "metrics": _VALUE_METRICS,
        "governance_decision": _GOV_REVIEW,
    }


@router.get("/frameworks", summary="All 3 value frameworks")
def get_frameworks() -> dict[str, Any]:
    """Return efficiency, compliance, and growth value frameworks."""
    return {
        "frameworks": _VALUE_FRAMEWORKS,
        "governance_decision": _GOV_REVIEW,
    }


@router.post("/build-case", summary="Build a quantified value case for a client")
def build_value_case(body: ValueCaseInput) -> dict[str, Any]:
    """Accept client baseline metrics and return a computed value case.

    Governance decision: APPROVAL_FIRST.
    """
    return _build_value_case(body)
