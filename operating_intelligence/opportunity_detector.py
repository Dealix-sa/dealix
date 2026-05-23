"""
Opportunity detector.

Surfaces above-target signals that warrant doubling down.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Opportunity:
    signal: str
    actual: float
    target: float
    lift: float


class OpportunityDetector:
    def __init__(self, lift_threshold: float = 0.20) -> None:
        self.lift_threshold = lift_threshold

    def detect(self, signals: dict[str, tuple[float, float]]) -> list[Opportunity]:
        out: list[Opportunity] = []
        for name, (actual, target) in signals.items():
            if target <= 0:
                continue
            lift = (actual - target) / target
            if lift >= self.lift_threshold:
                out.append(Opportunity(name, actual, target, round(lift, 3)))
        out.sort(key=lambda o: o.lift, reverse=True)
        return out
