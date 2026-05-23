#!/usr/bin/env python3
"""Append a worker_state row.

Usage:
    python scripts/update_worker_state.py --worker ceo_summary --status ok --notes "ran ok"
"""

from __future__ import annotations

import argparse
import csv
import os
from datetime import datetime, timezone
from pathlib import Path


FIELDS = ["worker", "last_run", "status", "failures_24h", "next_run", "notes"]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--worker", required=True)
    parser.add_argument("--status", default="ok")
    parser.add_argument("--failures-24h", default="0")
    parser.add_argument("--next-run", default="")
    parser.add_argument("--notes", default="")
    parser.add_argument(
        "--private-ops",
        default=os.environ.get("DEALIX_PRIVATE_OPS", "/opt/dealix-ops-private"),
    )
    args = parser.parse_args()

    path = Path(args.private_ops) / "runtime" / "worker_state.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    is_new = not path.exists()
    with path.open("a", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=FIELDS)
        if is_new:
            writer.writeheader()
        writer.writerow(
            {
                "worker": args.worker,
                "last_run": datetime.now(timezone.utc).isoformat(),
                "status": args.status,
                "failures_24h": args.failures_24h,
                "next_run": args.next_run,
                "notes": args.notes,
            }
        )
    print(f"[update_worker_state] worker={args.worker} status={args.status}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
