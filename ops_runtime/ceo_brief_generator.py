from __future__ import annotations

"""Generate the daily CEO/founder brief."""

from datetime import date
from pathlib import Path
from typing import Any

from .markdown_writer import write_markdown

DAILY_BRIEF_RELPATH = "founder/daily_brief.md"


def generate_daily_brief(metrics: dict[str, Any], private_ops_path: Path) -> Path:
    """Write `founder/daily_brief.md`.

    The brief answers five founder questions: revenue movers, blockers,
    approvals needed, at-risk delivery, things to kill/defer.
    """
    private_ops_path = Path(private_ops_path)
    target = private_ops_path / DAILY_BRIEF_RELPATH

    pipeline = metrics.get("pipeline", {})
    revenue = metrics.get("revenue", {})
    delivery = metrics.get("delivery", {})

    body_parts: list[str] = []
    body_parts.append(f"# Daily Brief — {date.today().isoformat()}")
    body_parts.append("")

    body_parts.append("## What moves revenue today")
    proposals_sent = revenue.get("proposals_sent", 0)
    payments = revenue.get("payments_pursued", 0)
    body_parts.append(
        f"- Proposals out so far: {proposals_sent}. Payments/POs pursued: {payments}."
    )
    if proposals_sent > 0 and payments == 0:
        body_parts.append("- Action: convert at least one proposal into a payment ask.")
    body_parts.append("")

    body_parts.append("## What is blocked")
    blocked = delivery.get("at_risk", 0)
    if blocked:
        body_parts.append(f"- {blocked} client(s) flagged at_risk in clients/.")
    else:
        body_parts.append("- No blocked items reported.")
    body_parts.append("")

    body_parts.append("## What needs approval")
    high_priority = pipeline.get("priority_high", 0)
    body_parts.append(
        f"- {high_priority} high-priority lead(s) await founder review."
    )
    body_parts.append("")

    body_parts.append("## Delivery at risk")
    body_parts.append(
        f"- Active clients: {delivery.get('active_clients', 0)}; "
        f"in delivery: {delivery.get('in_delivery', 0)}; "
        f"at risk: {delivery.get('at_risk', 0)}; "
        f"completed: {delivery.get('completed', 0)}."
    )
    body_parts.append("")

    body_parts.append("## Kill / defer")
    by_stage = pipeline.get("by_stage", {})
    stalled = by_stage.get("stalled", 0)
    if stalled:
        body_parts.append(f"- {stalled} stalled lead(s); review and kill or revive.")
    else:
        body_parts.append("- Nothing flagged for kill/defer today.")
    body_parts.append("")

    frontmatter = {
        "type": "daily_brief",
        "date": date.today().isoformat(),
    }
    return write_markdown(target, frontmatter, "\n".join(body_parts))
