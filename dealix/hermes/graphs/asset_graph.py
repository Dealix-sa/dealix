"""AssetGraph — which assets influence which deals."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field


@dataclass
class AssetEdge:
    asset_id: str
    deal_id: str
    verified_revenue_sar: float


@dataclass
class AssetGraph:
    edges: list[AssetEdge] = field(default_factory=list)

    def add(self, edge: AssetEdge) -> None:
        self.edges.append(edge)

    def revenue_by_asset(self) -> dict[str, float]:
        out: dict[str, float] = defaultdict(float)
        for e in self.edges:
            out[e.asset_id] += e.verified_revenue_sar
        return dict(out)
