"""Shared schemas for the AI Layers pipeline."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

LayerName = Literal[
    "lead_scoring",
    "account_scoring",
    "content_generation",
    "decision_passport",
    "compliance_reasoning",
    "proof_curation",
    "customer_health",
    "growth_signals",
    "executive_intelligence",
]

AI_LAYERS: tuple[LayerName, ...] = (
    "lead_scoring",
    "account_scoring",
    "content_generation",
    "decision_passport",
    "compliance_reasoning",
    "proof_curation",
    "customer_health",
    "growth_signals",
    "executive_intelligence",
)


@dataclass(frozen=True, slots=True)
class LayerContext:
    """Input contract for any AI layer.

    Attributes:
        customer_id: Tenant scope; required for every layer call.
        payload: Layer-specific dict; documented per layer.
        source_refs: Founder-supplied source references (no scraping).
        actor: Internal identity invoking the layer (governance_os.agent_id).
        external_action_requested: If True, an approval gate fires.
        contains_pii_hint: Caller's best-effort PII flag; layer re-checks.
    """

    customer_id: str
    payload: dict[str, Any] = field(default_factory=dict)
    source_refs: tuple[str, ...] = field(default_factory=tuple)
    actor: str = "dealix-internal"
    external_action_requested: bool = False
    contains_pii_hint: bool = False


@dataclass(frozen=True, slots=True)
class LayerResult:
    """Output contract for any AI layer.

    Every output must carry governance_decision (one of GovernanceDecision values).
    Notes are bilingual-friendly short strings; ledgered events are mirrored
    into value_os / friction_log / capital_os by the orchestrator.
    """

    layer: LayerName
    customer_id: str
    ok: bool
    governance_decision: str
    output: dict[str, Any]
    notes: tuple[str, ...] = field(default_factory=tuple)
    capital_asset_candidates: tuple[str, ...] = field(default_factory=tuple)
    friction_events: tuple[dict[str, Any], ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, Any]:
        return {
            "layer": self.layer,
            "customer_id": self.customer_id,
            "ok": self.ok,
            "governance_decision": self.governance_decision,
            "output": self.output,
            "notes": list(self.notes),
            "capital_asset_candidates": list(self.capital_asset_candidates),
            "friction_events": list(self.friction_events),
        }


@dataclass(frozen=True, slots=True)
class PipelineResult:
    """Result of running multiple layers under one context."""

    customer_id: str
    layers_run: tuple[LayerName, ...]
    results: dict[LayerName, LayerResult]
    overall_decision: str
    blocked_layers: tuple[LayerName, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, Any]:
        return {
            "customer_id": self.customer_id,
            "layers_run": list(self.layers_run),
            "results": {k: v.to_dict() for k, v in self.results.items()},
            "overall_decision": self.overall_decision,
            "blocked_layers": list(self.blocked_layers),
        }
