#!/usr/bin/env python3
"""Verify the agent registry is well-formed and A3 is banned."""
from __future__ import annotations

import sys
from pathlib import Path

REQUIRED_IDS = {
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
}


def main() -> int:
    repo = Path(__file__).resolve().parents[1]
    path = repo / "registries" / "agent_registry.yaml"
    if not path.exists():
        print("FAIL: agent registry missing:", path)
        return 1
    try:
        import yaml  # type: ignore
    except ImportError:
        print("WARN: pyyaml not installed; cannot fully verify registry")
        return 0
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    agents = data.get("agents") or []
    ids = {a.get("id") for a in agents}
    missing = REQUIRED_IDS - ids
    a3_violations = [
        a.get("id") for a in agents if a.get("approval_class_max") == "A3" or a.get("external_action_allowed")
    ]
    kill_switch_violations = [a.get("id") for a in agents if not a.get("kill_switch")]
    print("[agent-registry]")
    print(f"  agents present: {len(ids)}")
    print(f"  missing required: {sorted(missing)}")
    print(f"  A3 / external-action violations: {a3_violations}")
    print(f"  kill-switch violations: {kill_switch_violations}")
    fail = bool(missing) or bool(a3_violations) or bool(kill_switch_violations)
    print("RESULT:", "FAIL" if fail else "PASS")
    return 1 if fail else 0


if __name__ == "__main__":
    sys.exit(main())
