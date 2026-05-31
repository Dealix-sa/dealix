"""AttributionRecord — links a revenue record to its touchpoints."""

from __future__ import annotations

from datetime import UTC, datetime

from pydantic import BaseModel, ConfigDict, Field

from dealix.growth_os.attribution.types import AttributionType


def _utcnow() -> datetime:
    return datetime.now(UTC)


class AttributionRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    record_id: str = Field(..., min_length=1)
    revenue_record_id: str = Field(..., min_length=1)
    attribution_type: AttributionType
    weight: float = Field(default=1.0, ge=0.0, le=1.0)
    channel: str = ""
    offer_key: str = ""
    campaign_key: str = ""
    asset_key: str = ""
    agent_key: str = ""
    partner_key: str = ""
    occurred_at: datetime = Field(default_factory=_utcnow)


__all__ = ["AttributionRecord"]
