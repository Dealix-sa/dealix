#!/usr/bin/env python3
"""Update a row in runtime/worker_state.csv.

Usage:
    python scripts/update_worker_state.py --worker ceo_summary_worker --status ok
"""

from __future__ import annotations

import argparse
import csv
import os
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_ROOT = os.environ.get("PRIVATE_OPS") or os.environ.get("PRIVATE_OPS_ROOT") or "/opt/dealix-ops-private"
WORKER_FILE = "runtime/worker_state.csv"
HEADERS = ["worker", "last_run", "status", "failures_24h", "next_run", "notes"]


def upsert(root: Path, worker: str, status: str, failures: int, next_run: str | None, notes: str | None) -> None:
    target = root / WORKER_FILE
    target.parent.mkdir(parents=True, exist_ok=True)

    rows: list[dict[str, str]] = []
    if target.exists():
        with target.open("r", encoding="utf-8") as fh:
            rows = list(csv.DictReader(fh))

    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    found = False
    for row in rows:
        if row.get("worker") == worker:
            row["last_run"] = now
            row["status"] = status
            row["failures_24h"] = str(failures)
            row["next_run"] = next_run or row.get("next_run", "")
            row["notes"] = notes or row.get("notes", "")
            found = True
            break

    if not found:
        rows.append(
            {
                "worker": worker,
                "last_run": now,
                "status": status,
                "failures_24h": str(failures),
                "next_run": next_run or "",
                "notes": notes or "",
            }
        )

    with target.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=HEADERS)
        writer.writeheader()
        for row in rows:
            writer.writerow({h: row.get(h, "") for h in HEADERS})


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--root", default=DEFAULT_ROOT)
    p.add_argument("--worker", required=True)
    p.add_argument("--status", default="ok")
    p.add_argument("--failures", type=int, default=0)
    p.add_argument("--next-run", dest="next_run", default=None)
    p.add_argument("--notes", default=None)
    args = p.parse_args()

    root = Path(args.root).expanduser().resolve()
    upsert(root, args.worker, args.status, args.failures, args.next_run, args.notes)
    print(f"[worker] {args.worker} -> {args.status}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
