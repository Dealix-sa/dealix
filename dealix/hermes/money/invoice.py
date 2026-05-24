"""Invoice draft — produces a structured invoice payload.

This module never issues an invoice externally. Issuing is a sovereign
action; the founder reviews the draft and sends it through the existing
ZATCA pipeline.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, date, datetime, timezone
from typing import Any

from dealix.hermes.sovereignty import SovereigntyLevel

VAT_RATE_KSA = 0.15


@dataclass
class InvoiceLine:
    description: str
    quantity: float
    unit_price_sar: float

    @property
    def subtotal_sar(self) -> float:
        return round(self.quantity * self.unit_price_sar, 2)


@dataclass
class InvoiceDraft:
    id: str
    client_name: str
    issue_date: date
    due_date: date
    lines: list[InvoiceLine] = field(default_factory=list)
    notes: str | None = None
    sovereignty_level: SovereigntyLevel = SovereigntyLevel.L6_SOVEREIGN_ONLY

    @property
    def subtotal_sar(self) -> float:
        return round(sum(line.subtotal_sar for line in self.lines), 2)

    @property
    def vat_sar(self) -> float:
        return round(self.subtotal_sar * VAT_RATE_KSA, 2)

    @property
    def total_sar(self) -> float:
        return round(self.subtotal_sar + self.vat_sar, 2)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "client_name": self.client_name,
            "issue_date": self.issue_date.isoformat(),
            "due_date": self.due_date.isoformat(),
            "lines": [
                {
                    "description": line.description,
                    "quantity": line.quantity,
                    "unit_price_sar": line.unit_price_sar,
                    "subtotal_sar": line.subtotal_sar,
                }
                for line in self.lines
            ],
            "subtotal_sar": self.subtotal_sar,
            "vat_sar": self.vat_sar,
            "total_sar": self.total_sar,
            "notes": self.notes,
            "sovereignty_level": self.sovereignty_level.name,
        }


def draft_invoice(
    invoice_id: str,
    client_name: str,
    lines: list[dict[str, Any]],
    issue_date: date | None = None,
    due_in_days: int = 14,
    notes: str | None = None,
) -> InvoiceDraft:
    issued = issue_date or datetime.now(UTC).date()
    due = issued.replace(day=min(issued.day, 28))  # safe rebuild
    # Compute due date with arithmetic that works at month-end boundaries.
    from datetime import timedelta

    due = issued + timedelta(days=due_in_days)
    invoice_lines = [
        InvoiceLine(
            description=item["description"],
            quantity=float(item.get("quantity", 1)),
            unit_price_sar=float(item["unit_price_sar"]),
        )
        for item in lines
    ]
    return InvoiceDraft(
        id=invoice_id,
        client_name=client_name,
        issue_date=issued,
        due_date=due,
        lines=invoice_lines,
        notes=notes,
    )
