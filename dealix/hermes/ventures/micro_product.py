"""Small, ship-this-week products surfaced from outcomes."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field


@dataclass
class MicroProduct:
    id: str
    name: str
    cost_to_ship_sar: float
    revenue_target_sar: float
    timeline_weeks: int


@dataclass
class MicroProductFactory:
    _by_id: dict[str, MicroProduct] = field(default_factory=dict)

    def add(self, *, name: str, cost_to_ship_sar: float, revenue_target_sar: float, timeline_weeks: int) -> MicroProduct:
        if cost_to_ship_sar < 0:
            raise ValueError("cost_to_ship_sar must be >= 0.")
        if revenue_target_sar <= 0:
            raise ValueError("revenue_target_sar must be > 0.")
        m = MicroProduct(
            id=f"mp_{uuid.uuid4().hex[:10]}",
            name=name,
            cost_to_ship_sar=float(cost_to_ship_sar),
            revenue_target_sar=float(revenue_target_sar),
            timeline_weeks=int(timeline_weeks),
        )
        self._by_id[m.id] = m
        return m

    def all(self) -> list[MicroProduct]:
        return list(self._by_id.values())


__all__ = ["MicroProduct", "MicroProductFactory"]
