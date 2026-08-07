"""Dealix V3 — Revenue Machine integration registry + readiness verifier.

V3 is the *wiring map* over the canonical architecture (not a parallel package):
it proves the seven Revenue-Machine layers — lead capture → CRM ledger → offer
builder → case studies → KPIs → delivery → security/doctrine — are realised by
real, existing artifacts, and that the V3 micro-gap (inbound attribution capture)
is in place.

``verify_v3_revenue_machine_repo()`` checks that every ``canonical_artifact``
referenced in ``dealix/config/v3_revenue_machine.yaml`` exists on disk, so the
"Revenue Machine is wired" claim is a check, never a promise.
"""

from __future__ import annotations

from functools import lru_cache
from typing import Any

import yaml

from dealix.commercial_ops.paths import REPO_ROOT

_REGISTRY_YAML = REPO_ROOT / "dealix" / "config" / "v3_revenue_machine.yaml"


@lru_cache(maxsize=1)
def load_v3_revenue_machine_config() -> dict[str, Any]:
    """Load (and cache) the V3 registry YAML; ``{}`` if missing/malformed."""
    if not _REGISTRY_YAML.is_file():
        return {}
    data = yaml.safe_load(_REGISTRY_YAML.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def _layers(cfg: dict[str, Any]) -> list[dict[str, Any]]:
    layers = cfg.get("layers")
    return [x for x in layers if isinstance(x, dict)] if isinstance(layers, list) else []


def verify_v3_revenue_machine_repo() -> dict[str, Any]:
    """Ensure the registry, its map doc, and every canonical artifact exist on disk."""
    issues: list[str] = []
    cfg = load_v3_revenue_machine_config()
    if not cfg:
        return {
            "issues": ["missing dealix/config/v3_revenue_machine.yaml"],
            "ok": False,
            "layers_checked": 0,
            "artifacts_checked": 0,
        }

    map_doc = (cfg.get("map_doc") or "").strip()
    if not map_doc:
        issues.append("registry missing map_doc")
    elif not (REPO_ROOT / map_doc).is_file():
        issues.append(f"missing map doc: {map_doc}")

    for rel in cfg.get("new_in_v3") or []:
        if rel and not (REPO_ROOT / rel).is_file():
            issues.append(f"new_in_v3 artifact missing: {rel}")

    layers = _layers(cfg)
    artifacts_checked = 0
    for layer in layers:
        lid = layer.get("id", "?")
        arts = layer.get("canonical_artifacts") or []
        if not arts:
            issues.append(f"layer '{lid}' has no canonical_artifacts")
        for rel in arts:
            artifacts_checked += 1
            if rel and not (REPO_ROOT / rel).is_file():
                issues.append(f"[{lid}] canonical artifact missing: {rel}")

    return {
        "issues": issues,
        "ok": len(issues) == 0,
        "layers_checked": len(layers),
        "artifacts_checked": artifacts_checked,
    }


def build_v3_revenue_machine_snapshot() -> dict[str, Any]:
    """Compact, serializable view of the V3 registry for reports/APIs."""
    cfg = load_v3_revenue_machine_config()
    layers = _layers(cfg)
    return {
        "version": cfg.get("version"),
        "map_doc": cfg.get("map_doc"),
        "new_in_v3": cfg.get("new_in_v3") or [],
        "layers": [
            {
                "id": layer.get("id"),
                "title_en": layer.get("title_en"),
                "title_ar": layer.get("title_ar"),
                "api_endpoints": layer.get("api_endpoints") or [],
                "artifact_count": len(layer.get("canonical_artifacts") or []),
                "doctrine": layer.get("doctrine") or [],
            }
            for layer in layers
        ],
        "registry_path": str(_REGISTRY_YAML.relative_to(REPO_ROOT)).replace("\\", "/"),
    }
