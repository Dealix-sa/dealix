"""Partner scouting — register candidates with a type and a contact."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from enum import Enum


class PartnerType(str, Enum):
    REFERRAL = "referral"
    WHITE_LABEL = "white_label"
    IMPLEMENTATION = "implementation"
    TRAINING = "training"
    DATA = "data"
    STRATEGIC = "strategic"
    CHANNEL = "channel"


@dataclass
class Partner:
    id: str
    name: str
    type: PartnerType
    sector: str
    contact: str
    enabled: bool = True


@dataclass
class PartnerScout:
    _by_id: dict[str, Partner] = field(default_factory=dict)

    def add(self, *, name: str, type: PartnerType, sector: str, contact: str) -> Partner:
        p = Partner(
            id=f"prt_{uuid.uuid4().hex[:10]}",
            name=name,
            type=type,
            sector=sector,
            contact=contact,
        )
        self._by_id[p.id] = p
        return p

    def disable(self, partner_id: str) -> None:
        self._by_id[partner_id].enabled = False

    def all(self) -> list[Partner]:
        return list(self._by_id.values())

    def get(self, partner_id: str) -> Partner:
        return self._by_id[partner_id]


__all__ = ["Partner", "PartnerScout", "PartnerType"]
