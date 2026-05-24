"""AI Layers — unified orchestration of the 9 governed AI capabilities.

Layers:
    1. lead_scoring          — score inbound leads (founder-supplied data only).
    2. account_scoring       — rank target accounts (Trust-Plane sourced).
    3. content_generation    — bilingual drafts under draft_gate + claim_safety.
    4. decision_passport     — assemble per-decision evidence chain.
    5. compliance_reasoning  — PDPL/ZATCA/SAMA/NCA reasoning per action.
    6. proof_curation        — choose best proof artifacts for context.
    7. customer_health       — health score from observed signals only.
    8. growth_signals        — warm signals from founder inputs (no scraping).
    9. executive_intelligence — exec summary across the company brain.

Every layer enforces the 11 non-negotiables via governance_os + claim_safety +
source_passport gates. Outputs carry a governance_decision; nothing leaves a
layer without one.
"""
from __future__ import annotations

from auto_client_acquisition.ai_layers.orchestrator import (
    LayerName,
    run_layer,
    run_pipeline,
)
from auto_client_acquisition.ai_layers.schemas import (
    AI_LAYERS,
    LayerContext,
    LayerResult,
    PipelineResult,
)

__all__ = [
    "AI_LAYERS",
    "LayerContext",
    "LayerName",
    "LayerResult",
    "PipelineResult",
    "run_layer",
    "run_pipeline",
]
