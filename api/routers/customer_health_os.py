"""
Wave 16.0 — Customer Health OS HTTP surface.

Exposes churn prediction, revenue forecast, expansion signals, and
intervention playbooks for the founder's customer portfolio:
  POST /api/v1/customer-health/churn-predict        — single customer churn score
  POST /api/v1/customer-health/churn-batch          — batch churn scoring (max 50)
  POST /api/v1/customer-health/forecast             — 30/60/90-day revenue forecast
  POST /api/v1/customer-health/expansion-signals    — upsell readiness flags
  GET  /api/v1/customer-health/health-dashboard     — schema + governance guide
  POST /api/v1/customer-health/intervention-playbook — action plan by churn band

Hard gates:
  - no_pii_in_logs: customer_id only, never log names/emails
  - no_upsell_without_proof: expansion signals only recommended, not auto-executed
  - is_estimate_always_true: all scores carry is_estimate=True
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from auto_client_acquisition.revenue_science.churn_model import predict_churn
from auto_client_acquisition.revenue_science.forecast import compute_forecast

try:
    from auto_client_acquisition.revenue_science.expansion_model import (
        predict_expansion as _predict_expansion_native,
    )
    _HAS_NATIVE_EXPANSION = True
except Exception:  # noqa: BLE001
    _HAS_NATIVE_EXPANSION = False

router = APIRouter(
    prefix="/api/v1/customer-health",
    tags=["Wave 16 — Customer Health OS"],
)

_HARD_GATES: dict[str, bool] = {
    "no_pii_in_logs": True,
    "no_upsell_without_proof": True,
    "is_estimate_always_true": True,
    "no_auto_execute_offer": True,
}

_MAX_BATCH = 50


# ── Pydantic models ──────────────────────────────────────────────────────────


class ChurnInput(BaseModel):
    customer_id: str
    days_since_last_login: int = 0
    monthly_engagement_drop_pct: float = Field(default=0.0, ge=0.0, le=1.0)  # 0..1
    support_tickets_open: int = 0
    billing_failures_last_90d: int = 0
    nps: int | None = None
    pipeline_added_drop_pct: float = 0.0  # 0..1
    months_as_customer: int = 6


class DealInput(BaseModel):
    id: str
    company_name: str = ""
    stage: str = "new"
    value_sar: float = 0.0
    days_in_stage: int = 0
    multi_threaded: bool = False


class ForecastInput(BaseModel):
    customer_id: str
    open_deals: list[DealInput] = []
    horizon_days: int = 30


class PortfolioHealthRequest(BaseModel):
    customers: list[ChurnInput]


# ── Internal helpers ─────────────────────────────────────────────────────────


def _churn_prediction_to_dict(prediction: Any) -> dict[str, Any]:
    """Serialise a ChurnPrediction dataclass to a plain dict."""
    return {
        "customer_id": prediction.customer_id,
        "score": prediction.score,
        "band": prediction.band,
        "drivers": prediction.drivers,
        "recommended_action_ar": prediction.recommended_action_ar,
        "confidence": prediction.confidence,
        "is_estimate": True,
    }


def _compute_expansion_inline(body: ChurnInput) -> dict[str, Any]:
    """Inline expansion scoring used when the native expansion model is unavailable."""
    score = 0.0
    if (
        body.months_as_customer >= 6
        and body.monthly_engagement_drop_pct < 0.1
        and body.nps is not None
        and body.nps >= 8
    ):
        score += 0.4
    if body.support_tickets_open == 0 and body.billing_failures_last_90d == 0:
        score += 0.3
    if body.pipeline_added_drop_pct < 0.1:
        score += 0.3

    if score >= 0.6:
        band = "expand_now"
    elif score >= 0.3:
        band = "potential"
    else:
        band = "hold"

    return {
        "customer_id": body.customer_id,
        "expansion_score": round(score, 3),
        "band": band,
        "is_estimate": True,
    }


# ── Endpoints ────────────────────────────────────────────────────────────────


@router.post("/churn-predict")
async def churn_predict(body: ChurnInput) -> dict[str, Any]:
    """Compute churn probability for a single customer.

    Hard gate: is_estimate=True on all scored output.
    """
    prediction = predict_churn(**body.model_dump())
    return _churn_prediction_to_dict(prediction)


@router.post("/churn-batch")
async def churn_batch(body: PortfolioHealthRequest) -> dict[str, Any]:
    """Score a portfolio of customers and sort by churn risk DESC.

    Hard gate: maximum 50 customers per call.
    """
    if len(body.customers) > _MAX_BATCH:
        raise HTTPException(
            status_code=422,
            detail=f"Batch size {len(body.customers)} exceeds maximum of {_MAX_BATCH}.",
        )

    results: list[dict[str, Any]] = []
    for customer in body.customers:
        prediction = predict_churn(**customer.model_dump())
        results.append(_churn_prediction_to_dict(prediction))

    results.sort(key=lambda r: r["score"], reverse=True)

    critical_count = sum(1 for r in results if r["band"] == "critical")
    at_risk_count = sum(1 for r in results if r["band"] == "at_risk")

    return {
        "results": results,
        "critical_count": critical_count,
        "at_risk_count": at_risk_count,
        "is_estimate": True,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }


@router.post("/forecast")
async def forecast(body: ForecastInput) -> dict[str, Any]:
    """Compute best/likely/worst revenue forecast over the requested horizon."""
    open_deals = [d.model_dump() for d in body.open_deals]
    result = compute_forecast(
        customer_id=body.customer_id,
        open_deals=open_deals,
        horizon_days=body.horizon_days,
    )
    return {
        "customer_id": result.customer_id,
        "horizon_days": result.horizon_days,
        "period_label": result.period_label,
        "best": {
            "label": result.best.label,
            "revenue_sar": result.best.revenue_sar,
            "n_deals_closing": result.best.n_deals_closing,
            "confidence": result.best.confidence,
        },
        "likely": {
            "label": result.likely.label,
            "revenue_sar": result.likely.revenue_sar,
            "n_deals_closing": result.likely.n_deals_closing,
            "confidence": result.likely.confidence,
        },
        "worst": {
            "label": result.worst.label,
            "revenue_sar": result.worst.revenue_sar,
            "n_deals_closing": result.worst.n_deals_closing,
            "confidence": result.worst.confidence,
        },
        "deals_breakdown": result.deals_breakdown,
        "risks_ar": result.risks_ar,
        "decisions_required_ar": result.decisions_required_ar,
        "is_estimate": True,
    }


@router.post("/expansion-signals")
async def expansion_signals(body: ChurnInput) -> dict[str, Any]:
    """Return expansion readiness signal for a customer.

    Attempts the native expansion model first; falls back to inline scoring.
    Hard gate: result is recommendation only — no auto-execute upsell.
    """
    if _HAS_NATIVE_EXPANSION:
        # Derive a 0..100 health score from the available ChurnInput signals.
        health_score = max(
            0.0,
            (1.0 - body.monthly_engagement_drop_pct) * 50.0
            + (20.0 if body.support_tickets_open == 0 else 0.0)
            + (10.0 if body.billing_failures_last_90d == 0 else 0.0),
        )
        result = _predict_expansion_native(
            customer_id=body.customer_id,
            health_score=health_score,
            nps=body.nps,
            pipeline_added_growth_pct=0.0,
        )
        if result.likelihood >= 0.6:
            band = "expand_now"
        elif result.likelihood >= 0.3:
            band = "potential"
        else:
            band = "hold"
        return {
            "customer_id": body.customer_id,
            "expansion_score": result.likelihood,
            "band": band,
            "is_estimate": True,
        }

    return _compute_expansion_inline(body)


@router.get("/health-dashboard")
async def health_dashboard() -> dict[str, Any]:
    """Return the Customer Health OS schema and endpoint guide (no I/O)."""
    return {
        "module": "customer_health_os",
        "version": "16.0",
        "endpoints": [
            "POST /api/v1/customer-health/churn-predict",
            "POST /api/v1/customer-health/churn-batch",
            "POST /api/v1/customer-health/forecast",
            "POST /api/v1/customer-health/expansion-signals",
            "GET  /api/v1/customer-health/health-dashboard",
            "POST /api/v1/customer-health/intervention-playbook",
        ],
        "governance": [
            "no_upsell_without_proof",
            "is_estimate_always_true",
        ],
        "hard_gates": _HARD_GATES,
        "is_estimate": False,
    }


@router.post("/intervention-playbook")
async def intervention_playbook(body: ChurnInput) -> dict[str, Any]:
    """Return a prioritised intervention playbook based on churn band.

    Hard gate: upsell actions appear only for band='safe' and always require
    proof — the copy enforces no_upsell_without_proof at the language level.
    """
    prediction = predict_churn(**body.model_dump())

    playbooks: dict[str, dict[str, Any]] = {
        "critical": {
            "priority": "P0",
            "actions_ar": [
                "اتصل خلال 24 ساعة",
                "اعرض QBR مجاني",
                "وسّع الدعم إلى يومي",
            ],
            "actions_en": [
                "Call within 24h",
                "Offer free QBR",
                "Expand support to daily",
            ],
        },
        "at_risk": {
            "priority": "P1",
            "actions_ar": [
                "قرر call مع صانع القرار",
                "ابعث Proof Pack محدّث",
            ],
            "actions_en": [
                "Schedule decision-maker call",
                "Send updated Proof Pack",
            ],
        },
        "watch": {
            "priority": "P2",
            "actions_ar": [
                "راقب أسبوعياً",
                "ابعث insights مخصصة",
            ],
            "actions_en": [
                "Weekly monitoring",
                "Send personalized insights",
            ],
        },
        "safe": {
            "priority": "P3 (expansion)",
            "actions_ar": [
                "فكّر في upsell — لكن مع proof",
            ],
            "actions_en": [
                "Consider upsell — only with proof",
            ],
        },
    }

    playbook = playbooks.get(prediction.band, playbooks["watch"])

    return {
        "customer_id": body.customer_id,
        "churn_band": prediction.band,
        "churn_score": prediction.score,
        "playbook": playbook,
        "is_estimate": True,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }
