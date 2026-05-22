"""
Billing Gateway — Moyasar-compatible sandbox payment links and webhooks.

  POST /api/v1/billing/create-link
  GET  /api/v1/billing/status/{payment_id}
  POST /api/v1/billing/webhook
  GET  /api/v1/billing/invoices
  POST /api/v1/billing/simulate-success/{payment_id}
"""

from __future__ import annotations

import logging
import uuid
from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel, EmailStr

from auto_client_acquisition.governance_os.runtime_decision import decide

router = APIRouter(prefix="/api/v1/billing", tags=["billing-gateway"])
log = logging.getLogger(__name__)

# In-memory invoice store keyed by payment_id
_invoices: dict[str, dict[str, Any]] = {}

_SANDBOX_BASE_URL = "https://api.moyasar.com/v1/invoices"


# ---------------------------------------------------------------------------
# Pydantic models
# ---------------------------------------------------------------------------


class PaymentLinkRequest(BaseModel):
    client_name: str
    client_email: EmailStr
    amount_sar: float
    description: str
    offer_tier: str


class PaymentLinkResponse(BaseModel):
    payment_id: str
    checkout_url: str
    amount_sar: float
    status: str
    created_at: str


class WebhookEvent(BaseModel):
    event_type: str
    payment_id: str
    amount: float
    status: str
    metadata: dict[str, Any] = {}


# ---------------------------------------------------------------------------
# Pure-function helpers
# ---------------------------------------------------------------------------


def _new_payment_id() -> str:
    return f"pay_{uuid.uuid4().hex[:16]}"


def _utcnow_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _build_checkout_url(payment_id: str) -> str:
    return f"{_SANDBOX_BASE_URL}/{payment_id}"


def create_payment_link(req: PaymentLinkRequest) -> dict[str, Any]:
    """Create a sandbox payment link record and return it."""
    payment_id = _new_payment_id()
    record: dict[str, Any] = {
        "payment_id": payment_id,
        "checkout_url": _build_checkout_url(payment_id),
        "amount_sar": req.amount_sar,
        "status": "pending",
        "client_name": req.client_name,
        "client_email": req.client_email,
        "description": req.description,
        "offer_tier": req.offer_tier,
        "created_at": _utcnow_iso(),
        "updated_at": _utcnow_iso(),
    }
    _invoices[payment_id] = record
    return record


def get_invoice(payment_id: str) -> dict[str, Any] | None:
    return _invoices.get(payment_id)


def apply_webhook_event(event: WebhookEvent) -> dict[str, Any] | None:
    """Update invoice status from a webhook event. Returns updated record or None."""
    record = _invoices.get(event.payment_id)
    if record is None:
        return None
    record["status"] = event.status
    record["updated_at"] = _utcnow_iso()
    record["last_webhook_event"] = event.event_type
    return record


def simulate_payment_success(payment_id: str) -> dict[str, Any] | None:
    """Mark a sandbox payment as paid."""
    record = _invoices.get(payment_id)
    if record is None:
        return None
    record["status"] = "paid"
    record["updated_at"] = _utcnow_iso()
    record["paid_at"] = _utcnow_iso()
    return record


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------


@router.post("/create-link", response_model=None)
async def create_link(req: PaymentLinkRequest) -> dict[str, Any]:
    """Generate a sandbox payment link."""
    gov = decide(action_type="billing_create_link", context={"amount": req.amount_sar})
    record = create_payment_link(req)
    log.info("billing_link_created payment_id=%s amount=%s", record["payment_id"], req.amount_sar)
    return {"governance_decision": gov.decision, **record}


@router.get("/status/{payment_id}")
async def payment_status(payment_id: str) -> dict[str, Any]:
    """Return current payment status."""
    gov = decide(action_type="billing_status", context={})
    record = get_invoice(payment_id)
    if record is None:
        raise HTTPException(status_code=404, detail="payment_not_found")
    return {"governance_decision": gov.decision, **record}


@router.post("/webhook")
async def moyasar_webhook(
    event: WebhookEvent,
    x_moyasar_signature: str | None = Header(default=None, alias="X-Moyasar-Signature"),
) -> dict[str, Any]:
    """Handle inbound Moyasar webhook event."""
    if x_moyasar_signature is None:
        log.warning("moyasar_webhook_missing_signature payment_id=%s", event.payment_id)
        # In sandbox mode: log and continue; do not block.

    gov = decide(action_type="billing_webhook", context={"event_type": event.event_type})
    record = apply_webhook_event(event)
    if record is None:
        log.warning("moyasar_webhook_unknown_payment payment_id=%s", event.payment_id)
        return {"governance_decision": gov.decision, "status": "unknown_payment", "payment_id": event.payment_id}

    log.info("billing_webhook_processed payment_id=%s status=%s", event.payment_id, record["status"])
    return {"governance_decision": gov.decision, "status": "processed", "payment": record}


@router.get("/invoices")
async def list_invoices() -> dict[str, Any]:
    """List all invoices."""
    gov = decide(action_type="billing_list_invoices", context={})
    return {
        "governance_decision": gov.decision,
        "count": len(_invoices),
        "invoices": list(_invoices.values()),
    }


@router.post("/simulate-success/{payment_id}")
async def simulate_success(payment_id: str) -> dict[str, Any]:
    """Sandbox: mark payment as paid (no live charge)."""
    gov = decide(action_type="billing_simulate_success", context={})
    record = simulate_payment_success(payment_id)
    if record is None:
        raise HTTPException(status_code=404, detail="payment_not_found")
    log.info("billing_simulate_success payment_id=%s", payment_id)
    return {
        "governance_decision": gov.decision,
        "sandbox_only": True,
        "payment": record,
    }
