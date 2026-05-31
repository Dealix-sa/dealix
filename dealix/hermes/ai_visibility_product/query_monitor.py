"""Track which queries the brand should appear in across AI engines (product-side)."""

from __future__ import annotations

import time
from dataclasses import dataclass

_QUERIES: dict[str, "TrackedQuery"] = {}


@dataclass(frozen=True)
class TrackedQuery:
    customer_id: str
    query: str
    priority: int
    registered_at: float = 0.0


def _key(customer_id: str, query: str) -> str:
    return f"{customer_id}:{query}"


def track(customer_id: str, query: str, priority: int = 1) -> TrackedQuery:
    """Track a query a customer wants to appear in across AI engines."""
    tq = TrackedQuery(customer_id=customer_id, query=query, priority=int(priority), registered_at=time.time())
    _QUERIES[_key(customer_id, query)] = tq
    return tq


def list_tracked(customer_id: str) -> list[TrackedQuery]:
    """Return tracked queries for a customer."""
    return [v for v in _QUERIES.values() if v.customer_id == customer_id]


def reset() -> None:
    """Clear tracked queries (test helper)."""
    _QUERIES.clear()
