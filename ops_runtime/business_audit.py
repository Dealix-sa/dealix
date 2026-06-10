"""Business score reader.

Reads the founder's pipeline / sales / cash signals from the private ops
directory and produces the canonical CEO Business Score plus the underlying
metric counts consumed by mission control and the control tower.
"""

from __future__ import annotations

from pathlib import Path

from ._io import count_with_value, first_existing, read_csv_rows, sum_float, sum_int


def _coerce_int(value) -> int:
    if value in (None, ""):
        return 0
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return 0


def _load_pipeline_rows(root: Path) -> list[dict]:
    candidate = first_existing(
        root / "revenue/pipeline_tracker.csv",
        root / "sales/pipeline_tracker.csv",
        root / "revenue/pipeline.csv",
    )
    return read_csv_rows(candidate) if candidate else []


def _load_revenue_action_rows(root: Path) -> list[dict]:
    candidate = first_existing(
        root / "revenue/revenue_action_log.csv",
        root / "founder/revenue_action_log.csv",
    )
    return read_csv_rows(candidate) if candidate else []


def _load_cash_rows(root: Path) -> list[dict]:
    candidate = first_existing(
        root / "finance/cash_collected.csv",
        root / "revenue/cash_collected.csv",
    )
    return read_csv_rows(candidate) if candidate else []


def _stage_counts(pipeline_rows: list[dict]) -> dict[str, int]:
    stages = {
        "lead_count": 0,
        "contacted": 0,
        "replied": 0,
        "sample_sent": 0,
        "proposal_sent": 0,
        "paid": 0,
        "delivered": 0,
        "retainer": 0,
    }
    stage_field_candidates = ("stage", "status", "state")
    for row in pipeline_rows:
        stages["lead_count"] += 1
        stage_value = ""
        for field in stage_field_candidates:
            if row.get(field):
                stage_value = row[field].strip().lower()
                break
        if not stage_value:
            continue
        for key in (
            "contacted",
            "replied",
            "sample_sent",
            "proposal_sent",
            "paid",
            "delivered",
            "retainer",
        ):
            token = key.replace("_", " ")
            if key in stage_value or token in stage_value:
                stages[key] += 1
    return stages


def calculate_business_score(private_ops_root: str) -> dict:
    """Return CEO Business Score and underlying revenue metrics."""
    root = Path(private_ops_root).resolve()

    pipeline_rows = _load_pipeline_rows(root)
    revenue_rows = _load_revenue_action_rows(root)
    cash_rows = _load_cash_rows(root)

    metrics = _stage_counts(pipeline_rows)

    if not metrics["contacted"]:
        metrics["contacted"] = count_with_value(revenue_rows, "contacted_at")
    if not metrics["replied"]:
        metrics["replied"] = count_with_value(revenue_rows, "replied_at")

    cash_collected = sum_float(cash_rows, "amount")
    if cash_collected <= 0:
        cash_collected = sum_float(pipeline_rows, "amount_paid")
    metrics["cash_collected"] = int(round(cash_collected))

    weighting = {
        "lead_count": 5,
        "contacted": 5,
        "replied": 10,
        "sample_sent": 15,
        "proposal_sent": 20,
        "paid": 25,
        "delivered": 10,
        "retainer": 10,
    }
    score = 0
    for key, weight in weighting.items():
        value = metrics.get(key, 0)
        if value > 0:
            score += weight
    score = min(score, 100)

    return {
        "total_score": score,
        "metrics": metrics,
        "sources": {
            "pipeline_rows": len(pipeline_rows),
            "revenue_action_rows": len(revenue_rows),
            "cash_rows": len(cash_rows),
        },
    }
