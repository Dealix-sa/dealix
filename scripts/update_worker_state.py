#!/usr/bin/env python3
"""Update one row in the worker_state.csv heartbeat file.

Usage::

    python scripts/update_worker_state.py \\
        --worker ceo_summary \\
        --status ok \\
        --notes "ran from manual session"

Idempotent: if the worker already exists, its row is replaced.
"""

from __future__ import annotations

import argparse
import csv
import datetime as _dt
import os
import sys
from pathlib import Path


def _root() -> Path:
    return Path(os.environ.get("DEALIX_PRIVATE_OPS", "/opt/dealix-ops-private"))


def _now() -> str:
    return _dt.datetime.now(_dt.UTC).replace(microsecond=0).isoformat()


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--worker", required=True)
    p.add_argument("--status", default="ok", choices=["ok", "failed", "skipped", "queued"])
    p.add_argument("--failures-24h", type=int, default=0)
    p.add_argument("--next-run", default="")
    p.add_argument("--notes", default="")
    args = p.parse_args()

    path = _root() / "runtime/worker_state.csv"
    path.parent.mkdir(parents=True, exist_ok=True)

    headers = ["worker", "last_run", "status", "failures_24h", "next_run", "notes"]
    rows: list[dict[str, str]] = []
    if path.exists():
        with path.open("r", encoding="utf-8", newline="") as fh:
            rows = list(csv.DictReader(fh))

    found = False
    for r in rows:
        if r.get("worker") == args.worker:
            r["last_run"] = _now()
            r["status"] = args.status
            r["failures_24h"] = str(args.failures_24h)
            r["next_run"] = args.next_run
            r["notes"] = args.notes
            found = True
            break

    if not found:
        rows.append(
            {
                "worker": args.worker,
                "last_run": _now(),
                "status": args.status,
                "failures_24h": str(args.failures_24h),
                "next_run": args.next_run,
                "notes": args.notes,
            }
        )

    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=headers)
        writer.writeheader()
        for r in rows:
            writer.writerow({k: r.get(k, "") for k in headers})

    print(f"[OK] worker_state updated: worker={args.worker} status={args.status}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
