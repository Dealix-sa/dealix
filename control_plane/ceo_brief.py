"""
Daily CEO Brief.

Generates the markdown brief the founder reads each morning. The brief
is deterministic from a CompanyState, which makes it easy to test.
"""
from __future__ import annotations

from dataclasses import dataclass

from .company_state import CompanyState


@dataclass(slots=True)
class CEOBrief:
    title: str
    body: str

    def as_markdown(self) -> str:
        return f"# {self.title}\n\n{self.body}\n"


def generate_ceo_brief(state: CompanyState) -> CEOBrief:
    """Render a CompanyState into a CEO brief."""
    date = state.as_of.date().isoformat()
    health_band = (
        "HEALTHY" if state.is_healthy
        else "WATCH" if state.company_health_score >= 60
        else "ALERT"
    )

    lines: list[str] = []
    lines.append(f"**Date:** {date}")
    lines.append(f"**Stage:** {state.stage}")
    lines.append(f"**Company health:** {state.company_health_score}/100 ({health_band})")
    lines.append("")
    lines.append("## Pipeline")
    lines.append(f"- Leads this week: {state.leads_this_week}")
    lines.append(f"- Qualified: {state.qualified_leads}")
    lines.append(f"- Proposals out: {state.proposals_out}")
    lines.append(f"- Paid sprints: {state.paid_sprints}")
    lines.append("")
    lines.append("## Money")
    lines.append(f"- Cash collected (30d): {state.cash_collected_30d:,.0f} SAR")
    lines.append(f"- MRR: {state.mrr:,.0f} SAR")
    lines.append(f"- Runway: {state.runway_months:.1f} months")
    lines.append("")
    lines.append("## Decision Queue")
    lines.append(f"- Pending approvals: {state.pending_approvals}")
    lines.append("")
    lines.append("## Risks")
    if state.open_risks:
        for r in state.open_risks:
            lines.append(f"- {r}")
    else:
        lines.append("- (none open)")

    return CEOBrief(title=f"Daily CEO Brief — {date}", body="\n".join(lines))
