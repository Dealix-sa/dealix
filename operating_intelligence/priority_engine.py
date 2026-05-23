"""
Priority engine.

Ranks work items by impact / leverage / reversibility. Used by the CEO
brief and the focus queue.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PrioritizedItem:
    label: str
    impact: int      # 1..5
    leverage: int    # 1..5
    reversibility: int  # 1..5 (1=hard to reverse, 5=easy)
    score: float


class PriorityEngine:
    """Score = impact * leverage / (6 - reversibility)."""

    def score(self, *, label: str, impact: int, leverage: int, reversibility: int) -> PrioritizedItem:
        impact = max(1, min(5, int(impact)))
        leverage = max(1, min(5, int(leverage)))
        reversibility = max(1, min(5, int(reversibility)))
        s = (impact * leverage) / (6 - reversibility)
        return PrioritizedItem(label, impact, leverage, reversibility, round(s, 3))

    def rank(self, items: list[PrioritizedItem]) -> list[PrioritizedItem]:
        return sorted(items, key=lambda x: x.score, reverse=True)
