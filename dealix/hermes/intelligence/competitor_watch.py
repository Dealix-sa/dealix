"""CompetitorWatch — logs moves by competitors."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class CompetitorMove:
    id: str
    competitor: str
    move: str       # "launched_X" | "priced_Y" | "hired_Z" | ...
    detail: str
    observed_at: datetime


@dataclass
class CompetitorWatch:
    _moves: list[CompetitorMove] = field(default_factory=list)

    def log(self, *, competitor: str, move: str, detail: str = "") -> CompetitorMove:
        m = CompetitorMove(
            id=f"cmp_{uuid.uuid4().hex[:10]}",
            competitor=competitor,
            move=move,
            detail=detail,
            observed_at=datetime.now(timezone.utc),
        )
        self._moves.append(m)
        return m

    def recent(self, n: int = 20) -> list[CompetitorMove]:
        return list(self._moves[-n:])


__all__ = ["CompetitorMove", "CompetitorWatch"]
