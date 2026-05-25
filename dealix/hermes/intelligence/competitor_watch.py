"""Competitor watch."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from pydantic import BaseModel, ConfigDict, Field


class CompetitorMove(BaseModel):
    model_config = ConfigDict(extra="forbid")

    competitor: str
    move: str
    observed_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())
    impact_score: int = Field(default=1, ge=1, le=5)


@dataclass
class CompetitorWatch:
    _moves: list[CompetitorMove] = field(default_factory=list)

    def log(self, move: CompetitorMove) -> CompetitorMove:
        self._moves.append(move)
        return move

    def recent(self, limit: int = 25) -> list[CompetitorMove]:
        return self._moves[-limit:]
