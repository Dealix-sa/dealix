from __future__ import annotations

"""Enhanced weekly review with prior-week comparisons and learning decisions."""

from datetime import date, timedelta
from pathlib import Path
from typing import Any

from .markdown_writer import write_markdown

WEEKLY_DIR = "weekly_reviews"


def _monday_of(today: date) -> date:
    return today - timedelta(days=today.weekday())


def _format_delta(value: float) -> str:
    if value > 0:
        return f"+{value}"
    return str(value)


def generate_weekly_review_v2(
    metrics: dict[str, Any],
    comparisons: dict[str, Any],
    learning_actions: list[dict[str, Any]],
    private_ops_path: Path,
) -> Path:
    """Write the v2 weekly review with deltas and learning decisions."""
    private_ops_path = Path(private_ops_path)
    monday = _monday_of(date.today())
    target = private_ops_path / WEEKLY_DIR / f"{monday.isoformat()}_v2.md"

    pipeline = metrics.get("pipeline", {})
    revenue = metrics.get("revenue", {})
    delivery = metrics.get("delivery", {})

    body: list[str] = []
    body.append(f"# Weekly Review v2 — week of {monday.isoformat()}")
    body.append("")

    body.append("## Headline metrics")
    body.append(f"- Pipeline value (SAR): {pipeline.get('pipeline_value_sar', 0.0)}")
    body.append(f"- Proposals sent: {revenue.get('proposals_sent', 0)}")
    body.append(f"- Cash collected (SAR): {revenue.get('cash_collected_sar', 0.0)}")
    body.append(f"- Active clients: {delivery.get('active_clients', 0)}")
    body.append("")

    body.append("## Compared to prior week")
    if not comparisons.get("available"):
        body.append("- No prior week recorded yet.")
    else:
        deltas = comparisons.get("deltas", {})
        for key, value in deltas.items():
            body.append(f"- {key}: {_format_delta(value)}")
    body.append("")

    body.append("## Learning decisions")
    if not learning_actions:
        body.append("- No new learning decisions this week.")
    else:
        for item in learning_actions:
            body.append(
                f"- {item.get('type', 'note').upper()} {item.get('target', '')}: "
                f"{item.get('reason', '')} (evidence: {item.get('evidence', '')})"
            )
    body.append("")

    body.append("## Decisions made / deferred")
    body.append("- Made: see decision_queue.md")
    body.append("- Deferred: see decision_queue.md")
    body.append("")

    frontmatter = {
        "type": "weekly_review_v2",
        "week_of": monday.isoformat(),
    }
    return write_markdown(target, frontmatter, "\n".join(body))
