"""Sector-focused radar wrapper around MarketRadar."""

from __future__ import annotations

from dataclasses import dataclass, field

from dealix.hermes.core.schemas import Signal
from dealix.hermes.intelligence.market_radar import MarketRadar, MarketSignalKind


@dataclass
class SectorRadar:
    sectors: list[str] = field(default_factory=list)
    _radar: MarketRadar = field(default_factory=MarketRadar)

    def watch(self, sector: str) -> None:
        if sector not in self.sectors:
            self.sectors.append(sector)

    def emit(self, *, sector: str, kind: MarketSignalKind, summary: str, intent: str) -> Signal:
        if sector not in self.sectors:
            raise ValueError(f"Sector '{sector}' is not being watched.")
        return self._radar.emit(kind=kind, summary=summary, intent=intent, sector=sector)


__all__ = ["SectorRadar"]
