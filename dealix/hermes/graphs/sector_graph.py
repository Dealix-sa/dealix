"""SectorGraph — verified revenue, opportunities, and risk by sector."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field


@dataclass
class SectorRow:
    sector: str
    verified_revenue_sar: float
    open_opportunities: int
    risk_events: int


@dataclass
class SectorGraph:
    rows: dict[str, SectorRow] = field(default_factory=dict)

    def add_revenue(self, sector: str, sar: float) -> None:
        row = self.rows.setdefault(sector, SectorRow(sector, 0.0, 0, 0))
        row.verified_revenue_sar += sar

    def add_opportunity(self, sector: str) -> None:
        row = self.rows.setdefault(sector, SectorRow(sector, 0.0, 0, 0))
        row.open_opportunities += 1

    def add_risk(self, sector: str) -> None:
        row = self.rows.setdefault(sector, SectorRow(sector, 0.0, 0, 0))
        row.risk_events += 1

    def ranked_by_revenue(self) -> list[SectorRow]:
        return sorted(self.rows.values(), key=lambda r: r.verified_revenue_sar, reverse=True)
