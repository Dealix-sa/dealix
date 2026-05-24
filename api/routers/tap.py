"""
Tap.company checkout + webhook endpoints.

Endpoints:
  POST /api/v1/checkout/tap         — create a Tap charge, return hosted URL
  POST /api/v1/webhooks/tap         — verify Tap-Signature, dedupe + DLQ on error

This router is the backup processor while Moyasar KYC activates. Plans are
sourced from :mod:`api.routers.pricing` (the single source of truth for
allowed plans and their amounts) so we cannot drift price tables across
processors.

Mirrors the structure of ``api/routers/pricing.py`` (Moyasar) — same
idempotency window, same DLQ queue, same fingerprinting / no-PII logging.
"""

from __future__ import annotations

import hashlib
import logging
import os
from typing import Any

from fastapi import APIRouter, Header, HTTPException, Request
from pydantic import BaseModel, EmailStr, Field

from dealix.payments import TapClient, verify_tap_webhook
from dealix.reliability.dlq import DLQ, WEBHOOKS_DLQ
from dealix.reliability.idempotency import IdempotencyStore

log = logging.getLogger(__name__)

router = APIRouter(tags=["pricing"])


def _fingerprint(value: str) -> str:
    if not value:
        return ""
    return hashlib.sha256(value.encode("utf-8")).hexdigest()[:12]


class TapCheckoutRequest(BaseModel):
    """Incoming /checkout/tap body."""

    plan: str = Field(..., min_length=1, max_length=64)
    email: EmailStr
    lead_id: str = Field(default="", max_length=128)
    name: str = Field(default="", max_length=128)


class TapCheckoutResponse(BaseModel):
    charge_id: str | None
    status: str | None
    amount_sar: float
    payment_url: str | None
    plan: str
    processor: str = "tap"


def _resolve_plan(plan: str) -> dict[str, Any]:
    """Look up plan in the canonical pricing table (single source of truth)."""
    # Imported lazily to avoid a circular import at module load.
    from api.routers.pricing import PLANS

    plan_info = PLANS.get(plan)
    if not plan_info:
        raise HTTPException(status_code=400, detail=f"unknown_plan: {plan}")
    return plan_info


@router.post("/api/v1/checkout/tap", response_model=TapCheckoutResponse)
async def create_tap_checkout(req: TapCheckoutRequest) -> TapCheckoutResponse:
    """Create a Tap charge for the requested plan and return the hosted URL."""
    plan = req.plan.lower()
    plan_info = _resolve_plan(plan)

    amount_sar = float(int(plan_info["amount_halalas"])) / 100.0
    callback_base = os.getenv("APP_URL", "https://dealix.sa")
    callback_url = f"{callback_base}/checkout/return"

    client = TapClient()
    customer: dict[str, Any] = {"email": str(req.email)}
    if req.name:
        customer["first_name"] = req.name

    try:
        charge = await client.create_charge(
            amount=amount_sar,
            currency="SAR",
            description=f"Dealix — {plan_info['name']}",
            callback_url=callback_url,
            metadata={
                "plan": plan,
                "lead_id": req.lead_id,
                "source": "dealix.checkout.tap",
                "email_fp": _fingerprint(str(req.email)),
            },
            customer=customer,
        )
    except RuntimeError as exc:
        # Missing key → 503 (we are not configured for this processor yet)
        log.error("tap_not_configured plan=%s email_fp=%s", plan, _fingerprint(str(req.email)))
        raise HTTPException(status_code=503, detail="tap_not_configured") from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        log.exception(
            "tap_charge_failed plan=%s email_fp=%s",
            plan,
            _fingerprint(str(req.email)),
        )
        raise HTTPException(status_code=502, detail="payment_provider_error") from exc

    transaction = charge.get("transaction") or {}
    return TapCheckoutResponse(
        charge_id=charge.get("id"),
        status=charge.get("status"),
        amount_sar=amount_sar,
        payment_url=transaction.get("url"),
        plan=plan,
    )


@router.post("/api/v1/webhooks/tap")
async def tap_webhook(
    req: Request,
    tap_signature: str | None = Header(default=None, alias="Tap-Signature"),
) -> dict[str, Any]:
    """
    Tap webhook receiver. Verifies HMAC-SHA256 over the body hashstring and
    dedupes by charge id. Failed processing → DLQ(webhooks) for replay.

    Always returns 200 once signature is valid so Tap stops retrying — we
    own replay via the DLQ.
    """
    try:
        body = await req.json()
    except Exception as exc:
        raise HTTPException(status_code=400, detail="invalid_json") from exc

    if not verify_tap_webhook(body, tap_signature):
        log.warning("tap_webhook_bad_signature")
        raise HTTPException(status_code=401, detail="bad_signature")

    event_id = str(body.get("id") or "")
    event_status = str(body.get("status") or "")
    event_fp = _fingerprint(event_id)
    idem = IdempotencyStore(prefix="idem:tap:")
    if event_id and not idem.claim(event_id, ttl_seconds=7 * 86400):
        log.info("tap_webhook_duplicate event_fp=%s", event_fp)
        return {"status": "duplicate", "id": event_id}

    try:
        log.info(
            "tap_webhook_processed event_fp=%s status=%s amount=%s currency=%s",
            event_fp,
            event_status,
            body.get("amount"),
            body.get("currency"),
        )
        # charge.succeeded / charge.failed handling. Side-effects mirror the
        # Moyasar flow but are intentionally minimal here: persistence and
        # downstream activation are wired in a follow-up PR once Tap KYC is
        # confirmed end-to-end.
        return {
            "status": "ok",
            "event_id": event_id,
            "event_status": event_status,
            "processor": "tap",
        }
    except Exception as exc:
        log.exception("tap_webhook_processing_failed event_fp=%s", event_fp)
        DLQ(WEBHOOKS_DLQ).push(
            source="tap.webhook",
            payload=body,
            error=str(exc)[:500],
            metadata={"event_id": event_id, "event_status": event_status},
        )
        return {"status": "dlq", "event_id": event_id}
