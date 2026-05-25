"""OpportunityGraph — opportunities linked to offers, sectors, channels."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field


@dataclass
class OpportunityNode:
    opportunity_id: str
    offer_id: str
    sector: str
    channel: str
    estimated_value_sar: float
    status: str = "open"  # "open" | "won" | "lost"


@dataclass
class OpportunityGraph:
    nodes: dict[str, OpportunityNode] = field(default_factory=dict)

    def add(self, node: OpportunityNode) -> None:
        self.nodes[node.opportunity_id] = node

    def by_offer(self) -> dict[str, list[OpportunityNode]]:
        out: dict[str, list[OpportunityNode]] = defaultdict(list)
        for n in self.nodes.values():
            out[n.offer_id].append(n)
        return out

    def win_rate(self, offer_id: str) -> float:
        items = self.by_offer().get(offer_id, [])
        if not items:
            return 0.0
        won = sum(1 for n in items if n.status == "won")
        return round(won / len(items), 4)
