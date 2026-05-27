"""Single deal room — one per active opportunity."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum


class DealStage(str, Enum):
    QUALIFY = "qualify"
    PILOT = "pilot"
    PROPOSAL = "proposal"
    NEGOTIATION = "negotiation"
    CLOSED_WON = "closed_won"
    CLOSED_LOST = "closed_lost"


@dataclass
class DealRoom:
    opportunity_id: str
    customer: str
    stage: DealStage = DealStage.QUALIFY
    notes: list[str] = field(default_factory=list)
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def advance(self, stage: DealStage, *, note: str = "") -> None:
        self.stage = stage
        if note:
            self.notes.append(note)
        self.updated_at = datetime.now(timezone.utc)


__all__ = ["DealRoom", "DealStage"]
