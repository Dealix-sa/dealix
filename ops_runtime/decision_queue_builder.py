from __future__ import annotations

"""Write the founder decision queue Markdown file."""

from datetime import date
from pathlib import Path
from typing import Any

from .markdown_writer import write_markdown

DECISION_QUEUE_RELPATH = "founder/decision_queue.md"


def build_decision_queue(
    private_ops_path: Path, alerts: list[dict[str, Any]]
) -> Path:
    """Write `founder/decision_queue.md` listing items awaiting decision."""
    private_ops_path = Path(private_ops_path)
    target = private_ops_path / DECISION_QUEUE_RELPATH

    body: list[str] = []
    body.append(f"# Decision Queue — {date.today().isoformat()}")
    body.append("")
    if not alerts:
        body.append("No decisions awaiting founder review.")
    else:
        body.append("## Pending")
        body.append("")
        for alert in alerts:
            severity = alert.get("severity", "info")
            kpi = alert.get("kpi", "general")
            message = alert.get("message", "")
            body.append(f"- [{severity.upper()}] {kpi}: {message}")
        body.append("")
        body.append("## Notes")
        body.append("- Mark each item resolved/deferred when reviewed.")
    body.append("")

    frontmatter = {
        "type": "decision_queue",
        "date": date.today().isoformat(),
    }
    return write_markdown(target, frontmatter, "\n".join(body))
