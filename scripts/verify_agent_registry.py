#!/usr/bin/env python3
"""Verify ``registries/agent_registry.yaml`` matches Dealix safety contract.

Every agent must:
* declare ``approval_class_max`` and it must be one of A0/A1/A2 (NEVER A3);
* have ``external_action_allowed: false``;
* have ``kill_switch: true``, ``eval_required: true``, ``audit_required: true``;
* declare ``owner``;
* declare ``allowed_write_targets`` (may be empty list, but must be present).

Exits with code 0 on PASS, 1 on FAIL.
"""

from __future__ import annotations

import sys
from pathlib import Path

REGISTRY = Path("registries/agent_registry.yaml")
REQUIRED_FIELDS = {
    "id",
    "name",
    "purpose",
    "approval_class_max",
    "external_action_allowed",
    "kill_switch",
    "eval_required",
    "audit_required",
    "owner",
}
ALLOWED_CLASSES = {"A0", "A1", "A2"}


def _load() -> list[dict]:
    text = REGISTRY.read_text(encoding="utf-8")
    try:
        import yaml  # type: ignore[import-not-found]

        data = yaml.safe_load(text) or {}
        agents = data.get("agents", [])
        return [a for a in agents if isinstance(a, dict)]
    except ImportError:
        return _shallow(text)


def _shallow(text: str) -> list[dict]:
    agents: list[dict] = []
    current: dict | None = None
    in_agents = False
    for raw in text.splitlines():
        line = raw.rstrip()
        if not line or line.lstrip().startswith("#"):
            continue
        if not line.startswith(" "):
            in_agents = line.startswith("agents")
            continue
        if not in_agents:
            continue
        stripped = line.strip()
        if stripped.startswith("- id:"):
            if current is not None:
                agents.append(current)
            current = {"id": stripped.split(":", 1)[1].strip()}
        elif current is not None and ":" in stripped and not stripped.startswith("-"):
            k, v = stripped.split(":", 1)
            v = v.strip()
            if v.lower() == "true":
                current[k.strip()] = True
            elif v.lower() == "false":
                current[k.strip()] = False
            else:
                current[k.strip()] = v
    if current is not None:
        agents.append(current)
    return agents


def main() -> int:
    if not REGISTRY.exists():
        print("[FAIL] registry file missing", file=sys.stderr)
        return 1

    agents = _load()
    if not agents:
        print("[FAIL] no agents loaded from registry", file=sys.stderr)
        return 1

    errors: list[str] = []
    for agent in agents:
        aid = agent.get("id", "<unknown>")
        for field in REQUIRED_FIELDS:
            if field not in agent:
                errors.append(f"agent {aid}: missing field '{field}'")
        cls = agent.get("approval_class_max")
        if cls not in ALLOWED_CLASSES:
            errors.append(f"agent {aid}: approval_class_max must be in {ALLOWED_CLASSES}, got {cls!r}")
        if agent.get("external_action_allowed") is not False:
            errors.append(f"agent {aid}: external_action_allowed must be false")
        if agent.get("kill_switch") is not True:
            errors.append(f"agent {aid}: kill_switch must be true")
        if agent.get("eval_required") is not True:
            errors.append(f"agent {aid}: eval_required must be true")
        if agent.get("audit_required") is not True:
            errors.append(f"agent {aid}: audit_required must be true")
        if not agent.get("owner"):
            errors.append(f"agent {aid}: owner missing")
        if "allowed_write_targets" not in agent:
            errors.append(f"agent {aid}: allowed_write_targets must be present (may be empty)")

    if errors:
        for e in errors:
            print(f"[FAIL] {e}", file=sys.stderr)
        return 1

    print(f"[PASS] agent registry: {len(agents)} agents, all safe-defaults")
    return 0


if __name__ == "__main__":
    sys.exit(main())
