#!/usr/bin/env python3
"""Export a local JSON snapshot of the private ops working tree.

The snapshot is intentionally local-only. Do NOT commit the produced file.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import sys
from pathlib import Path


CSV_FILES = [
    "pipeline/pipeline_tracker.csv",
    "revenue/revenue_action_log.csv",
    "revenue/cash_collected.csv",
    "revenue/pipeline_value.csv",
    "revenue/mrr_tracker.csv",
    "sales/proposal_tracker.csv",
    "finance/expenses.csv",
    "finance/unit_economics.csv",
    "trust/approval_log.csv",
    "trust/risk_register.csv",
    "evidence/execution_evidence_ledger.csv",
    "business_audit/score_history.csv",
    "metrics_history/weekly_metrics.csv",
]


def read_csv(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default="../dealix-ops-private")
    parser.add_argument("--out", default="../dealix-ops-private/exports/snapshot.json")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    if not root.exists():
        print(f"ERROR: private root missing: {root}")
        return 1
    out_path = Path(args.out).resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)

    snapshot: dict = {
        "generated_at": dt.datetime.utcnow().isoformat() + "Z",
        "root": str(root),
        "tables": {},
    }
    for rel in CSV_FILES:
        snapshot["tables"][rel] = read_csv(root / rel)

    out_path.write_text(json.dumps(snapshot, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Snapshot written: {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
