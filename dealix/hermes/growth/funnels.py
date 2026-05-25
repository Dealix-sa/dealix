"""Funnel analytics — measure drop-off."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class FunnelMetric:
    stage: str
    count: int


@dataclass
class FunnelReport:
    metrics: list[FunnelMetric]

    def conversion(self, start_stage: str, end_stage: str) -> float:
        start = next((m.count for m in self.metrics if m.stage == start_stage), 0)
        end = next((m.count for m in self.metrics if m.stage == end_stage), 0)
        return round(end / start, 4) if start else 0.0
