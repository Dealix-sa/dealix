from __future__ import annotations

from dataclasses import dataclass

from dealix.hermes.board.executive_metrics import ExecutiveMetrics


@dataclass
class InvestorUpdate:
    period: str
    headline: str
    metrics: ExecutiveMetrics
    highlights: list[str]
    lowlights: list[str]
    asks: list[str]


def render_investor_update(update: InvestorUpdate) -> str:
    m = update.metrics
    lines = [
        f"# Dealix — Investor Update — {update.period}",
        "",
        f"**Headline:** {update.headline}",
        "",
        "## Verified results",
        f"- Verified revenue (SAR): {m.verified_revenue_sar:,.0f}",
        f"- Gross margin: {m.gross_margin_pct:.1f}%",
        f"- Retainer conversion: {m.retainer_conversion_pct:.1f}%",
        f"- Revenue quality score: {m.revenue_quality_score:.1f}/100",
        f"- Customer value delivered: {m.customer_value_delivered_sar:,.0f}",
        f"- Agent ROI: {m.agent_roi:.2f}",
        f"- Partner revenue: {m.partner_revenue_sar:,.0f}",
        f"- Founder strategic-time leverage: {m.founder_time_leverage:.2f}",
        f"- Trust incidents this period: {m.trust_incidents}",
        "",
        "## Highlights",
    ]
    lines.extend(f"- {h}" for h in update.highlights)
    lines.append("")
    lines.append("## Lowlights")
    lines.extend(f"- {h}" for h in update.lowlights)
    lines.append("")
    lines.append("## Asks")
    lines.extend(f"- {h}" for h in update.asks)
    return "\n".join(lines)
