"""
Section 69 — Intelligence Graph.

Dealix's accumulating memory of *who*, *what*, *how*, and *what worked*.
Nodes are things that exist; edges record the relationship that built
them. The graph answers: best sector? best message? best offer? best
partner? riskiest tool? recurring objection?
"""

from __future__ import annotations

import uuid
from collections import Counter, defaultdict
from collections.abc import Iterable
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any


class NodeKind(StrEnum):
    SIGNAL = "signal"
    OPPORTUNITY = "opportunity"
    OFFER = "offer"
    CUSTOMER = "customer"
    PARTNER = "partner"
    SECTOR = "sector"
    MESSAGE = "message"
    PROPOSAL = "proposal"
    OUTCOME = "outcome"
    ASSET = "asset"
    AGENT = "agent"
    TOOL = "tool"
    RISK = "risk"


class EdgeKind(StrEnum):
    SIGNAL_CREATED_OPPORTUNITY = "signal_created_opportunity"
    OPPORTUNITY_USED_OFFER = "opportunity_used_offer"
    OFFER_GENERATED_PROPOSAL = "offer_generated_proposal"
    PROPOSAL_LED_TO_OUTCOME = "proposal_led_to_outcome"
    OUTCOME_CREATED_ASSET = "outcome_created_asset"
    PARTNER_GENERATED_CUSTOMER = "partner_generated_customer"
    AGENT_USED_TOOL = "agent_used_tool"
    TOOL_CREATED_RISK = "tool_created_risk"


@dataclass(frozen=True)
class Node:
    node_id: str
    kind: NodeKind
    label: str
    payload: dict[str, Any] = field(default_factory=dict)
    workspace_id: str | None = None


@dataclass(frozen=True)
class Edge:
    edge_id: str
    kind: EdgeKind
    src: str
    dst: str
    weight: float = 1.0
    payload: dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))


class IntelligenceGraph:
    def __init__(self) -> None:
        self._nodes: dict[str, Node] = {}
        self._edges: dict[str, Edge] = {}
        self._out: dict[str, list[Edge]] = defaultdict(list)
        self._in: dict[str, list[Edge]] = defaultdict(list)

    def add_node(
        self,
        *,
        kind: NodeKind,
        label: str,
        payload: dict[str, Any] | None = None,
        workspace_id: str | None = None,
        node_id: str | None = None,
    ) -> Node:
        node = Node(
            node_id=node_id or f"n_{uuid.uuid4().hex[:12]}",
            kind=kind,
            label=label,
            payload=dict(payload or {}),
            workspace_id=workspace_id,
        )
        self._nodes[node.node_id] = node
        return node

    def add_edge(
        self,
        *,
        kind: EdgeKind,
        src: str,
        dst: str,
        weight: float = 1.0,
        payload: dict[str, Any] | None = None,
    ) -> Edge:
        if src not in self._nodes or dst not in self._nodes:
            raise KeyError("edge endpoints must be registered nodes")
        edge = Edge(
            edge_id=f"e_{uuid.uuid4().hex[:12]}",
            kind=kind,
            src=src,
            dst=dst,
            weight=weight,
            payload=dict(payload or {}),
        )
        self._edges[edge.edge_id] = edge
        self._out[src].append(edge)
        self._in[dst].append(edge)
        return edge

    def neighbours(self, node_id: str) -> list[Edge]:
        return list(self._out.get(node_id, ()))

    def incoming(self, node_id: str) -> list[Edge]:
        return list(self._in.get(node_id, ()))

    def nodes(self, *, kind: NodeKind | None = None) -> list[Node]:
        if kind is None:
            return list(self._nodes.values())
        return [n for n in self._nodes.values() if n.kind is kind]

    def edges(self, *, kind: EdgeKind | None = None) -> list[Edge]:
        if kind is None:
            return list(self._edges.values())
        return [e for e in self._edges.values() if e.kind is kind]

    def best_sector(self) -> Node | None:
        return self._top_by_revenue(NodeKind.SECTOR)

    def best_offer(self) -> Node | None:
        return self._top_by_revenue(NodeKind.OFFER)

    def best_partner(self) -> Node | None:
        return self._top_by_revenue(NodeKind.PARTNER)

    def riskiest_tool(self) -> Node | None:
        counts = Counter(
            edge.src
            for edge in self._edges.values()
            if edge.kind is EdgeKind.TOOL_CREATED_RISK
        )
        if not counts:
            return None
        return self._nodes.get(counts.most_common(1)[0][0])

    def recurring_objections(self, *, top: int = 5) -> list[tuple[str, int]]:
        counts: Counter[str] = Counter()
        for node in self._nodes.values():
            if node.kind is NodeKind.RISK and node.payload.get("category") == "objection":
                counts[node.label] += int(node.payload.get("count", 1))
        return counts.most_common(top)

    def revenue_for(self, node_id: str) -> float:
        total = 0.0
        for edge in self._in.get(node_id, ()):
            total += float(edge.payload.get("revenue_sar", 0.0))
        return total

    def _top_by_revenue(self, kind: NodeKind) -> Node | None:
        candidates = self.nodes(kind=kind)
        if not candidates:
            return None
        return max(candidates, key=lambda n: self.revenue_for(n.node_id))

    def summary(self) -> dict[str, Any]:
        kind_counts: dict[str, int] = {k.value: 0 for k in NodeKind}
        for node in self._nodes.values():
            kind_counts[node.kind.value] += 1
        edge_counts: dict[str, int] = {k.value: 0 for k in EdgeKind}
        for edge in self._edges.values():
            edge_counts[edge.kind.value] += 1
        return {
            "nodes": kind_counts,
            "edges": edge_counts,
            "total_nodes": len(self._nodes),
            "total_edges": len(self._edges),
        }
