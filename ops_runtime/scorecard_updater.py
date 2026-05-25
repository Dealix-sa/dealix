from __future__ import annotations

"""Write the CEO/founder KPI scorecard dashboard."""

from datetime import date
from pathlib import Path
from typing import Any

from .markdown_writer import write_markdown
from .target_scoring import score_against_targets

DASHBOARD_RELPATH = "founder/ceo_dashboard.md"


def update_scorecard(metrics: dict[str, Any], private_ops_path: Path) -> Path:
    """Write `founder/ceo_dashboard.md` with current KPI scoring."""
    private_ops_path = Path(private_ops_path)
    target = private_ops_path / DASHBOARD_RELPATH

    scores = score_against_targets(metrics)
    overall = scores.pop("_overall_percent", 0.0)

    body: list[str] = []
    body.append(f"# CEO Dashboard — {date.today().isoformat()}")
    body.append("")
    body.append(f"Overall weekly target hit: {overall}%")
    body.append("")
    body.append("## KPI scorecard")
    body.append("")
    body.append("| KPI | Actual | Target | % |")
    body.append("|---|---|---|---|")
    for kpi, row in scores.items():
        body.append(
            f"| {kpi} | {row['actual']} | {row['target']} | {row['percent']}% |"
        )
    body.append("")

    frontmatter = {
        "type": "ceo_dashboard",
        "date": date.today().isoformat(),
        "overall_percent": overall,
    }
    return write_markdown(target, frontmatter, "\n".join(body))
