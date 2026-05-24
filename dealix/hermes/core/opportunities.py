"""OpportunityBook — the queue of scored hypotheses.

Every opportunity points back at the signal that birthed it (lineage).
Every opportunity must be scored before it can be 'queued' for decision.
"""

from __future__ import annotations

from dealix.hermes.core.schemas import Opportunity, OpportunityStatus


class OpportunityBook:
    def __init__(self) -> None:
        self._by_id: dict[str, Opportunity] = {}

    def add(self, opp: Opportunity) -> Opportunity:
        if opp.id in self._by_id:
            raise ValueError(f"Duplicate opportunity id: {opp.id}")
        self._by_id[opp.id] = opp
        return opp

    def get(self, opportunity_id: str) -> Opportunity:
        return self._by_id[opportunity_id]

    def mark_scored(self, opportunity_id: str) -> Opportunity:
        opp = self._by_id[opportunity_id]
        if opp.score is None:
            raise ValueError(f"Opportunity {opportunity_id} has no score yet.")
        opp.status = OpportunityStatus.SCORED
        opp.touch()
        return opp

    def queue(self, opportunity_id: str) -> Opportunity:
        opp = self._by_id[opportunity_id]
        if opp.status != OpportunityStatus.SCORED:
            raise ValueError("Only SCORED opportunities can be queued.")
        opp.status = OpportunityStatus.QUEUED
        opp.touch()
        return opp

    def mark_decided(self, opportunity_id: str) -> Opportunity:
        opp = self._by_id[opportunity_id]
        opp.status = OpportunityStatus.DECIDED
        opp.touch()
        return opp

    def drop(self, opportunity_id: str, *, reason: str) -> Opportunity:
        opp = self._by_id[opportunity_id]
        opp.status = OpportunityStatus.DROPPED
        opp.payload.setdefault("drop_reason", reason)
        opp.touch()
        return opp

    def all(self) -> list[Opportunity]:
        return list(self._by_id.values())

    def by_status(self, status: OpportunityStatus) -> list[Opportunity]:
        return [o for o in self._by_id.values() if o.status == status]

    def top_n(self, n: int) -> list[Opportunity]:
        scored = [o for o in self._by_id.values() if o.score is not None]
        return sorted(scored, key=lambda o: (o.score or 0.0), reverse=True)[:n]

    def unscored(self) -> list[Opportunity]:
        return [o for o in self._by_id.values() if o.score is None]


__all__ = ["OpportunityBook"]
