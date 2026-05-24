#!/usr/bin/env python3
"""Append a finance-summary snapshot to runtime/ (safe, read-only)."""

from __future__ import annotations

import argparse
import csv
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_ROOT = os.environ.get("PRIVATE_OPS") or os.environ.get("PRIVATE_OPS_ROOT") or "/opt/dealix-ops-private"
TARGET = "finance/finance_summary.csv"
HEADERS = [
    "as_of",
    "cash_collected",
    "mrr",
    "pipeline_weighted",
    "proposal_value",
    "payment_followups",
    "ai_cost_per_lead",
    "ai_cost_per_proposal",
    "ai_cost_per_paid_client",
    "runway_months",
]


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--root", default=DEFAULT_ROOT)
    args = p.parse_args()
    root = Path(args.root).expanduser().resolve()

    target = root / TARGET
    target.parent.mkdir(parents=True, exist_ok=True)
    row = {h: "" for h in HEADERS}
    row["as_of"] = datetime.now(timezone.utc).isoformat(timespec="seconds")

    write_header = not target.exists()
    with target.open("a", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=HEADERS)
        if write_header:
            writer.writeheader()
        writer.writerow(row)

    print(f"[finance_summary_worker] appended row to {target}")
    subprocess.run(
        [sys.executable, "scripts/update_worker_state.py", "--worker", "finance_summary_worker", "--status", "ok"],
        check=False,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
