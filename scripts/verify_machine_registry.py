#!/usr/bin/env python3
"""verify_machine_registry.py — every automated machine must be ownable.

Mandatory per machine:
    owner, kpi, failure_mode, recovery_path, schedule, surface.
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
REGISTRY = REPO / "registries" / "machine_registry.yaml"

REQUIRED_FIELDS = (
    "owner",
    "kpi",
    "failure_mode",
    "recovery_path",
    "schedule",
    "surface",
)


def main() -> int:
    if not REGISTRY.exists():
        print(f"missing:{REGISTRY.relative_to(REPO)}", file=sys.stderr)
        return 1
    try:
        data = yaml.safe_load(REGISTRY.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        print(f"invalid_yaml:{exc}", file=sys.stderr)
        return 1

    machines = (data or {}).get("machines") or {}
    if not isinstance(machines, dict) or not machines:
        print("no_machines_defined", file=sys.stderr)
        return 1

    failures: list[str] = []
    for name, spec in machines.items():
        if not isinstance(spec, dict):
            failures.append(f"bad_shape:{name}")
            continue
        for field in REQUIRED_FIELDS:
            if not spec.get(field):
                failures.append(f"missing_field:{name}:{field}")

    for f in failures:
        print(f, file=sys.stderr)
    ok = not failures
    print(
        f"MACHINE_REGISTRY_PASS={'true' if ok else 'false'} "
        f"(machines={len(machines)}, failures={len(failures)})"
    )
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
