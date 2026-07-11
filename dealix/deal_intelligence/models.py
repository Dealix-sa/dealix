"""Typed, evidence-aware deal intelligence models.

This package contains no sender, scheduler, payment capture, or production code.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import StrEnum
from typing import Any

from dealix.client_acquisition.models import CONTACTABLE_SOURCES


class DealStage(StrEnum):
    RESEARCH_HOLD = "research_hold"
    NEW = "new"
    CONTACTED = "contacted"
    ENGAGED = "engaged"
    PROPOSED = "proposed"
    PAID = "paid"
    PROOF_DELIVERED = "proof_delivered"
    REFERRAL = "referral"
    LOST = "lost"


@dataclass(frozen=True)
class DealEvent:
    event_type: str
    occurred_at: str
    detail: str = ""

    def __post_init__(self) -> None:
        event_type = self.event_type.strip().casefold()
        occurred_at = self.occurred_at.strip()
        if not event_type:
            raise ValueError("event_type is required")
        if not occurred_at:
            raise ValueError("occurred_at is required")
        object.__setattr__(self, "event_type", event_type)
        object.__setattr__(self, "occurred_at", occurred_at)

    def to_dict(self) -> dict[str, str]:
        return asdict(self)

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "DealEvent":
        if not isinstance(payload, dict):
            raise TypeError("deal event must be an object")
        return cls(
            event_type=str(payload.get("event_type") or payload.get("event") or ""),
            occurred_at=str(payload.get("occurred_at") or payload.get("at") or ""),
            detail=str(payload.get("detail") or ""),
        )


@dataclass(frozen=True)
class DealRecord:
    deal_id: str
    account_name: str
    source: str
    offer_name: str = "Revenue Proof Sprint"
    value_sar: int = 499
    created_at: str = ""
    last_touch_at: str = ""
    owner: str = "founder"
    notes: str = ""
    events: tuple[DealEvent, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        deal_id = self.deal_id.strip()
        account_name = self.account_name.strip()
        source = self.source.strip().casefold()
        if not deal_id:
            raise ValueError("deal_id is required")
        if not account_name:
            raise ValueError("account_name is required")
        if isinstance(self.value_sar, bool) or not isinstance(self.value_sar, int):
            raise TypeError("value_sar must be an integer")
        if self.value_sar < 0:
            raise ValueError("value_sar must be non-negative")
        if any(not isinstance(event, DealEvent) for event in self.events):
            raise TypeError("events must contain DealEvent objects")
        object.__setattr__(self, "deal_id", deal_id)
        object.__setattr__(self, "account_name", account_name)
        object.__setattr__(self, "source", source)
        object.__setattr__(self, "events", tuple(self.events))

    @property
    def contact_permission_confirmed(self) -> bool:
        return self.source in CONTACTABLE_SOURCES

    def to_dict(self) -> dict[str, Any]:
        return {
            "deal_id": self.deal_id,
            "account_name": self.account_name,
            "source": self.source,
            "offer_name": self.offer_name,
            "value_sar": self.value_sar,
            "created_at": self.created_at,
            "last_touch_at": self.last_touch_at,
            "owner": self.owner,
            "notes": self.notes,
            "events": [event.to_dict() for event in self.events],
        }

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "DealRecord":
        if not isinstance(payload, dict):
            raise TypeError("deal record must be an object")
        raw_events = payload.get("events") or []
        if not isinstance(raw_events, list):
            raise ValueError("events must be a list")
        if any(not isinstance(item, dict) for item in raw_events):
            raise ValueError("events must contain objects only")
        raw_value = payload.get("value_sar", 499)
        if isinstance(raw_value, bool):
            raise TypeError("value_sar must not be boolean")
        try:
            value_sar = int(raw_value)
        except (TypeError, ValueError) as exc:
            raise TypeError("value_sar must be an integer") from exc
        return cls(
            deal_id=str(payload.get("deal_id") or payload.get("id") or ""),
            account_name=str(payload.get("account_name") or ""),
            source=str(payload.get("source") or "unknown"),
            offer_name=str(payload.get("offer_name") or payload.get("offer") or "Revenue Proof Sprint"),
            value_sar=value_sar,
            created_at=str(payload.get("created_at") or ""),
            last_touch_at=str(payload.get("last_touch_at") or ""),
            owner=str(payload.get("owner") or "founder"),
            notes=str(payload.get("notes") or ""),
            events=tuple(DealEvent.from_dict(item) for item in raw_events),
        )


@dataclass(frozen=True)
class DealSnapshot:
    deal_id: str
    account_name: str
    stage: DealStage
    value_sar: int
    contact_permission_confirmed: bool
    valid_payment: bool
    proof_delivered: bool
    close_ready: bool
    stalled: bool
    days_since_touch: int
    forecast_probability: float
    anomalies: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["stage"] = self.stage.value
        payload["anomalies"] = list(self.anomalies)
        return payload


@dataclass(frozen=True)
class NextAction:
    deal_id: str
    action_key: str
    rationale: str
    requires_approval: bool
    external_action_allowed: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class PortfolioMetrics:
    total_deals: int
    active_deals: int
    lost_deals: int
    stalled_deals: int
    recognized_revenue_sar: int
    open_pipeline_sar: int
    weighted_pipeline_sar: float
    anomaly_count: int

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["weighted_pipeline_sar"] = round(self.weighted_pipeline_sar, 2)
        return payload
