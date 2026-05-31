"""
Output lineage — directed graph that lets you trace any output back to its sources.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field


@dataclass
class LineageGraph:
    edges: dict[str, set[str]] = field(default_factory=dict)

    def add_edge(self, parent_id: str, child_id: str) -> None:
        self.edges.setdefault(parent_id, set()).add(child_id)

    def ancestors(self, object_id: str) -> set[str]:
        """All upstream object_ids reachable from `object_id` (which is downstream)."""
        # invert
        reverse: dict[str, set[str]] = {}
        for p, children in self.edges.items():
            for c in children:
                reverse.setdefault(c, set()).add(p)
        seen: set[str] = set()
        queue = deque([object_id])
        while queue:
            node = queue.popleft()
            for p in reverse.get(node, set()):
                if p not in seen:
                    seen.add(p)
                    queue.append(p)
        return seen

    def descendants(self, object_id: str) -> set[str]:
        seen: set[str] = set()
        queue = deque([object_id])
        while queue:
            node = queue.popleft()
            for c in self.edges.get(node, set()):
                if c not in seen:
                    seen.add(c)
                    queue.append(c)
        return seen


def build_lineage(edges: list[tuple[str, str]]) -> LineageGraph:
    g = LineageGraph()
    for parent, child in edges:
        g.add_edge(parent, child)
    return g
