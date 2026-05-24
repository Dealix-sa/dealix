"""Cashflow Brief — weekly cash-in / cash-expected summary."""

from __future__ import annotations

from dataclasses import dataclass

from dealix.hermes.core.outcomes import get_outcome_store
from dealix.hermes.core.schemas import OutcomeStatus


@dataclass
class CashflowSummary:
    paid_sar: float
    won_unpaid_sar: float
    expected_sar: float
    cash_risk: str


class CashflowBrief:
    def summary(self) -> CashflowSummary:
        outs = get_outcome_store().list()
        paid = sum(o.revenue_sar for o in outs if o.status == OutcomeStatus.PAID.value)
        won = sum(o.revenue_sar for o in outs if o.status == OutcomeStatus.WON.value)
        expected = paid + won
        risk = "high" if expected < 10_000 else ("medium" if expected < 50_000 else "low")
        return CashflowSummary(paid_sar=paid, won_unpaid_sar=won, expected_sar=expected, cash_risk=risk)
