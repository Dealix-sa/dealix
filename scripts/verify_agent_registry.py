#!/usr/bin/env python3
"""Verify registries/agent_registry.yaml is well-formed.

Requirements enforced:
- every agent has id, name, purpose, approval_class_max, tools, outputs
- no A3 agent has external_action_allowed: true
- every agent has kill_switch: true and eval_required: true
"""

from __future__ import annotations

import sys
from pathlib import Path

REGISTRY_PATH = (
    Path(__file__).resolve().parents[1] / "registries" / "agent_registry.yaml"
)
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
}


def main() -> int:
    if not REGISTRY_PATH.exists():
        print(f"FAIL: missing registry {REGISTRY_PATH}")
        return 1
    try:
        import yaml  # type: ignore
    except ImportError:
        print("FAIL: PyYAML not installed; pip install pyyaml")
        return 1
    with REGISTRY_PATH.open("r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh)
    if not isinstance(data, dict):
        print("FAIL: registry is not a mapping")
        return 1
    agents = data.get("agents") or []
    if not isinstance(agents, list) or not agents:
        print("FAIL: agents list is empty")
        return 1

    errors: list[str] = []
    seen_ids: set[str] = set()
    for idx, agent in enumerate(agents):
        if not isinstance(agent, dict):
            errors.append(f"agent[{idx}] is not a mapping")
            continue
        missing = REQUIRED_FIELDS - set(agent.keys())
        if missing:
            errors.append(f"agent[{idx}] ({agent.get('id', '?')}) missing: {sorted(missing)}")
        agent_id = agent.get("id")
        if agent_id in seen_ids:
            errors.append(f"duplicate agent id: {agent_id}")
        if agent_id:
            seen_ids.add(agent_id)
        if agent.get("kill_switch") is not True:
            errors.append(f"{agent_id}: kill_switch must be true")
        if agent.get("eval_required") is not True:
            errors.append(f"{agent_id}: eval_required must be true")
        if (
            (agent.get("approval_class_max") or "").upper() == "A3"
            and agent.get("external_action_allowed") is True
        ):
            errors.append(f"{agent_id}: A3 agent cannot have external_action_allowed: true")
        # No agent except A0-restricted ones may default external_action_allowed true.
        if (
            agent.get("external_action_allowed") is True
            and (agent.get("approval_class_max") or "").upper() not in {"A0"}
        ):
            errors.append(
                f"{agent_id}: external_action_allowed: true requires approval_class_max == A0"
            )

    if errors:
        for err in errors:
            print(f"FAIL: {err}")
        return 1

    print(f"OK: agent_registry v{data.get('version', '?')}")
    print(f"  agents: {sorted(seen_ids)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
