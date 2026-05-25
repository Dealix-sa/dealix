"""Partner candidate scouting."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum

from pydantic import BaseModel, ConfigDict


class PartnerType(StrEnum):
    referral = "referral"
    white_label = "white_label"
    implementation = "implementation"
    training = "training"
    data = "data"
    strategic = "strategic"
    channel = "channel"


class PartnerCandidate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    candidate_id: str
    name: str
    partner_type: PartnerType
    sector: str
    notes: str = ""


@dataclass
class PartnerScout:
    _candidates: dict[str, PartnerCandidate] = field(default_factory=dict)

    def add(self, candidate: PartnerCandidate) -> PartnerCandidate:
        self._candidates[candidate.candidate_id] = candidate
        return candidate

    def list(self) -> list[PartnerCandidate]:
        return list(self._candidates.values())
