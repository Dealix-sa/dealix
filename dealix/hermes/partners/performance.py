"""Partner performance tracker — used for Performance Review (No-Orphan rule)."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone


@dataclass
class PartnerPerformance:
    partner_id: str
    leads_delivered: int = 0
    deals_won: int = 0
    revenue_sar: float = 0.0
    last_review_at: datetime | None = None

    def record(self, *, leads: int = 0, deals: int = 0, revenue_sar: float = 0.0) -> None:
        self.leads_delivered += leads
        self.deals_won += deals
        self.revenue_sar += revenue_sar

    def review(self) -> None:
        self.last_review_at = datetime.now(timezone.utc)

    def needs_review(self, *, max_gap: timedelta = timedelta(days=30)) -> bool:
        if self.last_review_at is None:
            return True
        return (datetime.now(timezone.utc) - self.last_review_at) > max_gap


__all__ = ["PartnerPerformance"]
