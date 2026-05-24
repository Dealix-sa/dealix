"""OfferCheckoutService — Phase 1 self-serve checkout orchestrator.

Single entrypoint for the 5 productized offers:

    diagnostic_free        — lead magnet; no Moyasar call
    sprint_499             — 499 SAR pilot (auto-approve class)
    data_pack_1500         — 1,500 SAR one-time (auto-approve class)
    managed_ops_retainer   — 2,999-4,999 SAR/mo (escalates to founder once)
    custom_ai              — 5,000-25,000 SAR (always escalates)

Responsibilities:
  1. Run SelfServeIntakeGuard.evaluate_intake (refuse on any violation).
  2. Compute the deterministic idempotency key (sha256(passport_id|offer_id)).
  3. Look up cached invoice for the key (re-uses prior Moyasar HPP URL).
  4. Otherwise mint a new Moyasar hosted-payment invoice for paid offers.
  5. Return a CheckoutResult with the URL the customer should be sent to.

This service is deterministic and never sends any external message. The
Moyasar HPP URL is returned to the caller (the API router), which renders
it into a redirect or a CTA — the customer's click is what triggers the
charge, satisfying Non-Negotiable #6.

Storage: in-memory dict by default (process-local, replaced by Postgres
in Phase 3). The interface is a Protocol so callers may inject a Postgres
adapter without touching this module.
"""

from __future__ import annotations

import hashlib
import logging
from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Protocol

from auto_client_acquisition.governance_os.lawful_basis import LawfulBasis
from auto_client_acquisition.governance_os.self_serve_intake_guard import (
    IntakeVerdict,
    evaluate_intake,
    is_auto_approve_offer,
)

log = logging.getLogger(__name__)

# Offer catalog — single source of truth for amount + flow.
# Amounts are in SAR halalas (1 SAR = 100 halalas).
OFFER_CATALOG: dict[str, dict[str, Any]] = {
    "diagnostic_free": {
        "amount_halalas": 0,
        "currency": "SAR",
        "requires_payment": False,
        "approval_class": "auto_approve",
    },
    "sprint_499": {
        "amount_halalas": 49_900,
        "currency": "SAR",
        "requires_payment": True,
        "approval_class": "auto_approve",
    },
    "data_pack_1500": {
        "amount_halalas": 150_000,
        "currency": "SAR",
        "requires_payment": True,
        "approval_class": "auto_approve",
    },
    "managed_ops_retainer": {
        "amount_halalas": 299_900,  # minimum tier; per-customer override
        "currency": "SAR",
        "requires_payment": True,
        "approval_class": "escalate_first_time",
    },
    "custom_ai": {
        "amount_halalas": 500_000,  # minimum; always escalates
        "currency": "SAR",
        "requires_payment": True,
        "approval_class": "escalate_always",
    },
}


def compute_idempotency_key(*, source_passport_id: str, offer_id: str) -> str:
    """Deterministic idempotency key for (passport, offer) pair."""
    raw = f"{source_passport_id}|{offer_id}".encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


@dataclass(frozen=True, slots=True)
class CheckoutResult:
    """Returned to the API router for the customer."""

    status: str  # "ok" | "rejected" | "escalated" | "free"
    offer_id: str
    idempotency_key: str
    approval_class: str
    invoice_id: str | None = None
    hosted_payment_url: str | None = None
    amount_halalas: int = 0
    currency: str = "SAR"
    verdict: IntakeVerdict | None = None
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "offer_id": self.offer_id,
            "idempotency_key": self.idempotency_key,
            "approval_class": self.approval_class,
            "invoice_id": self.invoice_id,
            "hosted_payment_url": self.hosted_payment_url,
            "amount_halalas": self.amount_halalas,
            "currency": self.currency,
            "created_at": self.created_at,
            "verdict": self.verdict.to_dict() if self.verdict else None,
        }


class CheckoutStore(Protocol):
    """Storage interface for idempotent checkout state."""

    def get(self, idempotency_key: str) -> CheckoutResult | None:
        ...  # pragma: no cover

    def put(self, result: CheckoutResult) -> None:
        ...  # pragma: no cover


class InMemoryCheckoutStore:
    """Default process-local store. Swap with a Postgres adapter in Phase 3."""

    def __init__(self) -> None:
        self._data: dict[str, CheckoutResult] = {}

    def get(self, idempotency_key: str) -> CheckoutResult | None:
        return self._data.get(idempotency_key)

    def put(self, result: CheckoutResult) -> None:
        self._data[result.idempotency_key] = result

    def __len__(self) -> int:
        return len(self._data)


# Callable signature for the Moyasar hosted-payment factory. Injected at
# construction so tests can pass a no-network stub.
HostedPaymentFactory = Callable[..., Awaitable[dict[str, Any]]]


class OfferCheckoutService:
    """Stateless orchestrator over a CheckoutStore + Moyasar factory."""

    def __init__(
        self,
        *,
        store: CheckoutStore | None = None,
        hosted_payment_factory: HostedPaymentFactory | None = None,
        callback_base_url: str = "https://api.dealix.me",
    ) -> None:
        self.store = store or InMemoryCheckoutStore()
        self.hosted_payment_factory = hosted_payment_factory
        self.callback_base_url = callback_base_url.rstrip("/")

    async def checkout(
        self,
        *,
        offer_id: str,
        source_passport_id: str,
        lawful_basis: LawfulBasis | str | None = LawfulBasis.CONSENT,
        consent_given: bool = False,
        customer_handle: str | None = None,
        free_text: str = "",
        locale: str = "ar",
    ) -> CheckoutResult:
        """Run the self-serve checkout flow end-to-end."""

        verdict = evaluate_intake(
            offer_id=offer_id,
            source_passport_id=source_passport_id,
            lawful_basis=lawful_basis,
            consent_given=consent_given,
            free_text=free_text,
        )
        if offer_id not in OFFER_CATALOG:
            # Treat unknown offer as a hard reject regardless of guard
            # (defensive: guard already adds offer_id_invalid).
            return CheckoutResult(
                status="rejected",
                offer_id=offer_id,
                idempotency_key="",
                approval_class="unknown_offer",
                verdict=verdict,
            )

        spec = OFFER_CATALOG[offer_id]
        idem_key = compute_idempotency_key(
            source_passport_id=source_passport_id or "anonymous",
            offer_id=offer_id,
        )

        if not verdict.allow:
            return CheckoutResult(
                status="rejected",
                offer_id=offer_id,
                idempotency_key=idem_key,
                approval_class=spec["approval_class"],
                amount_halalas=int(spec["amount_halalas"]),
                currency=str(spec["currency"]),
                verdict=verdict,
            )

        # Idempotency: re-use the prior invoice (and HPP URL) for this key.
        cached = self.store.get(idem_key)
        if cached is not None:
            log.info("offer_checkout_idempotent_hit", extra={"idem_key": idem_key})
            return cached

        # Free diagnostic — no payment, just register the intent.
        if not spec["requires_payment"]:
            result = CheckoutResult(
                status="free",
                offer_id=offer_id,
                idempotency_key=idem_key,
                approval_class=spec["approval_class"],
                amount_halalas=0,
                currency=str(spec["currency"]),
                verdict=verdict,
            )
            self.store.put(result)
            return result

        # Escalate-always offers do NOT mint a Moyasar invoice via self-serve;
        # they queue a human pitch first. Non-Negotiable #6 compliance.
        if spec["approval_class"] == "escalate_always":
            result = CheckoutResult(
                status="escalated",
                offer_id=offer_id,
                idempotency_key=idem_key,
                approval_class=spec["approval_class"],
                amount_halalas=int(spec["amount_halalas"]),
                currency=str(spec["currency"]),
                verdict=verdict,
            )
            self.store.put(result)
            return result

        # First-time managed_ops_retainer also escalates (founder pitch),
        # but is_auto_approve_offer keeps the auto class for the 3 lower tiers.
        if not is_auto_approve_offer(offer_id):
            result = CheckoutResult(
                status="escalated",
                offer_id=offer_id,
                idempotency_key=idem_key,
                approval_class=spec["approval_class"],
                amount_halalas=int(spec["amount_halalas"]),
                currency=str(spec["currency"]),
                verdict=verdict,
            )
            self.store.put(result)
            return result

        # Auto-approve path: mint a Moyasar HPP invoice.
        if self.hosted_payment_factory is None:
            raise RuntimeError(
                "OfferCheckoutService: hosted_payment_factory not configured"
            )

        callback_url = f"{self.callback_base_url}/api/v1/webhooks/moyasar"
        invoice = await self.hosted_payment_factory(
            amount_halalas=int(spec["amount_halalas"]),
            offer_id=offer_id,
            source_passport_id=source_passport_id,
            callback_url=callback_url,
            customer_handle=customer_handle,
            locale=locale,
            currency=str(spec["currency"]),
            idempotency_key=idem_key,
        )

        result = CheckoutResult(
            status="ok",
            offer_id=offer_id,
            idempotency_key=idem_key,
            approval_class=spec["approval_class"],
            invoice_id=str(invoice.get("id", "")),
            hosted_payment_url=str(invoice.get("url", "")),
            amount_halalas=int(spec["amount_halalas"]),
            currency=str(spec["currency"]),
            verdict=verdict,
        )
        self.store.put(result)
        # offer_id is validated via OFFER_CATALOG membership above, so it is
        # closed-set safe to log; the structured `extra` dict bypasses the
        # log format string entirely (CWE-117 safe).
        log.info(
            "offer_checkout_invoice_created",
            extra={
                "idem_key": idem_key,
                "offer_id": offer_id,
                "amount_halalas": spec["amount_halalas"],
            },
        )
        return result


__all__ = [
    "OFFER_CATALOG",
    "CheckoutResult",
    "CheckoutStore",
    "InMemoryCheckoutStore",
    "OfferCheckoutService",
    "compute_idempotency_key",
]
