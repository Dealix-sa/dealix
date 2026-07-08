"""Typed records for the draft-only Opportunity Graph."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(slots=True)
class CompanyRecord:
    id: str
    name: str
    sector: str
    country: str = "Saudi Arabia"
    city: str = "Riyadh"
    source: str = "seed"
    source_url: str = ""
    confidence: float = 0.5

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class SignalRecord:
    id: str
    company_id: str
    signal_type: str
    description: str
    confidence: float
    source_url: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class OpportunityRecord:
    id: str
    company_id: str
    company_name: str
    vertical: str
    offer_match: str
    reason: str
    score: int
    risk: str = "low"
    channel: str = "email_or_linkedin_manual"
    next_action: str = "draft_message_for_approval"
    evidence: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
