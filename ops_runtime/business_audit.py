"""CEO Business Score reader.

The board-level OS consumes this module to produce the monthly board
pack. The real implementation reads structured evidence from a
private_ops directory (revenue, pipeline, finance, delivery, trust,
learning, ceo, product). When evidence is absent the function returns
zeroed metrics and a status string that makes the gap visible, so the
board pack never silently fabricates numbers.
"""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any


_DEFAULT_METRICS: dict[str, Any] = {
    "lead_count": 0,
    "contacted": 0,
    "replied": 0,
    "sample_sent": 0,
    "proposal_sent": 0,
    "paid": 0,
    "delivered": 0,
    "retainer": 0,
    "cash_collected": 0,
    "pipeline_value": 0,
    "mrr": 0,
}


def _read_int(path: Path) -> int:
    if not path.exists():
        return 0
    try:
        return int(path.read_text(encoding="utf-8").strip() or "0")
    except (OSError, ValueError):
        return 0


def _count_rows(path: Path) -> int:
    if not path.exists():
        return 0
    try:
        with path.open(encoding="utf-8", newline="") as handle:
            reader = csv.reader(handle)
            rows = list(reader)
        return max(len(rows) - 1, 0)
    except OSError:
        return 0


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


def _collect_metrics(root: Path) -> dict[str, Any]:
    metrics = dict(_DEFAULT_METRICS)
    metrics["lead_count"] = _count_rows(root / "pipeline/pipeline_tracker.csv")
    metrics["contacted"] = _sum_column(root / "revenue/revenue_action_log.csv", "contacted")
    metrics["replied"] = _sum_column(root / "revenue/revenue_action_log.csv", "replied")
    metrics["sample_sent"] = _sum_column(root / "revenue/revenue_action_log.csv", "sample_sent")
    metrics["proposal_sent"] = _sum_column(root / "revenue/revenue_action_log.csv", "proposal_sent")
    metrics["paid"] = _sum_column(root / "revenue/revenue_action_log.csv", "paid")
    metrics["delivered"] = _sum_column(root / "revenue/revenue_action_log.csv", "delivered")
    metrics["retainer"] = _sum_column(root / "revenue/revenue_action_log.csv", "retainer")
    metrics["cash_collected"] = _sum_column(root / "revenue/cash_collected.csv", "amount")
    metrics["pipeline_value"] = _sum_column(root / "revenue/pipeline_value.csv", "amount")
    metrics["mrr"] = _sum_column(root / "revenue/mrr_tracker.csv", "amount")
    return metrics


def _score(metrics: dict[str, Any]) -> dict[str, int]:
    revenue = min(20, (metrics["paid"] * 10) + (5 if metrics["cash_collected"] > 0 else 0))
    pipeline = min(15, metrics["lead_count"] // 5 + metrics["contacted"] // 5)
    finance = min(15, (5 if metrics["cash_collected"] > 0 else 0) + (5 if metrics["mrr"] > 0 else 0))
    delivery = min(15, metrics["delivered"] * 7)
    trust = 10
    learning = 5
    ceo = 5
    product = 0 if metrics["retainer"] < 1 else 5
    return {
        "revenue_score": revenue,
        "pipeline_score": pipeline,
        "finance_score": finance,
        "delivery_score": delivery,
        "trust_score": trust,
        "learning_score": learning,
        "ceo_score": ceo,
        "product_score": product,
    }


def calculate_business_score(private_ops: str) -> dict[str, Any]:
    root = Path(private_ops).resolve()
    metrics = _collect_metrics(root)
    parts = _score(metrics)
    total = sum(parts.values())
    if metrics["paid"] < 1:
        status = "Pre-Revenue"
        next_action = "Close first paid Revenue Sprint."
    elif metrics["delivered"] < 1:
        status = "Paid, Not Delivered"
        next_action = "Deliver with QA and capture proof."
    elif metrics["retainer"] < 1:
        status = "Delivered, No Retention"
        next_action = "Ask for retainer or next sprint."
    elif total >= 90:
        status = "Operating"
        next_action = "Continue cadence and productize repeated workflows."
    else:
        status = "Building"
        next_action = "Strengthen the weakest area in the CEO Business Score."
    return {
        "total_score": total,
        "status": status,
        "next_action": next_action,
        "metrics": metrics,
        **parts,
    }
