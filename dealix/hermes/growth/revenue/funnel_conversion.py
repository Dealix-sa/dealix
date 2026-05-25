"""Compute funnel conversion rates between consecutive stages."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class FunnelStage:
    name: str
    count: int


@dataclass(frozen=True)
class FunnelReport:
    stages: tuple[FunnelStage, ...]
    rates: tuple[tuple[str, str, float], ...] = field(default_factory=tuple)
    overall_rate: float = 0.0


def assess(stages: list[FunnelStage]) -> FunnelReport:
    """Return per-step and overall conversion rates for an ordered funnel."""
    if not stages:
        return FunnelReport(stages=())
    rates: list[tuple[str, str, float]] = []
    for i in range(1, len(stages)):
        prev = stages[i - 1].count
        cur = stages[i].count
        rate = round(cur / prev, 4) if prev > 0 else 0.0
        rates.append((stages[i - 1].name, stages[i].name, rate))
    overall = round(stages[-1].count / stages[0].count, 4) if stages[0].count > 0 else 0.0
    return FunnelReport(stages=tuple(stages), rates=tuple(rates), overall_rate=overall)
