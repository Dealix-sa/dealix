"""Finance roll-up reader for the board-level OS.

Reads cash, pipeline, MRR, and expense evidence from a private_ops
directory and returns a finance summary the board pack consumes. When
evidence is missing the values are zero so the gap is visible.
"""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any


def _sum_column(path: Path, column: str) -> int:
    if not path.exists():
        return 0
    total = 0
    try:
        with path.open(encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            for row in reader:
                try:
                    total += int(float(row.get(column, "0") or 0))
                except ValueError:
                    continue
    except OSError:
        return 0
    return total


def calculate_finance(private_ops: str) -> dict[str, Any]:
    root = Path(private_ops).resolve()
    cash_collected = _sum_column(root / "revenue/cash_collected.csv", "amount")
    pipeline_value = _sum_column(root / "revenue/pipeline_value.csv", "amount")
    mrr = _sum_column(root / "revenue/mrr_tracker.csv", "amount")
    weighted_pipeline = _sum_column(root / "revenue/pipeline_value.csv", "weighted_amount") or pipeline_value // 2
    monthly_expenses = _sum_column(root / "finance/monthly_expenses.csv", "amount")
    net_burn = max(monthly_expenses - cash_collected - mrr, 0)
    return {
        "cash_collected": cash_collected,
        "pipeline_value": pipeline_value,
        "weighted_pipeline": weighted_pipeline,
        "mrr": mrr,
        "monthly_expenses": monthly_expenses,
        "net_burn": net_burn,
    }
