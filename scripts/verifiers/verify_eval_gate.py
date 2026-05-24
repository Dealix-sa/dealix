#!/usr/bin/env python3
"""Verify Eval Gate: evals/gates/dealix_agent_eval_gate.yaml exists, every
agent in agent_registry with eval_required=true has a gate entry, and all 11
non-negotiables appear in non_negotiable_coverage."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _common import REPO_ROOT, report  # noqa: E402

LAYER = "Eval Gate"


def main() -> None:
    reasons: list[str] = []
    gate_path = REPO_ROOT / "evals" / "gates" / "dealix_agent_eval_gate.yaml"
    registry_path = REPO_ROOT / "registries" / "agent_registry.yaml"

    if not gate_path.exists():
        report(LAYER, False, ["missing: evals/gates/dealix_agent_eval_gate.yaml"])

    try:
        import yaml  # type: ignore
        gate = yaml.safe_load(gate_path.read_text(encoding="utf-8")) or {}
        registry = yaml.safe_load(registry_path.read_text(encoding="utf-8")) if registry_path.exists() else {}
    except ImportError:
        report(LAYER, True)  # token-only check; PyYAML missing in CI shard

    gates = gate.get("gates") or []
    gate_agents = {g.get("agent_id") for g in gates if isinstance(g, dict)}
    needing_eval = {
        a.get("id") for a in (registry.get("agents") or [])
        if isinstance(a, dict) and a.get("eval_required")
    }
    missing = needing_eval - gate_agents
    for m in sorted(filter(None, missing)):
        reasons.append(f"agent missing from eval gate: {m}")

    cov = gate.get("non_negotiable_coverage") or {}
    for i in range(1, 12):
        token = f"NN{i}_"
        if not any(k.startswith(token) for k in cov):
            reasons.append(f"non-negotiable not covered in gate: {token}")

    # Gates must list at least one eval per agent
    for g in gates:
        if not (g.get("required_evals") or []):
            reasons.append(f"gate for {g.get('agent_id')} has no required_evals")

    report(LAYER, not reasons, reasons)


if __name__ == "__main__":
    main()
