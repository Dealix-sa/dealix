"""Revenue Hunter — converts ranked cash signals into opportunities."""

from __future__ import annotations

from dealix.hermes.core.opportunities import OpportunityBook
from dealix.hermes.core.schemas import Opportunity, Signal
from dealix.hermes.core.scoring import OpportunityScorer, ScoreInputs


class RevenueHunter:
    def __init__(self, book: OpportunityBook, scorer: OpportunityScorer) -> None:
        self.book = book
        self.scorer = scorer

    def hunt(self, signal: Signal, *, owner: str = "sami") -> Opportunity:
        cash = signal.payload.get("cash") or {}
        opp = Opportunity.make(
            signal_id=signal.id,
            domain="money",
            title=f"Cash: {signal.summary[:80]}",
            owner=owner,
        )
        inputs = ScoreInputs(
            cash_speed=1.0 - min(int(cash.get("days_to_cash", 60)), 90) / 90.0,
            close_probability=float(cash.get("win_probability", 0.3)),
            deal_value_sar=float(cash.get("expected_revenue_sar", 0)),
            strategic_value=float(cash.get("strategic_value", 0.3)),
            risk=float(cash.get("risk", 0.2)),
        )
        self.scorer.score(opp, inputs)
        self.book.add(opp)
        self.book.mark_scored(opp.id)
        return opp


__all__ = ["RevenueHunter"]
