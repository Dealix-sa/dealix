"""RiskGraph — recurring risks observed across deals, partners, agents."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field


@dataclass
class RiskEvent:
    risk_id: str
    category: str
    severity: str  # "low" | "medium" | "high"
    deal_id: str | None = None
    partner_id: str | None = None
    agent_id: str | None = None


@dataclass
class RiskGraph:
    events: list[RiskEvent] = field(default_factory=list)

    def add(self, event: RiskEvent) -> None:
        self.events.append(event)

    def top_categories(self, limit: int = 5) -> list[tuple[str, int]]:
        counts = Counter(e.category for e in self.events)
        return counts.most_common(limit)

    def by_agent(self) -> dict[str, int]:
        counts = Counter(e.agent_id for e in self.events if e.agent_id)
        return dict(counts)
