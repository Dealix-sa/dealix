"""خادم الذكاء — ReportBuilder.

Aggregates market signals + sector snapshots into a Report.
"""

from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field

from dealix.hermes.core.schemas import utcnow
from dealix.intelligence.market_radar import MarketSignal
from dealix.intelligence.sector_radar import SectorSnapshot


def _new_report_id() -> str:
    return f"rep_{uuid4().hex[:12]}"


class Report(BaseModel):
    """An intelligence digest combining market + sector data."""

    model_config = ConfigDict(extra="forbid")

    report_id: str = Field(default_factory=_new_report_id)
    title: str = Field(..., min_length=1, max_length=200)
    market_signals: list[MarketSignal] = Field(default_factory=list)
    sector_snapshots: list[SectorSnapshot] = Field(default_factory=list)
    headline_findings: list[str] = Field(default_factory=list, max_length=10)
    created_at: datetime = Field(default_factory=utcnow)


class ReportBuilder:
    """Combine MarketRadar + SectorRadar output into a Report."""

    def build(
        self,
        market_signals: list[MarketSignal],
        sector_snapshots: list[SectorSnapshot],
        title: str = "Weekly intelligence digest",
    ) -> Report:
        findings: list[str] = []
        if market_signals:
            top = market_signals[0]
            findings.append(
                f"Top market signal: {top.headline} ({top.category}, score={top.score:.2f})"
            )
        category_counts: dict[str, int] = {}
        for s in market_signals:
            category_counts[s.category] = category_counts.get(s.category, 0) + 1
        for cat, count in sorted(category_counts.items(), key=lambda kv: -kv[1])[:3]:
            findings.append(f"{count} signal(s) in category '{cat}'")
        if sector_snapshots:
            findings.append(
                f"Covered sectors: {', '.join(s.sector for s in sector_snapshots)}"
            )
        return Report(
            title=title,
            market_signals=list(market_signals),
            sector_snapshots=list(sector_snapshots),
            headline_findings=findings[:10],
        )


__all__ = ["Report", "ReportBuilder"]
