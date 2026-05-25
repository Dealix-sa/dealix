"""Revenue streams and revenue events."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class StreamType(StrEnum):
    sprint = "sprint"
    data_pack = "data_pack"
    managed_ops = "managed_ops"
    custom_ai = "custom_ai"
    partner_share = "partner_share"
    training = "training"
    report = "report"
    marketplace = "marketplace"
    api = "api"


def _now() -> str:
    return datetime.now(UTC).isoformat()


def _eid() -> str:
    return f"rev_{uuid.uuid4().hex[:16]}"


class RevenueEvent(BaseModel):
    model_config = ConfigDict(extra="forbid")

    event_id: str = Field(default_factory=_eid)
    stream: StreamType
    amount_sar: float
    customer_id: str | None = None
    invoice_id: str | None = None
    deal_id: str | None = None
    campaign_id: str | None = None
    verified: bool = False
    occurred_at: str = Field(default_factory=_now)


@dataclass
class RevenueStream:
    stream: StreamType
    events: list[RevenueEvent] = field(default_factory=list)

    def record(self, event: RevenueEvent) -> RevenueEvent:
        self.events.append(event)
        return event

    @property
    def total_sar(self) -> float:
        return sum(e.amount_sar for e in self.events)

    @property
    def verified_sar(self) -> float:
        return sum(e.amount_sar for e in self.events if e.verified)
