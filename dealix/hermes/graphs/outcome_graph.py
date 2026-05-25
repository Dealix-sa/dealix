"""OutcomeGraph — outcomes grouped by capability and agent."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field


@dataclass
class OutcomeNode:
    request_id: str
    capability: str
    agent_id: str | None
    success: bool
    value_sar: float = 0.0


@dataclass
class OutcomeGraph:
    nodes: list[OutcomeNode] = field(default_factory=list)

    def add(self, node: OutcomeNode) -> None:
        self.nodes.append(node)

    def success_rate(self, capability: str) -> float:
        items = [n for n in self.nodes if n.capability == capability]
        if not items:
            return 0.0
        return round(sum(1 for n in items if n.success) / len(items), 4)

    def value_by_agent(self) -> dict[str, float]:
        out: dict[str, float] = defaultdict(float)
        for n in self.nodes:
            if n.agent_id:
                out[n.agent_id] += n.value_sar
        return dict(out)
