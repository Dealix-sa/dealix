#!/usr/bin/env python3
"""Update a worker's state in runtime/worker_state.csv.

Usage:
    python scripts/update_worker_state.py --worker outreach_queue_worker --status healthy
"""
from __future__ import annotations

import argparse
import csv
import datetime
import os
from pathlib import Path


def workspace() -> Path:
    return Path(os.environ.get("DEALIX_PRIVATE_OPS", "/opt/dealix-ops-private"))


def update(worker: str, status: str) -> None:
    path = workspace() / "runtime" / "worker_state.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, str]] = []
    if path.exists():
        with path.open("r", encoding="utf-8") as fh:
            rows = list(csv.DictReader(fh))
    updated = False
    now = datetime.datetime.utcnow().isoformat(timespec="seconds")
    for row in rows:
        if row.get("worker_id") == worker:
            row["last_run_iso"] = now
            row["status"] = status
            row["kill_switch"] = "scripts/update_worker_state.py"
            updated = True
            break
    if not updated:
        rows.append({
            "worker_id": worker,
            "last_run_iso": now,
            "status": status,
            "kill_switch": "scripts/update_worker_state.py",
        })
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=["worker_id", "last_run_iso", "status", "kill_switch"])
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker", required=True)
    parser.add_argument("--status", default="healthy")
    args = parser.parse_args()
    update(args.worker, args.status)
    print(f"worker {args.worker} -> {args.status}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
