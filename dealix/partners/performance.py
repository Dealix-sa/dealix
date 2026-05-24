"""خادم الشركاء — PartnerPerformance.snapshot.

Aggregates a partner's closed deal outcomes into a snapshot with
closed_deals, revenue, avg_cycle_days and health_score.
"""

from __future__ import annotations

from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from dealix.hermes.core.outcomes import Outcome, OutcomeKind
from dealix.hermes.core.schemas import Money


class PartnerPerformanceSnapshot(BaseModel):
    """A snapshot of one partner's closed-deal performance."""

    model_config = ConfigDict(extra="forbid")

    partner_id: str = Field(..., min_length=1, max_length=128)
    closed_deals: int = Field(..., ge=0)
    revenue: Money
    avg_cycle_days: float = Field(..., ge=0.0)
    health_score: float = Field(..., ge=0.0, le=5.0)
    risk_flags: int = Field(default=0, ge=0)


class PartnerPerformance:
    """Compute a PartnerPerformanceSnapshot from a list of outcomes."""

    def snapshot(
        self,
        partner_id: str,
        deals: list[Outcome],
        avg_cycle_days: float | None = None,
    ) -> PartnerPerformanceSnapshot:
        money_deals = [
            o for o in deals
            if o.kind == OutcomeKind.MONEY and o.value is not None
        ]
        revenue_amount = sum(
            (o.value.amount for o in money_deals if o.value is not None),
            start=Decimal("0"),
        )
        revenue = Money.sar(revenue_amount)
        cycle = avg_cycle_days if avg_cycle_days is not None else self._estimate_cycle(deals)
        risk_flags = sum(1 for o in deals if o.risk_flag)
        health = self._health_score(
            count=len(money_deals),
            revenue=revenue_amount,
            cycle_days=cycle,
            risk_flags=risk_flags,
        )
        return PartnerPerformanceSnapshot(
            partner_id=partner_id,
            closed_deals=len(money_deals),
            revenue=revenue,
            avg_cycle_days=float(round(cycle, 2)),
            health_score=float(round(health, 3)),
            risk_flags=risk_flags,
        )

    @staticmethod
    def _estimate_cycle(deals: list[Outcome]) -> float:
        if not deals:
            return 0.0
        # Without explicit timestamps in our outcomes we proxy cycle days
        # via the metrics dict; fall back to 30 days when no proxy exists.
        cycles: list[float] = []
        for d in deals:
            metric = d.metrics.get("cycle_days")
            if isinstance(metric, (int, float)):
                cycles.append(float(metric))
        if not cycles:
            return 30.0
        return sum(cycles) / len(cycles)

    @staticmethod
    def _health_score(
        count: int,
        revenue: Decimal,
        cycle_days: float,
        risk_flags: int,
    ) -> float:
        score = 0.0
        if count >= 1:
            score += 1.5
        if count >= 3:
            score += 1.0
        if revenue >= Decimal("10000"):
            score += 1.0
        if revenue >= Decimal("50000"):
            score += 0.5
        if 0 < cycle_days <= 30:
            score += 1.0
        elif cycle_days <= 60:
            score += 0.5
        # Each risk flag costs 0.5; never go below 0.
        score = max(0.0, score - 0.5 * risk_flags)
        return min(5.0, score)


__all__ = ["PartnerPerformance", "PartnerPerformanceSnapshot"]
