"""Per-partner performance summary."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PartnerPerformance:
    partner_id: str
    deals_in_flight: int
    deals_won: int
    revenue_attributed_sar: float
    last_activity_at: str | None

    @property
    def win_rate(self) -> float:
        total = self.deals_in_flight + self.deals_won
        return round(self.deals_won / total, 4) if total else 0.0
