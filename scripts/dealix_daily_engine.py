#!/usr/bin/env python3
"""Daily operating engine — the external-cron entrypoint.

Runs the full daily loop once: outreach drafts, social content drafts,
partner-intro surfacing, approval expire-sweep, and the founder action
list. Idempotent per day (re-running prints ``already_ran`` unless
``--force``). Nothing is sent and nothing is charged — every output
lands in the approval queue for the founder to approve.

Usage:
    python scripts/dealix_daily_engine.py
    python scripts/dealix_daily_engine.py --print     # also print the action list
    python scripts/dealix_daily_engine.py --force     # re-run a day that already ran

Designed to run via an external scheduler (Railway / GitHub Actions / n8n).
"""
from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys

# Adjust path so we can import from repo root when run as a script.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from auto_client_acquisition.content_os.daily_engine import run_daily_engine


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Dealix daily operating engine")
    p.add_argument(
        "--force", action="store_true",
        help="re-run even if the engine already ran today",
    )
    p.add_argument(
        "--print", dest="print_only", action="store_true",
        help="print the founder action list after running",
    )
    return p.parse_args()


def main() -> int:
    args = parse_args()
    try:
        result = asyncio.run(run_daily_engine(force=args.force))
    except Exception as exc:
        print(f"FAIL: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1

    status = result.get("status")
    if status == "already_ran":
        print(f"already_ran: daily engine already completed for {result.get('date')}")
        print("re-run with --force to run again.")
        return 0

    stages = result.get("stages", {})
    print(f"OK: daily engine completed for {result.get('date')}")
    print(json.dumps(stages, ensure_ascii=False, indent=2))
    if args.print_only:
        print("\n--- founder action list ---\n")
        print(result.get("action_list", ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
