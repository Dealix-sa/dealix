"""
Revenue Events — append-only log of every money-relevant event. The log is the
source of truth; aggregates (RevenueGraph) are projections of this log.
"""

from __future__ import annotations

import threading
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import StrEnum
from typing import Any


class RevenueEventKind(StrEnum):
    PROPOSAL_SENT = "proposal_sent"
    PROPOSAL_WON = "proposal_won"
    PAYMENT_RECEIVED = "payment_received"
    SIGNED_AGREEMENT = "signed_agreement"
    INVOICE_ISSUED = "invoice_issued"
    INVOICE_PAID = "invoice_paid"
    REFUND_ISSUED = "refund_issued"
    RETAINER_STARTED = "retainer_started"
    RETAINER_RENEWED = "retainer_renewed"
    RETAINER_CHURNED = "retainer_churned"
    PARTNER_PAID_CUSTOMER = "partner_paid_customer"


@dataclass
class RevenueEvent:
    event_id: str
    kind: RevenueEventKind
    customer_id: str
    offer_id: str
    amount_sar: int
    occurred_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    deal_id: str | None = None
    partner_id: str | None = None
    invoice_id: str | None = None
    payment_reference: str | None = None
    note: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


class RevenueEventLog:
    def __init__(self) -> None:
        self._events: list[RevenueEvent] = []
        self._lock = threading.Lock()

    def append(self, event: RevenueEvent) -> RevenueEvent:
        if not event.event_id:
            event.event_id = f"rev_{uuid.uuid4().hex[:16]}"
        with self._lock:
            self._events.append(event)
        return event

    def by_customer(self, customer_id: str) -> list[RevenueEvent]:
        with self._lock:
            return [e for e in self._events if e.customer_id == customer_id]

    def by_kind(self, kind: RevenueEventKind) -> list[RevenueEvent]:
        with self._lock:
            return [e for e in self._events if e.kind == kind]

    def all(self) -> list[RevenueEvent]:
        with self._lock:
            return list(self._events)


__all__ = ["RevenueEvent", "RevenueEventKind", "RevenueEventLog"]
