"""Forward-looking cashflow rollup."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass(frozen=True)
class ForecastEntry:
    bucket: str             # e.g. "this_week" | "next_30d" | "next_90d"
    expected_sar: float
    confidence: float       # 0..1


@dataclass
class CashflowForecast:
    entries: list[ForecastEntry] = field(default_factory=list)
    as_of: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def add(self, entry: ForecastEntry) -> None:
        self.entries.append(entry)

    def total(self) -> float:
        return sum(e.expected_sar * e.confidence for e in self.entries)


__all__ = ["CashflowForecast", "ForecastEntry"]
