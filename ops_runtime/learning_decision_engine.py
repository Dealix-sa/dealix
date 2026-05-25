from __future__ import annotations

"""Emit keep/kill/double learning decisions from metrics and deltas."""

from typing import Any


def decide_learning_actions(
    metrics: dict[str, Any], comparisons: dict[str, Any]
) -> list[dict[str, Any]]:
    """Return a list of {type, target, reason, evidence} dicts."""
    actions: list[dict[str, Any]] = []
    pipeline = metrics.get("pipeline", {})
    revenue = metrics.get("revenue", {})

    by_sector = pipeline.get("by_sector", {}) or {}
    if by_sector:
        top_sector, top_count = max(by_sector.items(), key=lambda kv: kv[1])
        if top_count >= 5:
            actions.append(
                {
                    "type": "double",
                    "target": f"sector:{top_sector}",
                    "reason": "Most-represented sector in pipeline",
                    "evidence": f"{top_count} leads",
                }
            )
        worst_sector, worst_count = min(by_sector.items(), key=lambda kv: kv[1])
        if worst_count == 0 and worst_sector != top_sector:
            actions.append(
                {
                    "type": "kill",
                    "target": f"sector:{worst_sector}",
                    "reason": "No traction",
                    "evidence": "0 leads",
                }
            )

    # If we keep sending proposals but get no payment motion, that is a signal.
    proposals = revenue.get("proposals_sent", 0)
    payments = revenue.get("payments_pursued", 0)
    if proposals >= 3 and payments == 0:
        actions.append(
            {
                "type": "keep",
                "target": "proposal_template",
                "reason": "Proposals are going out; convert to payment asks",
                "evidence": f"{proposals} proposals / {payments} payment asks",
            }
        )

    if comparisons.get("available"):
        deltas = comparisons.get("deltas", {}) or {}
        if deltas.get("cash_collected_sar", 0) > 0:
            actions.append(
                {
                    "type": "double",
                    "target": "current_revenue_motion",
                    "reason": "Cash collection is trending up",
                    "evidence": f"+{deltas['cash_collected_sar']} SAR vs prior week",
                }
            )
        if deltas.get("dms_sent", 0) < 0:
            actions.append(
                {
                    "type": "keep",
                    "target": "outbound_cadence",
                    "reason": "DM volume dropped vs prior week",
                    "evidence": f"{deltas['dms_sent']} DMs delta",
                }
            )

    return actions
