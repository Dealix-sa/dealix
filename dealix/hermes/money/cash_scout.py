"""CashScout — surfaces the fastest path to cash from a set of signals.

Input is a list of signals; output is a ranked list of cash actions. The
scout never sends external messages; it just ranks.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from dealix.hermes.core.schemas import Signal


@dataclass
class CashSignalPayload:
    expected_revenue_sar: float
    days_to_cash: int
    win_probability: float        # 0..1

    @property
    def speed_score(self) -> float:
        if self.days_to_cash <= 0:
            return 1.0
        return max(0.0, 1.0 - min(self.days_to_cash, 90) / 90.0)


class CashScout:
    def score(self, signal: Signal) -> float:
        payload = signal.payload.get("cash") or {}
        try:
            data = CashSignalPayload(
                expected_revenue_sar=float(payload.get("expected_revenue_sar", 0)),
                days_to_cash=int(payload.get("days_to_cash", 60)),
                win_probability=float(payload.get("win_probability", 0.3)),
            )
        except (TypeError, ValueError):
            return 0.0
        # 0.5 speed + 0.3 probability + 0.2 normalized revenue (anchor 100k)
        return (
            0.5 * data.speed_score
            + 0.3 * data.win_probability
            + 0.2 * min(1.0, data.expected_revenue_sar / 100_000.0)
        )

    def rank(self, signals: Iterable[Signal]) -> list[tuple[Signal, float]]:
        scored = [(s, self.score(s)) for s in signals]
        return sorted(scored, key=lambda x: x[1], reverse=True)


__all__ = ["CashScout", "CashSignalPayload"]
