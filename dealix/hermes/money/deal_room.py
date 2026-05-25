"""Per-deal context room."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class DealStage(StrEnum):
    discovery = "discovery"
    qualified = "qualified"
    proposed = "proposed"
    negotiation = "negotiation"
    won = "won"
    lost = "lost"


class DealRoom(BaseModel):
    model_config = ConfigDict(extra="forbid")

    deal_id: str
    customer_id: str
    stage: DealStage = DealStage.discovery
    estimated_value_sar: float = 0.0
    primary_offer_id: str | None = None
    next_action: str = ""
    last_touch_at: str | None = None
    risks: list[str] = Field(default_factory=list)
    evidence_pack_id: str | None = None


@dataclass
class DealRoomStore:
    _rooms: dict[str, DealRoom] = field(default_factory=dict)

    def upsert(self, room: DealRoom) -> DealRoom:
        self._rooms[room.deal_id] = room
        return room

    def advance(self, deal_id: str, stage: DealStage) -> DealRoom:
        r = self._rooms[deal_id]
        updated = r.model_copy(update={"stage": stage})
        self._rooms[deal_id] = updated
        return updated

    def get(self, deal_id: str) -> DealRoom:
        return self._rooms[deal_id]

    def list(self) -> list[DealRoom]:
        return list(self._rooms.values())
