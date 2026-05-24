"""
Tap.company client — Charges + Webhook verification.

Ref: https://developers.tap.company/reference/api-endpoint

Backup processor to Moyasar. Switching costs are minimised by keeping the
public interface shape parallel to :class:`MoyasarClient`.

Security model:
  - API key in TAP_SECRET_KEY (HTTP Bearer auth)
  - Webhooks authenticated via HMAC-SHA256 over the canonical "hashstring"
    representation that Tap sends with the `Tap-Signature` header, compared
    in constant time against TAP_WEBHOOK_SECRET.

Amount handling:
  - Tap accepts amounts in MAJOR units (e.g. 1.00 SAR), unlike Moyasar which
    uses halalas. Callers should pass major-unit floats; this client never
    silently converts.
"""

from __future__ import annotations

import hashlib
import hmac
import logging
import os
from typing import Any

import httpx

log = logging.getLogger(__name__)

# ISO 4217 currencies Tap supports for KSA-native flows. Restrict to the set
# Dealix actually invoices in to surface configuration mistakes fast.
_ALLOWED_CURRENCIES: frozenset[str] = frozenset({"SAR", "AED", "BHD", "KWD", "OMR", "QAR", "USD"})


class TapClient:
    BASE = "https://api.tap.company/v2"

    def __init__(self, secret_key: str | None = None) -> None:
        self.secret_key = secret_key or os.getenv("TAP_SECRET_KEY", "")
        self._auth_header = {"Authorization": f"Bearer {self.secret_key}"}

    def _headers(self) -> dict[str, str]:
        return {**self._auth_header, "Content-Type": "application/json"}

    async def create_charge(
        self,
        amount: float,
        currency: str = "SAR",
        description: str = "",
        callback_url: str | None = None,
        metadata: dict[str, str] | None = None,
        customer: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Create a hosted Tap charge. Returns the charge object whose
        ``transaction.url`` field is the hosted checkout URL the customer
        visits to pay.

        Amount is in MAJOR units (e.g. 99.00 SAR) — Tap converts internally.
        """
        if not self.secret_key:
            raise RuntimeError("TAP_SECRET_KEY not set")
        if currency not in _ALLOWED_CURRENCIES:
            raise ValueError(f"unsupported_currency: {currency}")
        if amount is None or float(amount) <= 0:
            raise ValueError("amount must be > 0")

        payload: dict[str, Any] = {
            "amount": float(amount),
            "currency": currency,
            "description": description or "Dealix subscription",
            "customer": customer or {"first_name": "Dealix", "email": "billing@dealix.sa"},
            "source": {"id": "src_all"},  # let Tap show all enabled methods
        }
        if callback_url:
            # Tap calls these `redirect` (post-payment) and `post` (webhook).
            payload["redirect"] = {"url": callback_url}
            payload["post"] = {"url": callback_url}
        if metadata:
            payload["metadata"] = {k: str(v) for k, v in metadata.items()}

        async with httpx.AsyncClient(timeout=15) as c:
            r = await c.post(f"{self.BASE}/charges", headers=self._headers(), json=payload)
            r.raise_for_status()
            return r.json()

    async def fetch_charge(self, charge_id: str) -> dict[str, Any]:
        """Look up a Tap charge by id (e.g. ``chg_TS01A...``)."""
        if not self.secret_key:
            raise RuntimeError("TAP_SECRET_KEY not set")
        if not charge_id:
            raise ValueError("charge_id required")
        async with httpx.AsyncClient(timeout=15) as c:
            r = await c.get(f"{self.BASE}/charges/{charge_id}", headers=self._headers())
            r.raise_for_status()
            return r.json()


def _hashstring_from_body(body: dict[str, Any]) -> str:
    """
    Build the Tap "hashstring" payload that the signature is computed over.

    Tap's documented format concatenates a stable, ordered subset of fields:
        x_id<id>x_amount<amount>x_currency<currency>x_gateway_reference<ref>
        x_payment_reference<pay_ref>x_status<status>x_created<created>

    Missing fields are treated as empty strings so verification is robust
    against partial payloads (test events, refund events, etc.).
    """
    def s(v: Any) -> str:
        return "" if v is None else str(v)

    reference = body.get("reference") or {}
    return (
        f"x_id{s(body.get('id'))}"
        f"x_amount{s(body.get('amount'))}"
        f"x_currency{s(body.get('currency'))}"
        f"x_gateway_reference{s(reference.get('gateway'))}"
        f"x_payment_reference{s(reference.get('payment'))}"
        f"x_status{s(body.get('status'))}"
        f"x_created{s(body.get('transaction', {}).get('created'))}"
    )


def verify_webhook(
    body: dict[str, Any],
    header_signature: str | None,
    expected_secret: str | None = None,
) -> bool:
    """
    Verify a Tap webhook by recomputing HMAC-SHA256 over the canonical
    hashstring of ``body`` using ``TAP_WEBHOOK_SECRET`` and comparing in
    constant time to the value Tap sent in the ``Tap-Signature`` header.

    Returns False on any missing-input / mismatch path. Never raises.
    """
    expected = expected_secret or os.getenv("TAP_WEBHOOK_SECRET", "")
    if not expected:
        log.warning("tap_webhook_no_secret_configured")
        return False
    if not header_signature:
        return False
    try:
        hashstring = _hashstring_from_body(body)
        computed = hmac.new(
            expected.encode("utf-8"),
            hashstring.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
    except Exception:  # pragma: no cover — defensive
        return False
    return hmac.compare_digest(computed, str(header_signature))
