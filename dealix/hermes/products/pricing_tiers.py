"""Pricing tiers — every offer can have multiple tiers."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class PricingTier(BaseModel):
    model_config = ConfigDict(extra="forbid")

    tier_id: str
    offer_id: str
    name: str
    price_sar: float = Field(ge=0)
    inclusions: list[str] = Field(default_factory=list)
