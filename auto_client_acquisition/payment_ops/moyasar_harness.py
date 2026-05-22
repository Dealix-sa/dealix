"""Moyasar test-mode harness — pure-logic adapter for the payment path.

Deliberately does NOT talk to the Moyasar API. The harness produces the
exact request payload Moyasar expects, verifies the HMAC signature on
inbound webhooks, and parses paid events into a typed shape. The HTTP
plumbing lives in the existing router; this module is what the router
calls so the business logic is unit-testable without a live network
or a live key.

Test-mode safety rail: ``enforce_test_mode`` refuses any secret key that
begins with ``sk_live_`` unless ``DEALIX_MOYASAR_MODE=live`` is explicitly
set — protects against accidentally charging a real card while wiring
the harness on the activation branch.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import os
from dataclasses import dataclass, field
from typing import Any

MOYASAR_CURRENCY = "SAR"
MIN_AMOUNT_HALALAS = 100
MAX_AMOUNT_HALALAS = 5_000_000


class MoyasarHarnessError(ValueError):
    """Raised for any harness-level violation (live key without opt-in, bad signature, etc.)."""


@dataclass(frozen=True, slots=True)
class MoyasarPaymentRequest:
    """The payload Moyasar's invoice/payment endpoint expects."""

    amount_halalas: int
    currency: str
    description: str
    callback_url: str
    metadata: dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "amount": self.amount_halalas,
            "currency": self.currency,
            "description": self.description,
            "callback_url": self.callback_url,
            "metadata": dict(self.metadata),
        }


@dataclass(frozen=True, slots=True)
class MoyasarWebhookEvent:
    """Parsed Moyasar webhook event — only fields the harness cares about."""

    type: str
    payment_id: str
    status: str
    amount_halalas: int
    currency: str
    metadata: dict[str, str] = field(default_factory=dict)

    @property
    def is_paid(self) -> bool:
        return self.type == "payment_paid" and self.status == "paid"


def enforce_test_mode(secret_key: str) -> None:
    """Refuse a live key unless DEALIX_MOYASAR_MODE=live is explicitly set."""
    if not secret_key:
        raise MoyasarHarnessError("MOYASAR secret key is empty")
    if secret_key.startswith("sk_live_") and os.environ.get("DEALIX_MOYASAR_MODE") != "live":
        raise MoyasarHarnessError(
            "live Moyasar key supplied without DEALIX_MOYASAR_MODE=live opt-in"
        )


def build_payment_request(
    *,
    amount_sar: float,
    description: str,
    callback_url: str,
    metadata: dict[str, str] | None = None,
) -> MoyasarPaymentRequest:
    """Build a typed payment request. Amount in SAR (converted to halalas internally)."""
    if amount_sar <= 0:
        raise MoyasarHarnessError("amount_sar must be > 0")
    if not description.strip():
        raise MoyasarHarnessError("description is required")
    if not callback_url.strip():
        raise MoyasarHarnessError("callback_url is required")
    amount_halalas = int(round(amount_sar * 100))
    if amount_halalas < MIN_AMOUNT_HALALAS:
        raise MoyasarHarnessError(
            f"amount {amount_halalas} halalas below Moyasar minimum {MIN_AMOUNT_HALALAS}"
        )
    if amount_halalas > MAX_AMOUNT_HALALAS:
        raise MoyasarHarnessError(
            f"amount {amount_halalas} halalas above safety cap {MAX_AMOUNT_HALALAS}"
        )
    return MoyasarPaymentRequest(
        amount_halalas=amount_halalas,
        currency=MOYASAR_CURRENCY,
        description=description.strip(),
        callback_url=callback_url.strip(),
        metadata=dict(metadata or {}),
    )


def verify_webhook_hmac(*, secret: str, body: bytes, signature_hex: str) -> bool:
    """Constant-time HMAC-SHA256 verification of a Moyasar webhook body."""
    if not secret or not signature_hex:
        return False
    expected = hmac.new(secret.encode("utf-8"), body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature_hex)


def parse_webhook_event(body: bytes) -> MoyasarWebhookEvent:
    """Parse a Moyasar webhook body into a typed event. Raises on malformed input."""
    try:
        raw = json.loads(body.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise MoyasarHarnessError(f"webhook body is not valid JSON: {exc}") from exc
    if not isinstance(raw, dict):
        raise MoyasarHarnessError("webhook body must be a JSON object")
    event_type = str(raw.get("type", "")).strip()
    data = raw.get("data", {}) if isinstance(raw.get("data"), dict) else {}
    payment_id = str(data.get("id", "")).strip()
    status = str(data.get("status", "")).strip()
    if not event_type or not payment_id:
        raise MoyasarHarnessError("webhook missing type or data.id")
    amount = data.get("amount", 0)
    try:
        amount_halalas = int(amount)
    except (TypeError, ValueError):
        amount_halalas = 0
    metadata_raw = data.get("metadata", {}) or {}
    metadata = {
        str(k): str(v) for k, v in metadata_raw.items() if isinstance(metadata_raw, dict)
    }
    return MoyasarWebhookEvent(
        type=event_type,
        payment_id=payment_id,
        status=status,
        amount_halalas=amount_halalas,
        currency=str(data.get("currency", MOYASAR_CURRENCY)),
        metadata=metadata,
    )


__all__ = [
    "MAX_AMOUNT_HALALAS",
    "MIN_AMOUNT_HALALAS",
    "MOYASAR_CURRENCY",
    "MoyasarHarnessError",
    "MoyasarPaymentRequest",
    "MoyasarWebhookEvent",
    "build_payment_request",
    "enforce_test_mode",
    "parse_webhook_event",
    "verify_webhook_hmac",
]
