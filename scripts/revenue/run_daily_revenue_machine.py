#!/usr/bin/env python3
"""
Run the complete daily revenue machine. Never sends externally.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]


def run_step(name: str, cmd: list[str]) -> bool:
    print(f"\n▶ {name}")
    result = subprocess.run(cmd, cwd=REPO_ROOT)
    if result.returncode != 0:
        print(f"❌ {name} failed")
        return False
    print(f"✅ {name} complete")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="Run daily revenue machine")
    parser.add_argument("--input", default="ledgers/prospects.csv")
    parser.add_argument("--min-score", type=float, default=2.0)
    parser.add_argument("--followup-cooldown", type=int, default=3)
    args = parser.parse_args()

    steps = [
        ("Validate targets", ["python3", "scripts/revenue/find_targets_manual_workflow.py", "--validate", args.input]),
        ("Score targets", ["python3", "scripts/revenue/score_targets.py", "--input", args.input]),
        ("Generate outreach", ["python3", "scripts/revenue/generate_outreach.py", "--input", args.input, "--min-score", str(args.min_score)]),
        ("Generate follow-ups", ["python3", "scripts/revenue/generate_followups.py", "--cooldown-days", str(args.followup_cooldown)]),
        ("Generate proposals", ["python3", "scripts/revenue/generate_proposal_brief.py", "--input", args.input]),
        ("Daily CEO report", ["python3", "scripts/revenue/generate_daily_revenue_report.py", "--prospects", args.input]),
    ]

    all_ok = all(run_step(name, cmd) for name, cmd in steps)
    print("\n" + "=" * 60)
    if all_ok:
        print("✅ Daily revenue machine completed. Review drafts before any manual send.")
        return 0
    print("❌ Daily revenue machine completed with errors.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
