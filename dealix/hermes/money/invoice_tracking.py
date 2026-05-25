"""Invoice tracker — open / sent / paid / overdue."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict


class InvoiceState(StrEnum):
    draft = "draft"
    sent = "sent"
    paid = "paid"
    overdue = "overdue"
    cancelled = "cancelled"


class Invoice(BaseModel):
    model_config = ConfigDict(extra="forbid")

    invoice_id: str
    customer_id: str
    amount_sar: float
    state: InvoiceState = InvoiceState.draft
    due_at: str | None = None
    paid_at: str | None = None


@dataclass
class InvoiceTracker:
    _invoices: dict[str, Invoice] = field(default_factory=dict)

    def upsert(self, invoice: Invoice) -> Invoice:
        self._invoices[invoice.invoice_id] = invoice
        return invoice

    def mark_paid(self, invoice_id: str) -> Invoice:
        i = self._invoices[invoice_id]
        updated = i.model_copy(update={
            "state": InvoiceState.paid,
            "paid_at": datetime.now(UTC).isoformat(),
        })
        self._invoices[invoice_id] = updated
        return updated

    def mark_overdue(self, invoice_id: str) -> Invoice:
        i = self._invoices[invoice_id]
        updated = i.model_copy(update={"state": InvoiceState.overdue})
        self._invoices[invoice_id] = updated
        return updated

    def overdue(self) -> list[Invoice]:
        return [i for i in self._invoices.values() if i.state == InvoiceState.overdue]

    def list(self) -> list[Invoice]:
        return list(self._invoices.values())
