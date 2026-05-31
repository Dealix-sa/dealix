"""Money Dashboard — Sami's primary money view."""

from __future__ import annotations

from dataclasses import dataclass, field

from dealix.hermes.money.cashflow import CashflowBrief
from dealix.hermes.money.deal_room import DealRoom, DealStage


@dataclass
class MoneyDashboard:
    fastest_cash_action: str = ""
    highest_value_deal_id: str | None = None
    open_proposals: int = 0
    followups_due: int = 0
    pending_payments: int = 0
    upsell_candidates: int = 0
    partner_revenue_sar: float = 0.0
    expected_revenue_sar: float = 0.0
    cash_risk: str = "low"
    best_next_action: str = ""

    @classmethod
    def from_inputs(
        cls,
        *,
        cashflow: CashflowBrief,
        deals: list[DealRoom],
        open_proposals: int = 0,
        followups_due: int = 0,
        pending_payments: int = 0,
        upsell_candidates: int = 0,
        partner_revenue_sar: float = 0.0,
        best_next_action: str = "",
    ) -> "MoneyDashboard":
        open_or_proposed = [d for d in deals if d.stage in {DealStage.qualified, DealStage.proposed, DealStage.negotiation}]
        highest = max(open_or_proposed, key=lambda d: d.estimated_value_sar, default=None)
        return cls(
            fastest_cash_action=cashflow.fastest_cash_action,
            highest_value_deal_id=highest.deal_id if highest else None,
            open_proposals=open_proposals,
            followups_due=followups_due,
            pending_payments=pending_payments,
            upsell_candidates=upsell_candidates,
            partner_revenue_sar=partner_revenue_sar,
            expected_revenue_sar=cashflow.expected_inflow_sar,
            cash_risk=cashflow.cash_risk,
            best_next_action=best_next_action or cashflow.fastest_cash_action,
        )
