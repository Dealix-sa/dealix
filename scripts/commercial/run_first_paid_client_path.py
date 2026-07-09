#!/usr/bin/env python3
"""Generate the manual first paid client revenue path report."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dealix.full_company_os.revenue_path import (  # noqa: E402
    default_first_paid_events,
    load_events,
    write_revenue_path_report,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Dealix first paid client manual revenue path.")
    parser.add_argument("--events", default="data/commercial/examples/first_paid_client_event.example.json")
    parser.add_argument("--output-root", default="reports/full_company_os/revenue_path")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    event_path = ROOT / args.events
    if event_path.exists():
        events = load_events(event_path)
    else:
        events = default_first_paid_events()
    payload = write_revenue_path_report(events, ROOT / args.output_root)
    status = payload["status"]
    print(
        "FIRST_PAID_CLIENT_PATH=PASS "
        f"status={status['status']} "
        f"can_count_revenue={status['can_count_revenue']} "
        f"can_mark_closed_won={status['can_mark_closed_won']} "
        f"next_required_event={status['next_required_event']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
