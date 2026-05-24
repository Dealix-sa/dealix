"""AI Layers HTTP surface — one unified router for the 9 governed AI layers.

Routes:
    GET  /api/v1/ai-layers/                 — catalog of layers + status
    GET  /api/v1/ai-layers/{layer_name}     — layer spec (inputs, outputs)
    POST /api/v1/ai-layers/{layer_name}/run — run a single layer
    POST /api/v1/ai-layers/pipeline/run     — run the full or partial pipeline

Read-only-by-default — never sends external messages. All outputs carry a
governance_decision. Calls flow through the canonical orchestrator.
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from auto_client_acquisition.ai_layers import (
    AI_LAYERS,
    LayerContext,
    LayerName,
    run_layer,
    run_pipeline,
)

router = APIRouter(prefix="/api/v1/ai-layers", tags=["ai-layers"])

_HARD_GATES: dict[str, bool] = {
    "no_live_send": True,
    "no_external_action_without_approval": True,
    "no_pii_in_logs": True,
    "no_scraping": True,
    "no_guaranteed_claims": True,
    "every_output_has_governance_decision": True,
}


class LayerRunRequest(BaseModel):
    customer_id: str = Field(min_length=1, max_length=128)
    payload: dict[str, Any] = Field(default_factory=dict)
    source_refs: list[str] = Field(default_factory=list)
    actor: str = "dealix-internal"
    external_action_requested: bool = False
    contains_pii_hint: bool = False


class PipelineRunRequest(LayerRunRequest):
    layers: list[str] | None = None


def _to_ctx(req: LayerRunRequest) -> LayerContext:
    return LayerContext(
        customer_id=req.customer_id,
        payload=req.payload,
        source_refs=tuple(req.source_refs),
        actor=req.actor,
        external_action_requested=req.external_action_requested,
        contains_pii_hint=req.contains_pii_hint,
    )


_LAYER_SPECS: dict[LayerName, dict[str, Any]] = {
    "lead_scoring": {
        "purpose": "Score founder-supplied lead signals → route bucket.",
        "required_payload_keys": [],
        "boolean_signal_keys": [
            "title_founder_exec", "b2b_company", "crm_or_pipeline",
            "uses_or_plans_ai", "saudi_or_gcc", "urgent_within_30d",
            "budget_5k_plus_sar", "partner_or_referral_potential",
            "no_company", "student_or_job_seeker", "vague_ai_curiosity",
            "no_clear_workflow_pain",
        ],
        "needs_source_refs": True,
    },
    "account_scoring": {
        "purpose": "Rank target accounts on ICP + readiness + deal bucket.",
        "required_payload_keys": ["account_name"],
        "needs_source_refs": True,
    },
    "content_generation": {
        "purpose": "Generate bilingual drafts under claim_safety + PII redact.",
        "required_payload_keys": [],
        "needs_source_refs": False,
    },
    "decision_passport": {
        "purpose": "Assemble evidence chain for a decision.",
        "required_payload_keys": ["action"],
        "needs_source_refs": True,
    },
    "compliance_reasoning": {
        "purpose": "Reason across PDPL/ZATCA/SAMA/NCA before an action.",
        "required_payload_keys": [],
        "needs_source_refs": False,
    },
    "proof_curation": {
        "purpose": "Pick best sourced proof artifacts for sector + stage.",
        "required_payload_keys": ["artifacts"],
        "needs_source_refs": False,
    },
    "customer_health": {
        "purpose": "Composite health from adoption, usage, friction, tier.",
        "required_payload_keys": [],
        "needs_source_refs": False,
    },
    "growth_signals": {
        "purpose": "Rank founder-supplied warm signals (no scraping).",
        "required_payload_keys": [],
        "needs_source_refs": False,
    },
    "executive_intelligence": {
        "purpose": "Composite executive read across health, proof, growth, compliance.",
        "required_payload_keys": [],
        "needs_source_refs": False,
    },
}


@router.get("/")
async def catalog() -> dict[str, Any]:
    return {
        "service": "ai_layers",
        "version": "1.0.0",
        "layers": list(AI_LAYERS),
        "layer_count": len(AI_LAYERS),
        "hard_gates": _HARD_GATES,
    }


# Register the pipeline routes BEFORE the catch-all /{layer_name} routes so
# they take precedence in FastAPI's path matcher.
@router.post("/pipeline/run")
async def run_pipeline_endpoint(req: PipelineRunRequest) -> dict[str, Any]:
    ctx = _to_ctx(req)
    if req.layers:
        unknown = [layer for layer in req.layers if layer not in AI_LAYERS]
        if unknown:
            raise HTTPException(
                status_code=400, detail=f"unknown_layers:{unknown}"
            )
        chosen: tuple[LayerName, ...] = tuple(req.layers)  # type: ignore[assignment]
    else:
        chosen = AI_LAYERS
    result = run_pipeline(ctx, layers=chosen)
    return {"result": result.to_dict(), "hard_gates": _HARD_GATES}


@router.get("/{layer_name}")
async def layer_spec(layer_name: str) -> dict[str, Any]:
    if layer_name not in AI_LAYERS:
        raise HTTPException(status_code=404, detail=f"unknown_layer:{layer_name}")
    return {
        "layer": layer_name,
        "spec": _LAYER_SPECS[layer_name],  # type: ignore[index]
        "hard_gates": _HARD_GATES,
    }


@router.post("/{layer_name}/run")
async def run_one(layer_name: str, req: LayerRunRequest) -> dict[str, Any]:
    if layer_name not in AI_LAYERS:
        raise HTTPException(status_code=404, detail=f"unknown_layer:{layer_name}")
    ctx = _to_ctx(req)
    result = run_layer(layer_name, ctx)  # type: ignore[arg-type]
    return {"result": result.to_dict(), "hard_gates": _HARD_GATES}
