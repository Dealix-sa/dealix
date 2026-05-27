"""PricingPolicy — sovereign-owned pricing bands.

Price changes are S3 (sovereign memo). The policy object is the *only*
place the kernel reads pricing from; agents must never invent numbers.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass(frozen=True)
class PriceBand:
    name: str               # "pilot" | "managed_ops" | "custom_ai"
    min_sar: float
    max_sar: float
    list_sar: float

    def contains(self, amount_sar: float) -> bool:
        return self.min_sar <= amount_sar <= self.max_sar


@dataclass
class PricingPolicy:
    bands: dict[str, PriceBand] = field(default_factory=dict)
    last_changed_at: datetime | None = None
    last_changed_by: str | None = None
    sovereign_author: str = "sami"

    def set_band(self, band: PriceBand, *, by: str) -> None:
        if by != self.sovereign_author:
            raise PermissionError(f"Only '{self.sovereign_author}' may change pricing (S3).")
        self.bands[band.name] = band
        self.last_changed_at = datetime.now(timezone.utc)
        self.last_changed_by = by

    def get(self, band_name: str) -> PriceBand:
        return self.bands[band_name]

    def validate(self, band_name: str, amount_sar: float) -> bool:
        return self.bands[band_name].contains(amount_sar)


__all__ = ["PricingPolicy", "PriceBand"]
