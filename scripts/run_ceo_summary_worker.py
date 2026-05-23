#!/usr/bin/env python3
"""Append a CEO summary snapshot to runtime/ceo_summary.csv.

Safe-by-default: never sends, never calls external APIs. Reads other runtime
CSVs to derive aggregate fields when present, else writes empty fields.
"""

from __future__ import annotations

import argparse
import csv
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_ROOT = os.environ.get("PRIVATE_OPS") or os.environ.get("PRIVATE_OPS_ROOT") or "/opt/dealix-ops-private"
TARGET = "runtime/ceo_summary.csv"
HEADERS = [
    "as_of",
    "pipeline_weighted",
    "cash_collected",
    "approvals_pending",
    "trust_flags_open",
    "workers_fresh",
]


def count_rows(path: Path) -> int:
    if not path.exists():
        return 0
    with path.open("r", encoding="utf-8") as fh:
        return max(0, sum(1 for _ in csv.reader(fh)) - 1)


def open_trust_flags(path: Path) -> int:
    if not path.exists():
        return 0
    with path.open("r", encoding="utf-8") as fh:
        return sum(1 for r in csv.DictReader(fh) if (r.get("status") or "").lower() == "open")


def workers_fresh(path: Path) -> int:
    if not path.exists():
        return 0
    with path.open("r", encoding="utf-8") as fh:
        return sum(1 for r in csv.DictReader(fh) if (r.get("status") or "").lower() == "ok")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--root", default=DEFAULT_ROOT)
    args = p.parse_args()
    root = Path(args.root).expanduser().resolve()
    target = root / TARGET
    target.parent.mkdir(parents=True, exist_ok=True)

    row = {
        "as_of": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "pipeline_weighted": "",
        "cash_collected": "",
        "approvals_pending": str(count_rows(root / "approvals" / "approval_queue.csv")),
        "trust_flags_open": str(open_trust_flags(root / "trust" / "trust_flags.csv")),
        "workers_fresh": str(workers_fresh(root / "runtime" / "worker_state.csv")),
    }

    write_header = not target.exists()
    with target.open("a", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=HEADERS)
        if write_header:
            writer.writeheader()
        writer.writerow(row)

    print(f"[ceo_summary_worker] appended row to {target}")

    # Stamp worker state.
    subprocess.run(
        [sys.executable, "scripts/update_worker_state.py", "--worker", "ceo_summary_worker", "--status", "ok"],
        check=False,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
