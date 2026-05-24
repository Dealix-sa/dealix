"""Cash Scout — ranks live opportunities by their realisable cash potential.

Given the opportunity graph + outstanding proposals + collection delays,
the scout answers one question every morning: "what is the single fastest
path to cash this week?"
"""

from __future__ import annotations

from dataclasses import dataclass

from dealix.hermes.core.opportunities import OpportunityGraph
from dealix.hermes.core.schemas import Opportunity, OpportunityKind
from dealix.hermes.core.scoring import revenue_priority


@dataclass(slots=True)
class CashAction:
    opportunity_id: str
    title: str
    kind: OpportunityKind
    expected_value_sar: float
    priority: float
    days_to_close: float
    next_action: str


class CashScout:
    def __init__(self, graph: OpportunityGraph) -> None:
        self._graph = graph

    def fastest_cash(self, *, top_n: int = 5, delivery_capacity: float = 0.8) -> list[CashAction]:
        items: list[CashAction] = []
        for opp in self._graph.all():
            days = self._estimate_days(opp)
            priority = revenue_priority(
                expected_value_sar=opp.expected_value_sar,
                days_to_close=days,
                delivery_capacity=delivery_capacity,
            )
            if priority <= 0:
                continue
            items.append(
                CashAction(
                    opportunity_id=opp.opportunity_id,
                    title=opp.title,
                    kind=opp.kind,
                    expected_value_sar=opp.expected_value_sar,
                    priority=priority,
                    days_to_close=days,
                    next_action=self._next_action(opp),
                )
            )
        items.sort(key=lambda x: x.priority, reverse=True)
        return items[:top_n]

    @staticmethod
    def _estimate_days(opp: Opportunity) -> float:
        # Heuristic: more direct + higher close prob → fewer days.
        if opp.kind in {OpportunityKind.DIRECT_DEAL, OpportunityKind.TRAINING}:
            base = 7.0
        elif opp.kind in {OpportunityKind.PARTNERSHIP, OpportunityKind.PMO}:
            base = 21.0
        elif opp.kind in {OpportunityKind.TENDER, OpportunityKind.ACQUISITION}:
            base = 60.0
        else:
            base = 14.0
        return base * (1.6 - opp.close_probability)

    @staticmethod
    def _next_action(opp: Opportunity) -> str:
        if opp.close_probability >= 0.7:
            return "Send proposal & schedule call"
        if opp.close_probability >= 0.4:
            return "Qualify pain & confirm budget"
        return "Discovery message draft (no send without approval)"


__all__ = ["CashScout", "CashAction"]
