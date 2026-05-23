#!/usr/bin/env python3
"""
Update the worker state CSV in the private ops runtime.

Usage:
    python scripts/update_worker_state.py --id ceo_summary --status ok
    python scripts/update_worker_state.py --id sales_funnel --status failed --note "DB timeout"
"""
from __future__ import annotations

import argparse
import csv
import os
import sys
from datetime import datetime, timezone
from pathlib import Path


def _runtime_dir() -> Path:
    raw = os.getenv("PRIVATE_OPS") or os.getenv("DEALIX_PRIVATE_OPS_DIR") or "/opt/dealix-ops-private"
    return Path(raw).expanduser()


HEADER = ["id", "name", "status", "last_run", "failure_count", "owner"]


def update(worker_id: str, status: str, name: str | None, owner: str | None, note: str | None) -> int:
    base = _runtime_dir()
    target = base / "runtime" / "worker_state.csv"
    target.parent.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, str]] = []
    if target.exists():
        with target.open("r", encoding="utf-8", newline="") as fh:
            rows = list(csv.DictReader(fh))
    found = False
    for r in rows:
        if r.get("id") == worker_id:
            r["status"] = status
            r["last_run"] = datetime.now(timezone.utc).isoformat()
            if status == "failed":
                r["failure_count"] = str(int(r.get("failure_count", "0") or 0) + 1)
            elif status == "ok":
                r["failure_count"] = "0"
            if name:
                r["name"] = name
            if owner:
                r["owner"] = owner
            found = True
            break
    if not found:
        rows.append(
            {
                "id": worker_id,
                "name": name or worker_id,
                "status": status,
                "last_run": datetime.now(timezone.utc).isoformat(),
                "failure_count": "1" if status == "failed" else "0",
                "owner": owner or "founder",
            }
        )
    with target.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=HEADER)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in HEADER})
    print(f"[ok] worker {worker_id} -> {status} ({target})")
    if note:
        print(f"  note: {note}")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--id", required=True, help="Worker id (e.g., ceo_summary)")
    ap.add_argument("--status", required=True, choices=["ok", "failed", "running", "paused"])
    ap.add_argument("--name")
    ap.add_argument("--owner")
    ap.add_argument("--note")
    args = ap.parse_args(argv)
    return update(args.id, args.status, args.name, args.owner, args.note)


if __name__ == "__main__":
    sys.exit(main())
