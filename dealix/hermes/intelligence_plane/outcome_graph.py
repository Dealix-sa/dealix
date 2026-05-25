"""
Outcome Graph — كل تنفيذ يجب أن يُغلق بـ outcome (CTRL-OPS-001).
الـ runtime يتوقع outcome خلال نافذة زمنية، وإلا يُرفع في `learning_engine`
كـ "execution without outcome".
"""

from __future__ import annotations

import threading
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import StrEnum
from typing import Any


class OutcomeKind(StrEnum):
    REPLY_RECEIVED = "reply_received"
    CALL_BOOKED = "call_booked"
    PROPOSAL_SENT = "proposal_sent"
    PROPOSAL_WON = "proposal_won"
    PROPOSAL_LOST = "proposal_lost"
    NO_RESPONSE = "no_response"
    CHURNED = "churned"
    RETAINED = "retained"
    PILOT_STARTED = "pilot_started"
    PAYMENT_RECEIVED = "payment_received"
    INCIDENT = "incident"


@dataclass
class Outcome:
    outcome_id: str
    execution_id: str  # links to hermes_executions
    kind: OutcomeKind
    value_sar: int = 0
    notes: str = ""
    recorded_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: dict[str, Any] = field(default_factory=dict)


class OutcomeGraph:
    def __init__(self) -> None:
        self._outcomes: dict[str, Outcome] = {}
        self._by_execution: dict[str, list[str]] = defaultdict(list)
        self._lock = threading.Lock()

    def record(self, outcome: Outcome) -> Outcome:
        with self._lock:
            self._outcomes[outcome.outcome_id] = outcome
            self._by_execution[outcome.execution_id].append(outcome.outcome_id)
            return outcome

    def for_execution(self, execution_id: str) -> list[Outcome]:
        with self._lock:
            return [
                self._outcomes[oid]
                for oid in self._by_execution.get(execution_id, [])
            ]

    def win_loss_by_offer(self, offer_lookup: dict[str, str]) -> dict[str, dict[str, int]]:
        """Aggregate wins/losses bucketed by offer id (provided externally)."""
        with self._lock:
            stats: dict[str, dict[str, int]] = defaultdict(
                lambda: {"won": 0, "lost": 0}
            )
            for o in self._outcomes.values():
                offer = offer_lookup.get(o.execution_id)
                if not offer:
                    continue
                if o.kind == OutcomeKind.PROPOSAL_WON:
                    stats[offer]["won"] += 1
                elif o.kind == OutcomeKind.PROPOSAL_LOST:
                    stats[offer]["lost"] += 1
            return {k: dict(v) for k, v in stats.items()}


__all__ = ["Outcome", "OutcomeGraph", "OutcomeKind"]
