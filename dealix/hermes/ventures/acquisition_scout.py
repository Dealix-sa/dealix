"""Acquisition candidate scouting."""

from __future__ import annotations

from dataclasses import dataclass, field

from pydantic import BaseModel, ConfigDict, Field


class AcquisitionCandidate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    candidate_id: str
    name: str
    sector: str
    rationale: str
    estimated_value_sar: float = 0.0
    risk_notes: list[str] = Field(default_factory=list)


@dataclass
class AcquisitionScout:
    _candidates: dict[str, AcquisitionCandidate] = field(default_factory=dict)

    def add(self, candidate: AcquisitionCandidate) -> AcquisitionCandidate:
        self._candidates[candidate.candidate_id] = candidate
        return candidate

    def list(self) -> list[AcquisitionCandidate]:
        return list(self._candidates.values())
