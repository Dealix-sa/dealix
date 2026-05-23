"""
Decision engine.

Given a CompanyState, propose the next 1-3 decisions the founder should
make today. Each decision is tagged with an approval class consumed by
the approval router.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .company_state import CompanyState

# Approval classes match DEALIX_DECISION_RULES.md
_AUTO = "auto"
_FOUNDER = "founder"
_FOUNDER_24H = "founder_24h"
_FOUNDER_CAPITAL = "founder_capital"


@dataclass(frozen=True, slots=True)
class Decision:
    label: str
    rationale: str
    approval_class: str


class DecisionEngine:
    """Map company state -> ranked next decisions."""

    def __init__(
        self,
        *,
        target_leads_per_week: int = 25,
        target_proposals_per_week: int = 1,
        min_runway_months: float = 6.0,
    ) -> None:
        self.target_leads_per_week = target_leads_per_week
        self.target_proposals_per_week = target_proposals_per_week
        self.min_runway_months = min_runway_months

    def propose(self, state: CompanyState) -> list[Decision]:
        out: list[Decision] = []

        if state.pending_approvals > 0:
            out.append(
                Decision(
                    label=f"Clear {state.pending_approvals} pending approvals",
                    rationale="Approvals gate every outbound action and refund.",
                    approval_class=_FOUNDER,
                )
            )

        if state.runway_months and state.runway_months < self.min_runway_months:
            out.append(
                Decision(
                    label="Cut burn or accelerate cash",
                    rationale=(
                        f"Runway is {state.runway_months:.1f} months, below "
                        f"{self.min_runway_months}."
                    ),
                    approval_class=_FOUNDER_CAPITAL,
                )
            )

        if state.leads_this_week < self.target_leads_per_week:
            gap = self.target_leads_per_week - state.leads_this_week
            out.append(
                Decision(
                    label=f"Add {gap} qualified leads this week",
                    rationale=(
                        f"Pipeline is {state.leads_this_week}/"
                        f"{self.target_leads_per_week}."
                    ),
                    approval_class=_AUTO,
                )
            )

        if state.proposals_out < self.target_proposals_per_week:
            out.append(
                Decision(
                    label="Send at least one proposal this week",
                    rationale="Weekly proposal cadence is the leading revenue indicator.",
                    approval_class=_FOUNDER_24H,
                )
            )

        if not out:
            out.append(
                Decision(
                    label="Run weekly CEO review",
                    rationale="Nothing flagged — invest the slack in synthesis.",
                    approval_class=_AUTO,
                )
            )
        return out

    def filter_by_class(
        self, decisions: Iterable[Decision], approval_class: str
    ) -> list[Decision]:
        return [d for d in decisions if d.approval_class == approval_class]
