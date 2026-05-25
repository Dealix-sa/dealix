"""Market radar — captures pain signals."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from pydantic import BaseModel, ConfigDict, Field


class RadarSignal(BaseModel):
    model_config = ConfigDict(extra="forbid")

    signal_id: str
    source: str
    headline: str
    summary: str = ""
    captured_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())


@dataclass
class MarketRadar:
    _signals: list[RadarSignal] = field(default_factory=list)

    def emit(self, signal: RadarSignal) -> RadarSignal:
        self._signals.append(signal)
        return signal

    def recent(self, limit: int = 25) -> list[RadarSignal]:
        return self._signals[-limit:]
