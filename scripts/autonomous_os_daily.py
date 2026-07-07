#!/usr/bin/env python3
"""Dealix Autonomous Growth OS — daily draft-only runner.

Runs one full Autonomous OS cycle: plan every active strategy, route steps
through the safety gate into the action / approval queues, fold in commercial
recommendations, reflect via the learning loop, and write a daily report.

Draft-only and approval-first by construction — this script never sends any
external message and never approves anything. Outputs go to a runtime
directory (gitignored by default) so nothing generated is committed.

Usage:
    python3 scripts/autonomous_os_daily.py
    python3 scripts/autonomous_os_daily.py --root company/runtime/autonomous_os
    python3 scripts/autonomous_os_daily.py --context '{"warm_leads": 12}'
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dealix.autonomous_os import AutonomousOS  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Dealix Autonomous Growth OS daily runner")
    parser.add_argument(
        "--root",
        default=str(ROOT / "company" / "runtime" / "autonomous_os"),
        help="Runtime output directory (gitignored by default).",
    )
    parser.add_argument(
        "--context",
        default="{}",
        help="JSON growth context, e.g. '{\"warm_leads\": 12, \"proof_assets_ready\": 3}'.",
    )
    args = parser.parse_args()

    try:
        growth_context = json.loads(args.context)
        if not isinstance(growth_context, dict):
            raise ValueError("context must be a JSON object")
    except (json.JSONDecodeError, ValueError) as exc:
        print(f"AUTONOMOUS_OS=FAIL invalid --context: {exc}")
        return 2

    os_engine = AutonomousOS(runtime_root=args.root)
    summary = os_engine.run(growth_context=growth_context)

    print("AUTONOMOUS_OS=OK mode=draft_only")
    print(f"strategies_active={summary['strategies_active']}")
    print(
        "counters "
        f"drafted={summary['counters']['drafted']} "
        f"approval={summary['counters']['approval']} "
        f"blocked={summary['counters']['blocked']}"
    )
    print(f"pending_approvals={summary['approval_stats'].get('pending', 0)}")
    print(f"report_dir={Path(args.root) / 'reports'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
