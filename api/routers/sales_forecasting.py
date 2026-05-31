"""Sales forecasting for pipeline-to-close deal and quota analysis.

Provides forecast methodologies, stage win rates, and a pipeline
forecasting function. All data is static; no LLM or external API calls
are made.

Prefix: /api/v1/sales-forecasting
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter(
    prefix="/api/v1/sales-forecasting",
    tags=["Analytics"],
)

# ---------------------------------------------------------------------------
# Governance constants
# ---------------------------------------------------------------------------

_GOV_REVIEW = "ALLOW_WITH_REVIEW"

# ---------------------------------------------------------------------------
# Static data: forecast methodologies
# ---------------------------------------------------------------------------

_FORECAST_METHODOLOGIES: dict[str, Any] = {
    "pipeline_coverage": {
        "name_en": "Pipeline Coverage",
        "name_ar": "تغطية خط أنابيب الصفقات",
        "description_en": "Forecasts revenue based on the ratio of total pipeline value to quota.",
        "accuracy_claim_en": "Best used as a directional indicator; assumes average win rates across all stages.",
        "best_for_en": "High-volume, transactional sales cycles with consistent close rates.",
    },
    "stage_weighted": {
        "name_en": "Stage-Weighted",
        "name_ar": "مرجح بالمراحل",
        "description_en": "Multiplies each deal value by the win-rate probability of its current pipeline stage.",
        "accuracy_claim_en": "More accurate than simple pipeline coverage when stage data is clean.",
        "best_for_en": "Mid-market accounts with defined sales stages and consistent stage progression.",
    },
    "ai_guided": {
        "name_en": "AI-Guided",
        "name_ar": "موجه بالذكاء الاصطناعي",
        "description_en": "Incorporates behavioral signals, engagement data, and historical patterns alongside stage win rates.",
        "accuracy_claim_en": "Requires sufficient historical data; improves over time with more closed deals.",
        "best_for_en": "Enterprise accounts with long sales cycles and rich CRM data.",
    },
}

# ---------------------------------------------------------------------------
# Static data: stage win rates
# ---------------------------------------------------------------------------

_STAGE_WIN_RATES: dict[str, float] = {
    "discovery": 10.0,
    "qualification": 25.0,
    "demo": 40.0,
    "proposal": 60.0,
    "negotiation": 75.0,
    "closed": 100.0,
}

# ---------------------------------------------------------------------------
# Static data: quota attainment benchmarks
# ---------------------------------------------------------------------------

_QUOTA_ATTAINMENT_BENCHMARKS: dict[str, int] = {
    "world_class": 120,
    "good": 100,
    "at_risk": 80,
}

# ---------------------------------------------------------------------------
# Valid methodologies
# ---------------------------------------------------------------------------

_VALID_METHODOLOGIES: set[str] = {"pipeline_coverage", "stage_weighted", "ai_guided"}

# ---------------------------------------------------------------------------
# Pydantic models
# ---------------------------------------------------------------------------


class ForecastInput(BaseModel):
    rep_name: str
    quota_sar: float = Field(..., ge=0)
    methodology: str
    pipeline_deals: list[dict] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Pure-function core
# ---------------------------------------------------------------------------


def _run_sales_forecast(inp: ForecastInput) -> dict[str, Any]:
    """Run a pipeline-to-close sales forecast for a sales representative.

    Returns total pipeline, weighted forecast, coverage ratio, attainment
    percentage, and attainment label. Governance decision: ALLOW_WITH_REVIEW.
    """
    if inp.methodology not in _VALID_METHODOLOGIES:
        raise HTTPException(
            status_code=422,
            detail=(
                f"Invalid methodology '{inp.methodology}'. "
                f"Valid values: {sorted(_VALID_METHODOLOGIES)}"
            ),
        )

    total_pipeline_sar: float = 0.0
    weighted_forecast_sar: float = 0.0

    for deal in inp.pipeline_deals:
        stage = deal.get("stage", "")
        deal_value_sar = float(deal.get("deal_value_sar", 0.0))
        win_rate = _STAGE_WIN_RATES.get(stage, 10.0)
        total_pipeline_sar += deal_value_sar
        weighted_forecast_sar += deal_value_sar * (win_rate / 100)

    pipeline_coverage_ratio: float = (
        total_pipeline_sar / inp.quota_sar if inp.quota_sar > 0 else 0.0
    )
    forecast_attainment_pct: float = (
        weighted_forecast_sar / inp.quota_sar * 100 if inp.quota_sar > 0 else 0.0
    )

    if forecast_attainment_pct >= 120:
        attainment_label = "world_class"
    elif forecast_attainment_pct >= 100:
        attainment_label = "good"
    elif forecast_attainment_pct >= 80:
        attainment_label = "at_risk"
    else:
        attainment_label = "below_target"

    return {
        "rep_name": inp.rep_name,
        "methodology": inp.methodology,
        "quota_sar": inp.quota_sar,
        "deals_count": len(inp.pipeline_deals),
        "total_pipeline_sar": total_pipeline_sar,
        "weighted_forecast_sar": weighted_forecast_sar,
        "pipeline_coverage_ratio": pipeline_coverage_ratio,
        "forecast_attainment_pct": forecast_attainment_pct,
        "attainment_label": attainment_label,
        "governance_decision": _GOV_REVIEW,
    }


# ---------------------------------------------------------------------------
# Router endpoints
# ---------------------------------------------------------------------------


@router.get("/methodologies", summary="All 3 forecast methodologies")
def get_methodologies() -> dict[str, Any]:
    """Return all forecasting methodologies with descriptions and best-fit guidance."""
    return {
        "methodologies": _FORECAST_METHODOLOGIES,
        "governance_decision": _GOV_REVIEW,
    }


@router.get("/stage-win-rates", summary="All 6 pipeline stage win rates")
def get_stage_win_rates() -> dict[str, Any]:
    """Return win-rate probabilities for each pipeline stage."""
    return {
        "stage_win_rates": _STAGE_WIN_RATES,
        "governance_decision": _GOV_REVIEW,
    }


@router.post("/run", summary="Run a sales forecast for a rep's pipeline")
def run_sales_forecast(body: ForecastInput) -> dict[str, Any]:
    """Accept pipeline deals and quota, return a forecast with attainment analysis.

    Governance decision: ALLOW_WITH_REVIEW.
    """
    return _run_sales_forecast(body)
