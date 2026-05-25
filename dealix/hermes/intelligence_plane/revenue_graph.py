"""
Revenue Graph — يربط الصفقات بالدخل الحقيقي (verified).
لا يقبل أي حدث لم يمر بـ `money.revenue_verification`.
"""

from __future__ import annotations

import threading
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass
class RevenueRecord:
    revenue_id: str
    customer_id: str
    offer_id: str
    amount_sar: int
    verification_source: str  # "payment" | "signed_agreement" | "invoice"
    recorded_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    deal_id: str | None = None
    partner_id: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


class RevenueGraph:
    def __init__(self) -> None:
        self._records: dict[str, RevenueRecord] = {}
        self._by_customer: dict[str, list[str]] = defaultdict(list)
        self._by_offer: dict[str, list[str]] = defaultdict(list)
        self._lock = threading.Lock()

    def record(self, record: RevenueRecord) -> RevenueRecord:
        if record.verification_source not in {"payment", "signed_agreement", "invoice"}:
            raise ValueError(
                "revenue requires verification_source in "
                "{payment, signed_agreement, invoice}"
            )
        with self._lock:
            self._records[record.revenue_id] = record
            self._by_customer[record.customer_id].append(record.revenue_id)
            self._by_offer[record.offer_id].append(record.revenue_id)
            return record

    def total_by_offer(self) -> dict[str, int]:
        with self._lock:
            return {
                offer_id: sum(self._records[rid].amount_sar for rid in rids)
                for offer_id, rids in self._by_offer.items()
            }

    def total_by_customer(self) -> dict[str, int]:
        with self._lock:
            return {
                cust: sum(self._records[rid].amount_sar for rid in rids)
                for cust, rids in self._by_customer.items()
            }

    def all(self) -> list[RevenueRecord]:
        with self._lock:
            return list(self._records.values())


__all__ = ["RevenueGraph", "RevenueRecord"]
