#!/usr/bin/env python3
"""Append a sales-funnel snapshot to runtime/sales_funnel.csv (safe, read-only)."""

from __future__ import annotations

import argparse
import csv
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_ROOT = os.environ.get("PRIVATE_OPS") or os.environ.get("PRIVATE_OPS_ROOT") or "/opt/dealix-ops-private"
TARGET = "runtime/sales_funnel.csv"
HEADERS = [
    "as_of",
    "leads_researched",
    "a_leads",
    "approved_outreach",
    "sent_actions",
    "replies",
    "positive_replies",
    "samples_sent",
    "proposals_sent",
]


def count_csv(path: Path, where=None) -> int:
    if not path.exists():
        return 0
    with path.open("r", encoding="utf-8") as fh:
        n = 0
        for r in csv.DictReader(fh):
            if where is None or where(r):
                n += 1
        return n


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--root", default=DEFAULT_ROOT)
    args = p.parse_args()
    root = Path(args.root).expanduser().resolve()

    row = {
        "as_of": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "leads_researched": str(count_csv(root / "intelligence" / "account_scores.csv")),
        "a_leads": str(
            count_csv(
                root / "intelligence" / "account_scores.csv",
                where=lambda r: (r.get("final_priority") or "").upper() == "A",
            )
        ),
        "approved_outreach": str(
            count_csv(
                root / "approvals" / "approval_decisions.csv",
                where=lambda r: (r.get("decision") or "").lower() == "approved",
            )
        ),
        "sent_actions": "",
        "replies": "",
        "positive_replies": "",
        "samples_sent": "",
        "proposals_sent": "",
    }

    target = root / TARGET
    target.parent.mkdir(parents=True, exist_ok=True)
    write_header = not target.exists()
    with target.open("a", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=HEADERS)
        if write_header:
            writer.writeheader()
        writer.writerow(row)

    print(f"[sales_funnel_worker] appended row to {target}")
    subprocess.run(
        [sys.executable, "scripts/update_worker_state.py", "--worker", "sales_funnel_worker", "--status", "ok"],
        check=False,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
