from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol


@dataclass(frozen=True)
class IntelligenceSource:
    title: str
    url: str
    highlights: list[str] = field(default_factory=list)
    source_type: str = "web"
    provider: str = "unknown"


@dataclass(frozen=True)
class IntelligenceQuery:
    query: str
    sector: str
    city: str = "Riyadh"
    product: str = "Data Intelligence OS"
    intent: str = "research"


class ResearchConnector(Protocol):
    def configured(self) -> bool:
        ...

    def dry_run_search(self, query: str) -> dict:
        ...
