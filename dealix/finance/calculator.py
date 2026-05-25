"""Finance calculator — reads private ops CSV ledgers and returns core metrics.

Reads four CSV files from a private ops directory and returns a dict of:
cash_collected, pipeline_value, weighted_pipeline, mrr, monthly_expenses, net_burn.
"""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

PAID_STATUSES = {"paid", "collected", "done"}
ACTIVE_MRR_STATUSES = {"active", "paid", "current"}
RECURRING_TRUE = {"yes", "true", "1"}


def _read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _to_float(value: Any) -> float:
    try:
        return float(value or 0)
    except (TypeError, ValueError):
        return 0.0


def calculate_finance(private_ops_root: str | Path) -> dict[str, float]:
    """Compute Dealix finance metrics from a private ops directory.

    Args:
        private_ops_root: Path to dealix-ops-private/ root.

    Returns:
        dict with keys: cash_collected, pipeline_value, weighted_pipeline,
        mrr, monthly_expenses, net_burn.
    """
    root = Path(private_ops_root)
    cash_rows = _read_csv(root / "revenue" / "cash_collected.csv")
    pipeline_rows = _read_csv(root / "revenue" / "pipeline_value.csv")
    mrr_rows = _read_csv(root / "revenue" / "mrr_tracker.csv")
    expense_rows = _read_csv(root / "finance" / "expenses.csv")

    cash_collected = sum(
        _to_float(r.get("amount_sar"))
        for r in cash_rows
        if (r.get("status") or "").strip().lower() in PAID_STATUSES
    )
    pipeline_value = sum(_to_float(r.get("deal_value_sar")) for r in pipeline_rows)
    weighted_pipeline = sum(_to_float(r.get("weighted_value")) for r in pipeline_rows)
    mrr = sum(
        _to_float(r.get("monthly_amount_sar"))
        for r in mrr_rows
        if (r.get("status") or "").strip().lower() in ACTIVE_MRR_STATUSES
    )
    monthly_expenses = sum(
        _to_float(r.get("amount_sar"))
        for r in expense_rows
        if (r.get("recurring") or "").strip().lower() in RECURRING_TRUE
    )
    net_burn = max(monthly_expenses - mrr, 0.0)

    return {
        "cash_collected": cash_collected,
        "pipeline_value": pipeline_value,
        "weighted_pipeline": weighted_pipeline,
        "mrr": mrr,
        "monthly_expenses": monthly_expenses,
        "net_burn": net_burn,
    }
