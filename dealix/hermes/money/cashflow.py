"""Daily cashflow brief."""

from __future__ import annotations

from dataclasses import dataclass

from dealix.hermes.money.revenue_streams import RevenueStream


@dataclass(frozen=True)
class CashflowBrief:
    expected_inflow_sar: float
    verified_inflow_sar: float
    overdue_sar: float
    fastest_cash_action: str
    cash_risk: str  # "low" | "medium" | "high"


def build_cashflow_brief(
    streams: list[RevenueStream],
    *,
    overdue_sar: float = 0.0,
    fastest_cash_action: str = "",
) -> CashflowBrief:
    expected = sum(s.total_sar for s in streams)
    verified = sum(s.verified_sar for s in streams)
    risk = "low"
    if overdue_sar > verified * 0.5:
        risk = "high"
    elif overdue_sar > verified * 0.2:
        risk = "medium"
    return CashflowBrief(
        expected_inflow_sar=expected,
        verified_inflow_sar=verified,
        overdue_sar=overdue_sar,
        fastest_cash_action=fastest_cash_action,
        cash_risk=risk,
    )
