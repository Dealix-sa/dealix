"""خادم المال — MoneyDashboard (spec §41).

Aggregates the live state of money workflows: cash today, top
opportunity, pending approvals, biggest risk, and a weekly KPI
snapshot. Pure read-only — never mutates the inputs.
"""

from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from dealix.hermes.core.opportunities import Opportunity
from dealix.hermes.core.outcomes import Outcome, OutcomeKind
from dealix.hermes.core.schemas import Money, utcnow
from dealix.hermes.core.scoring import opportunity_score
from dealix.trust.approvals import ApprovalQueue, ApprovalTicket


class MoneyWeeklySnapshot(BaseModel):
    """Eight commercial KPIs for the week in review."""

    model_config = ConfigDict(extra="forbid")

    cash_collected: Money
    cash_at_risk: Money
    open_opportunities: int = Field(..., ge=0)
    proposals_drafted: int = Field(..., ge=0)
    approvals_pending: int = Field(..., ge=0)
    pilots_active: int = Field(..., ge=0)
    win_rate_pct: float = Field(..., ge=0.0, le=1.0)
    top_offer_name: str
    period_start: date
    period_end: date


class MoneyDashboard:
    """Read-only aggregator over outcomes / opportunities / approvals."""

    def __init__(self, outcomes: list[Outcome] | None = None) -> None:
        self._outcomes: list[Outcome] = list(outcomes or [])

    # ── tile helpers ─────────────────────────────────────────────
    def cash_today(self, now: datetime | None = None) -> Money:
        ref = now or utcnow()
        total = Decimal("0")
        for outcome in self._outcomes:
            if outcome.kind != OutcomeKind.MONEY or outcome.value is None:
                continue
            if outcome.created_at.date() == ref.date():
                total += outcome.value.amount
        return Money.sar(total)

    def top_opportunity_today(
        self,
        opportunities: list[Opportunity],
    ) -> Opportunity | None:
        if not opportunities:
            return None
        ranked = sorted(opportunities, key=opportunity_score, reverse=True)
        return ranked[0]

    def approvals_pending(self, queue: ApprovalQueue) -> list[ApprovalTicket]:
        return queue.pending()

    def biggest_risk(self, register: list[dict[str, Any]]) -> str:
        if not register:
            return "no open risks"
        # Score by severity weight if supplied, else fallback to amount.
        def weight(item: dict[str, Any]) -> float:
            sev = str(item.get("severity", "low")).lower()
            sev_w = {"low": 1.0, "medium": 2.0, "high": 3.0, "critical": 4.0}.get(sev, 1.0)
            amount = float(item.get("amount_sar", 0.0))
            return sev_w * 1000.0 + amount

        worst = max(register, key=weight)
        title = worst.get("title") or worst.get("summary") or "unnamed risk"
        return str(title)

    # ── weekly snapshot ─────────────────────────────────────────
    def weekly_snapshot(
        self,
        opportunities: list[Opportunity] | None = None,
        queue: ApprovalQueue | None = None,
        proposals_drafted: int = 0,
        pilots_active: int = 0,
        cash_at_risk: Money | None = None,
        period_start: date | None = None,
        period_end: date | None = None,
        top_offer_name: str = "Revenue Hunter Pilot",
    ) -> MoneyWeeklySnapshot:
        opps = opportunities or []
        outcomes = self._outcomes
        cash_collected = Money.sar(
            sum(
                (o.value.amount for o in outcomes if o.value is not None),
                start=Decimal("0"),
            )
        )
        wins = sum(
            1
            for o in outcomes
            if o.kind == OutcomeKind.MONEY and o.value is not None and o.value.amount > 0
        )
        attempts = max(1, len(outcomes))
        win_rate = round(wins / attempts, 3)
        end = period_end or utcnow().date()
        start = period_start or end
        return MoneyWeeklySnapshot(
            cash_collected=cash_collected,
            cash_at_risk=cash_at_risk or Money.sar(0),
            open_opportunities=len(opps),
            proposals_drafted=int(proposals_drafted),
            approvals_pending=len(queue.pending()) if queue is not None else 0,
            pilots_active=int(pilots_active),
            win_rate_pct=win_rate,
            top_offer_name=top_offer_name,
            period_start=start,
            period_end=end,
        )


__all__ = [
    "MoneyDashboard",
    "MoneyWeeklySnapshot",
]
