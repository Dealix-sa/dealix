"""Revenue forecasting for Dealix's Saudi B2B client pipeline.

Runs simple forecasting models with Saudi-specific seasonality adjustments.
All data is static; no LLM or external API calls are made.
Forecasts are indicative estimates and must be reviewed before use in
client-facing materials.

Prefix: /api/v1/revenue-forecast
"""
from __future__ import annotations

import calendar
from typing import Any

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

router = APIRouter(
    prefix="/api/v1/revenue-forecast",
    tags=["Analytics"],
)

# ---------------------------------------------------------------------------
# Governance constants
# ---------------------------------------------------------------------------

_GOV_REVIEW = "ALLOW_WITH_REVIEW"

_DISCLAIMER_EN = (
    "This forecast is an indicative estimate based on historical growth rates "
    "and seasonal adjustments. Actual results depend on market conditions, "
    "client activity, and execution. Not a guarantee of revenue."
)
_DISCLAIMER_AR = (
    "هذا التوقع تقدير استرشادي مستند إلى معدلات النمو التاريخية والتعديلات الموسمية. "
    "تعتمد النتائج الفعلية على ظروف السوق ونشاط العميل والتنفيذ. "
    "ليس ضماناً للإيرادات."
)

# ---------------------------------------------------------------------------
# Static data: monthly Saudi B2B seasonality factors
# ---------------------------------------------------------------------------

_SEASONALITY_FACTORS: dict[int, dict[str, Any]] = {
    1: {
        "month_name_en": "January",
        "month_name_ar": "يناير",
        "multiplier": 1.2,
        "reason_en": "Q1 budget kickoff — enterprise buyers release new fiscal-year budgets.",
        "reason_ar": "انطلاق ميزانية الربع الأول — يُطلق مشترو المؤسسات ميزانيات السنة المالية الجديدة.",
    },
    2: {
        "month_name_en": "February",
        "month_name_ar": "فبراير",
        "multiplier": 1.3,
        "reason_en": "LEAP conference and Founding Day energy drive accelerated deal activity.",
        "reason_ar": "مؤتمر LEAP وزخم يوم التأسيس يُسرّعان نشاط الصفقات.",
    },
    3: {
        "month_name_en": "March",
        "month_name_ar": "مارس",
        "multiplier": 0.7,
        "reason_en": "Typically overlaps with Ramadan start — decision cycles slow significantly.",
        "reason_ar": "يتزامن عادةً مع بداية رمضان — تتباطأ دورات اتخاذ القرار بشكل ملحوظ.",
    },
    4: {
        "month_name_en": "April",
        "month_name_ar": "أبريل",
        "multiplier": 1.3,
        "reason_en": "Post-Eid acceleration — deferred deals from Ramadan close rapidly.",
        "reason_ar": "تسارع ما بعد العيد — تُغلق الصفقات المؤجلة من رمضان بسرعة.",
    },
    5: {
        "month_name_en": "May",
        "month_name_ar": "مايو",
        "multiplier": 1.1,
        "reason_en": "Post-Eid deals continue closing and mid-cycle pipeline fills.",
        "reason_ar": "تستمر إغلاقات صفقات ما بعد العيد وتمتلئ قنوات منتصف الدورة.",
    },
    6: {
        "month_name_en": "June",
        "month_name_ar": "يونيو",
        "multiplier": 1.0,
        "reason_en": "Mid-year review period — activity normalises ahead of H2 planning.",
        "reason_ar": "فترة مراجعة منتصف العام — يتطبّع النشاط استعداداً لتخطيط النصف الثاني.",
    },
    7: {
        "month_name_en": "July",
        "month_name_ar": "يوليو",
        "multiplier": 0.8,
        "reason_en": "Summer slowdown — key decision-makers travel or are on leave.",
        "reason_ar": "تباطؤ الصيف — كبار متخذي القرار في إجازة أو سفر.",
    },
    8: {
        "month_name_en": "August",
        "month_name_ar": "أغسطس",
        "multiplier": 0.9,
        "reason_en": "Late summer — activity picks up slightly as organisations prepare for Q3.",
        "reason_ar": "أواخر الصيف — يزداد النشاط قليلاً مع تحضير المؤسسات للربع الثالث.",
    },
    9: {
        "month_name_en": "September",
        "month_name_ar": "سبتمبر",
        "multiplier": 1.2,
        "reason_en": "National Day momentum and Q3 pipeline push.",
        "reason_ar": "زخم اليوم الوطني ودفع خط أنابيب الربع الثالث.",
    },
    10: {
        "month_name_en": "October",
        "month_name_ar": "أكتوبر",
        "multiplier": 1.3,
        "reason_en": "Q4 budget push — highest deal-close velocity of the year for most sectors.",
        "reason_ar": "دفع ميزانية الربع الرابع — أعلى سرعة إغلاق صفقات في السنة لمعظم القطاعات.",
    },
    11: {
        "month_name_en": "November",
        "month_name_ar": "نوفمبر",
        "multiplier": 1.2,
        "reason_en": "Year-end pipeline — clients finalising annual commitments.",
        "reason_ar": "خط أنابيب نهاية السنة — يُنهي العملاء التزاماتهم السنوية.",
    },
    12: {
        "month_name_en": "December",
        "month_name_ar": "ديسمبر",
        "multiplier": 0.9,
        "reason_en": "Planning mode — organisations are in budgeting and strategy for next year.",
        "reason_ar": "وضع التخطيط — المؤسسات في مرحلة رسم الميزانية والاستراتيجية للعام القادم.",
    },
}

# ---------------------------------------------------------------------------
# Static data: forecast models
# ---------------------------------------------------------------------------

_FORECAST_MODELS: dict[str, dict[str, Any]] = {
    "linear_trend": {
        "name_en": "Linear Trend",
        "name_ar": "الاتجاه الخطي",
        "description_en": (
            "Projects MRR month-by-month using a constant monthly growth rate "
            "derived from historical performance. No seasonal adjustment applied."
        ),
        "description_ar": (
            "يُسقط الإيرادات الشهرية باستخدام معدل نمو شهري ثابت "
            "مستمد من الأداء التاريخي. لا يُطبَّق أي تعديل موسمي."
        ),
        "use_case_en": (
            "Best for stable, non-seasonal businesses or when seasonal data is unreliable."
        ),
    },
    "seasonality_adjusted": {
        "name_en": "Seasonality-Adjusted",
        "name_ar": "المعدَّل موسمياً",
        "description_en": (
            "Applies Saudi B2B monthly seasonality multipliers on top of the linear trend. "
            "Reflects Ramadan slowdowns, post-Eid surges, and budget-cycle effects."
        ),
        "description_ar": (
            "يُطبّق معاملات الموسمية الشهرية لسوق B2B السعودي على الاتجاه الخطي. "
            "يعكس تباطؤ رمضان وارتفاع ما بعد العيد وتأثيرات دورة الميزانية."
        ),
        "use_case_en": (
            "Recommended for most Saudi B2B clients. Captures calendar-driven revenue patterns."
        ),
    },
    "conservative": {
        "name_en": "Conservative",
        "name_ar": "المحافظ",
        "description_en": (
            "Linear trend multiplied by 0.7 to provide a planning buffer. "
            "Suitable for stress-testing and budget floor scenarios."
        ),
        "description_ar": (
            "الاتجاه الخطي مضروباً في 0.7 لتوفير هامش تخطيطي. "
            "مناسب لاختبار الإجهاد وسيناريوهات الحد الأدنى للميزانية."
        ),
        "use_case_en": (
            "Use when building downside-scenario plans or when historical growth data is sparse."
        ),
    },
}

_VALID_MODELS = set(_FORECAST_MODELS.keys())

# ---------------------------------------------------------------------------
# Pydantic models
# ---------------------------------------------------------------------------


class ForecastInput(BaseModel):
    company_name: str = Field(..., min_length=1, max_length=150)
    current_mrr_sar: float = Field(..., gt=0, description="Current MRR in SAR")
    historical_monthly_growth_rate_pct: float = Field(
        ...,
        ge=-50,
        le=200,
        description="Historical average monthly MRR growth rate as a percentage",
    )
    forecast_months: int = Field(..., ge=1, le=24, description="Number of months to forecast (1–24)")
    model: str = Field(
        default="seasonality_adjusted",
        description="Forecast model: linear_trend | seasonality_adjusted | conservative",
    )
    include_new_pipeline_sar: float = Field(
        default=0.0,
        ge=0,
        description="Additional expected new pipeline MRR to add to the starting base (SAR)",
    )


# ---------------------------------------------------------------------------
# Pure-function core
# ---------------------------------------------------------------------------


def _run_forecast(inp: ForecastInput) -> dict[str, Any]:
    """Compute a month-by-month revenue forecast for the given input.

    Applies seasonality if model is 'seasonality_adjusted'.
    Applies a 0.7× factor if model is 'conservative'.
    Returns monthly forecast list, ARR, peak month, trough month,
    and growth versus current MRR.
    """
    growth_rate = inp.historical_monthly_growth_rate_pct / 100.0
    base_mrr = inp.current_mrr_sar + inp.include_new_pipeline_sar

    conservative_factor = 0.7 if inp.model == "conservative" else 1.0
    apply_seasonality = inp.model == "seasonality_adjusted"

    # Determine starting calendar month (use month 1 as neutral baseline
    # when no calendar anchor is provided — forecasting from an arbitrary start)
    starting_month_index = 1  # January as neutral baseline

    monthly_forecast: list[dict[str, Any]] = []
    running_mrr = base_mrr

    for offset in range(inp.forecast_months):
        month_number_in_year = ((starting_month_index - 1 + offset) % 12) + 1
        seasonality_data = _SEASONALITY_FACTORS[month_number_in_year]
        multiplier = seasonality_data["multiplier"] if apply_seasonality else 1.0

        projected_mrr = running_mrr * (1 + growth_rate) * multiplier * conservative_factor
        projected_mrr = round(projected_mrr, 2)

        monthly_forecast.append(
            {
                "forecast_month": offset + 1,
                "month_name_en": seasonality_data["month_name_en"],
                "month_name_ar": seasonality_data["month_name_ar"],
                "mrr_sar": projected_mrr,
                "seasonality_multiplier": multiplier,
            }
        )

        # Advance the running MRR by the raw growth rate (without seasonality)
        # so seasonality affects the reported figure but not the base for the next month
        running_mrr = running_mrr * (1 + growth_rate)

    # Summary stats
    mrr_values = [m["mrr_sar"] for m in monthly_forecast]
    peak_entry = max(monthly_forecast, key=lambda m: m["mrr_sar"])
    trough_entry = min(monthly_forecast, key=lambda m: m["mrr_sar"])

    total_forecast_arr_sar = round(sum(mrr_values) / len(mrr_values) * 12, 2)
    final_mrr = mrr_values[-1] if mrr_values else base_mrr
    growth_vs_current_pct = (
        round((final_mrr - inp.current_mrr_sar) / inp.current_mrr_sar * 100, 1)
        if inp.current_mrr_sar > 0
        else 0.0
    )

    return {
        "company_name": inp.company_name,
        "model_used": inp.model,
        "model_name_en": _FORECAST_MODELS[inp.model]["name_en"],
        "model_name_ar": _FORECAST_MODELS[inp.model]["name_ar"],
        "inputs_summary": {
            "current_mrr_sar": inp.current_mrr_sar,
            "include_new_pipeline_sar": inp.include_new_pipeline_sar,
            "effective_starting_mrr_sar": base_mrr,
            "historical_monthly_growth_rate_pct": inp.historical_monthly_growth_rate_pct,
            "forecast_months": inp.forecast_months,
        },
        "monthly_forecast": monthly_forecast,
        "total_forecast_arr_sar": total_forecast_arr_sar,
        "peak_month": {
            "forecast_month": peak_entry["forecast_month"],
            "month_name_en": peak_entry["month_name_en"],
            "month_name_ar": peak_entry["month_name_ar"],
            "mrr_sar": peak_entry["mrr_sar"],
        },
        "trough_month": {
            "forecast_month": trough_entry["forecast_month"],
            "month_name_en": trough_entry["month_name_en"],
            "month_name_ar": trough_entry["month_name_ar"],
            "mrr_sar": trough_entry["mrr_sar"],
        },
        "growth_vs_current_pct": growth_vs_current_pct,
        "disclaimer_en": _DISCLAIMER_EN,
        "disclaimer_ar": _DISCLAIMER_AR,
        "governance_decision": _GOV_REVIEW,
    }


# ---------------------------------------------------------------------------
# Router endpoints
# ---------------------------------------------------------------------------


@router.get("/seasonality", summary="Monthly Saudi B2B seasonality factors")
def get_seasonality() -> dict[str, Any]:
    """Return the 12-month Saudi B2B seasonality multiplier table."""
    return {
        "seasonality_factors": [
            {"month": month, **data}
            for month, data in _SEASONALITY_FACTORS.items()
        ],
        "note_en": (
            "Multipliers reflect typical Saudi B2B deal-close velocity patterns. "
            "A multiplier of 1.0 represents an average month. "
            "Values above 1.0 indicate faster-than-average close rates."
        ),
        "note_ar": (
            "تعكس المعاملات أنماط سرعة إغلاق صفقات B2B السعودي النموذجية. "
            "معامل 1.0 يمثل شهراً متوسطاً. "
            "القيم فوق 1.0 تشير إلى معدلات إغلاق أسرع من المتوسط."
        ),
        "governance_decision": _GOV_REVIEW,
    }


@router.get("/models", summary="Forecast model descriptions")
def get_models() -> dict[str, Any]:
    """Return descriptions and use cases for all available forecast models."""
    return {
        "models": [
            {"model_id": model_id, **model_data}
            for model_id, model_data in _FORECAST_MODELS.items()
        ],
        "default_model": "seasonality_adjusted",
        "governance_decision": _GOV_REVIEW,
    }


@router.post("/run", summary="Run a revenue forecast")
def run_forecast(body: ForecastInput) -> dict[str, Any]:
    """Accept forecast inputs and return a month-by-month revenue forecast.

    Three models are available: linear_trend, seasonality_adjusted, conservative.
    Governance decision: ALLOW_WITH_REVIEW.
    """
    if body.model not in _VALID_MODELS:
        raise HTTPException(
            status_code=422,
            detail={
                "error": f"Invalid model '{body.model}'.",
                "valid_models": sorted(_VALID_MODELS),
                "governance_decision": _GOV_REVIEW,
            },
        )
    return _run_forecast(body)


@router.get("/quick-estimate", summary="Quick 12-month MRR estimate")
def quick_estimate(
    current_mrr_sar: float = Query(..., gt=0, description="Current MRR in SAR"),
    growth_rate_pct: float = Query(default=10.0, ge=-50, le=200, description="Monthly growth rate %"),
) -> dict[str, Any]:
    """Return a simple 12-month seasonality-adjusted MRR estimate without full model input.

    Uses the seasonality_adjusted model for all 12 calendar months starting from month 1.
    """
    base_mrr = current_mrr_sar
    monthly_results: list[dict[str, Any]] = []
    growth_rate = growth_rate_pct / 100.0
    running_mrr = base_mrr

    for month in range(1, 13):
        seasonality_data = _SEASONALITY_FACTORS[month]
        projected = round(running_mrr * (1 + growth_rate) * seasonality_data["multiplier"], 2)
        monthly_results.append(
            {
                "month": month,
                "month_name_en": seasonality_data["month_name_en"],
                "month_name_ar": seasonality_data["month_name_ar"],
                "mrr_sar": projected,
                "seasonality_multiplier": seasonality_data["multiplier"],
            }
        )
        running_mrr = running_mrr * (1 + growth_rate)

    mrr_values = [m["mrr_sar"] for m in monthly_results]
    estimated_arr_sar = round(sum(mrr_values) / 12 * 12, 2)
    final_mrr = mrr_values[-1]
    growth_vs_current_pct = round((final_mrr - current_mrr_sar) / current_mrr_sar * 100, 1)

    return {
        "current_mrr_sar": current_mrr_sar,
        "growth_rate_pct": growth_rate_pct,
        "model_used": "seasonality_adjusted",
        "monthly_estimate": monthly_results,
        "estimated_arr_sar": estimated_arr_sar,
        "growth_vs_current_pct": growth_vs_current_pct,
        "note_en": "Quick estimate using seasonality_adjusted model. Use POST /run for full model options.",
        "note_ar": "تقدير سريع بالنموذج المعدَّل موسمياً. استخدم POST /run لخيارات النماذج الكاملة.",
        "disclaimer_en": _DISCLAIMER_EN,
        "disclaimer_ar": _DISCLAIMER_AR,
        "governance_decision": _GOV_REVIEW,
    }
