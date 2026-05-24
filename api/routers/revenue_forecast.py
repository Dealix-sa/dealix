"""Wave 16 — Revenue Forecast OS HTTP surface.

Endpoints:
  POST /api/v1/revenue-forecast/forecast          — 30/60/90-day pipeline forecast
  POST /api/v1/revenue-forecast/simulate-impact   — causal impact simulation
  POST /api/v1/revenue-forecast/attribution       — channel attribution (4 models)
  GET  /api/v1/revenue-forecast/pipeline-health   — stage base probabilities
  POST /api/v1/revenue-forecast/scenarios         — all 3 horizons in one call

Hard rules:
- no_fake_revenue: all outputs are probability-weighted estimates, never confirmed revenue
- is_estimate_always_true: every scored/forecasted response carries is_estimate=True
- no_pii_in_logs: customer_id is tenant key only; no personal data in request bodies
"""
from __future__ import annotations

from dataclasses import asdict
from typing import Any, Literal

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

from auto_client_acquisition.revenue_science.forecast import (
    STAGE_BASE_PROBABILITY,
    compute_forecast,
)
from auto_client_acquisition.revenue_science.causal_impact import simulate_impact
from auto_client_acquisition.revenue_science.attribution import (
    compute_first_touch,
    compute_last_touch,
    compute_linear,
    compute_time_decay,
)

router = APIRouter(
    prefix="/api/v1/revenue-forecast",
    tags=["Wave 16 — Revenue Forecast OS"],
)

_HARD_GATES: dict[str, bool] = {
    "no_fake_revenue": True,
    "is_estimate_always_true": True,
    "no_pii_in_logs": True,
}

_GOVERNANCE_NOTE = (
    "no_fake_revenue: these are probability-weighted estimates only"
)


# ── Pydantic models ────────────────────────────────────────────────────────────


class DealItem(BaseModel):
    id: str = ""
    company_name: str = ""
    stage: str = "new"
    value_sar: float = 0.0
    days_in_stage: int = 0
    multi_threaded: bool = False


class ForecastRequest(BaseModel):
    customer_id: str
    open_deals: list[DealItem] = []
    horizon_days: Literal[30, 60, 90] = 30


class SimulateImpactRequest(BaseModel):
    """Inputs for the causal impact simulator."""

    current_baseline_revenue_sar: float = Field(
        ..., ge=0, description="Baseline SAR revenue to project from"
    )
    response_time_reduction_hours: float = Field(
        default=0.0, ge=0,
        description="How many hours faster you will respond to leads"
    )
    extra_followup_touches: int = Field(
        default=0, ge=0,
        description="Additional follow-up touches per prospect (capped at 3)"
    )
    shift_to_whatsapp_pct: float = Field(
        default=0.0, ge=0.0, le=1.0,
        description="Fraction of outreach shifted from email to WhatsApp (0..1)"
    )
    drop_n_sectors: int = Field(
        default=0, ge=0,
        description="Number of low-priority sectors to stop pursuing"
    )
    scenario_name: str = "scenario_1"


class Touchpoint(BaseModel):
    channel: str
    timestamp: str = Field(..., description="ISO 8601 timestamp")
    value_sar: float = 0.0


class AttributionRequest(BaseModel):
    customer_id: str
    touchpoints: list[Touchpoint]
    model: str = Field(
        default="linear",
        description="first_touch | last_touch | linear | time_decay",
    )


class ScenariosRequest(ForecastRequest):
    """Run all 3 horizons (30/60/90 days) in a single call."""


# ── Helper ─────────────────────────────────────────────────────────────────────


def _forecast_to_dict(forecast: Any) -> dict[str, Any]:
    """Convert Forecast dataclass to a JSON-serialisable dict."""
    return {
        "customer_id": forecast.customer_id,
        "horizon_days": forecast.horizon_days,
        "period_label": forecast.period_label,
        "best": asdict(forecast.best),
        "likely": asdict(forecast.likely),
        "worst": asdict(forecast.worst),
        "deals_breakdown": forecast.deals_breakdown,
        "risks_ar": forecast.risks_ar,
        "decisions_required_ar": forecast.decisions_required_ar,
    }


# ── Endpoints ──────────────────────────────────────────────────────────────────


@router.post("/forecast")
async def forecast(body: ForecastRequest) -> dict[str, Any]:
    """Compute a probability-weighted revenue forecast for the supplied pipeline.

    All bands (best / likely / worst) carry is_estimate=True per the
    no_fake_revenue hard rule.
    """
    result = compute_forecast(
        customer_id=body.customer_id,
        open_deals=[d.model_dump() for d in body.open_deals],
        horizon_days=body.horizon_days,
    )
    return {
        **_forecast_to_dict(result),
        "is_estimate": True,
        "governance_note": _GOVERNANCE_NOTE,
        "hard_gates": _HARD_GATES,
    }


@router.post("/simulate-impact")
async def simulate_impact_endpoint(body: SimulateImpactRequest) -> dict[str, Any]:
    """Project incremental revenue from operational changes (levers).

    Applies multiplicative lift coefficients calibrated from pilot data.
    Result is always is_estimate=True.
    """
    scenario = simulate_impact(
        current_baseline_revenue_sar=body.current_baseline_revenue_sar,
        response_time_reduction_hours=body.response_time_reduction_hours,
        extra_followup_touches=body.extra_followup_touches,
        shift_to_whatsapp_pct=body.shift_to_whatsapp_pct,
        drop_n_sectors=body.drop_n_sectors,
        scenario_name=body.scenario_name,
    )
    return {
        "scenario_name": scenario.scenario_name,
        "baseline_revenue_sar": scenario.baseline_revenue_sar,
        "scenario_revenue_sar": scenario.scenario_revenue_sar,
        "delta_sar": scenario.delta_sar,
        "delta_pct": scenario.delta_pct,
        "explanation_ar": scenario.explanation_ar,
        "confidence": scenario.confidence,
        "risk_warnings_ar": scenario.risk_warnings_ar,
        "is_estimate": True,
        "governance_note": _GOVERNANCE_NOTE,
        "hard_gates": _HARD_GATES,
    }


@router.post("/attribution")
async def attribution(body: AttributionRequest) -> dict[str, Any]:
    """Attribute revenue across touchpoints using the requested model.

    The attribution functions expect a list of deal dicts, each containing
    touchpoints with 'channel' and 'at' (datetime) fields and a 'status'
    of 'won'.  The endpoint reshapes the flat touchpoints list into a
    synthetic single-deal envelope so callers supply only what they have.

    is_estimate=True because attribution models are approximations.
    """
    from datetime import datetime, timezone

    # Convert caller's ISO timestamp strings to datetime objects.
    touchpoints_parsed: list[dict[str, Any]] = []
    for tp in body.touchpoints:
        try:
            at = datetime.fromisoformat(tp.timestamp.replace("Z", "+00:00"))
        except ValueError:
            at = datetime.now(timezone.utc)
        touchpoints_parsed.append({"channel": tp.channel, "at": at})

    # Build a synthetic won-deal envelope.
    total_value = sum(tp.value_sar for tp in body.touchpoints)
    deals: list[dict[str, Any]] = [
        {
            "status": "won",
            "value_sar": total_value,
            "touchpoints": touchpoints_parsed,
        }
    ]

    _VALID_ATTRIBUTION_MODELS = frozenset(
        {"first_touch", "last_touch", "linear", "time_decay"}
    )
    model = body.model
    if model not in _VALID_ATTRIBUTION_MODELS:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "invalid_attribution_model",
                "message": (
                    f"model '{model}' is not supported. "
                    f"Valid values: {sorted(_VALID_ATTRIBUTION_MODELS)}"
                ),
            },
        )
    if model == "first_touch":
        result = compute_first_touch(deals=deals)
    elif model == "last_touch":
        result = compute_last_touch(deals=deals)
    elif model == "time_decay":
        result = compute_time_decay(deals=deals)
    else:
        result = compute_linear(deals=deals)

    return {
        "customer_id": body.customer_id,
        "model": result.model,
        "by_channel": result.by_channel,
        "total_revenue_sar": result.total_revenue_sar,
        "touchpoint_count": len(body.touchpoints),
        "is_estimate": True,
        "governance_note": _GOVERNANCE_NOTE,
        "hard_gates": _HARD_GATES,
    }


@router.get("/pipeline-health")
async def pipeline_health(
    horizon_days: int = Query(default=30, description="Forecast horizon in days"),
) -> dict[str, Any]:
    """Return stage base win-rate probabilities.

    is_estimate=False because these are static calibrated benchmarks,
    not a customer-specific projection.
    """
    return {
        "module": "revenue_forecast_os",
        "horizon_days": horizon_days,
        "stage_probabilities": {
            stage: prob for stage, prob in STAGE_BASE_PROBABILITY.items()
        },
        "is_estimate": False,
        "governance": "no_fake_revenue",
        "hard_gates": _HARD_GATES,
    }


@router.post("/scenarios")
async def scenarios(body: ScenariosRequest) -> dict[str, Any]:
    """Run forecast for all three horizons (30 / 60 / 90 days) in one call.

    All scenario bands carry is_estimate=True.
    """
    deals_dicts = [d.model_dump() for d in body.open_deals]
    results: dict[int, dict[str, Any]] = {}
    for horizon in (30, 60, 90):
        fc = compute_forecast(
            customer_id=body.customer_id,
            open_deals=deals_dicts,
            horizon_days=horizon,
        )
        results[horizon] = _forecast_to_dict(fc)

    return {
        "customer_id": body.customer_id,
        "scenarios": results,
        "is_estimate": True,
        "governance_note": _GOVERNANCE_NOTE,
        "hard_gates": _HARD_GATES,
    }
