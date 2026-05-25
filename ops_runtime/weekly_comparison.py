from __future__ import annotations

"""Compare current-week metrics to the prior recorded week."""

import csv
from pathlib import Path
from typing import Any

METRICS_RELPATH = "metrics_history/weekly_metrics.csv"

_NUMERIC_KEYS: tuple[str, ...] = (
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
)


def _to_float(value: Any) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def compare_to_prior_week(private_ops_path: Path) -> dict[str, Any]:
    """Return deltas between the last two rows of weekly_metrics.csv.

    If fewer than two rows exist, returns {available: False, deltas: {}}.
    """
    target = Path(private_ops_path) / METRICS_RELPATH
    if not target.exists():
        return {"available": False, "deltas": {}}

    try:
        with target.open("r", encoding="utf-8", newline="") as fh:
            rows = list(csv.DictReader(fh))
    except (OSError, csv.Error):
        return {"available": False, "deltas": {}}

    if len(rows) < 2:
        return {"available": False, "deltas": {}}

    current = rows[-1]
    prior = rows[-2]
    deltas: dict[str, float] = {}
    for key in _NUMERIC_KEYS:
        deltas[key] = round(_to_float(current.get(key)) - _to_float(prior.get(key)), 2)
    return {
        "available": True,
        "current_week_of": current.get("week_of", ""),
        "prior_week_of": prior.get("week_of", ""),
        "deltas": deltas,
    }
