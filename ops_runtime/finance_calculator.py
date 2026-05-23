from pathlib import Path
import csv


def read_csv(path: Path):
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def to_float(value):
    try:
        return float(value or 0)
    except ValueError:
        return 0.0


def calculate_finance(private_ops_root: str):
    root = Path(private_ops_root)
    cash_rows = read_csv(root / "revenue/cash_collected.csv")
    pipeline_rows = read_csv(root / "revenue/pipeline_value.csv")
    mrr_rows = read_csv(root / "revenue/mrr_tracker.csv")
    expense_rows = read_csv(root / "finance/expenses.csv")

    cash_collected = sum(
        to_float(r.get("amount_sar"))
        for r in cash_rows
        if (r.get("status") or "").lower() in {"paid", "collected", "done"}
    )
    pipeline_value = sum(to_float(r.get("deal_value_sar")) for r in pipeline_rows)
    weighted_pipeline = sum(to_float(r.get("weighted_value")) for r in pipeline_rows)
    mrr = sum(
        to_float(r.get("monthly_amount_sar"))
        for r in mrr_rows
        if (r.get("status") or "").lower() in {"active", "paid", "current"}
    )
    monthly_expenses = sum(
        to_float(r.get("amount_sar"))
        for r in expense_rows
        if (r.get("recurring") or "").lower() in {"yes", "true", "1"}
    )
    net_burn = max(monthly_expenses - mrr, 0)
    return {
        "cash_collected": cash_collected,
        "pipeline_value": pipeline_value,
        "weighted_pipeline": weighted_pipeline,
        "mrr": mrr,
        "monthly_expenses": monthly_expenses,
        "net_burn": net_burn,
    }
