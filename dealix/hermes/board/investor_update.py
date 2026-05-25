"""Render a monthly investor update from BoardMetrics."""

from __future__ import annotations

from .metrics import BoardMetrics


def render(metrics: BoardMetrics, *, narrative: str = "") -> str:
    """Render a markdown investor update from a BoardMetrics snapshot."""
    lines = [
        f"# Dealix Investor Update — {metrics.period}",
        "",
        "## Verified Outcomes",
        f"- Verified revenue: {metrics.verified_revenue_sar:,.0f} SAR",
        f"- Revenue quality grade: {metrics.revenue_quality_grade}",
        f"- Pipeline quality grade: {metrics.pipeline_quality_grade}",
        f"- Gross margin: {metrics.gross_margin * 100:.1f}%",
        f"- Retainer conversion: {metrics.retainer_conversion * 100:.1f}%",
        "",
        "## Operating Leverage",
        f"- Agent ROI: {metrics.agent_roi:.2f}x",
        f"- Assets created / reused: {metrics.assets_created} / {metrics.assets_reused}",
        f"- Founder time leverage: {metrics.founder_time_leverage_hours:.1f} hours",
        "",
        "## Governance",
        f"- Trust incidents: {metrics.trust_incidents}",
        f"- Approvals pending: {metrics.approvals_pending}",
        "",
        "## Ecosystem",
        f"- Partner revenue: {metrics.partner_revenue_sar:,.0f} SAR",
    ]
    if narrative:
        lines.extend(["", "## Narrative", narrative.strip()])
    return "\n".join(lines)
