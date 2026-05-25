from __future__ import annotations

"""Append a row to the weekly metrics history CSV."""

import csv
from datetime import date, timedelta
from pathlib import Path
from typing import Any

METRICS_RELPATH = "metrics_history/weekly_metrics.csv"

_HEADER = [
    "week_of",
    "total_leads",
    "pipeline_value_sar",
    "priority_high",
    "dms_sent",
    "samples_sent",
    "proposals_sent",
    "payments_pursued",
    "cash_collected_sar",
    "active_clients",
    "in_delivery",
    "completed",
    "at_risk",
]


def _monday_of(today: date) -> date:
    return today - timedelta(days=today.weekday())


def write_weekly_metrics(metrics: dict[str, Any], private_ops_path: Path) -> Path:
    """Append a flat metrics row keyed by this week's Monday date."""
    private_ops_path = Path(private_ops_path)
    target = private_ops_path / METRICS_RELPATH
    target.parent.mkdir(parents=True, exist_ok=True)

    pipeline = metrics.get("pipeline", {})
    revenue = metrics.get("revenue", {})
    delivery = metrics.get("delivery", {})

    row = {
        "week_of": _monday_of(date.today()).isoformat(),
        "total_leads": pipeline.get("total_leads", 0),
        "pipeline_value_sar": pipeline.get("pipeline_value_sar", 0.0),
        "priority_high": pipeline.get("priority_high", 0),
        "dms_sent": revenue.get("dms_sent", 0),
        "samples_sent": revenue.get("samples_sent", 0),
        "proposals_sent": revenue.get("proposals_sent", 0),
        "payments_pursued": revenue.get("payments_pursued", 0),
        "cash_collected_sar": revenue.get("cash_collected_sar", 0.0),
        "active_clients": delivery.get("active_clients", 0),
        "in_delivery": delivery.get("in_delivery", 0),
        "completed": delivery.get("completed", 0),
        "at_risk": delivery.get("at_risk", 0),
    }

    write_header = not target.exists()
    with target.open("a", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=_HEADER)
        if write_header:
            writer.writeheader()
        writer.writerow(row)
    return target
