"""Packaging — bundle offers into named SKUs."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class OfferPackage(BaseModel):
    model_config = ConfigDict(extra="forbid")

    package_id: str
    name: str
    offer_ids: list[str] = Field(default_factory=list)
    bundle_discount_pct: float = Field(default=0.0, ge=0.0, le=0.5)
