#!/usr/bin/env python3
"""CLI: generate a Dealix daily brief from a pipeline snapshot.

Usage:
    python scripts/os_daily_brief.py --snapshot '{"leads": 5, "cash_sar": 120000}'
    echo '{"leads": 3}' | python scripts/os_daily_brief.py
    python scripts/os_daily_brief.py --demo
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from os_runtime.daily_brief import generate_brief

DEMO_SNAPSHOT: dict = {
    "leads": 12,
    "drafts": 3,
    "calls": 2,
    "pipeline_value_sar": 480000,
    "cash_sar": 95000,
    "top_leads": [
        "Al-Mustaqbal Facilities Co.",
        "Gulf Contracting Group",
        "Riyadh PMO Services",
    ],
    "projects": [
        {"name": "Maintenance OS — Client Alpha", "at_risk": False},
        {"name": "Workflow Audit — Beta Corp", "at_risk": True},
    ],
}


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate Dealix daily brief")
    parser.add_argument("--snapshot", type=str, help="JSON snapshot string")
    parser.add_argument("--demo", action="store_true", help="Use demo snapshot")
    args = parser.parse_args()

    if args.demo:
        snapshot = DEMO_SNAPSHOT
    elif args.snapshot:
        try:
            snapshot = json.loads(args.snapshot)
        except json.JSONDecodeError as exc:
            print(f"ERROR: Invalid JSON in --snapshot: {exc}", file=sys.stderr)
            return 1
    elif not sys.stdin.isatty():
        raw = sys.stdin.read().strip()
        if not raw:
            snapshot = {}
        else:
            try:
                snapshot = json.loads(raw)
            except json.JSONDecodeError as exc:
                print(f"ERROR: Invalid JSON on stdin: {exc}", file=sys.stderr)
                return 1
    else:
        snapshot = {}

    print(generate_brief(snapshot))
    return 0


if __name__ == "__main__":
    sys.exit(main())
