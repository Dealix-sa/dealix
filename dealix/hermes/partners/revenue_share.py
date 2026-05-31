"""Revenue share calculation."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class RevenueShare(BaseModel):
    model_config = ConfigDict(extra="forbid")

    partner_id: str
    deal_id: str
    base_amount_sar: float = Field(ge=0)
    share_pct: float = Field(ge=0.0, le=1.0)


def share_amount_sar(share: RevenueShare) -> float:
    return round(share.base_amount_sar * share.share_pct, 2)
