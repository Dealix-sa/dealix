"""
OutcomeGate — refuses to close a request unless the executor recorded
an Outcome. This is the platform-level enforcement of the "measure
everything" rule: without an Outcome, no learning, no attribution, no
revenue assurance.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any


class OutcomeStatus(StrEnum):
    PENDING = "pending"
    SUCCESS = "success"
    FAILURE = "failure"
    CANCELLED = "cancelled"


@dataclass
class Outcome:
    request_id: str
    status: OutcomeStatus
    artifacts: tuple[str, ...] = field(default_factory=tuple)
    metrics: dict[str, float] = field(default_factory=dict)
    notes: str = ""
    recorded_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def to_dict(self) -> dict[str, Any]:
        return {
            "request_id": self.request_id,
            "status": self.status.value,
            "artifacts": list(self.artifacts),
            "metrics": dict(self.metrics),
            "notes": self.notes,
            "recorded_at": self.recorded_at.isoformat(),
        }


class OutcomeRegistry:
    def __init__(self) -> None:
        self._by_request: dict[str, Outcome] = {}

    def record(self, outcome: Outcome) -> None:
        self._by_request[outcome.request_id] = outcome

    def get(self, request_id: str) -> Outcome | None:
        return self._by_request.get(request_id)

    def __len__(self) -> int:
        return len(self._by_request)


REGISTRY = OutcomeRegistry()


def require(request_id: str) -> Outcome:
    """Return the recorded outcome or raise."""
    outcome = REGISTRY.get(request_id)
    if outcome is None:
        raise RuntimeError(
            f"OutcomeGate: request {request_id!r} closed without an Outcome. "
            "Every executed request must record an Outcome."
        )
    return outcome
