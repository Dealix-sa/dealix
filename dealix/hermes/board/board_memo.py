"""Render a concise board memo with a decision request."""

from __future__ import annotations

from dataclasses import dataclass

from .metrics import BoardMetrics


@dataclass(frozen=True)
class BoardMemo:
    title: str
    body: str
    decision_requested: str


def compose(*, metrics: BoardMetrics, title: str, narrative: str, decision_requested: str) -> BoardMemo:
    """Compose a BoardMemo summarizing metrics, narrative and an explicit decision request."""
    body = "\n".join(
        [
            f"Period: {metrics.period}",
            f"Verified revenue: {metrics.verified_revenue_sar:,.0f} SAR",
            f"Revenue quality: {metrics.revenue_quality_grade}",
            f"Pipeline quality: {metrics.pipeline_quality_grade}",
            f"Trust incidents: {metrics.trust_incidents}",
            "",
            narrative.strip(),
        ]
    )
    return BoardMemo(title=title, body=body, decision_requested=decision_requested.strip())
