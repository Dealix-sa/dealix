"""Track brand mentions for a customer across AI engines (product surface)."""

from __future__ import annotations

import time
from dataclasses import dataclass

_MENTIONS: list["MentionRecord"] = []


@dataclass(frozen=True)
class MentionRecord:
    customer_id: str
    engine: str
    query: str
    snippet: str
    sentiment: str
    observed_at: float = 0.0


def record(customer_id: str, engine: str, query: str, snippet: str, sentiment: str = "neutral") -> MentionRecord:
    """Record a brand mention observed in an AI engine answer."""
    m = MentionRecord(
        customer_id=customer_id,
        engine=engine,
        query=query,
        snippet=snippet,
        sentiment=sentiment,
        observed_at=time.time(),
    )
    _MENTIONS.append(m)
    return m


def list_mentions(customer_id: str) -> list[MentionRecord]:
    """Return all recorded mentions for a customer."""
    return [m for m in _MENTIONS if m.customer_id == customer_id]


def reset() -> None:
    """Clear mention records (test helper)."""
    _MENTIONS.clear()
