"""
Intelligence graph — §101.

A tiny in-memory graph that aggregates "what works" across sectors,
messages, offers, partners, agents, tools, objections, prices.
"""

from __future__ import annotations

import threading
from dataclasses import dataclass, field
from typing import Any


@dataclass
class Node:
    node_id: str
    kind: str
    attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {"node_id": self.node_id, "kind": self.kind, "attrs": dict(self.attrs)}


@dataclass
class Edge:
    from_id: str
    to_id: str
    relation: str
    weight: float = 1.0

    def to_dict(self) -> dict[str, Any]:
        return {
            "from_id": self.from_id, "to_id": self.to_id,
            "relation": self.relation, "weight": self.weight,
        }


class IntelligenceGraph:
    def __init__(self) -> None:
        self._nodes: dict[str, Node] = {}
        self._edges: list[Edge] = []
        self._lock = threading.Lock()

    def add_node(self, node_id: str, kind: str, attrs: dict[str, Any] | None = None) -> Node:
        with self._lock:
            node = Node(node_id=node_id, kind=kind, attrs=dict(attrs or {}))
            self._nodes[node_id] = node
            return node

    def add_edge(self, from_id: str, to_id: str, relation: str, weight: float = 1.0) -> Edge:
        with self._lock:
            edge = Edge(from_id=from_id, to_id=to_id, relation=relation, weight=weight)
            self._edges.append(edge)
            return edge

    def neighbors(self, node_id: str, relation: str | None = None) -> list[Edge]:
        return [e for e in self._edges
                if e.from_id == node_id and (relation is None or e.relation == relation)]

    def _sum_by_kind(self, kind: str, relation: str) -> dict[str, float]:
        agg: dict[str, float] = {}
        for n in self._nodes.values():
            if n.kind != kind:
                continue
            total = sum(e.weight for e in self._edges
                        if e.from_id == n.node_id and e.relation == relation)
            agg[n.node_id] = total
        return agg

    def _top(self, agg: dict[str, float]) -> str | None:
        if not agg:
            return None
        return max(agg.items(), key=lambda kv: kv[1])[0]

    def best_sector(self) -> str | None:
        return self._top(self._sum_by_kind("sector", "produced_revenue"))

    def best_message(self) -> str | None:
        return self._top(self._sum_by_kind("message", "won_reply"))

    def most_profitable_offer(self) -> str | None:
        return self._top(self._sum_by_kind("offer", "closed_deal"))

    def best_partner(self) -> str | None:
        return self._top(self._sum_by_kind("partner", "delivered_revenue"))

    def revenue_producing_agents(self) -> list[str]:
        agg = self._sum_by_kind("agent", "produced_revenue")
        return [k for k, v in agg.items() if v > 0]

    def risky_tools(self) -> list[str]:
        return [n.node_id for n in self._nodes.values()
                if n.kind == "tool" and n.attrs.get("risk") in ("high", "critical")]

    def recurring_objections(self) -> list[str]:
        agg: dict[str, int] = {}
        for n in self._nodes.values():
            if n.kind == "objection":
                agg[n.node_id] = sum(
                    1 for e in self._edges
                    if e.from_id == n.node_id and e.relation == "raised_in_deal"
                )
        return [k for k, c in agg.items() if c >= 2]

    def accepted_prices(self) -> list[float]:
        out: list[float] = []
        for n in self._nodes.values():
            if n.kind == "price_point" and n.attrs.get("accepted"):
                out.append(float(n.attrs.get("price_sar", 0.0)))
        return out
