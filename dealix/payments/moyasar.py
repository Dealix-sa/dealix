"""
Moyasar client — Invoices + Payments + Hosted Payment Pages + Webhook verification.
Ref: https://docs.moyasar.com/api/invoices/01-create-invoice
     https://docs.moyasar.com/api/other/webhooks/webhook-reference/

Security model:
  - API key in MOYASAR_SECRET_KEY (HTTP Basic auth, key is the username).
  - Webhooks authenticated via a shared secret_token included in the webhook body
    and compared in constant time against MOYASAR_WEBHOOK_SECRET.
  - Live-charge gate: MoyasarLiveGateError is raised on any LIVE charge attempt
    unless moyasar_mode == "live" AND moyasar_live_verified is True.
    Non-Negotiable #6 (no live charge without approval) enforced here.

Amount is in the smallest currency unit (SAR halalas) — 10 SAR = 1000.
"""

from __future__ import annotations

import base64
import hmac
import logging
import os
import time
from typing import Any

import httpx

log = logging.getLogger(__name__)


class MoyasarLiveGateError(RuntimeError):
    """Raised when a live Moyasar action is attempted without explicit gate."""


class MoyasarAccountInactiveError(RuntimeError):
    """Raised when Moyasar reports the account is not activated."""


class MoyasarClient:
    BASE = "https://api.moyasar.com/v1"
    _account_status_cache: dict[str, tuple[float, dict[str, Any]]] = {}
    _CACHE_TTL_SECONDS = 300

    def __init__(
        self,
        secret_key: str | None = None,
        *,
        mode: str | None = None,
        live_verified: bool | None = None,
    ) -> None:
        self.secret_key = secret_key or os.getenv("MOYASAR_SECRET_KEY", "")
        # Mode + verification are explicit. Falling back to Settings only if
        # neither is passed and the env vars are unset.
        if mode is None or live_verified is None:
            try:
                from core.config.settings import get_settings

                s = get_settings()
                if mode is None:
                    mode = s.moyasar_mode
                if live_verified is None:
                    live_verified = s.moyasar_live_verified
            except Exception:  # noqa: BLE001 — settings optional in tests
                mode = mode or "test"
                live_verified = bool(live_verified)
        self.mode = mode or "test"
        self.live_verified = bool(live_verified)
        auth = base64.b64encode(f"{self.secret_key}:".encode()).decode()
        self._auth_header = {"Authorization": f"Basic {auth}"}

    def _headers(self) -> dict[str, str]:
        return {**self._auth_header, "Content-Type": "application/json"}

    def _enforce_live_gate(self, *, amount_halalas: int) -> None:
        """Block any live charge unless mode==live AND live_verified==True.

        Non-Negotiable #6: NO live charge without approval. The gate also
        requires a positive amount to avoid no-op test bypass.
        """
        if self.mode == "test":
            return
        if not self.live_verified:
            raise MoyasarLiveGateError(
                "moyasar_live_gate_blocked: mode=live but live_verified=False. "
                "Set MOYASAR_LIVE_VERIFIED=true only after account activation "
                "is confirmed via verify_account_status()."
            )
        if amount_halalas <= 0:
            raise MoyasarLiveGateError(
                "moyasar_live_gate_blocked: amount must be > 0 halalas in live mode."
            )

    async def verify_account_status(self, *, force_refresh: bool = False) -> dict[str, Any]:
        """Probe Moyasar to confirm account is activated.

        Cached for 5 minutes per secret key to avoid hammering the API.
        Returns the account info dict on success; raises
        MoyasarAccountInactiveError if Moyasar returns account_inactive_error.
        """
        if not self.secret_key:
            raise RuntimeError("MOYASAR_SECRET_KEY not set")

        cache_key = self.secret_key
        now = time.time()
        if not force_refresh:
            cached = self._account_status_cache.get(cache_key)
            if cached and (now - cached[0]) < self._CACHE_TTL_SECONDS:
                return cached[1]

        # Moyasar does not expose a dedicated account-status endpoint, but
        # listing payments with limit=1 confirms whether the account is
        # activated. If inactive, Moyasar returns 400 with account_inactive_error.
        async with httpx.AsyncClient(timeout=10) as c:
            r = await c.get(
                f"{self.BASE}/payments",
                headers=self._headers(),
                params={"limit": 1},
            )
        if r.status_code == 200:
            info = {"active": True, "mode": self.mode, "checked_at": now}
            self._account_status_cache[cache_key] = (now, info)
            return info
        # Inactive account surfaces an explicit error type from Moyasar.
        try:
            err = r.json()
        except Exception:  # noqa: BLE001
            err = {"raw": r.text}
        if err.get("type") == "account_inactive_error":
            raise MoyasarAccountInactiveError(
                f"moyasar_account_inactive: {err.get('message', 'see KYC dashboard')}"
            )
        r.raise_for_status()
        return err

    async def create_invoice(
        self,
        amount_halalas: int,
        currency: str = "SAR",
        description: str = "",
        callback_url: str | None = None,
        metadata: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """
        Create a hosted payment invoice. Returns invoice object with `url` field
        that the customer visits to pay.
        """
        if not self.secret_key:
            raise RuntimeError("MOYASAR_SECRET_KEY not set")
        self._enforce_live_gate(amount_halalas=amount_halalas)
        payload: dict[str, Any] = {
            "amount": int(amount_halalas),
            "currency": currency,
            "description": description or "Dealix subscription",
        }
        if callback_url:
            payload["callback_url"] = callback_url
        if metadata:
            payload["metadata"] = {k: str(v) for k, v in metadata.items()}

        async with httpx.AsyncClient(timeout=15) as c:
            r = await c.post(f"{self.BASE}/invoices", headers=self._headers(), json=payload)
            r.raise_for_status()
            return r.json()

    async def create_hosted_payment(
        self,
        *,
        amount_halalas: int,
        offer_id: str,
        source_passport_id: str,
        callback_url: str,
        customer_handle: str | None = None,
        locale: str = "ar",
        currency: str = "SAR",
        idempotency_key: str | None = None,
    ) -> dict[str, Any]:
        """
        Phase 1: self-serve hosted payment for the 5 productized offers.

        Requires a Source Passport ID (Non-Negotiable #10) and an offer ID.
        The returned dict carries `url` (HPP) and `id` (invoice id) that the
        caller stores against the OfferCheckoutService idempotency key.
        """
        if not source_passport_id:
            raise ValueError("source_passport_id is required (Non-Negotiable #10)")
        if not offer_id:
            raise ValueError("offer_id is required")

        description_ar = f"Dealix — {offer_id}"
        description_en = f"Dealix — {offer_id}"
        description = description_ar if locale == "ar" else description_en

        metadata = {
            "offer_id": offer_id,
            "source_passport_id": source_passport_id,
            "locale": locale,
            "customer_handle": customer_handle or "anonymous",
        }
        if idempotency_key:
            metadata["idempotency_key"] = idempotency_key

        return await self.create_invoice(
            amount_halalas=amount_halalas,
            currency=currency,
            description=description,
            callback_url=callback_url,
            metadata=metadata,
        )

    async def fetch_payment(self, payment_id: str) -> dict[str, Any]:
        if not self.secret_key:
            raise RuntimeError("MOYASAR_SECRET_KEY not set")
        async with httpx.AsyncClient(timeout=10) as c:
            r = await c.get(f"{self.BASE}/payments/{payment_id}", headers=self._headers())
            r.raise_for_status()
            return r.json()

    async def fetch_invoice(self, invoice_id: str) -> dict[str, Any]:
        if not self.secret_key:
            raise RuntimeError("MOYASAR_SECRET_KEY not set")
        async with httpx.AsyncClient(timeout=10) as c:
            r = await c.get(f"{self.BASE}/invoices/{invoice_id}", headers=self._headers())
            r.raise_for_status()
            return r.json()


def verify_webhook(body: dict[str, Any], expected_secret: str | None = None) -> bool:
    """
    Moyasar webhook verification.
    Webhooks include a `secret_token` field in the JSON body which is the per-endpoint
    secret the merchant set when registering the webhook. Compare in constant time.
    """
    expected = expected_secret or os.getenv("MOYASAR_WEBHOOK_SECRET", "")
    if not expected:
        log.warning("moyasar_webhook_no_secret_configured")
        return False
    provided = str(body.get("secret_token") or "")
    if not provided:
        return False
    return hmac.compare_digest(provided, expected)
