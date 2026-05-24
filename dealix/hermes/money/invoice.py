"""InvoiceLedger — tracks invoices but never moves funds.

Money movement is S5. This ledger records issuance + collection only.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum


class InvoiceStatus(str, Enum):
    DRAFT = "draft"
    ISSUED = "issued"
    PAID = "paid"
    OVERDUE = "overdue"
    VOID = "void"


@dataclass
class Invoice:
    id: str
    customer: str
    amount_sar: float
    due_at: datetime
    status: InvoiceStatus = InvoiceStatus.DRAFT
    issued_at: datetime | None = None
    paid_at: datetime | None = None
    payment_ref: str | None = None


@dataclass
class InvoiceLedger:
    _by_id: dict[str, Invoice] = field(default_factory=dict)

    def draft(self, *, customer: str, amount_sar: float, due_at: datetime) -> Invoice:
        if amount_sar <= 0:
            raise ValueError("Invoice amount must be > 0.")
        inv = Invoice(
            id=f"inv_{uuid.uuid4().hex[:10]}",
            customer=customer,
            amount_sar=amount_sar,
            due_at=due_at,
        )
        self._by_id[inv.id] = inv
        return inv

    def issue(self, invoice_id: str) -> Invoice:
        inv = self._by_id[invoice_id]
        inv.status = InvoiceStatus.ISSUED
        inv.issued_at = datetime.now(timezone.utc)
        return inv

    def mark_paid(self, invoice_id: str, *, ref: str) -> Invoice:
        inv = self._by_id[invoice_id]
        inv.status = InvoiceStatus.PAID
        inv.paid_at = datetime.now(timezone.utc)
        inv.payment_ref = ref
        return inv

    def mark_overdue_due(self) -> list[Invoice]:
        now = datetime.now(timezone.utc)
        out: list[Invoice] = []
        for inv in self._by_id.values():
            if inv.status == InvoiceStatus.ISSUED and inv.due_at < now:
                inv.status = InvoiceStatus.OVERDUE
                out.append(inv)
        return out

    def all(self) -> list[Invoice]:
        return list(self._by_id.values())

    def open(self) -> list[Invoice]:
        return [i for i in self._by_id.values() if i.status in {InvoiceStatus.ISSUED, InvoiceStatus.OVERDUE}]


__all__ = ["Invoice", "InvoiceLedger", "InvoiceStatus"]
