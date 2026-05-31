"""PartnerGraph — partner contribution to verified revenue, with incident rate."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field


@dataclass
class PartnerEdge:
    partner_id: str
    deal_id: str
    verified_revenue_sar: float
    incidents: int = 0


@dataclass
class PartnerGraph:
    edges: list[PartnerEdge] = field(default_factory=list)

    def add(self, edge: PartnerEdge) -> None:
        self.edges.append(edge)

    def revenue(self) -> dict[str, float]:
        out: dict[str, float] = defaultdict(float)
        for e in self.edges:
            out[e.partner_id] += e.verified_revenue_sar
        return dict(out)

    def incident_rate(self) -> dict[str, float]:
        out: dict[str, list[int]] = defaultdict(list)
        for e in self.edges:
            out[e.partner_id].append(e.incidents)
        return {p: round(sum(v) / len(v), 4) for p, v in out.items()}
