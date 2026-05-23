"""
Learning synthesizer.

Aggregates LearningSignals into a structured weekly summary the founder
can read in 60 seconds.
"""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Iterable

from control_plane.learning_router import LearningSignal


@dataclass(frozen=True, slots=True)
class LearningSummary:
    period: str
    counts_by_kind: dict[str, int]
    top_signals: list[str]


class LearningSynthesizer:
    def __init__(self, top_n: int = 5) -> None:
        self.top_n = top_n

    def summarize(self, signals: Iterable[LearningSignal], *, period: str) -> LearningSummary:
        signals = list(signals)
        counts = Counter(s.kind for s in signals)
        top = [s.summary for s in signals[: self.top_n]]
        return LearningSummary(period=period, counts_by_kind=dict(counts), top_signals=top)
