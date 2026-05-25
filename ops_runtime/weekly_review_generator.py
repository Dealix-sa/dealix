from __future__ import annotations

"""Generate the weekly review Markdown file."""

from datetime import date, timedelta
from pathlib import Path
from typing import Any

from .markdown_writer import write_markdown

WEEKLY_DIR = "weekly_reviews"


def _monday_of(today: date) -> date:
    """Return the Monday of `today`'s ISO week."""
    return today - timedelta(days=today.weekday())


def generate_weekly_review(metrics: dict[str, Any], private_ops_path: Path) -> Path:
    """Write `weekly_reviews/YYYY-MM-DD.md` dated to this week's Monday."""
    private_ops_path = Path(private_ops_path)
    monday = _monday_of(date.today())
    target = private_ops_path / WEEKLY_DIR / f"{monday.isoformat()}.md"

    pipeline = metrics.get("pipeline", {})
    revenue = metrics.get("revenue", {})
    delivery = metrics.get("delivery", {})

    body: list[str] = []
    body.append(f"# Weekly Review — week of {monday.isoformat()}")
    body.append("")
    body.append("## Pipeline")
    body.append(f"- Total leads: {pipeline.get('total_leads', 0)}")
    body.append(
        f"- Pipeline value (SAR): {pipeline.get('pipeline_value_sar', 0.0)}"
    )
    body.append(f"- High priority: {pipeline.get('priority_high', 0)}")
    body.append("")
    body.append("## Revenue activity")
    body.append(f"- DMs sent: {revenue.get('dms_sent', 0)}")
    body.append(f"- Samples sent: {revenue.get('samples_sent', 0)}")
    body.append(f"- Proposals sent: {revenue.get('proposals_sent', 0)}")
    body.append(f"- Payments pursued: {revenue.get('payments_pursued', 0)}")
    body.append(
        f"- Cash collected (SAR): {revenue.get('cash_collected_sar', 0.0)}"
    )
    body.append("")
    body.append("## Delivery")
    body.append(f"- Active: {delivery.get('active_clients', 0)}")
    body.append(f"- In delivery: {delivery.get('in_delivery', 0)}")
    body.append(f"- Completed: {delivery.get('completed', 0)}")
    body.append(f"- At risk: {delivery.get('at_risk', 0)}")
    body.append("")

    frontmatter = {
        "type": "weekly_review",
        "week_of": monday.isoformat(),
    }
    return write_markdown(target, frontmatter, "\n".join(body))
