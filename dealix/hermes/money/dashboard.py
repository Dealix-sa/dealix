"""Money Dashboard — what Sami opens first every morning."""

from __future__ import annotations

from dataclasses import dataclass

from dealix.hermes.core.outcomes import OutcomeLog
from dealix.hermes.money.cash_scout import CashAction, CashScout


@dataclass(slots=True)
class MoneyDashboard:
    pipeline_value_sar: float
    cash_collected_sar: float
    pipeline_to_paid_ratio: float
    fastest_cash: list[CashAction]
    open_proposals: int


def render(
    *,
    scout: CashScout,
    outcomes: OutcomeLog,
    open_proposals: int,
    top_n: int = 5,
) -> MoneyDashboard:
    actions = scout.fastest_cash(top_n=top_n)
    pipeline = sum(a.expected_value_sar for a in actions)
    cash = outcomes.cash_collected_sar()
    ratio = (pipeline / cash) if cash > 0 else float("inf") if pipeline > 0 else 0.0
    return MoneyDashboard(
        pipeline_value_sar=round(pipeline, 2),
        cash_collected_sar=round(cash, 2),
        pipeline_to_paid_ratio=round(ratio, 3) if ratio != float("inf") else -1.0,
        fastest_cash=actions,
        open_proposals=open_proposals,
    )


__all__ = ["MoneyDashboard", "render"]
