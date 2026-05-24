"""
Outcome store + aggregates.

Outcomes close the loop. They record what actually happened, what was
learned, and how much value (revenue, time saved, risk reduced) the
action produced.
"""

from __future__ import annotations

from uuid import uuid4

from dealix.hermes.core.schemas import HermesOutcome


class OutcomeStore:
    def __init__(self) -> None:
        self._outcomes: dict[str, HermesOutcome] = {}

    def add(self, outcome: HermesOutcome) -> str:
        oid = str(uuid4())
        self._outcomes[oid] = outcome
        return oid

    def get(self, oid: str) -> HermesOutcome | None:
        return self._outcomes.get(oid)

    def total_revenue_sar(self) -> float:
        return sum((o.revenue_sar or 0.0) for o in self._outcomes.values())

    def total_time_saved_minutes(self) -> int:
        return sum((o.time_saved_minutes or 0) for o in self._outcomes.values())

    def wins(self) -> list[tuple[str, HermesOutcome]]:
        return [(oid, o) for oid, o in self._outcomes.items() if o.status == "won"]


_default_store = OutcomeStore()


def default_store() -> OutcomeStore:
    return _default_store
