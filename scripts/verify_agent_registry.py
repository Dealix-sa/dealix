#!/usr/bin/env python3
"""Verify registries/agent_registry.yaml conforms to non-negotiables.

- Every agent has the required fields.
- No A3 agent has external_action_allowed = true.
- kill_switch, eval_required, audit_required are all true.
"""

from __future__ import annotations

import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("[verify_agent_registry] PyYAML not installed", file=sys.stderr)
    sys.exit(2)


REPO_ROOT = Path(__file__).resolve().parent.parent
PATH = REPO_ROOT / "registries" / "agent_registry.yaml"

REQUIRED_FIELDS = [
    "id",
    "name",
    "purpose",
    "approval_class_max",
    "tools",
    "outputs",
    "external_action_allowed",
    "kill_switch",
    "eval_required",
    "owner",
    "audit_required",
]


def main() -> int:
    if not PATH.exists():
        print(f"[verify_agent_registry] missing: {PATH}")
        return 1
    data = yaml.safe_load(PATH.read_text(encoding="utf-8")) or {}
    agents = data.get("agents", [])
    if not agents:
        print("[verify_agent_registry] FAIL: no agents declared")
        return 1

    failures: list[str] = []
    for agent in agents:
        if not isinstance(agent, dict):
            failures.append(f"agent is not a dict: {agent!r}")
            continue
        agent_id = agent.get("id", "<unknown>")
        for field in REQUIRED_FIELDS:
            if field not in agent:
                failures.append(f"{agent_id}: missing field {field}")
        if agent.get("approval_class_max") == "A3" and agent.get("external_action_allowed") is True:
            failures.append(f"{agent_id}: A3 agent must NOT have external_action_allowed=true")
        for must_be_true in ("kill_switch", "eval_required", "audit_required"):
            if agent.get(must_be_true) is not True:
                failures.append(f"{agent_id}: {must_be_true} must be true")

    if failures:
        for f in failures:
            print(f"[verify_agent_registry] FAIL: {f}")
        return 1

    print(f"[verify_agent_registry] PASS  agents={len(agents)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
