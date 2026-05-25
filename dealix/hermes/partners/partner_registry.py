"""Partner Registry — basic partner objects + status."""

from __future__ import annotations

import threading
from dataclasses import dataclass, field
from enum import StrEnum


class PartnerTier(StrEnum):
    PROSPECT = "prospect"
    ACTIVATED = "activated"
    SCALED = "scaled"
    SUNSET = "sunset"


class PartnerStatus(StrEnum):
    PENDING_REVIEW = "pending_review"
    ACTIVE = "active"
    PAUSED = "paused"
    OFFBOARDED = "offboarded"


@dataclass
class Partner:
    partner_id: str
    name: str
    contact_name: str
    contact_email: str
    sector_focus: list[str]
    offers_resold: list[str] = field(default_factory=list)
    tier: PartnerTier = PartnerTier.PROSPECT
    status: PartnerStatus = PartnerStatus.PENDING_REVIEW
    fit_score: int = 0
    notes: str | None = None


class PartnerRegistry:
    def __init__(self) -> None:
        self._partners: dict[str, Partner] = {}
        self._lock = threading.Lock()

    def register(self, partner: Partner) -> Partner:
        with self._lock:
            if partner.partner_id in self._partners:
                raise ValueError(f"partner `{partner.partner_id}` already registered")
            self._partners[partner.partner_id] = partner
        return partner

    def get(self, partner_id: str) -> Partner | None:
        with self._lock:
            return self._partners.get(partner_id)

    def active(self) -> list[Partner]:
        with self._lock:
            return [p for p in self._partners.values() if p.status == PartnerStatus.ACTIVE]


__all__ = ["Partner", "PartnerRegistry", "PartnerStatus", "PartnerTier"]
