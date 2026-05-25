"""Monitor a watchlist of queries the brand should appear in across AI engines."""

from __future__ import annotations

import time
from dataclasses import dataclass, field

_QUERIES: dict[str, "MonitoredQuery"] = {}
_OBSERVATIONS: list["QueryObservation"] = []


@dataclass(frozen=True)
class MonitoredQuery:
    query: str
    engines: tuple[str, ...]
    priority: int = 1
    registered_at: float = 0.0


@dataclass(frozen=True)
class QueryObservation:
    query: str
    engine: str
    brand_mentioned: bool
    snippet: str = ""
    observed_at: float = 0.0
    metadata: dict[str, str] = field(default_factory=dict)


def watch(query: str, engines: list[str], priority: int = 1) -> MonitoredQuery:
    """Add a query to the watchlist (no network call is performed)."""
    mq = MonitoredQuery(query=query, engines=tuple(engines), priority=priority, registered_at=time.time())
    _QUERIES[query] = mq
    return mq


def record_observation(query: str, engine: str, brand_mentioned: bool, snippet: str = "") -> QueryObservation:
    """Record a manual or batch-loaded observation for a watched query."""
    obs = QueryObservation(query=query, engine=engine, brand_mentioned=brand_mentioned, snippet=snippet, observed_at=time.time())
    _OBSERVATIONS.append(obs)
    return obs


def coverage(query: str) -> float:
    """Return mention rate for a watched query across recorded observations."""
    pool = [o for o in _OBSERVATIONS if o.query == query]
    if not pool:
        return 0.0
    return round(sum(1 for o in pool if o.brand_mentioned) / len(pool), 4)


def reset() -> None:
    """Clear monitor state (test helper)."""
    _QUERIES.clear()
    _OBSERVATIONS.clear()
