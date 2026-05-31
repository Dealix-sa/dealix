"""Customer-side webhook subscription endpoints (W12.1).

Customers (and via R6 White-Label, agency partners) subscribe their
own HTTPS endpoints to Dealix events. Enables real-time integrations
without polling.

Supported event types (kept in sync with internal emitters):
  lead.created          — new lead enters tenant pipeline
  lead.replied          — Arabic-reply detected (R3 billing event)
  lead.demo_booked      — Calendar booking detected (R3 billing event)
  payment.received      — Moyasar webhook successful upsert
  decision_passport.entry_added  — new audit entry on external commitment
  tenant.usage.over_cap          — leads_per_month exceeded
  tenant.health.score_changed    — Health Score band changed

Endpoints:

  POST   /api/v1/customer-webhooks/{handle}/subscribe   (admin)
         Register a subscription. Validates URL (HTTPS only), event_types,
         generates secret for HMAC signing.

  GET    /api/v1/customer-webhooks/{handle}              (admin)
         List active subscriptions for a tenant.

  DELETE /api/v1/customer-webhooks/{handle}/{subscription_id}  (admin)
         Unsubscribe an endpoint.

  POST   /api/v1/customer-webhooks/{handle}/ping/{subscription_id}  (admin)
         Send a test delivery to verify the customer's endpoint.

Security:
  - All endpoints require admin key (only Dealix or tenant-authorized
    actor can manage subscriptions; future: tenant-scoped JWT)
  - URLs must be HTTPS (HTTP rejected — prevents MITM event leak)
  - Secrets generated server-side, never customer-supplied
  - HMAC-SHA256 signature on every delivery (X-Dealix-Signature header)
"""
from __future__ import annotations

import hashlib
import hmac
import logging
import re
import secrets
import time
from datetime import UTC, datetime, timezone
from typing import Any

from fastapi import APIRouter, Depends, Header, HTTPException, Path, Request
from pydantic import BaseModel, ConfigDict, Field

from api.security.api_key import require_admin_key
from core.config.settings import get_settings

log = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/v1/customer-webhooks",
    tags=["customer-webhooks"],
    dependencies=[Depends(require_admin_key)],
)

# Inbound deliveries authenticate via HMAC signature (X-Dealix-Signature),
# not the admin key, so they live on a separate router without the
# admin-key dependency.
inbound_router = APIRouter(
    prefix="/api/v1/customer-webhooks",
    tags=["customer-webhooks"],
)

SIGNATURE_HEADER = "X-Dealix-Signature"


SUPPORTED_EVENT_TYPES = {
    "lead.created",
    "lead.replied",
    "lead.demo_booked",
    "payment.received",
    "decision_passport.entry_added",
    "tenant.usage.over_cap",
    "tenant.health.score_changed",
}


class _SubscribeRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    url: str = Field(..., min_length=10, max_length=2048)
    event_types: list[str] = Field(..., min_length=1, max_length=20)


def _validate_https_url(url: str) -> bool:
    """Reject any URL that isn't HTTPS. Blocks data:, file:, http:."""
    if not url.startswith("https://"):
        return False
    return not bool(re.search(r"[\s<>\"\\'`]", url))


def _validate_event_types(event_types: list[str]) -> str | None:
    """Return error message if any event_type is unsupported."""
    invalid = [e for e in event_types if e not in SUPPORTED_EVENT_TYPES]
    if invalid:
        return (
            f"unsupported event types: {invalid}. "
            f"Valid: {sorted(SUPPORTED_EVENT_TYPES)}"
        )
    return None


def _generate_subscription_id(tenant_id: str, url: str) -> str:
    seed = f"{tenant_id}:{url}:{time.time()}"
    return f"cwh_{hashlib.sha256(seed.encode()).hexdigest()[:20]}"


def _generate_secret() -> str:
    """64-char hex (256-bit) signing secret."""
    return secrets.token_hex(32)


def _expected_signature(secret: str, body: bytes) -> str:
    """HMAC-SHA256(secret, raw_body) as lowercase hex."""
    return hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()


def verify_inbound_signature(*, secret: str, body: bytes, signature: str | None) -> bool:
    """Constant-time HMAC-SHA256 check of an inbound webhook signature.

    The header may carry an optional ``sha256=`` prefix. Returns False for a
    missing secret or signature so the caller can decide how to respond.
    """
    if not secret or not signature:
        return False
    provided = signature.strip().removeprefix("sha256=")
    expected = _expected_signature(secret, body)
    return hmac.compare_digest(expected, provided)


# Literal route declared before the parameterized GET /{handle} so it is not
# shadowed by the handle matcher during routing.
@router.get("/_supported-events")
async def list_supported_events() -> dict[str, Any]:
    """Return the set of event types a customer may subscribe to."""
    return {
        "event_types": sorted(SUPPORTED_EVENT_TYPES),
        "signature_header": SIGNATURE_HEADER,
        "signature_algorithm": "HMAC-SHA256(secret, raw_body)",
        "delivery_semantics": "at-least-once",
        "retry_policy": "exponential backoff 5 attempts over 24 hours "
                        "(deferred to follow-up commit)",
    }


@router.post("/{handle}/subscribe", status_code=201)
async def subscribe_webhook(
    body: _SubscribeRequest,
    handle: str = Path(..., pattern=r"^[a-z][a-z0-9_]{1,62}[a-z0-9]$"),
) -> dict[str, Any]:
    """Register a webhook subscription for a tenant. Returns subscription_id + secret.

    The secret is shown ONCE in this response — caller must store it. It is used
    to compute the HMAC-SHA256 X-Dealix-Signature on deliveries, and to verify
    the signature on inbound callbacks (see POST .../inbound).
    """
    if not _validate_https_url(body.url):
        raise HTTPException(
            status_code=400,
            detail="url must be HTTPS only (no http://, no data:, no javascript:)",
        )
    err = _validate_event_types(body.event_types)
    if err:
        raise HTTPException(status_code=400, detail=err)

    try:
        from sqlalchemy import select

        from db.models import CustomerWebhookSubscription, TenantRecord
        from db.session import async_session_factory
    except Exception:
        raise HTTPException(status_code=503, detail="DB layer unavailable")

    async with async_session_factory()() as session:
        tenant = (
            await session.execute(
                select(TenantRecord).where(TenantRecord.slug == handle)
            )
        ).scalar_one_or_none()
        if tenant is None:
            raise HTTPException(
                status_code=404, detail=f"tenant {handle!r} not found"
            )

        subscription_id = _generate_subscription_id(tenant.id, body.url)
        secret = _generate_secret()

        sub = CustomerWebhookSubscription(
            id=subscription_id,
            tenant_id=tenant.id,
            url=body.url,
            secret=secret,
            event_types=body.event_types,
            is_active=True,
        )
        session.add(sub)
        await session.commit()

    log.info(
        "customer_webhook_subscribed id=%s tenant=%s events=%d",
        subscription_id, handle, len(body.event_types),
    )
    return {
        "subscription_id": subscription_id,
        "tenant_handle": handle,
        "url": body.url,
        "event_types": body.event_types,
        "secret": secret,
        "secret_note": (
            "STORE THIS SECRET NOW — it will NOT be shown again. "
            "Used to verify HMAC-SHA256 signatures on incoming events "
            "via the X-Dealix-Signature header."
        ),
        "signature_algorithm": "HMAC-SHA256(secret, raw_body)",
    }


@router.get("/{handle}")
async def list_webhooks(
    handle: str = Path(..., pattern=r"^[a-z][a-z0-9_]{1,62}[a-z0-9]$"),
) -> dict[str, Any]:
    """List a tenant's active webhook subscriptions. Secrets are NEVER returned."""
    try:
        from sqlalchemy import select

        from db.models import CustomerWebhookSubscription, TenantRecord
        from db.session import async_session_factory
    except Exception:
        raise HTTPException(status_code=503, detail="DB layer unavailable")

    async with async_session_factory()() as session:
        tenant = (
            await session.execute(
                select(TenantRecord).where(TenantRecord.slug == handle)
            )
        ).scalar_one_or_none()
        if tenant is None:
            raise HTTPException(status_code=404, detail=f"tenant {handle!r} not found")

        subs = (
            await session.execute(
                select(CustomerWebhookSubscription).where(
                    CustomerWebhookSubscription.tenant_id == tenant.id
                )
            )
        ).scalars().all()

    return {
        "tenant_handle": handle,
        "subscriptions": [
            {
                "id": s.id,
                "url": s.url,
                "event_types": s.event_types,
                "is_active": s.is_active,
                "last_delivery_at": s.last_delivery_at.isoformat() if s.last_delivery_at else None,
                "last_delivery_status": s.last_delivery_status,
                "consecutive_failures": s.consecutive_failures,
                "created_at": s.created_at.isoformat() if s.created_at else None,
            }
            for s in subs
        ],
    }


@router.delete("/{handle}/{subscription_id}")
async def unsubscribe_webhook(
    handle: str = Path(..., pattern=r"^[a-z][a-z0-9_]{1,62}[a-z0-9]$"),
    subscription_id: str = Path(..., pattern=r"^cwh_[a-f0-9]{20}$"),
) -> dict[str, Any]:
    """Soft-delete a subscription (sets is_active=False; row retained for audit)."""
    try:
        from sqlalchemy import select

        from db.models import CustomerWebhookSubscription, TenantRecord
        from db.session import async_session_factory
    except Exception:
        raise HTTPException(status_code=503, detail="DB layer unavailable")

    async with async_session_factory()() as session:
        tenant = (
            await session.execute(
                select(TenantRecord).where(TenantRecord.slug == handle)
            )
        ).scalar_one_or_none()
        if tenant is None:
            raise HTTPException(status_code=404, detail=f"tenant {handle!r} not found")

        sub = (
            await session.execute(
                select(CustomerWebhookSubscription).where(
                    CustomerWebhookSubscription.id == subscription_id,
                    CustomerWebhookSubscription.tenant_id == tenant.id,
                )
            )
        ).scalar_one_or_none()
        if sub is None:
            raise HTTPException(
                status_code=404,
                detail=f"subscription {subscription_id!r} not found for tenant",
            )

        sub.is_active = False
        sub.updated_at = datetime.now(UTC)
        await session.commit()

    log.info("customer_webhook_unsubscribed id=%s tenant=%s", subscription_id, handle)
    return {
        "status": "unsubscribed",
        "subscription_id": subscription_id,
        "tenant_handle": handle,
    }


@router.post("/{handle}/ping/{subscription_id}")
async def ping_subscription(
    handle: str = Path(..., pattern=r"^[a-z][a-z0-9_]{1,62}[a-z0-9]$"),
    subscription_id: str = Path(..., pattern=r"^cwh_[a-f0-9]{20}$"),
) -> dict[str, Any]:
    """Send a test 'dealix.ping' event to verify the customer's endpoint.

    Stub: real delivery requires httpx outbound + HMAC signing, deferred
    to follow-up commit. This endpoint validates the subscription exists
    and returns the payload shape that would be sent.
    """
    try:
        from sqlalchemy import select

        from db.models import CustomerWebhookSubscription, TenantRecord
        from db.session import async_session_factory
    except Exception:
        raise HTTPException(status_code=503, detail="DB layer unavailable")

    async with async_session_factory()() as session:
        tenant = (
            await session.execute(
                select(TenantRecord).where(TenantRecord.slug == handle)
            )
        ).scalar_one_or_none()
        if tenant is None:
            raise HTTPException(status_code=404, detail=f"tenant {handle!r} not found")

        sub = (
            await session.execute(
                select(CustomerWebhookSubscription).where(
                    CustomerWebhookSubscription.id == subscription_id,
                    CustomerWebhookSubscription.tenant_id == tenant.id,
                    CustomerWebhookSubscription.is_active.is_(True),
                )
            )
        ).scalar_one_or_none()
        if sub is None:
            raise HTTPException(
                status_code=404,
                detail=f"active subscription {subscription_id!r} not found",
            )

    payload = {
        "event_id": f"ping_{int(time.time())}",
        "event_type": "dealix.ping",
        "tenant_handle": handle,
        "delivered_at": datetime.now(UTC).isoformat(),
        "data": {
            "message": "If you see this in your endpoint, integration works.",
        },
    }
    return {
        "status": "pinged_in_memory",
        "subscription_id": subscription_id,
        "would_deliver_to": sub.url,
        "payload_preview": payload,
        "note": (
            "Real outbound delivery deferred to follow-up commit (W12.1.b). "
            "Schema + auth + DB + payload shape locked in this commit."
        ),
    }


@inbound_router.post("/inbound")
async def receive_inbound(
    request: Request,
    x_dealix_signature: str | None = Header(default=None, alias=SIGNATURE_HEADER),
) -> dict[str, Any]:
    """Receive an inbound webhook callback, authenticated by HMAC signature.

    The X-Dealix-Signature header must be HMAC-SHA256(secret, raw_body), hex
    encoded, optionally prefixed with ``sha256=``. Verification is constant-time.

    Secret resolution and unconfigured behaviour mirror the rest of the codebase:
      - secret configured + staging/production: missing/invalid signature -> 401
      - secret configured + dev/test: only a present-but-invalid signature -> 401
        (a missing signature is allowed so local tooling stays usable)
      - no secret configured: permissive, logs a warning (does not hard-fail)
    """
    body = await request.body()
    settings = get_settings()
    secret_obj = settings.customer_webhook_secret
    secret = secret_obj.get_secret_value() if secret_obj else ""
    has_secret = bool(secret)
    strict_env = settings.app_env in ("staging", "production")

    if not has_secret:
        log.warning("customer_webhook_inbound_no_secret_configured env=%s", settings.app_env)
    elif strict_env:
        if not verify_inbound_signature(
            secret=secret, body=body, signature=x_dealix_signature
        ):
            log.warning("customer_webhook_inbound_invalid_signature_strict_env")
            raise HTTPException(status_code=401, detail="missing_or_invalid_signature")
    elif x_dealix_signature is not None:
        if not verify_inbound_signature(
            secret=secret, body=body, signature=x_dealix_signature
        ):
            log.warning("customer_webhook_inbound_invalid_signature")
            raise HTTPException(status_code=401, detail="invalid_signature")

    return {
        "status": "accepted",
        "signature_verified": has_secret
        and verify_inbound_signature(
            secret=secret, body=body, signature=x_dealix_signature
        ),
        "bytes_received": len(body),
    }
