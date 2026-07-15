"""
Hyperpay client — parallel-to-Moyasar Saudi PSP.

Wired as part of Track 2 of the 180-day Build-Out Plan to ensure revenue
is uncoupled from any single PSP's KYC timeline. If Moyasar account
activation stalls, Hyperpay carries production traffic.

Hyperpay (https://hyperpay.com) is a KSA-licensed PSP supporting Mada,
Visa, Mastercard, Apple Pay, STC Pay, Tabby, Tamara. Webhooks signed
via HMAC-SHA256 with shared secret.

Security model:
  - API key in HYPERPAY_ACCESS_TOKEN (Bearer auth)
  - Entity ID in HYPERPAY_ENTITY_ID (account identifier)
  - Webhooks authenticated via X-Hyperpay-Signature header
  - Amount is in major currency units (10.00 SAR = "10.00")

Mirrors the surface of dealix/payments/moyasar.py to enable PSP-router
selection by region/customer preference.

Status: SCAFFOLDED (Day 1 of plan). Sandbox keys wired Day 1–7;
live keys + webhook + 1 SAR live charge by Day 14.
"""

from __future__ import annotations

import hashlib
import hmac
import logging
import os
from decimal import Decimal
from typing import Any

import httpx

log = logging.getLogger(__name__)


class HyperpayClient:
    """Hyperpay COPYandPAY + Server-to-Server API client."""

    SANDBOX_BASE = "https://eu-test.oppwa.com/v1"
    LIVE_BASE = "https://eu-prod.oppwa.com/v1"

    def __init__(
        self,
        access_token: str | None = None,
        entity_id: str | None = None,
        live: bool | None = None,
    ) -> None:
        self.access_token = access_token or os.getenv("HYPERPAY_ACCESS_TOKEN", "")
        self.entity_id = entity_id or os.getenv("HYPERPAY_ENTITY_ID", "")
        env_live = os.getenv("HYPERPAY_LIVE", "false").lower() in ("true", "1", "yes")
        self.live = env_live if live is None else live
        self.base = self.LIVE_BASE if self.live else self.SANDBOX_BASE

    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/x-www-form-urlencoded",
        }

    async def create_checkout(
        self,
        amount_sar: Decimal | float | str,
        currency: str = "SAR",
        merchant_transaction_id: str | None = None,
        customer_email: str | None = None,
        billing_descriptor: str = "Dealix",
        metadata: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """
        Create a checkout session. Returns checkout object with `id` field
        used to render the embedded form, and a redirect URL on completion.

        Amount is in major units (e.g., "10.00" = 10 SAR).
        """
        if not self.access_token or not self.entity_id:
            raise RuntimeError("HYPERPAY_ACCESS_TOKEN / HYPERPAY_ENTITY_ID not set")

        amount_str = f"{Decimal(str(amount_sar)):.2f}"
        payload: dict[str, Any] = {
            "entityId": self.entity_id,
            "amount": amount_str,
            "currency": currency,
            "paymentType": "DB",  # debit
            "billing.descriptor": billing_descriptor,
        }
        if merchant_transaction_id:
            payload["merchantTransactionId"] = merchant_transaction_id
        if customer_email:
            payload["customer.email"] = customer_email
        if metadata:
            for k, v in metadata.items():
                payload[f"customParameters[{k}]"] = v

        async with httpx.AsyncClient(timeout=30.0) as http:
            r = await http.post(
                f"{self.base}/checkouts",
                headers=self._headers(),
                data=payload,
            )
            r.raise_for_status()
            return r.json()

    async def get_payment_status(self, payment_id: str) -> dict[str, Any]:
        """
        Retrieve payment status by ID. Returns full payment object.
        """
        if not self.access_token or not self.entity_id:
            raise RuntimeError("HYPERPAY_ACCESS_TOKEN / HYPERPAY_ENTITY_ID not set")

        async with httpx.AsyncClient(timeout=30.0) as http:
            r = await http.get(
                f"{self.base}/payments/{payment_id}",
                headers=self._headers(),
                params={"entityId": self.entity_id},
            )
            r.raise_for_status()
            return r.json()

    async def refund(
        self,
        payment_id: str,
        amount_sar: Decimal | float | str,
        currency: str = "SAR",
    ) -> dict[str, Any]:
        """
        Refund a payment, fully or partially. Returns refund object.
        """
        if not self.access_token or not self.entity_id:
            raise RuntimeError("HYPERPAY_ACCESS_TOKEN / HYPERPAY_ENTITY_ID not set")

        amount_str = f"{Decimal(str(amount_sar)):.2f}"
        payload = {
            "entityId": self.entity_id,
            "amount": amount_str,
            "currency": currency,
            "paymentType": "RF",  # refund
        }
        async with httpx.AsyncClient(timeout=30.0) as http:
            r = await http.post(
                f"{self.base}/payments/{payment_id}",
                headers=self._headers(),
                data=payload,
            )
            r.raise_for_status()
            return r.json()


def verify_webhook(
    body: bytes,
    signature_header: str,
    webhook_secret: str | None = None,
) -> bool:
    """
    Verify a Hyperpay webhook signature.

    Hyperpay signs the raw body with HMAC-SHA256 using a shared secret;
    the signature is sent in the X-Hyperpay-Signature header (hex digest).

    Use constant-time comparison to prevent timing attacks.
    """
    secret = webhook_secret or os.getenv("HYPERPAY_WEBHOOK_SECRET", "")
    if not secret:
        log.warning("HYPERPAY_WEBHOOK_SECRET not set — rejecting webhook")
        return False
    if not signature_header:
        return False

    expected = hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature_header.strip())


__all__ = ["HyperpayClient", "verify_webhook"]
