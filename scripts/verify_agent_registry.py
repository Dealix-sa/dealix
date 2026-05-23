#!/usr/bin/env python3
"""Verify registries/agent_registry.yaml against the required agent set.

Each agent must declare a minimal contract: id, name, purpose,
approval_class_max, tools, outputs, external_action_allowed, kill_switch,
eval_required, audit_required, owner, allowed_write_targets.

Exit 0 on success, 1 on any failure.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import List, Tuple

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
REGISTRY_PATH = REPO_ROOT / "registries" / "agent_registry.yaml"

REQUIRED_AGENTS = [
    "ceo_copilot",
    "brand_guardian",
    "growth_strategist",
    "distribution_operator",
    "content_strategist",
    "offer_architect",
    "performance_analyst",
    "trust_guardian",
    "eval_guardian",
    "finance_copilot",
    "delivery_copilot",
    "security_guardian",
    "productization_agent",
    "partner_revenue_agent",
    "proof_safety_agent",
    "incident_response_agent",
]

REQUIRED_FIELDS = {
    "id",
    "name",
    "purpose",
    "approval_class_max",
    "tools",
    "outputs",
    "external_action_allowed",
    "kill_switch",
    "eval_required",
    "audit_required",
    "owner",
    "allowed_write_targets",
}

ALLOWED_APPROVAL_CLASSES = {"A1", "A2", "A3"}


def load_registry() -> dict:
    if not REGISTRY_PATH.exists():
        raise SystemExit(f"missing registry: {REGISTRY_PATH}")
    with REGISTRY_PATH.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}


def main() -> int:
    registry = load_registry()
    agents = registry.get("agents") or []

    results: List[Tuple[str, bool, str]] = []
    results.append((
        "agents is a non-empty list",
        isinstance(agents, list) and len(agents) > 0,
        f"got {type(agents).__name__} of length "
        f"{len(agents) if isinstance(agents, list) else 'n/a'}",
    ))

    by_id = {a.get("id"): a for a in agents if isinstance(a, dict)}
    for agent_id in REQUIRED_AGENTS:
        agent = by_id.get(agent_id)
        if agent is None:
            results.append((f"agent {agent_id} present", False, "missing"))
            continue
        missing = REQUIRED_FIELDS - set(agent.keys())
        if missing:
            results.append((
                f"agent {agent_id} fields",
                False,
                f"missing: {sorted(missing)}",
            ))
            continue
        if agent.get("approval_class_max") not in ALLOWED_APPROVAL_CLASSES:
            results.append((
                f"agent {agent_id} approval_class_max",
                False,
                f"got {agent.get('approval_class_max')!r}",
            ))
            continue
        if not isinstance(agent.get("tools"), list) or not agent.get("tools"):
            results.append((f"agent {agent_id} tools", False, "tools must be a non-empty list"))
            continue
        if not isinstance(agent.get("outputs"), list) or not agent.get("outputs"):
            results.append((f"agent {agent_id} outputs", False, "outputs must be a non-empty list"))
            continue
        results.append((f"agent {agent_id} valid", True, "ok"))

    passed = sum(1 for _, ok, _ in results if ok)
    total = len(results)
    print("Dealix agent-registry verification")
    print("-" * 40)
    for label, ok, detail in results:
        status = "PASS" if ok else "FAIL"
        print(f"  [{status}] {label}: {detail}")
    print("-" * 40)
    print(f"summary: {passed}/{total} checks passed "
          f"({len(REQUIRED_AGENTS)} required agents)")
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
