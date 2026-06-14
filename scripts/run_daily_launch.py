#!/usr/bin/env python3
"""
Morning launch script.

Run:
    python scripts/run_daily_launch.py          # dry-run (prints emails, no Gmail API)
    python scripts/run_daily_launch.py --send   # create real Gmail drafts for review

Default: dry-run — never auto-sends without explicit --send flag.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Ensure repo root is on sys.path when running as a script
_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Daily targeting engine — scores Saudi accounts, composes Arabic emails, queues Gmail drafts.",
    )
    parser.add_argument(
        "--send",
        action="store_true",
        default=False,
        help="Create real Gmail drafts (requires GMAIL_* env vars). Default: dry-run print only.",
    )
    args = parser.parse_args()

    dry_run = not args.send

    from dealix.daily_targeting.daily_engine import DailyTargetingEngine, _print_war_room_banner

    engine = DailyTargetingEngine(dry_run=dry_run)
    report = engine.run()
    _print_war_room_banner(report)


if __name__ == "__main__":
    main()
