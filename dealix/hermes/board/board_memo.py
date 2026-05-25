from __future__ import annotations

from dataclasses import dataclass

from dealix.hermes.board.executive_metrics import ExecutiveMetrics


@dataclass
class BoardMemo:
    period: str
    decision_topic: str
    recommendation: str
    options_considered: list[str]
    metrics: ExecutiveMetrics
    risks: list[str]
    next_review_date: str


def render_board_memo(memo: BoardMemo) -> str:
    lines = [
        f"# Board memo — {memo.period}",
        "",
        f"## Decision topic\n{memo.decision_topic}",
        "",
        f"## Recommendation\n{memo.recommendation}",
        "",
        "## Options considered",
    ]
    lines.extend(f"- {o}" for o in memo.options_considered)
    lines.extend(
        [
            "",
            "## Headline metrics",
            f"- Verified revenue: SAR {memo.metrics.verified_revenue_sar:,.0f}",
            f"- Gross margin: {memo.metrics.gross_margin_pct:.1f}%",
            f"- Revenue quality: {memo.metrics.revenue_quality_score:.1f}",
            f"- Trust incidents: {memo.metrics.trust_incidents}",
            "",
            "## Risks",
        ]
    )
    lines.extend(f"- {r}" for r in memo.risks)
    lines.extend(["", f"## Next review\n{memo.next_review_date}"])
    return "\n".join(lines)
