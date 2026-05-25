"""
CostIntelligence — a small per-deal cost ledger covering agent, tool,
human, delivery, support, and revision costs.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum


class CostKind(StrEnum):
    AGENT = "agent"
    TOOL = "tool"
    HUMAN = "human"
    DELIVERY = "delivery"
    SUPPORT = "support"
    REVISION = "revision"


@dataclass
class CostEntry:
    deal_id: str
    kind: CostKind
    amount_sar: float
    description: str
    occurred_at: datetime = field(default_factory=lambda: datetime.now(UTC))


@dataclass
class CostBreakdown:
    deal_id: str
    totals: dict[CostKind, float] = field(default_factory=dict)
    entries: list[CostEntry] = field(default_factory=list)

    @property
    def total_sar(self) -> float:
        return sum(self.totals.values())


_LEDGER: dict[str, CostBreakdown] = {}


def register_cost(entry: CostEntry) -> CostBreakdown:
    breakdown = _LEDGER.setdefault(entry.deal_id, CostBreakdown(deal_id=entry.deal_id))
    breakdown.totals[entry.kind] = breakdown.totals.get(entry.kind, 0.0) + entry.amount_sar
    breakdown.entries.append(entry)
    return breakdown


def total_cost(deal_id: str) -> float:
    return _LEDGER.get(deal_id, CostBreakdown(deal_id=deal_id)).total_sar
