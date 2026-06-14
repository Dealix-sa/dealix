"""Finance calculator.

Reads ``finance/finance_ledger.csv`` from the private-ops root and
derives the headline numbers the Monthly Strategy Review needs.

Schema (header row, all columns optional):

    date,type,amount_sar,probability,note

``type`` is one of: ``cash_in``, ``pipeline``, ``mrr``, ``expense``.
For ``pipeline`` rows, ``probability`` is a float in [0, 1] used to
compute the weighted pipeline.
"""
from __future__ import annotations

import csv
from pathlib import Path


FINANCE_CSV = "finance/finance_ledger.csv"


def _empty_finance() -> dict:
    return {
        "cash_collected": 0,
        "pipeline_value": 0,
        "weighted_pipeline": 0,
        "mrr": 0,
        "monthly_expenses": 0,
        "net_burn": 0,
    }


def _safe_float(value: str) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def calculate_finance(private_root: str) -> dict:
    root = Path(private_root)
    csv_path = root / FINANCE_CSV
    result = _empty_finance()
    if not csv_path.exists():
        return result

    weighted = 0.0
    with csv_path.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            kind = (row.get("type") or "").strip().lower()
            amount = _safe_float(row.get("amount_sar", "0"))
            prob = _safe_float(row.get("probability", "0"))
            if kind == "cash_in":
                result["cash_collected"] += int(amount)
            elif kind == "pipeline":
                result["pipeline_value"] += int(amount)
                weighted += amount * max(0.0, min(prob, 1.0))
            elif kind == "mrr":
                result["mrr"] += int(amount)
            elif kind == "expense":
                result["monthly_expenses"] += int(amount)

    result["weighted_pipeline"] = int(round(weighted))
    result["net_burn"] = result["monthly_expenses"] - result["mrr"]
    return result
