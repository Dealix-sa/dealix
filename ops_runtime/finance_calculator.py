"""Finance snapshot reader."""

from __future__ import annotations

from pathlib import Path

from ._io import first_existing, read_csv_rows, sum_float


def _safe_int(value: float) -> int:
    return int(round(value))


def calculate_finance(private_ops_root: str) -> dict:
    root = Path(private_ops_root).resolve()

    cash_path = first_existing(
        root / "finance/cash_collected.csv",
        root / "revenue/cash_collected.csv",
    )
    cash_rows = read_csv_rows(cash_path) if cash_path else []
    cash_collected = sum_float(cash_rows, "amount")

    pipeline_path = first_existing(
        root / "revenue/pipeline_value.csv",
        root / "revenue/pipeline_tracker.csv",
        root / "sales/pipeline_tracker.csv",
    )
    pipeline_rows = read_csv_rows(pipeline_path) if pipeline_path else []
    pipeline_value = sum_float(pipeline_rows, "amount")
    if pipeline_value <= 0:
        pipeline_value = sum_float(pipeline_rows, "value")

    weighted_pipeline = 0.0
    for row in pipeline_rows:
        try:
            amount = float((row.get("amount") or row.get("value") or "0") or 0)
        except ValueError:
            amount = 0.0
        try:
            probability = float((row.get("probability") or "0") or 0)
        except ValueError:
            probability = 0.0
        if probability > 1:
            probability = probability / 100.0
        weighted_pipeline += amount * probability

    mrr_path = first_existing(
        root / "finance/mrr.csv",
        root / "revenue/mrr.csv",
    )
    mrr_rows = read_csv_rows(mrr_path) if mrr_path else []
    mrr = sum_float(mrr_rows, "amount")

    expenses_path = first_existing(
        root / "finance/expenses.csv",
        root / "finance/monthly_expenses.csv",
    )
    expenses_rows = read_csv_rows(expenses_path) if expenses_path else []
    monthly_expenses = sum_float(expenses_rows, "amount")

    net_burn = monthly_expenses - mrr

    return {
        "cash_collected": _safe_int(cash_collected),
        "pipeline_value": _safe_int(pipeline_value),
        "weighted_pipeline": _safe_int(weighted_pipeline),
        "mrr": _safe_int(mrr),
        "monthly_expenses": _safe_int(monthly_expenses),
        "net_burn": _safe_int(net_burn),
    }
