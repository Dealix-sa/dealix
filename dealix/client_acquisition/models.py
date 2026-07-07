"""Data models for the Dealix client acquisition queue.

Standard-library only so this can run in CI without extra dependencies.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import date
from typing import Any


@dataclass(frozen=True)
class ClientCard:
    """A compact opportunity profile for one company or contact."""

    company: str
    contact: str = ""
    source: str = "manual"
    segment: str = "local_b2b"
    signal: str = ""
    likely_pain: str = ""
    offer_fit: str = "Revenue Proof Sprint"
    intent_score: int = 50
    urgency_score: int = 50
    value_score: int = 50
    trust_score: int = 50
    risk_score: int = 20
    next_action_date: str = field(default_factory=lambda: date.today().isoformat())
    notes: str = ""

    @property
    def priority_score(self) -> int:
        positive = self.intent_score + self.urgency_score + self.value_score + self.trust_score
        return max(0, min(100, round((positive / 4) - (self.risk_score * 0.25))))

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["priority_score"] = self.priority_score
        return data


@dataclass(frozen=True)
class QueueItem:
    """One ranked next action prepared for founder review."""

    client: ClientCard
    status: str
    recommended_channel: str
    local_angle: str
    next_action: str
    suggested_copy: str
    objection_to_expect: str
    proof_to_show: str
    approval_required: bool = True

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["client"] = self.client.to_dict()
        return data


@dataclass(frozen=True)
class QueueBundle:
    """Daily acquisition queue output."""

    generated_at: str
    mode: str
    items: list[QueueItem]
    safeguards: list[str]

    def to_dict(self) -> dict[str, Any]:
        return {
            "generated_at": self.generated_at,
            "mode": self.mode,
            "items": [item.to_dict() for item in self.items],
            "safeguards": list(self.safeguards),
        }
