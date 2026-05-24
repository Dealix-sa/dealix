"""خادم المغامرات — VenturePortfolio.

Aggregates VerticalCards + pilot outcomes into a portfolio view.
"""

from __future__ import annotations

from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from dealix.hermes.core.outcomes import Outcome, OutcomeKind
from dealix.hermes.core.schemas import Money
from dealix.ventures.vertical_launcher import VerticalCard, VerticalLauncher


class VerticalPerformance(BaseModel):
    """One vertical's roll-up of pilot outcomes."""

    model_config = ConfigDict(extra="forbid")

    vertical: str
    pilots_run: int = Field(..., ge=0)
    revenue: Money
    risk_flags: int = Field(..., ge=0)


class PortfolioSnapshot(BaseModel):
    """The full portfolio overview."""

    model_config = ConfigDict(extra="forbid")

    cards: list[VerticalCard]
    performance: list[VerticalPerformance]
    total_revenue: Money


class VenturePortfolio:
    """Pair VerticalLauncher with the outcomes that came from each card."""

    def __init__(self, launcher: VerticalLauncher | None = None) -> None:
        self._launcher = launcher or VerticalLauncher()
        self._outcomes_by_vertical: dict[str, list[Outcome]] = {}

    def attach_outcomes(self, vertical: str, outcomes: list[Outcome]) -> None:
        self._launcher.get(vertical)  # validate vertical exists
        bucket = self._outcomes_by_vertical.setdefault(vertical, [])
        bucket.extend(outcomes)

    def snapshot(self) -> PortfolioSnapshot:
        cards = self._launcher.all()
        performance: list[VerticalPerformance] = []
        total = Decimal("0")
        for card in cards:
            bucket = self._outcomes_by_vertical.get(card.vertical, [])
            revenue = sum(
                (o.value.amount for o in bucket
                 if o.kind == OutcomeKind.MONEY and o.value is not None),
                start=Decimal("0"),
            )
            risk_flags = sum(1 for o in bucket if o.risk_flag)
            performance.append(
                VerticalPerformance(
                    vertical=card.vertical,
                    pilots_run=len(bucket),
                    revenue=Money.sar(revenue),
                    risk_flags=risk_flags,
                )
            )
            total += revenue
        return PortfolioSnapshot(
            cards=cards,
            performance=performance,
            total_revenue=Money.sar(total),
        )


__all__ = ["PortfolioSnapshot", "VenturePortfolio", "VerticalPerformance"]
