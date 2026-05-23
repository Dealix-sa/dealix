from __future__ import annotations

"""Compute the founder's top 3 actions for today."""

from typing import Any


def compute_founder_focus(
    metrics: dict[str, Any], alerts: list[dict[str, Any]]
) -> list[str]:
    """Return up to three plain-text action strings.

    Critical alerts are surfaced first, then warnings, then a default revenue
    nudge if there is still room.
    """
    focus: list[str] = []

    for alert in alerts:
        if alert.get("severity") == "critical":
            focus.append(f"Resolve: {alert.get('message', '')}")
        if len(focus) >= 3:
            return focus[:3]

    for alert in alerts:
        if alert.get("severity") == "warn":
            focus.append(f"Address: {alert.get('message', '')}")
        if len(focus) >= 3:
            return focus[:3]

    revenue = metrics.get("revenue", {})
    if revenue.get("proposals_sent", 0) == 0:
        focus.append("Send at least one proposal today.")
    if revenue.get("payments_pursued", 0) == 0:
        focus.append("Pursue a payment or PO from an existing proposal.")
    if len(focus) < 3:
        focus.append("Add 5 new qualified leads to pipeline_tracker.csv.")

    return focus[:3]
