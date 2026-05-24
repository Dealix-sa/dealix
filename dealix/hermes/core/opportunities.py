"""
Opportunity store + helpers.

Holds opportunities derived from signals. Pairs with ``scoring`` to rank
the backlog and surface what to execute next.
"""

from __future__ import annotations

from uuid import uuid4

from dealix.hermes.core.schemas import HermesOpportunity
from dealix.hermes.core.scoring import opportunity_score, should_execute_now


class OpportunityStore:
    def __init__(self) -> None:
        self._opportunities: dict[str, HermesOpportunity] = {}

    def add(self, opportunity: HermesOpportunity) -> str:
        oid = str(uuid4())
        self._opportunities[oid] = opportunity
        return oid

    def get(self, oid: str) -> HermesOpportunity | None:
        return self._opportunities.get(oid)

    def list_all(self) -> list[tuple[str, HermesOpportunity]]:
        return list(self._opportunities.items())

    def ranked(self) -> list[tuple[str, HermesOpportunity, float]]:
        scored = [(oid, o, opportunity_score(o)) for oid, o in self._opportunities.items()]
        scored.sort(key=lambda row: row[2], reverse=True)
        return scored

    def executable_now(self) -> list[tuple[str, HermesOpportunity]]:
        return [(oid, o) for oid, o in self._opportunities.items() if should_execute_now(o)]


_default_store = OpportunityStore()


def default_store() -> OpportunityStore:
    return _default_store
