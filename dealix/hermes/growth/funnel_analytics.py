"""
Funnel Analytics — snapshot لكل قناة على شكل (signal → lead → call → proposal → won).
المخرج deterministic وقابل للعرض في الـ Growth Workspace.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum


class FunnelStage(StrEnum):
    SIGNAL = "signal"
    LEAD = "lead"
    QUALIFIED = "qualified"
    CALL = "call"
    PROPOSAL = "proposal"
    WON = "won"


@dataclass
class FunnelSnapshot:
    channel: str
    counts: dict[FunnelStage, int] = field(default_factory=dict)

    @property
    def conversion_rates(self) -> dict[str, float]:
        order = list(FunnelStage)
        rates: dict[str, float] = {}
        for i in range(1, len(order)):
            prev = self.counts.get(order[i - 1], 0)
            curr = self.counts.get(order[i], 0)
            key = f"{order[i - 1].value}->{order[i].value}"
            rates[key] = (curr / prev) if prev else 0.0
        return rates


class FunnelAnalytics:
    def snapshot(
        self, channel: str, counts: dict[FunnelStage, int]
    ) -> FunnelSnapshot:
        return FunnelSnapshot(channel=channel, counts=dict(counts))


__all__ = ["FunnelAnalytics", "FunnelSnapshot", "FunnelStage"]
