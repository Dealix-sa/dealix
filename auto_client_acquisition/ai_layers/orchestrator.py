"""AI Layers orchestrator — runs single layers or the full pipeline.

The orchestrator never re-implements layer logic. It only routes a LayerContext
to the chosen layer(s), aggregates LayerResult objects into a PipelineResult,
and computes an overall_decision = the strictest decision across layers.
"""
from __future__ import annotations

from typing import Any, Callable

from auto_client_acquisition.ai_layers import (
    account_scoring,
    compliance_reasoning,
    content_generation,
    customer_health,
    decision_passport as decision_passport_layer,
    executive_intelligence,
    growth_signals,
    lead_scoring,
    proof_curation,
)
from auto_client_acquisition.ai_layers.schemas import (
    AI_LAYERS,
    LayerContext,
    LayerName,
    LayerResult,
    PipelineResult,
)

_REGISTRY: dict[LayerName, Callable[[LayerContext], LayerResult]] = {
    "lead_scoring": lead_scoring.run,
    "account_scoring": account_scoring.run,
    "content_generation": content_generation.run,
    "decision_passport": decision_passport_layer.run,
    "compliance_reasoning": compliance_reasoning.run,
    "proof_curation": proof_curation.run,
    "customer_health": customer_health.run,
    "growth_signals": growth_signals.run,
    "executive_intelligence": executive_intelligence.run,
}

_STRICTNESS = {
    "ALLOW": 0,
    "ALLOW_WITH_REVIEW": 1,
    "DRAFT_ONLY": 2,
    "REQUIRE_APPROVAL": 3,
    "REDACT": 4,
    "BLOCK": 5,
    "ESCALATE": 6,
}


def run_layer(name: LayerName, ctx: LayerContext) -> LayerResult:
    """Run a single named layer."""
    runner = _REGISTRY.get(name)
    if runner is None:
        return LayerResult(
            layer=name,  # type: ignore[arg-type]
            customer_id=ctx.customer_id,
            ok=False,
            governance_decision="BLOCK",
            output={"reason": f"unknown_layer:{name}"},
            notes=("unknown layer requested",),
        )
    return runner(ctx)


def run_pipeline(
    ctx: LayerContext,
    *,
    layers: tuple[LayerName, ...] | None = None,
) -> PipelineResult:
    """Run multiple layers under one context and aggregate results.

    Default order is the canonical AI_LAYERS order. The result includes an
    overall_decision = the strictest governance_decision seen.
    """
    chosen: tuple[LayerName, ...] = layers or AI_LAYERS
    results: dict[LayerName, LayerResult] = {}
    blocked: list[LayerName] = []
    overall = "ALLOW"

    for layer_name in chosen:
        r = run_layer(layer_name, ctx)
        results[layer_name] = r
        if r.governance_decision == "BLOCK":
            blocked.append(layer_name)
        if _STRICTNESS.get(r.governance_decision, 0) > _STRICTNESS.get(overall, 0):
            overall = r.governance_decision

    return PipelineResult(
        customer_id=ctx.customer_id,
        layers_run=chosen,
        results=results,
        overall_decision=overall,
        blocked_layers=tuple(blocked),
    )
