#!/usr/bin/env python3
"""
verify_machine_registry.py — assert registries/machine_registry.yaml
mirrors dealix/execution_assurance/registry.yaml with owner_role, KPI,
failure_mode for each machine.

Exit: 0 PASS / 1 FAIL / 2 missing deps.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VIEW = ROOT / "registries" / "machine_registry.yaml"
CANON = ROOT / "dealix" / "execution_assurance" / "registry.yaml"


def main() -> int:
    strict = "--strict" in sys.argv
    failures: list[str] = []
    warnings: list[str] = []

    try:
        import yaml  # type: ignore
    except ImportError:
        print("MACHINE_REGISTRY=fail reason=pyyaml_not_installed")
        return 2

    for p in (VIEW, CANON):
        if not p.exists():
            print(f"MACHINE_REGISTRY=fail reason=missing path={p}")
            return 1

    with VIEW.open(encoding="utf-8") as f:
        view = yaml.safe_load(f)
    with CANON.open(encoding="utf-8") as f:
        canon = yaml.safe_load(f)

    canon_machines = set(canon.get("machines", {}).keys())
    view_machines = {m["name"] for m in view.get("machines", [])}

    missing = canon_machines - view_machines
    if missing:
        failures.append(f"missing in view: {sorted(missing)}")
    extra = view_machines - canon_machines
    if extra:
        failures.append(f"extra in view (not in canonical): {sorted(extra)}")

    for entry in view.get("machines", []):
        name = entry.get("name")
        for required in ("owner_role", "failure_mode", "kpi_targets", "target_grade_before_scale"):
            if not entry.get(required):
                failures.append(f"machine {name}: missing {required}")
        if not entry.get("name_ar"):
            warnings.append(f"machine {name}: missing Arabic name")

    verdict = "PASS" if not failures and (not strict or not warnings) else "FAIL"
    print(f"MACHINE_REGISTRY={verdict.lower()}")
    print(f"MACHINE_REGISTRY_CANON_COUNT={len(canon_machines)}")
    print(f"MACHINE_REGISTRY_VIEW_COUNT={len(view_machines)}")
    print(f"MACHINE_REGISTRY_FAILS={len(failures)}")
    print(f"MACHINE_REGISTRY_WARNS={len(warnings)}")
    if failures:
        print("\n## Machine Registry FAILURES")
        for f in failures:
            print(f"  - {f}")
    if warnings:
        print("\n## Machine Registry WARNINGS")
        for w in warnings:
            print(f"  - {w}")
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
