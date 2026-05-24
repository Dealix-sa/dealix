"""Layer health snapshot — per-layer status + AI Stack overview.

The health endpoint surfaces a snapshot of the eleven AI Stack layers so
operators and the demo UI can see at a glance whether the stack is
healthy. Each layer reports its module path, version (best-effort), and
whether its imports succeed.

This module performs **read-only** introspection — it never mutates state
and never calls handlers.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime, timezone
from importlib import import_module
from typing import Any

# Canonical layer name → import path. Order matches the AI Stack execution
# order so the snapshot list reads top-to-bottom.
_LAYER_MODULES: tuple[tuple[str, str, str], ...] = (
    ("L1_source_passport", "auto_client_acquisition.data_os.source_passport", "Source Passport"),
    ("L2_data_quality", "auto_client_acquisition.data_os.data_quality_score", "Data Quality"),
    ("L3_intelligence", "auto_client_acquisition.intelligence_os.rag_pipeline", "Intelligence / RAG"),
    ("L4_model_router", "auto_client_acquisition.ai.model_router", "Model Router"),
    ("L5_agent_mesh", "auto_client_acquisition.agent_os.agent_mesh", "Agent Mesh"),
    ("L6_governance", "auto_client_acquisition.governance_os.runtime_decision", "Governance Gate"),
    ("L7_proof_pack", "auto_client_acquisition.proof_os.proof_pack", "Proof Pack v2"),
    ("L8_value_ledger", "auto_client_acquisition.value_os.value_ledger", "Value Ledger"),
    ("L9_capital_ledger", "auto_client_acquisition.capital_os.capital_ledger", "Capital Ledger"),
    ("L10_adoption", "auto_client_acquisition.adoption_os.retainer_readiness", "Adoption / Retainer"),
    ("L11_self_evolving", "auto_client_acquisition.self_evolving_os.learning_store", "Self-Evolving (shadow)"),
)


@dataclass(frozen=True, slots=True)
class LayerHealth:
    """Health record for one layer."""

    layer: str
    label: str
    module: str
    healthy: bool
    version: str
    detail: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class StackHealth:
    """Health record for the full AI Stack."""

    overall_healthy: bool
    layers: tuple[LayerHealth, ...] = field(default_factory=tuple)
    snapshot_at: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "overall_healthy": self.overall_healthy,
            "snapshot_at": self.snapshot_at,
            "layers": [layer.to_dict() for layer in self.layers],
        }


def _probe_module(module_path: str) -> tuple[bool, str, str]:
    try:
        mod = import_module(module_path)
    except Exception as exc:
        return False, "0.0.0", f"import_error: {exc!r}"
    version = str(getattr(mod, "__version__", "n/a") or "n/a")
    return True, version, "ok"


def snapshot_health() -> StackHealth:
    """Snapshot the health of every AI Stack layer (read-only)."""
    layers: list[LayerHealth] = []
    overall = True
    for layer_name, module_path, label in _LAYER_MODULES:
        healthy, version, detail = _probe_module(module_path)
        if not healthy:
            overall = False
        layers.append(
            LayerHealth(
                layer=layer_name,
                label=label,
                module=module_path,
                healthy=healthy,
                version=version,
                detail=detail,
            )
        )
    return StackHealth(
        overall_healthy=overall,
        layers=tuple(layers),
        snapshot_at=datetime.now(UTC).isoformat(),
    )


def layer_versions() -> dict[str, str]:
    """Compact ``{layer: version}`` mapping for diagnostics."""
    snapshot = snapshot_health()
    return {layer.layer: layer.version for layer in snapshot.layers}


__all__ = [
    "LayerHealth",
    "StackHealth",
    "layer_versions",
    "snapshot_health",
]
