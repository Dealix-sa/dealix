#!/usr/bin/env python3
"""
verify_agent_registry.py — assert registries/agent_registry.yaml mirrors
the canonical Python agent registry, with every agent carrying
eval_required + kill_switch + audit_required.

Exit: 0 PASS / 1 FAIL / 2 missing deps.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
YAML_PATH = ROOT / "registries" / "agent_registry.yaml"


def main() -> int:
    strict = "--strict" in sys.argv
    failures: list[str] = []
    warnings: list[str] = []

    try:
        import yaml  # type: ignore
    except ImportError:
        print("AGENT_REGISTRY=fail reason=pyyaml_not_installed")
        return 2

    if not YAML_PATH.exists():
        print(f"AGENT_REGISTRY=fail reason=missing path={YAML_PATH}")
        return 1

    try:
        sys.path.insert(0, str(ROOT))
        from auto_client_acquisition.agent_governance.agent_registry import AGENT_REGISTRY
    except Exception as exc:  # noqa: BLE001
        print(f"AGENT_REGISTRY=fail reason=cannot_import_canonical err={exc}")
        return 1

    with YAML_PATH.open(encoding="utf-8") as f:
        view = yaml.safe_load(f)

    yaml_ids = {a["agent_id"] for a in view.get("agents", [])}
    canon_ids = set(AGENT_REGISTRY.keys())

    missing_in_yaml = canon_ids - yaml_ids
    extra_in_yaml = yaml_ids - canon_ids
    if missing_in_yaml:
        failures.append(f"missing in YAML: {sorted(missing_in_yaml)}")
    if extra_in_yaml:
        failures.append(f"extra in YAML (not in canonical): {sorted(extra_in_yaml)}")

    for entry in view.get("agents", []):
        aid = entry.get("agent_id")
        for required_flag in ("eval_required", "kill_switch", "audit_required"):
            if not entry.get(required_flag, False):
                failures.append(f"agent {aid}: {required_flag} not true")
        if "max_autonomy" not in entry:
            failures.append(f"agent {aid}: max_autonomy missing")

    defaults = view.get("default_governance", {})
    for flag in ("eval_required", "kill_switch", "audit_required", "logging_required"):
        if not defaults.get(flag):
            warnings.append(f"default_governance.{flag} not true")

    verdict = "PASS" if not failures and (not strict or not warnings) else "FAIL"
    print(f"AGENT_REGISTRY={verdict.lower()}")
    print(f"AGENT_REGISTRY_AGENTS_CANON={len(canon_ids)}")
    print(f"AGENT_REGISTRY_AGENTS_YAML={len(yaml_ids)}")
    print(f"AGENT_REGISTRY_FAILS={len(failures)}")
    print(f"AGENT_REGISTRY_WARNS={len(warnings)}")
    if failures:
        print("\n## Agent Registry FAILURES")
        for f in failures:
            print(f"  - {f}")
    if warnings:
        print("\n## Agent Registry WARNINGS")
        for w in warnings:
            print(f"  - {w}")
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
