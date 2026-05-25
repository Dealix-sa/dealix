"""RevenueGraph — verified revenue grouped by offer, channel, sector."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field


@dataclass
class RevenueNode:
    deal_id: str
    offer_id: str
    sector: str
    channel: str
    verified_revenue_sar: float


@dataclass
class RevenueGraph:
    nodes: list[RevenueNode] = field(default_factory=list)

    def add(self, node: RevenueNode) -> None:
        self.nodes.append(node)

    def revenue_by(self, key: str) -> dict[str, float]:
        out: dict[str, float] = defaultdict(float)
        for n in self.nodes:
            value = getattr(n, key)
            out[value] += n.verified_revenue_sar
        return dict(out)

    def top_offer(self) -> str | None:
        totals = self.revenue_by("offer_id")
        return max(totals, key=totals.get) if totals else None
