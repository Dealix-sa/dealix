#!/usr/bin/env python3
"""verify_agent_registry.py — every agent must declare owner + safety controls.

Mandatory fields per agent:
    owner, kill_switch, eval_required, audit_required, allowed_write_targets,
    risk_class.
"""
from __future__ import annotations

import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("PyYAML missing", file=sys.stderr)
    sys.exit(2)

REPO = Path(__file__).resolve().parents[1]
REGISTRY = REPO / "registries" / "agent_registry.yaml"

REQUIRED_FIELDS = (
    "owner",
    "kill_switch",
    "eval_required",
    "audit_required",
    "allowed_write_targets",
    "risk_class",
)
ALLOWED_RISK = {"A1", "A2", "A3"}


def main() -> int:
    if not REGISTRY.exists():
        print(f"missing:{REGISTRY.relative_to(REPO)}", file=sys.stderr)
        return 1
    try:
        data = yaml.safe_load(REGISTRY.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        print(f"invalid_yaml:{exc}", file=sys.stderr)
        return 1
    if not isinstance(data, dict):
        print("registry_root_not_mapping", file=sys.stderr)
        return 1

    agents = data.get("agents") or {}
    if not isinstance(agents, dict) or not agents:
        print("no_agents_defined", file=sys.stderr)
        return 1

    failures: list[str] = []
    for name, spec in agents.items():
        if not isinstance(spec, dict):
            failures.append(f"bad_shape:{name}")
            continue
        for field in REQUIRED_FIELDS:
            if field not in spec:
                failures.append(f"missing_field:{name}:{field}")
        risk = spec.get("risk_class")
        if risk and risk not in ALLOWED_RISK:
            failures.append(f"bad_risk_class:{name}:{risk}")
        if spec.get("risk_class") == "A3" and spec.get("auto_execute") is True:
            failures.append(f"a3_auto_execute_forbidden:{name}")
        if not isinstance(spec.get("allowed_write_targets"), list):
            failures.append(f"allowed_write_targets_not_list:{name}")

    for f in failures:
        print(f, file=sys.stderr)
    ok = not failures
    print(
        f"AGENT_REGISTRY_PASS={'true' if ok else 'false'} "
        f"(agents={len(agents)}, failures={len(failures)})"
    )
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
