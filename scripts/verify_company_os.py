#!/usr/bin/env python3
"""
verify_company_os.py — meta-verifier. Runs each Dealix Company OS
sub-verifier as a subprocess and aggregates exit codes.

Each sub-verifier prints its own KEY=value summary. This script prints
a final aggregate block.

Exit: 0 PASS (all sub-verifiers PASS) / 1 FAIL.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SUB_VERIFIERS = [
    "verify_policy_as_code.py",
    "verify_agent_registry.py",
    "verify_machine_registry.py",
    "verify_eval_gate.py",
    "verify_brand_system.py",
    "verify_growth_system.py",
    "verify_marketing_system.py",
    "verify_product_distribution.py",
    "verify_market_attack_system.py",
    "verify_scale_moat_system.py",
    "verify_founder_ceo_hypergrowth_layer.py",
    "verify_prompt_output_quality.py",
]


def main() -> int:
    strict = "--strict" in sys.argv
    results: list[tuple[str, int, str]] = []
    for name in SUB_VERIFIERS:
        path = ROOT / "scripts" / name
        if not path.exists():
            results.append((name, 2, "missing script"))
            continue
        args = [sys.executable, str(path)]
        if strict:
            args.append("--strict")
        try:
            proc = subprocess.run(args, capture_output=True, text=True, timeout=60, check=False)
        except subprocess.TimeoutExpired:
            results.append((name, 1, "timeout"))
            continue
        last = (proc.stdout or "").strip().splitlines()
        head = last[0] if last else ""
        results.append((name, proc.returncode, head))

    fails = sum(1 for _, code, _ in results if code != 0)
    print("══ Dealix Company OS — Meta Verifier ══")
    for name, code, head in results:
        icon = "✅" if code == 0 else ("❌" if code == 1 else "⚠️ ")
        print(f"  {icon}  {name:<45} {head}")
    print(f"COMPANY_OS={'pass' if fails == 0 else 'fail'}")
    print(f"COMPANY_OS_FAILS={fails}")
    return 0 if fails == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
