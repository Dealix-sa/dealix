#!/usr/bin/env python3
"""Run Dealix as a company that operates itself — one command, one cycle.

Chains the safe commercial engines in order and prints a single consolidated
status. Everything is draft-only and approval-first.

    1. Money Now Sprint            (first-revenue founder action plan)
    2. Autonomous Growth OS        (strategy execution, content + approval queues)
    3. Autonomous Company OS       (stateful pipeline + Command Room)
    4. Launch-foundation verify    (safety + config sanity)

Usage:
    python scripts/commercial/run_company.py
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
COMMERCIAL = ROOT / "scripts" / "commercial"

STEPS = [
    ("Money Now Sprint", ["run_money_now_sprint.py"]),
    ("Autonomous Growth OS", ["run_autonomous_growth_daily.py", "--autonomy-level", "3", "--mode", "draft-only", "--limit", "50"]),
    ("Autonomous Company OS", ["run_autonomous_company.py", "--seed-inbox", "--top", "10"]),
    ("Launch foundation verify", ["verify_launch_foundation.py"]),
]


def _run(label: str, argv: list[str]) -> bool:
    script = COMMERCIAL / argv[0]
    if not script.exists():
        print(f"[SKIP] {label}: missing {argv[0]}")
        return True
    proc = subprocess.run(
        [sys.executable, str(script), *argv[1:]],
        capture_output=True,
        text=True,
        cwd=str(ROOT),
    )
    ok = proc.returncode == 0
    print(f"\n=== {label} -> {'OK' if ok else 'FAILED'} ===")
    for line in proc.stdout.strip().splitlines():
        print(f"  {line}")
    if not ok and proc.stderr.strip():
        print("  " + proc.stderr.strip().splitlines()[-1])
    return ok


def main() -> int:
    print("Dealix — Autonomous Company Run (draft-only, approval-first)")
    all_ok = True
    for label, argv in STEPS:
        all_ok = _run(label, argv) and all_ok

    print("\n" + "=" * 48)
    print("COMPANY_RUN=" + ("OK" if all_ok else "FAILED"))
    print("OPEN: reports/autonomous_company/command_room.html")
    print("Nothing was sent, published, or charged. Review the approval queue.")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
