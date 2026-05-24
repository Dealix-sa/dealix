"""Renewal planner — schedules next-step actions before renewal date."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone


@dataclass
class RenewalPlanner:
    _by_customer: dict[str, datetime] = field(default_factory=dict)

    def set_renewal(self, customer_id: str, when: datetime) -> None:
        self._by_customer[customer_id] = when

    def due_within(self, days: int) -> list[str]:
        cutoff = datetime.now(timezone.utc) + timedelta(days=days)
        return [c for c, when in self._by_customer.items() if when <= cutoff]


__all__ = ["RenewalPlanner"]
