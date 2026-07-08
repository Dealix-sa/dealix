"""Typed data model for the Autonomous Company OS. Stdlib-only."""

from __future__ import annotations

import enum
from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Any


class DealStage(str, enum.Enum):
    """Pipeline stages mapped to the real evidence chain."""

    NEW = "new"                    # lead_identified
    CONTACTED = "contacted"        # message_sent_manually (founder-confirmed)
    ENGAGED = "engaged"            # call_booked
    PROPOSED = "proposed"          # invoice_sent
    WON = "won"                    # payment_received  <- revenue recognized
    DELIVERED = "delivered"        # work_delivered
    PROOF = "proof"                # proof_pack_delivered
    REFERRAL = "referral"          # follow_up_scheduled / referral asked
    LOST = "lost"                  # terminal, no revenue


# Ordered progression (LOST is terminal and excluded from the ladder).
STAGE_ORDER: tuple[DealStage, ...] = (
    DealStage.NEW,
    DealStage.CONTACTED,
    DealStage.ENGAGED,
    DealStage.PROPOSED,
    DealStage.WON,
    DealStage.DELIVERED,
    DealStage.PROOF,
    DealStage.REFERRAL,
)

# Win-probability weighting per stage (for a conservative forecast).
STAGE_PROBABILITY: dict[DealStage, float] = {
    DealStage.NEW: 0.05,
    DealStage.CONTACTED: 0.15,
    DealStage.ENGAGED: 0.35,
    DealStage.PROPOSED: 0.60,
    DealStage.WON: 1.00,
    DealStage.DELIVERED: 1.00,
    DealStage.PROOF: 1.00,
    DealStage.REFERRAL: 1.00,
    DealStage.LOST: 0.00,
}

# Days a deal may sit in a stage before it is flagged as stalled.
STAGE_STALE_DAYS: dict[DealStage, int] = {
    DealStage.NEW: 2,
    DealStage.CONTACTED: 3,
    DealStage.ENGAGED: 4,
    DealStage.PROPOSED: 5,
    DealStage.WON: 7,
    DealStage.DELIVERED: 7,
    DealStage.PROOF: 14,
    DealStage.REFERRAL: 30,
}

# The single evidence event that recognizes revenue.
REVENUE_EVENT = "payment_received"


@dataclass
class DealEvent:
    event: str
    at: str  # ISO date
    detail: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {"event": self.event, "at": self.at, "detail": self.detail}

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "DealEvent":
        return cls(event=str(d.get("event", "")), at=str(d.get("at", "")), detail=str(d.get("detail", "")))


@dataclass
class Deal:
    id: str
    account_name: str
    sector: str = ""
    source: str = ""
    offer: str = "Revenue Proof Sprint"
    value_sar: int = 499
    stage: DealStage = DealStage.NEW
    created_at: str = ""
    last_touch_at: str = ""
    contact_hint: str = ""     # founder-owned channel note (no scraping)
    opted_in: bool = False     # only warm/opted-in contacts are actioned
    notes: str = ""
    events: list[DealEvent] = field(default_factory=list)

    # ---- derived / runtime (not persisted authoritatively) ----
    score: float = 0.0
    next_action: str = ""
    stalled: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "account_name": self.account_name,
            "sector": self.sector,
            "source": self.source,
            "offer": self.offer,
            "value_sar": self.value_sar,
            "stage": self.stage.value,
            "created_at": self.created_at,
            "last_touch_at": self.last_touch_at,
            "contact_hint": self.contact_hint,
            "opted_in": self.opted_in,
            "notes": self.notes,
            "events": [e.to_dict() for e in self.events],
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "Deal":
        try:
            stage = DealStage(str(d.get("stage", "new")))
        except ValueError:
            stage = DealStage.NEW
        return cls(
            id=str(d.get("id", "")),
            account_name=str(d.get("account_name", "")),
            sector=str(d.get("sector", "")),
            source=str(d.get("source", "")),
            offer=str(d.get("offer", "Revenue Proof Sprint")),
            value_sar=int(d.get("value_sar", 499) or 0),
            stage=stage,
            created_at=str(d.get("created_at", "")),
            last_touch_at=str(d.get("last_touch_at", "")),
            contact_hint=str(d.get("contact_hint", "")),
            opted_in=bool(d.get("opted_in", False)),
            notes=str(d.get("notes", "")),
            events=[DealEvent.from_dict(e) for e in d.get("events", []) or []],
        )

    def has_event(self, event: str) -> bool:
        return any(e.event == event for e in self.events)

    def days_since_touch(self, today: date) -> int:
        ref = self.last_touch_at or self.created_at
        if not ref:
            return 0
        try:
            then = datetime.fromisoformat(ref).date()
        except ValueError:
            return 0
        return max(0, (today - then).days)


@dataclass
class KPIs:
    total_deals: int = 0
    active_deals: int = 0
    won_deals: int = 0
    lost_deals: int = 0
    stalled_deals: int = 0
    recognized_revenue_sar: int = 0
    weighted_pipeline_sar: float = 0.0
    open_pipeline_sar: int = 0
    win_rate: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        return {
            "total_deals": self.total_deals,
            "active_deals": self.active_deals,
            "won_deals": self.won_deals,
            "lost_deals": self.lost_deals,
            "stalled_deals": self.stalled_deals,
            "recognized_revenue_sar": self.recognized_revenue_sar,
            "weighted_pipeline_sar": round(self.weighted_pipeline_sar, 2),
            "open_pipeline_sar": self.open_pipeline_sar,
            "win_rate": round(self.win_rate, 3),
        }
