"""SystemScorecard: score each Dealix operating system and aggregate."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List


class SystemStatus(str, Enum):
    PASS = "PASS"
    READY_INTERNAL = "READY INTERNAL"
    FIX = "FIX"
    BLOCKED = "BLOCKED"


@dataclass
class SystemScore:
    name: str
    score: int
    status: SystemStatus
    evidence: str
    next_action: str


SYSTEMS: List[str] = [
    "Founder OS",
    "Strategy OS",
    "Revenue OS",
    "Acquisition OS",
    "Sales OS",
    "Delivery OS",
    "Trust OS",
    "Finance OS",
    "Client Success OS",
    "Product OS",
    "Content OS",
    "Learning OS",
]


def status_for(score: int) -> SystemStatus:
    if score >= 90:
        return SystemStatus.PASS
    if score >= 75:
        return SystemStatus.READY_INTERNAL
    if score >= 50:
        return SystemStatus.FIX
    return SystemStatus.BLOCKED


@dataclass
class SystemScorecard:
    scores: Dict[str, SystemScore] = field(default_factory=dict)

    def set_score(
        self,
        name: str,
        score: int,
        evidence: str,
        next_action: str,
    ) -> SystemScore:
        clamped = max(0, min(100, int(score)))
        item = SystemScore(
            name=name,
            score=clamped,
            status=status_for(clamped),
            evidence=evidence,
            next_action=next_action,
        )
        self.scores[name] = item
        return item

    def aggregate(self) -> int:
        if not self.scores:
            return 0
        total = sum(s.score for s in self.scores.values())
        return total // len(self.scores)

    def aggregate_status(self) -> SystemStatus:
        return status_for(self.aggregate())

    def as_markdown_rows(self) -> List[str]:
        rows: List[str] = []
        for name in SYSTEMS:
            s = self.scores.get(name)
            if s is None:
                rows.append(f"| {name} | 0 | BLOCKED | — | Create baseline |")
            else:
                rows.append(
                    f"| {s.name} | {s.score} | {s.status.value} | {s.evidence} | {s.next_action} |"
                )
        return rows
