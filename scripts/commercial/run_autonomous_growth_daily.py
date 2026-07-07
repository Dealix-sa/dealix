#!/usr/bin/env python3
"""Run the Dealix daily internal planning loop."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from dealix.strategy_execution.orchestrator import run_daily_strategy_execution


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Dealix internal strategy loop")
    parser.add_argument("--autonomy-level", type=int, default=3, choices=[0, 1, 2, 3, 4])
    parser.add_argument("--mode", default="draft-only", choices=["draft-only"])
    parser.add_argument("--limit", type=int, default=50)
    parser.add_argument("--output-root", default="reports/autonomous_growth")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    result = run_daily_strategy_execution(
        output_root=Path(args.output_root),
        autonomy_level=args.autonomy_level,
        limit=args.limit,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
