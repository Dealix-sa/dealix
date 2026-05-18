"""Record a manual (non-Moyasar) bank-transfer payment.

The 11 non-negotiables forbid automatic card charging: every customer
is invoiced manually and pays by bank transfer. This module gives that
flow a single clean code path:

  1. build_manual_payment_record(...) -> a `payments` table row with
     provider="bank_transfer" (the table's `provider` column is a free
     String, so Moyasar is not required).
  2. record_manual_payment(...) -> persists that row AND appends a
     tier="verified" event to the value_os ledger, because a confirmed
     bank transfer with a reference is verified revenue.

The functions are pure where possible: build_manual_payment_record has
no side effects, and record_manual_payment takes the persistence
callable so it stays unit-testable without a live database.
"""

from __future__ import annotations

import hashlib
from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import ROUND_HALF_UP, Decimal

from auto_client_acquisition.value_os.value_ledger import ValueEvent, add_event

MANUAL_PROVIDER: str = "bank_transfer"
# A confirmed bank transfer carries a real reference -> verified tier.
MANUAL_PAYMENT_TIER: str = "verified"
_MIN_EVIDENCE_LEN: int = 5


class ManualPaymentError(ValueError):
    """Raised when a manual payment cannot be recorded safely."""


@dataclass(frozen=True)
class ManualPaymentResult:
    """Outcome of recording a manual bank-transfer payment."""

    payment_id: str
    provider: str
    bank_reference: str
    amount_halalas: int
    amount_sar: Decimal
    customer_id: str
    value_event: ValueEvent


def _payment_id(provider: str, bank_reference: str) -> str:
    digest = hashlib.sha256(f"{provider}:{bank_reference}".encode()).hexdigest()[:24]
    return f"pay_manual_{digest}"


def sar_to_halalas(amount_sar: Decimal | float | str) -> int:
    """Convert a SAR amount to integer halalas (1 SAR = 100 halalas)."""
    amount = Decimal(str(amount_sar))
    halalas = (amount * 100).quantize(Decimal("1"), rounding=ROUND_HALF_UP)
    return int(halalas)


def build_manual_payment_record(
    *,
    customer_id: str,
    bank_reference: str,
    amount_sar: Decimal | float | str,
    plan: str = "revenue_proof_sprint",
    email: str | None = None,
    tenant_id: str | None = None,
    confirmed_at: datetime | None = None,
):
    """Build a `payments` table row for a manual bank-transfer payment.

    Returns an unpersisted ``db.models.PaymentRecord`` with
    provider="bank_transfer" and status="paid". No card is charged and
    no external API is contacted. The caller is responsible for adding
    the row to a session and committing.
    """
    bank_reference = (bank_reference or "").strip()
    if len(bank_reference) < _MIN_EVIDENCE_LEN:
        raise ManualPaymentError(
            f"bank_reference must be at least {_MIN_EVIDENCE_LEN} characters "
            "(the bank transfer evidence reference)"
        )
    if not customer_id.strip():
        raise ManualPaymentError("customer_id is required")
    halalas = sar_to_halalas(amount_sar)
    if halalas <= 0:
        raise ManualPaymentError("amount_sar must be greater than zero")

    from db.models import PaymentRecord

    ts = confirmed_at or datetime.now(timezone.utc)
    return PaymentRecord(
        id=_payment_id(MANUAL_PROVIDER, bank_reference),
        tenant_id=tenant_id,
        provider=MANUAL_PROVIDER,
        provider_payment_id=bank_reference,
        plan=plan,
        amount_halalas=halalas,
        currency="SAR",
        status="paid",
        email=email,
        last_event_type="manual.bank_transfer.confirmed",
        raw_event={
            "source": "manual_bank_transfer",
            "bank_reference": bank_reference,
            "confirmed_at": ts.isoformat(),
            "no_live_charge": True,
        },
        created_at=ts,
        updated_at=ts,
    )


def record_manual_payment(
    *,
    customer_id: str,
    bank_reference: str,
    amount_sar: Decimal | float | str,
    confirmed_by: str,
    plan: str = "revenue_proof_sprint",
    email: str | None = None,
    tenant_id: str | None = None,
    persist: Callable[[object], None] | None = None,
) -> ManualPaymentResult:
    """Record a confirmed manual bank-transfer payment end to end.

    Builds the `payments` row, optionally persists it via the ``persist``
    callable, and appends a tier="verified" event to the value_os
    ledger using the bank reference as ``source_ref``. ``confirmed_by``
    identifies the founder who verified the funds landed.
    """
    if not confirmed_by.strip():
        raise ManualPaymentError("confirmed_by is required (founder confirmation)")

    record = build_manual_payment_record(
        customer_id=customer_id,
        bank_reference=bank_reference,
        amount_sar=amount_sar,
        plan=plan,
        email=email,
        tenant_id=tenant_id,
    )
    if persist is not None:
        persist(record)

    event = add_event(
        customer_id=customer_id,
        kind="manual_payment_received",
        amount=float(record.amount_halalas) / 100.0,
        tier=MANUAL_PAYMENT_TIER,
        source_ref=record.provider_payment_id,
        notes=f"manual bank transfer confirmed by {confirmed_by}; plan={plan}",
    )
    return ManualPaymentResult(
        payment_id=record.id,
        provider=record.provider,
        bank_reference=record.provider_payment_id,
        amount_halalas=record.amount_halalas,
        amount_sar=Decimal(record.amount_halalas) / Decimal("100"),
        customer_id=customer_id,
        value_event=event,
    )


__all__ = [
    "MANUAL_PAYMENT_TIER",
    "MANUAL_PROVIDER",
    "ManualPaymentError",
    "ManualPaymentResult",
    "build_manual_payment_record",
    "record_manual_payment",
    "sar_to_halalas",
]
