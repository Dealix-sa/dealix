"""PartnerMetrics — per-partner performance snapshot."""

from __future__ import annotations

from datetime import UTC, datetime

from pydantic import BaseModel, ConfigDict, Field


def _utcnow() -> datetime:
    return datetime.now(UTC)


class PartnerMetrics(BaseModel):
    model_config = ConfigDict(extra="forbid")

    partner_id: str = Field(..., min_length=1)
    partner_label: str = Field(..., min_length=1)
    stage: str
    sourced_leads: int = Field(default=0, ge=0)
    qualified_leads: int = Field(default=0, ge=0)
    deals_closed: int = Field(default=0, ge=0)
    real_revenue_usd: float = Field(default=0.0, ge=0.0)
    retainer_revenue_usd: float = Field(default=0.0, ge=0.0)
    last_activity_at: datetime = Field(default_factory=_utcnow)

    def conversion_rate(self) -> float:
        if self.sourced_leads <= 0:
            return 0.0
        return round(self.deals_closed / self.sourced_leads, 4)


__all__ = ["PartnerMetrics"]
