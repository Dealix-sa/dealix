"""
Weekly review generator.

Composes a CompanyState + bottleneck + learning summary into the
markdown the founder reviews each Sunday.
"""
from __future__ import annotations

from dataclasses import dataclass

from control_plane.company_state import CompanyState
from .bottleneck_detector import Bottleneck
from .learning_synthesizer import LearningSummary


@dataclass(slots=True)
class WeeklyReview:
    title: str
    body: str

    def as_markdown(self) -> str:
        return f"# {self.title}\n\n{self.body}\n"


def generate_weekly_review(
    state: CompanyState,
    *,
    bottleneck: Bottleneck | None,
    learning: LearningSummary,
) -> WeeklyReview:
    week = state.as_of.isocalendar()
    title = f"Weekly CEO Review — {state.as_of.year} W{week.week:02d}"

    lines: list[str] = []
    lines.append(f"**Stage:** {state.stage}")
    lines.append(f"**Health:** {state.company_health_score}/100")
    lines.append("")
    lines.append("## Pipeline")
    lines.append(f"- Leads: {state.leads_this_week}")
    lines.append(f"- Qualified: {state.qualified_leads}")
    lines.append(f"- Proposals: {state.proposals_out}")
    lines.append(f"- Paid sprints: {state.paid_sprints}")
    lines.append("")
    lines.append("## Money")
    lines.append(f"- Cash (30d): {state.cash_collected_30d:,.0f} SAR")
    lines.append(f"- MRR: {state.mrr:,.0f} SAR")
    lines.append(f"- Runway: {state.runway_months:.1f} months")
    lines.append("")
    lines.append("## Bottleneck")
    if bottleneck is None:
        lines.append("- (no bottleneck below target)")
    else:
        lines.append(
            f"- {bottleneck.stage}: actual {bottleneck.actual_ratio:.0%} vs "
            f"target {bottleneck.target_ratio:.0%} — severity {bottleneck.severity}"
        )
    lines.append("")
    lines.append("## Learning")
    if not learning.counts_by_kind:
        lines.append("- (no signals captured)")
    else:
        for k, v in sorted(learning.counts_by_kind.items()):
            lines.append(f"- {k}: {v}")
    if learning.top_signals:
        lines.append("")
        lines.append("### Top signals")
        for s in learning.top_signals:
            lines.append(f"- {s}")

    return WeeklyReview(title=title, body="\n".join(lines))
