"""Sector Radar — vertical-by-vertical opportunity surface."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class SectorView:
    sector: str
    opportunity_count: int
    average_value_sar: float
    top_offer: str


class SectorRadar:
    def view(self, sector: str, opportunities: list[dict]) -> SectorView:
        matches = [o for o in opportunities if (o.get("sector") or "").lower() == sector.lower()]
        if not matches:
            return SectorView(sector, 0, 0.0, "No fit yet")
        avg_value = sum(o.get("estimated_value_sar", 0.0) for o in matches) / max(len(matches), 1)
        top_offer = max(matches, key=lambda o: o.get("score", 0.0)).get("title", "Generic offer")
        return SectorView(sector, len(matches), round(avg_value, 2), top_offer)
