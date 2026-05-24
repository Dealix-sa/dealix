"""Money Dashboard — read-only view assembled from the other money parts."""

from __future__ import annotations

from dataclasses import dataclass

from dealix.hermes.core.opportunities import OpportunityBook
from dealix.hermes.money.followup import FollowUpTracker
from dealix.hermes.money.invoice import InvoiceLedger, InvoiceStatus
from dealix.hermes.money.proposal_factory import ProposalFactory


@dataclass(frozen=True)
class MoneyDashboardView:
    fastest_cash_action: str
    highest_value_deal_sar: float
    open_proposals: int
    follow_ups_due: int
    pending_payments_sar: float
    expected_revenue_sar: float
    cash_risk: str
    best_next_action: str


class MoneyDashboard:
    def __init__(
        self,
        *,
        opportunities: OpportunityBook,
        proposals: ProposalFactory,
        follow_ups: FollowUpTracker,
        invoices: InvoiceLedger,
    ) -> None:
        self._opps = opportunities
        self._props = proposals
        self._flw = follow_ups
        self._inv = invoices

    def view(self) -> MoneyDashboardView:
        top = self._opps.top_n(1)
        top_opp = top[0] if top else None
        open_props = self._props.open()
        due = self._flw.due()
        open_inv = self._inv.open()
        pending_sar = sum(i.amount_sar for i in open_inv)
        expected_sar = sum(o.estimated_value_sar * (o.score or 0.0) for o in self._opps.all())
        cash_risk = "high" if pending_sar > 100_000 else "low"
        next_action = "Send proposal" if any(p.status == "draft" for p in open_props) else "Follow up" if due else "Hunt new signals"
        return MoneyDashboardView(
            fastest_cash_action=("Score " + top_opp.title) if top_opp else "No opportunities yet.",
            highest_value_deal_sar=max((o.estimated_value_sar for o in self._opps.all()), default=0.0),
            open_proposals=len(open_props),
            follow_ups_due=len(due),
            pending_payments_sar=pending_sar,
            expected_revenue_sar=expected_sar,
            cash_risk=cash_risk,
            best_next_action=next_action,
        )


__all__ = ["MoneyDashboard", "MoneyDashboardView"]
