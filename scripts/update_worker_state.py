#!/usr/bin/env python3
"""Update worker_state.csv inside the private ops tree.

Usage:
    python scripts/update_worker_state.py \
        --worker ceo_summary --status ok --next-run "2026-05-24T05:00:00Z"

Existing row for the worker is replaced. failures_24h auto-increments when
--status is failed and --reset-failures is not passed.
"""

from __future__ import annotations

import argparse
import csv
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_ROOT = "/opt/dealix-ops-private"
RELATIVE = "runtime/worker_state.csv"
HEADERS = ["worker", "last_run", "status", "failures_24h", "next_run", "notes"]


def load_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8") as fh:
        return [dict(r) for r in csv.DictReader(fh)]


def write_rows(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=HEADERS)
        writer.writeheader()
        for row in rows:
            writer.writerow({h: row.get(h, "") for h in HEADERS})


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--worker", required=True)
    parser.add_argument(
        "--status",
        choices=["ok", "failed", "running", "warning"],
        required=True,
    )
    parser.add_argument("--next-run", default="")
    parser.add_argument("--notes", default="")
    parser.add_argument("--reset-failures", action="store_true")
    parser.add_argument(
        "--private-ops",
        default=os.environ.get("DEALIX_PRIVATE_OPS", DEFAULT_ROOT),
    )
    args = parser.parse_args(argv)

    path = Path(args.private_ops).expanduser().resolve() / RELATIVE
    rows = load_rows(path)

    now = datetime.now(timezone.utc).isoformat()
    existing = next(
        (r for r in rows if (r.get("worker") or "").strip() == args.worker),
        None,
    )

    failures = 0
    if existing and not args.reset_failures:
        try:
            failures = int(existing.get("failures_24h") or 0)
        except ValueError:
            failures = 0

    if args.status == "failed":
        failures += 1
    elif args.reset_failures:
        failures = 0

    new_row = {
        "worker": args.worker,
        "last_run": now,
        "status": args.status,
        "failures_24h": str(failures),
        "next_run": args.next_run,
        "notes": args.notes,
    }

    rows = [r for r in rows if (r.get("worker") or "").strip() != args.worker]
    rows.append(new_row)
    write_rows(path, rows)
    print(f"updated worker_state for {args.worker}: {args.status} (failures={failures})")
    print(f"  path: {path}")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(130)
