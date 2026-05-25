"""Render a traction report focused on verified-revenue movement and key ratios."""

from __future__ import annotations

from dataclasses import dataclass

from .metrics import BoardMetrics


@dataclass(frozen=True)
class TractionDelta:
    revenue_delta_sar: float
    margin_delta_pp: float
    retainer_delta_pp: float


def delta(previous: BoardMetrics, current: BoardMetrics) -> TractionDelta:
    """Compute traction deltas between two consecutive board metrics snapshots."""
    return TractionDelta(
        revenue_delta_sar=round(current.verified_revenue_sar - previous.verified_revenue_sar, 2),
        margin_delta_pp=round((current.gross_margin - previous.gross_margin) * 100, 2),
        retainer_delta_pp=round((current.retainer_conversion - previous.retainer_conversion) * 100, 2),
    )


def render(previous: BoardMetrics, current: BoardMetrics) -> str:
    """Render a markdown traction report between two periods."""
    d = delta(previous, current)
    return "\n".join(
        [
            f"# Traction Report — {previous.period} -> {current.period}",
            "",
            f"- Verified revenue delta: {d.revenue_delta_sar:,.0f} SAR",
            f"- Gross margin delta: {d.margin_delta_pp:+.2f} pp",
            f"- Retainer conversion delta: {d.retainer_delta_pp:+.2f} pp",
            f"- Trust incidents this period: {current.trust_incidents}",
        ]
    )
