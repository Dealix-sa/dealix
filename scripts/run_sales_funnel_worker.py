#!/usr/bin/env python3
"""Compute simple funnel counts from conversation_log.csv."""
from __future__ import annotations

import csv
import os
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


def _runtime_dir() -> Path:
    return Path(os.getenv("PRIVATE_OPS") or os.getenv("DEALIX_PRIVATE_OPS_DIR") or "/opt/dealix-ops-private").expanduser()


def main() -> int:
    base = _runtime_dir()
    log = base / "outreach" / "conversation_log.csv"
    if not log.exists():
        print(f"SKIP: {log} missing")
        return 0
    counts: Counter[str] = Counter()
    with log.open("r", encoding="utf-8", newline="") as fh:
        for r in csv.DictReader(fh):
            counts[(r.get("stage") or "lead").lower()] += 1
    print("[sales_funnel]", dict(counts), datetime.now(timezone.utc).isoformat())
    return 0


if __name__ == "__main__":
    sys.exit(main())
