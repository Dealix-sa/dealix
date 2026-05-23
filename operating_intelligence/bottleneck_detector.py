"""
Bottleneck detector.

Walks the funnel stages and reports the first stage where the conversion
ratio falls below the target. There is always exactly one bottleneck
worth fixing first.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Bottleneck:
    stage: str
    actual_ratio: float
    target_ratio: float
    severity: str  # P0 | P1 | P2

    @property
    def gap(self) -> float:
        return max(0.0, self.target_ratio - self.actual_ratio)


_DEFAULT_FUNNEL = [
    ("lead_to_qualified", 0.30),
    ("qualified_to_proposal", 0.40),
    ("proposal_to_paid", 0.25),
    ("paid_to_renewed", 0.50),
]


class BottleneckDetector:
    def __init__(self, targets: list[tuple[str, float]] | None = None) -> None:
        self.targets = targets or _DEFAULT_FUNNEL

    def detect(self, ratios: dict[str, float]) -> Bottleneck | None:
        for stage, target in self.targets:
            actual = float(ratios.get(stage, 0.0))
            if actual < target:
                gap = target - actual
                severity = "P0" if gap >= target / 2 else "P1" if gap >= target / 4 else "P2"
                return Bottleneck(stage, actual, target, severity)
        return None
