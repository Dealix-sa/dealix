"""Pricing intelligence — bands and recommendations."""

from __future__ import annotations

from dataclasses import dataclass, field

from pydantic import BaseModel, ConfigDict


class PricingBand(BaseModel):
    model_config = ConfigDict(extra="forbid")

    offer_id: str
    floor_sar: float
    target_sar: float
    ceiling_sar: float


@dataclass
class PricingIntelligence:
    _bands: dict[str, PricingBand] = field(default_factory=dict)

    def set_band(self, band: PricingBand) -> PricingBand:
        self._bands[band.offer_id] = band
        return band

    def get_band(self, offer_id: str) -> PricingBand | None:
        return self._bands.get(offer_id)

    def is_within_band(self, offer_id: str, proposed_sar: float) -> bool:
        b = self._bands.get(offer_id)
        if b is None:
            return False
        return b.floor_sar <= proposed_sar <= b.ceiling_sar
