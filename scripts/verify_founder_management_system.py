#!/usr/bin/env python3
"""Verify founder-management system docs + scorecards."""

from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

REQUIRED = (
    "docs/company/FOUNDER_COMMAND_CENTER.md",
    "docs/company/FOUNDER_KPIS_AR.md",
    "docs/company/MATURITY_BOARD.md",
    "dealix/config/founder_max_ops_backlog.yaml",
    "dealix/config/founder_strongest_plan_checklist.yaml",
    "dealix/config/founder_weekly_one_decision.yaml",
)


def main() -> int:
    missing = [p for p in REQUIRED if not (REPO / p).is_file()]
    for m in missing:
        print(f"missing_founder_artifact:{m}", file=sys.stderr)
    ok = not missing
    print(f"FOUNDER_MANAGEMENT_SYSTEM_PASS={'true' if ok else 'false'}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
