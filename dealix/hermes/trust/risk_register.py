"""Risk register — track open risks, treatments, and owners."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class RiskState(StrEnum):
    open = "open"
    mitigated = "mitigated"
    accepted = "accepted"
    closed = "closed"


def _rid() -> str:
    return f"rsk_{uuid.uuid4().hex[:16]}"


def _now() -> str:
    return datetime.now(UTC).isoformat()


class Risk(BaseModel):
    model_config = ConfigDict(extra="forbid")

    risk_id: str = Field(default_factory=_rid)
    title: str
    description: str = ""
    owner: str = "Sami"
    severity: int = Field(default=3, ge=1, le=5)
    likelihood: int = Field(default=3, ge=1, le=5)
    state: RiskState = RiskState.open
    treatment_plan: str = ""
    created_at: str = Field(default_factory=_now)
    updated_at: str = Field(default_factory=_now)

    @property
    def score(self) -> int:
        return self.severity * self.likelihood


@dataclass
class RiskRegister:
    _risks: dict[str, Risk] = field(default_factory=dict)

    def add(self, risk: Risk) -> Risk:
        self._risks[risk.risk_id] = risk
        return risk

    def update(self, risk_id: str, **fields_to_update: object) -> Risk:
        r = self._risks[risk_id]
        updated = r.model_copy(update={**fields_to_update, "updated_at": _now()})
        self._risks[risk_id] = updated
        return updated

    def get(self, risk_id: str) -> Risk:
        return self._risks[risk_id]

    def open_risks(self) -> list[Risk]:
        return sorted(
            (r for r in self._risks.values() if r.state == RiskState.open),
            key=lambda r: r.score,
            reverse=True,
        )

    def all(self) -> list[Risk]:
        return list(self._risks.values())
