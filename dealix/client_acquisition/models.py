"""Canonical data models for Dealix's internal client-acquisition queue.

The package is intentionally standard-library only, draft-only, and contains no
network or sender code.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import date
from typing import Any

_SCORE_FIELDS = (
    "intent_score",
    "urgency_score",
    "value_score",
    "trust_score",
    "risk_score",
)

CONTACTABLE_SOURCES = frozenset(
    {
        "manual_approved",
        "warm",
        "inbound",
        "referral",
        "existing_permission",
        "opt_in",
        "customer_request",
    }
)
RESEARCH_ONLY_SOURCES = frozenset(
    {
        "manual_research",
        "public_web_research",
        "seed",
        "unknown",
    }
)
ALLOWED_SOURCES = CONTACTABLE_SOURCES | RESEARCH_ONLY_SOURCES


@dataclass(frozen=True)
class ClientCard:
    """Evidence-aware profile for one warm, inbound, referral, or research target."""

    company: str
    contact: str = ""
    source: str = "manual_approved"
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

    def __post_init__(self) -> None:
        company = self.company.strip()
        source = self.source.strip().casefold()
        if not company:
            raise ValueError("company is required")
        if source not in ALLOWED_SOURCES:
            allowed = ", ".join(sorted(ALLOWED_SOURCES))
            raise ValueError(f"source must be one of: {allowed}")
        object.__setattr__(self, "company", company)
        object.__setattr__(self, "source", source)
        for field_name in _SCORE_FIELDS:
            value = getattr(self, field_name)
            if isinstance(value, bool) or not isinstance(value, int):
                raise TypeError(f"{field_name} must be an integer")
            if not 0 <= value <= 100:
                raise ValueError(f"{field_name} must be between 0 and 100")

    @property
    def contact_permission_confirmed(self) -> bool:
        """Return whether the recorded source permits preparing outreach for review."""

        return self.source in CONTACTABLE_SOURCES

    @property
    def priority_score(self) -> int:
        positive = (
            self.intent_score * 0.30
            + self.urgency_score * 0.25
            + self.value_score * 0.25
            + self.trust_score * 0.20
        )
        return max(0, min(100, round(positive - self.risk_score * 0.25)))

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["contact_permission_confirmed"] = self.contact_permission_confirmed
        payload["priority_score"] = self.priority_score
        return payload


@dataclass(frozen=True)
class QueueItem:
    """One ranked next action prepared for founder review."""

    client: ClientCard
    status: str
    priority_reason: str
    recommended_channel: str
    local_angle: str
    next_action: str
    suggested_copy: str
    objection_to_expect: str
    proof_to_show: str
    approval_required: bool = True
    external_action_allowed: bool = False

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["client"] = self.client.to_dict()
        return payload


@dataclass(frozen=True)
class QueueBundle:
    """Draft-only acquisition queue output."""

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
