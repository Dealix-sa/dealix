"""Wave 17.0 — Intelligence Compounding OS HTTP surface.

Compounds market intelligence, customer signals, and competitive data
into an ever-improving founder knowledge base.

Endpoints:
  GET  /api/v1/intelligence/status        — health check + module exports list
  POST /api/v1/intelligence/compound-score — compute a compound intelligence score
  GET  /api/v1/intelligence/signal-types  — list all known signal types
  POST /api/v1/intelligence/market-signals — analyze market signals and return insights
  GET  /api/v1/intelligence/learning-loop — describe the intelligence compounding loop

Hard gates:
  - no_pii_in_logs: never log company names or contact data
  - is_estimate_always_true: all intelligence scores carry is_estimate=True
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel, Field

from auto_client_acquisition.intelligence_compounding_os import (
    ARABIC_INTELLIGENCE_DIMENSIONS,
    BENCHMARK_CANDIDATE_SLUGS,
    CLIENT_INTELLIGENCE_METRICS,
    DATA_PATTERN_TYPES,
    GOVERNANCE_INTELLIGENCE_SIGNALS,
    INTELLIGENCE_DASHBOARD_SIGNALS,
    INTELLIGENCE_EVENT_STREAMS,
    INTELLIGENCE_QUALITY_CONTROLS,
    MARKET_SIGNAL_SOURCES,
    PRODUCT_SIGNAL_SOURCES,
    WORKFLOW_INTELLIGENCE_SIGNALS,
    CompoundingDecision,
    MarketSignalRecord,
    ProductIntelligenceVerdict,
    arabic_intelligence_coverage_score,
    benchmark_candidate_eligible,
    client_intelligence_coverage_score,
    data_pattern_actionable,
    governance_intelligence_coverage_score,
    intelligence_dashboard_coverage_score,
    intelligence_event_stream_valid,
    intelligence_quality_controls_met,
    market_pattern_actionable_repeats,
    market_signal_record_valid,
    pattern_confidence_band,
    product_intelligence_verdict,
    suggest_compounding_decision,
    workflow_productization_candidate,
)

router = APIRouter(
    prefix="/api/v1/intelligence",
    tags=["Wave 17 — Intelligence Compounding OS"],
)

_HARD_GATES: dict[str, bool] = {
    "no_pii_in_logs": True,
    "is_estimate_always_true": True,
}

# Signal weight table — used in compound score calculation.
# market_signals: 30, customer_signals: 30, competitive_signals: 20, sector_trends: 20
_SIGNAL_WEIGHTS: dict[str, float] = {
    "market_signals": 0.30,
    "customer_signals": 0.30,
    "competitive_signals": 0.20,
    "sector_trends": 0.20,
}

# Compound growth rate per month of data history (5% compounding).
_COMPOUND_RATE_PER_MONTH: float = 0.05

# Stale signal weight penalty — signals older than 30 days lose 20% weight.
_STALE_SIGNAL_PENALTY: float = 0.20
_STALE_THRESHOLD_DAYS: int = 30


# ── Request models ─────────────────────────────────────────────────────────────


class CompoundScoreRequest(BaseModel):
    """Inputs for computing a compound intelligence score.

    Each signal dimension is a normalized 0–100 score.
    months_of_data drives the compound growth multiplier.
    stale_signal_count adjusts the effective weight downward.
    """

    market_signals: float = Field(0.0, ge=0.0, le=100.0)
    customer_signals: float = Field(0.0, ge=0.0, le=100.0)
    competitive_signals: float = Field(0.0, ge=0.0, le=100.0)
    sector_trends: float = Field(0.0, ge=0.0, le=100.0)
    months_of_data: int = Field(0, ge=0)
    stale_signal_count: int = Field(0, ge=0)
    total_signal_count: int = Field(1, ge=1)


class MarketSignalAnalysisRequest(BaseModel):
    """Batch of raw market signals for insight extraction.

    Each signal record must satisfy MarketSignalRecord validation.
    """

    signals: list[dict[str, str]] = []
    pattern_occurrences: int = Field(0, ge=0)
    avg_proof_score: float = Field(0.0, ge=0.0, le=100.0)
    retainer_path_exists: bool = False
    governance_risk_low: bool = True


# ── Helpers ────────────────────────────────────────────────────────────────────


def _compound_score(
    *,
    market_signals: float,
    customer_signals: float,
    competitive_signals: float,
    sector_trends: float,
    months_of_data: int,
    stale_signal_count: int,
    total_signal_count: int,
) -> dict[str, Any]:
    """Return compound score dict — deterministic, no I/O."""
    base = (
        _SIGNAL_WEIGHTS["market_signals"] * market_signals
        + _SIGNAL_WEIGHTS["customer_signals"] * customer_signals
        + _SIGNAL_WEIGHTS["competitive_signals"] * competitive_signals
        + _SIGNAL_WEIGHTS["sector_trends"] * sector_trends
    )
    compound_multiplier = 1.0 + _COMPOUND_RATE_PER_MONTH * months_of_data
    # Stale penalty reduces the multiplier proportionally.
    stale_fraction = min(
        1.0,
        stale_signal_count / max(total_signal_count, 1),
    )
    stale_adjusted_multiplier = compound_multiplier * (
        1.0 - stale_fraction * _STALE_SIGNAL_PENALTY
    )
    raw_score = min(100.0, base * stale_adjusted_multiplier)
    return {
        "base_score": round(base, 2),
        "compound_multiplier": round(stale_adjusted_multiplier, 4),
        "compound_score": round(raw_score, 2),
        "months_of_data": months_of_data,
        "stale_signal_count": stale_signal_count,
        "total_signal_count": total_signal_count,
        "is_estimate": True,
    }


# ── Endpoints ──────────────────────────────────────────────────────────────────


@router.get("/status")
async def status() -> dict[str, Any]:
    """Layer health check and module exports list."""
    return {
        "service": "intelligence_compounding_os",
        "wave": "17.0",
        "hard_gates": _HARD_GATES,
        "module_exports": {
            "compounding_decisions": [d.value for d in CompoundingDecision],
            "product_verdicts": [v.value for v in ProductIntelligenceVerdict],
            "intelligence_event_streams": list(INTELLIGENCE_EVENT_STREAMS),
            "intelligence_dashboard_signals": list(INTELLIGENCE_DASHBOARD_SIGNALS),
            "intelligence_quality_controls": list(INTELLIGENCE_QUALITY_CONTROLS),
            "market_signal_sources": list(MARKET_SIGNAL_SOURCES),
            "product_signal_sources": list(PRODUCT_SIGNAL_SOURCES),
            "data_pattern_types": list(DATA_PATTERN_TYPES),
            "workflow_intelligence_signals": list(WORKFLOW_INTELLIGENCE_SIGNALS),
            "governance_intelligence_signals": list(GOVERNANCE_INTELLIGENCE_SIGNALS),
            "client_intelligence_metrics": list(CLIENT_INTELLIGENCE_METRICS),
            "arabic_intelligence_dimensions": list(ARABIC_INTELLIGENCE_DIMENSIONS),
            "benchmark_candidate_slugs": list(BENCHMARK_CANDIDATE_SLUGS),
        },
        "signal_weights": _SIGNAL_WEIGHTS,
        "compound_rate_per_month": _COMPOUND_RATE_PER_MONTH,
        "stale_threshold_days": _STALE_THRESHOLD_DAYS,
    }


@router.post("/compound-score")
async def compute_compound_score(req: CompoundScoreRequest) -> dict[str, Any]:
    """Compute a compound intelligence score from available signals.

    Score = weighted average of signal dimensions, then compounded at 5% per
    month of data history. Stale signals (>30 days) reduce effective weight by 20%.
    All returned scores carry is_estimate=True.
    """
    result = _compound_score(
        market_signals=req.market_signals,
        customer_signals=req.customer_signals,
        competitive_signals=req.competitive_signals,
        sector_trends=req.sector_trends,
        months_of_data=req.months_of_data,
        stale_signal_count=req.stale_signal_count,
        total_signal_count=req.total_signal_count,
    )
    return {
        "governance_decision": "estimate_only",
        **result,
        "hard_gates": _HARD_GATES,
    }


@router.get("/signal-types")
async def signal_types() -> dict[str, Any]:
    """List all known signal types across all intelligence streams."""
    return {
        "governance_decision": "read_only",
        "intelligence_event_streams": list(INTELLIGENCE_EVENT_STREAMS),
        "market_signal_sources": list(MARKET_SIGNAL_SOURCES),
        "data_pattern_types": list(DATA_PATTERN_TYPES),
        "product_signal_sources": list(PRODUCT_SIGNAL_SOURCES),
        "workflow_intelligence_signals": list(WORKFLOW_INTELLIGENCE_SIGNALS),
        "governance_intelligence_signals": list(GOVERNANCE_INTELLIGENCE_SIGNALS),
        "client_intelligence_metrics": list(CLIENT_INTELLIGENCE_METRICS),
        "arabic_intelligence_dimensions": list(ARABIC_INTELLIGENCE_DIMENSIONS),
        "dashboard_signals": list(INTELLIGENCE_DASHBOARD_SIGNALS),
        "quality_controls": list(INTELLIGENCE_QUALITY_CONTROLS),
        "is_estimate": True,
    }


@router.post("/market-signals")
async def analyze_market_signals(req: MarketSignalAnalysisRequest) -> dict[str, Any]:
    """Analyze a set of market signals and return actionable insights.

    Validates each signal record, checks pattern thresholds, and suggests
    a compounding decision if signal confidence is high enough.
    """
    valid_count = 0
    invalid_count = 0
    for raw in req.signals:
        try:
            rec = MarketSignalRecord(
                signal_id=raw.get("signal_id", ""),
                source=raw.get("source", ""),
                sector=raw.get("sector", ""),
                pain=raw.get("pain", ""),
                buyer=raw.get("buyer", ""),
                recommended_offer=raw.get("recommended_offer", ""),
                confidence=raw.get("confidence", ""),
            )
            if market_signal_record_valid(rec):
                valid_count += 1
            else:
                invalid_count += 1
        except Exception:  # noqa: BLE001
            invalid_count += 1

    pattern_actionable = market_pattern_actionable_repeats(req.pattern_occurrences)
    confidence = pattern_confidence_band(req.pattern_occurrences)

    suggested_decision: str | None = None
    if confidence in ("medium", "high"):
        decision = suggest_compounding_decision(
            pattern_occurrences=req.pattern_occurrences,
            avg_proof_score=req.avg_proof_score,
            retainer_path_exists=req.retainer_path_exists,
            governance_risk_low=req.governance_risk_low,
        )
        suggested_decision = decision.value if decision is not None else None

    return {
        "governance_decision": "estimate_only",
        "valid_signal_count": valid_count,
        "invalid_signal_count": invalid_count,
        "pattern_occurrences": req.pattern_occurrences,
        "pattern_confidence": confidence,
        "pattern_actionable": pattern_actionable,
        "suggested_compounding_decision": suggested_decision,
        "is_estimate": True,
        "hard_gates": _HARD_GATES,
    }


@router.get("/learning-loop")
async def learning_loop() -> dict[str, Any]:
    """Describe the intelligence compounding loop.

    Returns a structured description of what data flows in, what processing
    occurs, and what insights are produced at each stage.
    """
    return {
        "governance_decision": "read_only",
        "loop_description": {
            "stage_1_intake": {
                "name": "signal_intake",
                "inputs": list(INTELLIGENCE_EVENT_STREAMS),
                "description": "Raw signals are ingested from market, client, data, workflow, governance, and product streams.",
            },
            "stage_2_quality_gate": {
                "name": "quality_control",
                "controls": list(INTELLIGENCE_QUALITY_CONTROLS),
                "description": "Each signal is validated against quality controls. PII is removed before processing.",
            },
            "stage_3_pattern_detection": {
                "name": "pattern_detection",
                "threshold_medium": 3,
                "threshold_high": 6,
                "description": "Patterns emerge when a signal type repeats >= 3 times (medium) or >= 6 times (high).",
            },
            "stage_4_compound_scoring": {
                "name": "compound_scoring",
                "weights": _SIGNAL_WEIGHTS,
                "compound_rate_per_month": _COMPOUND_RATE_PER_MONTH,
                "stale_penalty_pct": _STALE_SIGNAL_PENALTY * 100,
                "stale_threshold_days": _STALE_THRESHOLD_DAYS,
                "description": (
                    "Weighted score is computed across four dimensions and compounded "
                    "at 5% per month of data history. Stale signals lose 20% weight."
                ),
            },
            "stage_5_decision": {
                "name": "compounding_decision",
                "possible_decisions": [d.value for d in CompoundingDecision],
                "description": "High-confidence patterns trigger compounding decisions: scale, build, pilot, hold, kill, or productize.",
            },
            "stage_6_output": {
                "name": "knowledge_output",
                "outputs": list(INTELLIGENCE_DASHBOARD_SIGNALS),
                "description": "Insights are surfaced as dashboard signals for founder review. All outputs carry is_estimate=True.",
            },
        },
        "is_estimate": True,
        "hard_gates": _HARD_GATES,
    }
