from __future__ import annotations

"""Emit alerts when metrics drop below thresholds."""

from typing import Any

_INFO = "info"
_WARN = "warn"
_CRITICAL = "critical"

# Weekly minimums for Stage 1.
_WEEKLY_MIN_DMS = 25
_WEEKLY_MIN_PROPOSALS = 1
_WEEKLY_MIN_LEADS = 25


def generate_alerts(
    metrics: dict[str, Any], comparisons: dict[str, Any]
) -> list[dict[str, Any]]:
    """Return a list of {severity, message, kpi} dicts."""
    alerts: list[dict[str, Any]] = []
    pipeline = metrics.get("pipeline", {})
    revenue = metrics.get("revenue", {})
    delivery = metrics.get("delivery", {})

    dms = revenue.get("dms_sent", 0)
    if dms < _WEEKLY_MIN_DMS:
        alerts.append(
            {
                "severity": _WARN,
                "kpi": "dms_sent",
                "message": f"DMs sent ({dms}) below weekly minimum ({_WEEKLY_MIN_DMS}).",
            }
        )

    proposals = revenue.get("proposals_sent", 0)
    if proposals < _WEEKLY_MIN_PROPOSALS:
        alerts.append(
            {
                "severity": _WARN,
                "kpi": "proposals_sent",
                "message": (
                    f"Proposals sent ({proposals}) below weekly minimum "
                    f"({_WEEKLY_MIN_PROPOSALS})."
                ),
            }
        )

    leads = pipeline.get("total_leads", 0)
    if leads < _WEEKLY_MIN_LEADS:
        alerts.append(
            {
                "severity": _INFO,
                "kpi": "total_leads",
                "message": (
                    f"Pipeline holds {leads} leads; target is at least {_WEEKLY_MIN_LEADS}."
                ),
            }
        )

    at_risk = delivery.get("at_risk", 0)
    if at_risk >= 2:
        alerts.append(
            {
                "severity": _CRITICAL,
                "kpi": "delivery_at_risk",
                "message": f"{at_risk} clients flagged at_risk in delivery.",
            }
        )

    if comparisons.get("available"):
        deltas = comparisons.get("deltas", {}) or {}
        if deltas.get("cash_collected_sar", 0) < 0:
            alerts.append(
                {
                    "severity": _CRITICAL,
                    "kpi": "cash_collected_sar",
                    "message": (
                        f"Cash collection dropped by {abs(deltas['cash_collected_sar'])} "
                        "SAR vs prior week."
                    ),
                }
            )

    return alerts
