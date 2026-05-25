"""Orchestrator: run every Dealix Company OS verify script.

Each child script is run as a subprocess. Aggregates pass/fail counts and
returns non-zero if any child fails.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"

SCRIPTS: list[str] = [
    "verify_tier0_safety.py",
    "verify_tier1_revenue.py",
    "verify_tier2_delivery.py",
    "verify_revenue_sprint_kit.py",
    "verify_execution_engine.py",
    "verify_stage_evidence_automation.py",
    "verify_stage_gated_roadmap.py",
    "verify_no_autonomous_external_actions.py",
    "verify_trust_boundary_terms.py",
    "verify_cli.py",
    "verify_dashboard_v2.py",
    "verify_weekly_automation.py",
    "verify_full_spectrum_os.py",
    "verify_document_quality.py",
]


def run_one(script: str) -> tuple[int, str]:
    path = SCRIPTS_DIR / script
    if not path.exists():
        return 127, f"missing {script}"
    proc = subprocess.run(
        [sys.executable, str(path)],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        timeout=120,
    )
    return proc.returncode, proc.stdout + ("\n--- stderr ---\n" + proc.stderr if proc.stderr else "")


def main() -> int:
    results: list[tuple[str, int, str]] = []
    for script in SCRIPTS:
        rc, out = run_one(script)
        results.append((script, rc, out))

    print("=" * 72)
    print("Dealix Company OS — full verify summary")
    print("=" * 72)
    pass_n = 0
    fail_n = 0
    for script, rc, _out in results:
        tag = "PASS" if rc == 0 else "FAIL"
        if rc == 0:
            pass_n += 1
        else:
            fail_n += 1
        print(f"  {tag}  {script}  (exit {rc})")
    print("-" * 72)
    print(f"  PASS: {pass_n} / {len(results)}")
    print(f"  FAIL: {fail_n} / {len(results)}")
    print("=" * 72)

    if fail_n:
        # Show stdout of failing scripts for context.
        for script, rc, out in results:
            if rc != 0:
                print(f"\n--- output of {script} ---\n{out}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
