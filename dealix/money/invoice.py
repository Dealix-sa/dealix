"""خادم المال — InvoiceGenerator (draft only).

Renders an `InvoiceDraft` from a ProposalDraft + customer record. The
draft is never charged — we don't have the payment-charge tool
allowlisted in the Trust plane. `requires_external_approval` is always
True so the trust layer routes the draft to a human.
"""

from __future__ import annotations

from datetime import datetime, timedelta
from decimal import Decimal
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field

from dealix.hermes.core.schemas import Money, utcnow
from dealix.money.proposal_factory import ProposalDraft


def _new_invoice_id() -> str:
    return f"inv_{uuid4().hex[:16]}"


class InvoiceLineItem(BaseModel):
    model_config = ConfigDict(extra="forbid")

    description: str = Field(..., min_length=1, max_length=240)
    quantity: int = Field(default=1, ge=1, le=1000)
    unit_amount: Money

    @property
    def line_total(self) -> Money:
        total = self.unit_amount.amount * Decimal(self.quantity)
        return Money(amount=total, currency=self.unit_amount.currency)


class InvoiceDraft(BaseModel):
    """A draft invoice — never charged automatically."""

    model_config = ConfigDict(extra="forbid")

    invoice_id: str = Field(default_factory=_new_invoice_id)
    customer_id: str = Field(..., min_length=1, max_length=128)
    customer_name: str = Field(..., min_length=1, max_length=200)
    line_items: list[InvoiceLineItem] = Field(..., min_length=1, max_length=50)
    subtotal: Money
    tax_pct: float = Field(default=0.15, ge=0.0, le=0.5)  # KSA VAT
    tax_amount: Money
    total: Money
    issued_at: datetime = Field(default_factory=utcnow)
    due_at: datetime
    requires_external_approval: bool = True
    notes: str = Field(default="", max_length=2000)


# ─────────────────────────────────────────────────────────────
# Generator
# ─────────────────────────────────────────────────────────────


class InvoiceGenerator:
    """Render an `InvoiceDraft` from a `ProposalDraft` + customer record."""

    def draft(
        self,
        proposal: ProposalDraft,
        customer: dict[str, str],
        tax_pct: float = 0.15,
        due_in_days: int = 14,
    ) -> InvoiceDraft:
        customer_id = customer.get("customer_id") or customer.get("id") or "unknown"
        customer_name = customer.get("name") or proposal.buyer
        items = [
            InvoiceLineItem(
                description=f"{proposal.offer_name} — pilot deliverable",
                quantity=1,
                unit_amount=proposal.price,
            )
        ]
        subtotal = items[0].line_total
        tax_decimal = Decimal(str(tax_pct))
        tax_amount = Money(
            amount=subtotal.amount * tax_decimal,
            currency=subtotal.currency,
        )
        total = Money(
            amount=subtotal.amount + tax_amount.amount,
            currency=subtotal.currency,
        )
        due_at = utcnow() + timedelta(days=due_in_days)
        notes_parts = [
            f"Approval status: {proposal.approval_status}",
            f"Sovereignty: {proposal.sovereignty_level.value}",
            "Draft only — no payment will be charged automatically.",
        ]
        return InvoiceDraft(
            customer_id=customer_id,
            customer_name=customer_name,
            line_items=items,
            subtotal=subtotal,
            tax_pct=tax_pct,
            tax_amount=tax_amount,
            total=total,
            due_at=due_at,
            requires_external_approval=True,
            notes="\n".join(notes_parts),
        )


__all__ = [
    "InvoiceDraft",
    "InvoiceGenerator",
    "InvoiceLineItem",
]
