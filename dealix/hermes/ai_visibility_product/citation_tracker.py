"""Track when AI engines cite customer pages/assets."""

from __future__ import annotations

import time
from dataclasses import dataclass

_CITATIONS: list["CitationRecord"] = []


@dataclass(frozen=True)
class CitationRecord:
    customer_id: str
    engine: str
    cited_url: str
    query: str
    rank: int
    observed_at: float = 0.0


def record(customer_id: str, engine: str, cited_url: str, query: str, rank: int) -> CitationRecord:
    """Record an AI engine citation pointing to a customer URL."""
    c = CitationRecord(
        customer_id=customer_id,
        engine=engine,
        cited_url=cited_url,
        query=query,
        rank=int(rank),
        observed_at=time.time(),
    )
    _CITATIONS.append(c)
    return c


def citations_for(customer_id: str) -> list[CitationRecord]:
    """Return all citations recorded for a customer."""
    return [c for c in _CITATIONS if c.customer_id == customer_id]


def reset() -> None:
    """Clear citation records (test helper)."""
    _CITATIONS.clear()
