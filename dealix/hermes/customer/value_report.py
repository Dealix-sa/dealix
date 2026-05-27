"""Monthly Value Report builder.

Section 121 rule: any paid customer without a Monthly Value Report is a
churn risk. The builder + ledger combo lets audit detect customers that
have been silent for too long.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone


@dataclass
class ValueReport:
    id: str
    customer_id: str
    period_end: datetime
    wins: list[str]
    metrics: dict[str, float]
    next_actions: list[str]
    issued_at: datetime


@dataclass
class ValueReportBuilder:
    _by_id: dict[str, ValueReport] = field(default_factory=dict)
    _last_by_customer: dict[str, datetime] = field(default_factory=dict)

    def issue(
        self,
        *,
        customer_id: str,
        period_end: datetime,
        wins: list[str],
        metrics: dict[str, float],
        next_actions: list[str],
    ) -> ValueReport:
        r = ValueReport(
            id=f"vrp_{uuid.uuid4().hex[:10]}",
            customer_id=customer_id,
            period_end=period_end,
            wins=list(wins),
            metrics=dict(metrics),
            next_actions=list(next_actions),
            issued_at=datetime.now(timezone.utc),
        )
        self._by_id[r.id] = r
        self._last_by_customer[customer_id] = r.issued_at
        return r

    def last_issued(self, customer_id: str) -> datetime | None:
        return self._last_by_customer.get(customer_id)

    def silent_customers(self, *, active_customers: list[str], window: timedelta = timedelta(days=35)) -> list[str]:
        cutoff = datetime.now(timezone.utc) - window
        return [c for c in active_customers if self._last_by_customer.get(c, datetime.min.replace(tzinfo=timezone.utc)) < cutoff]


__all__ = ["ValueReport", "ValueReportBuilder"]
