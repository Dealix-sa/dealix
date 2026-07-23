#!/usr/bin/env python3
"""Build a daily command-center JSON from the scored prospects CSV.

Summarizes the scored prospect file into a single daily report with priority
counts, a top-10 list, manual daily targets, and the governance rules that
gate any outreach. Read-only over your data; writes one JSON report. It does
not send anything.

Run ``dealix_lead_scoring.py`` first to produce the scored CSV.

Usage:
    python3 scripts/launch_package/dealix_daily_command_center.py
"""

from __future__ import annotations

import argparse
import csv
import json
from datetime import date
from pathlib import Path

PKG_DIR = Path(__file__).resolve().parent
REPO_ROOT = PKG_DIR.parents[1]
DEFAULT_INPUT = REPO_ROOT / "reports" / "launch_package" / "scored_prospects.csv"
DEFAULT_OUTPUT_DIR = REPO_ROOT / "reports" / "launch_package"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    rows: list[dict] = []
    if args.input.exists():
        with args.input.open(encoding="utf-8") as f:
            rows = list(csv.DictReader(f))

    priority = [r for r in rows if int(r.get("lead_score") or 0) >= 70]
    report = {
        "date": str(date.today()),
        "total_scored_prospects": len(rows),
        "priority_prospects": len(priority),
        "top_10": priority[:10],
        "daily_targets": {
            "new_accounts": 25,
            "human_reviewed_messages": 10,
            "call_attempts": 3,
            "qualified_meetings_target": 1,
        },
        "rules": [
            "no automated outbound",
            "human approval before sending",
            "use public/consented context only",
        ],
    }
    output = args.output_dir / f"command_center_{date.today()}.json"
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()
