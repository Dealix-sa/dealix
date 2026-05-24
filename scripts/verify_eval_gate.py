#!/usr/bin/env python3
"""
verify_eval_gate.py — assert evals/gates/dealix_agent_eval_gate.yaml
references real eval files, defines a gate per autonomy level, and
universally red-teams the four forbidden actions.

Exit: 0 PASS / 1 FAIL / 2 missing deps.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GATE = ROOT / "evals" / "gates" / "dealix_agent_eval_gate.yaml"

REQUIRED_LEVELS = {
    "L0_read_only",
    "L1_draft_only",
    "L2_approval_required",
    "L3_approved_execute",
    "L4_internal_automation_only",
    "L5_blocked_for_external",
}
REQUIRED_RED_TEAM_IDS = {
    "rt_no_send_without_approval",
    "rt_no_guarantee",
    "rt_no_scrape",
    "rt_no_auto_charge",
}


def main() -> int:
    strict = "--strict" in sys.argv
    failures: list[str] = []
    warnings: list[str] = []

    try:
        import yaml  # type: ignore
    except ImportError:
        print("EVAL_GATE=fail reason=pyyaml_not_installed")
        return 2

    if not GATE.exists():
        print(f"EVAL_GATE=fail reason=missing path={GATE}")
        return 1

    with GATE.open(encoding="utf-8") as f:
        gate = yaml.safe_load(f)

    gates = gate.get("gates", {})
    missing_levels = REQUIRED_LEVELS - set(gates.keys())
    if missing_levels:
        failures.append(f"missing autonomy gates: {sorted(missing_levels)}")

    # L5 must be blocked
    if not gates.get("L5_blocked_for_external", {}).get("blocked"):
        failures.append("L5_blocked_for_external.blocked != true")

    # Each referenced eval file must exist.
    referenced: set[str] = set()
    for level, spec in gates.items():
        if isinstance(spec, dict):
            for path in spec.get("required_evals", []) or []:
                referenced.add(path)
    for path in referenced:
        if not (ROOT / path).exists():
            failures.append(f"referenced eval missing: {path}")

    # Universal red-team coverage.
    red_team_ids = {rt.get("id") for rt in gate.get("universal_red_team", [])}
    missing_rt = REQUIRED_RED_TEAM_IDS - red_team_ids
    if missing_rt:
        failures.append(f"universal_red_team missing: {sorted(missing_rt)}")

    verdict = "PASS" if not failures and (not strict or not warnings) else "FAIL"
    print(f"EVAL_GATE={verdict.lower()}")
    print(f"EVAL_GATE_LEVELS_COVERED={len(gates)}")
    print(f"EVAL_GATE_EVALS_REFERENCED={len(referenced)}")
    print(f"EVAL_GATE_RED_TEAM_COUNT={len(red_team_ids)}")
    print(f"EVAL_GATE_FAILS={len(failures)}")
    if failures:
        print("\n## Eval Gate FAILURES")
        for f in failures:
            print(f"  - {f}")
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
