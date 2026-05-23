#!/usr/bin/env python3
"""Append a single worker status row to runtime/worker_state.csv.

Usage:
    python scripts/update_worker_state.py \
        --worker ceo_summary --status ok [--notes "..."] [--root /opt/dealix-ops-private]
"""

from __future__ import annotations

import argparse
import csv
import os
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import List


DEFAULT_ROOT = os.environ.get("PRIVATE_OPS", "/opt/dealix-ops-private")
WORKER_STATE_REL = "runtime/worker_state.csv"
HEADER = ["entry_id", "recorded_at", "worker", "status", "notes"]


def parse_args(argv: List[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--worker", required=True, help="Worker name (slug).")
    parser.add_argument(
        "--status",
        required=True,
        help="Status value (ok, warn, error, started, completed, ...).",
    )
    parser.add_argument("--notes", default="", help="Optional free-form note.")
    parser.add_argument(
        "--root",
        default=DEFAULT_ROOT,
        help="Private ops root (default: $PRIVATE_OPS or /opt/dealix-ops-private).",
    )
    return parser.parse_args(argv)


def append_state(root: Path, worker: str, status: str, notes: str) -> Path:
    path = root / WORKER_STATE_REL
    path.parent.mkdir(parents=True, exist_ok=True)
    file_exists = path.exists()
    with path.open("a", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        if not file_exists:
            writer.writerow(HEADER)
        writer.writerow([
            uuid.uuid4().hex,
            datetime.now(timezone.utc).isoformat(timespec="seconds"),
            worker,
            status,
            notes,
        ])
    return path


def main(argv: List[str] | None = None) -> int:
    args = parse_args(argv)
    root = Path(args.root).expanduser().resolve()
    path = append_state(root, args.worker, args.status, args.notes)
    print(f"appended worker_state row: worker={args.worker} status={args.status} -> {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
