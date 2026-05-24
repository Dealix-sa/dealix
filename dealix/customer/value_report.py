"""خادم العميل — MonthlyValueReportBuilder (spec §32).

The §32 monthly value report carries eight fields:

    1. customer_id
    2. period_start / period_end (joined as one period)
    3. revenue_delivered (Money)
    4. cost_to_serve (Money)
    5. assets_built (count + names)
    6. risks_avoided
    7. learnings
    8. next_quarter_plan
"""

from __future__ import annotations

from datetime import date, datetime, timedelta
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from dealix.hermes.core.outcomes import Outcome, OutcomeKind
from dealix.hermes.core.schemas import Money, utcnow


class MonthlyValueReport(BaseModel):
    """§32 monthly value report — eight required fields."""

    model_config = ConfigDict(extra="forbid")

    customer_id: str = Field(..., min_length=1, max_length=128)
    period_start: date
    period_end: date
    revenue_delivered: Money
    cost_to_serve: Money
    assets_built: list[str] = Field(default_factory=list, max_length=50)
    risks_avoided: list[str] = Field(default_factory=list, max_length=50)
    learnings: list[str] = Field(default_factory=list, max_length=50)
    next_quarter_plan: list[str] = Field(default_factory=list, max_length=10)


class MonthlyValueReportBuilder:
    """Aggregate Outcomes for a customer into a §32 monthly report."""

    def build(
        self,
        customer_id: str,
        period_outcomes: list[Outcome],
        period_start: date | None = None,
        period_end: date | None = None,
    ) -> MonthlyValueReport:
        end = period_end or utcnow().date()
        start = period_start or (end - timedelta(days=30))

        revenue = Decimal("0")
        cost = Decimal("0")
        assets: list[str] = []
        risks: list[str] = []
        learnings: list[str] = []

        for outcome in period_outcomes:
            if outcome.kind == OutcomeKind.MONEY and outcome.value is not None:
                revenue += outcome.value.amount
                cost += outcome.value.amount * Decimal("0.25")  # 25 % cost-to-serve heuristic
            if outcome.kind == OutcomeKind.ASSET:
                assets.append(outcome.summary)
            if outcome.kind == OutcomeKind.TRUST and outcome.risk_flag is False:
                risks.append(outcome.summary)
            if outcome.kind == OutcomeKind.LEARNING:
                learnings.extend(outcome.learnings or [outcome.summary])

        # Next-quarter plan: minimal, deterministic.
        next_quarter_plan = [
            "Retain renewal momentum",
            "Promote one new asset into productized offer",
            "Close one upsell opportunity",
        ]
        return MonthlyValueReport(
            customer_id=customer_id,
            period_start=start,
            period_end=end,
            revenue_delivered=Money.sar(revenue),
            cost_to_serve=Money.sar(cost),
            assets_built=assets[:50],
            risks_avoided=risks[:50],
            learnings=learnings[:50],
            next_quarter_plan=next_quarter_plan,
        )


__all__ = ["MonthlyValueReport", "MonthlyValueReportBuilder"]
