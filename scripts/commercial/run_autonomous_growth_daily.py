#!/usr/bin/env python3
"""Run one draft-only day of the Dealix Autonomous Growth & Strategy Execution OS.

Draft-only, approval-first. Never sends, publishes, or charges. Generates a daily
report, an action queue, an approval queue, a proof log, a content queue, and
learning notes under reports/autonomous_growth/.

Usage:
    python scripts/commercial/run_autonomous_growth_daily.py \
        --autonomy-level 3 --mode draft-only --limit 50
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dealix.strategy_execution import orchestrator
from dealix.strategy_execution.safety_gate import assert_no_live_send_enabled


def main() -> int:
    parser = argparse.ArgumentParser(description="Dealix Autonomous Growth daily run")
    parser.add_argument("--autonomy-level", type=int, default=3, choices=[0, 1, 2, 3, 4])
    parser.add_argument("--mode", default="draft-only", choices=["draft-only"])
    parser.add_argument("--limit", type=int, default=50)
    args = parser.parse_args()

    # Refuse to run if any live-send flag is enabled.
    violations = assert_no_live_send_enabled(orchestrator.env_snapshot())
    if violations:
        print("AUTONOMOUS_GROWTH_DAILY=ABORT")
        for v in violations:
            print(f"UNSAFE: {v}")
        return 2

    result = orchestrator.run_day(
        autonomy_level=args.autonomy_level,
        limit=args.limit,
        mode=args.mode,
        write=True,
    )

    print("AUTONOMOUS_GROWTH_DAILY=OK")
    print(f"MODE={args.mode}")
    print(f"AUTONOMY_LEVEL={result.autonomy_level}")
    print(f"STRATEGIES={len(result.strategies)}")
    print(f"INTERNAL_ACTIONS={result.executed_count}")
    print(f"APPROVALS_PENDING={result.approval_count}")
    print(f"LIVE_ACTIONS_BLOCKED={result.blocked_count}")
    for key, path in result.outputs.items():
        print(f"REPORT_{key.upper()}={path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
