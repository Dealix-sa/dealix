"""Moyasar payment webhook receiver.

Endpoints:
  POST /api/v1/webhooks/moyasar   — receive and process Moyasar payment events
  GET  /api/v1/webhooks/moyasar/health — liveness probe

Constitutional gates:
- APPROVAL_FIRST: every paid event creates a FounderAlertRecord (no auto-action).
- NO_PII_IN_LOGS: customer name / email never appear in log lines.
- Returns HTTP 200 always so Moyasar does not retry on internal errors.
"""

from __future__ import annotations

import hashlib
import hmac
import os
from typing import Any

from fastapi import APIRouter, Header, Request
from fastapi.responses import JSONResponse

from core.logging import get_logger

log = get_logger(__name__)

router = APIRouter(
    prefix="/api/v1/webhooks/moyasar",
    tags=["Webhooks"],
)


def _verify_moyasar_hmac(body: bytes, signature: str | None, secret: str) -> bool:
    """
    Verify X-Moyasar-Signature header using HMAC-SHA256.

    Returns True when the signature is valid.
    Returns True in dev mode (no secret configured) so local testing is easy.
    """
    if not secret:
        return True
    if not signature:
        return False
    expected = hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)


@router.get("/health")
async def webhook_health() -> dict[str, str]:
    """Liveness probe for the Moyasar webhook receiver."""
    return {"status": "ok"}


@router.post("")
async def receive_moyasar_webhook(
    request: Request,
    x_moyasar_signature: str | None = Header(default=None, alias="X-Moyasar-Signature"),
) -> JSONResponse:
    """
    Receive a Moyasar webhook, verify HMAC, process and persist.

    Always returns HTTP 200 so Moyasar does not retry on internal errors.
    """
    raw_body = await request.body()

    # HMAC verification
    secret = os.getenv("MOYASAR_WEBHOOK_SECRET", "")
    if not _verify_moyasar_hmac(raw_body, x_moyasar_signature, secret):
        log.warning("moyasar_webhook_hmac_failed")
        # Still return 200 to avoid Moyasar retry storms, but do not process.
        return JSONResponse({"received": True, "processed": False, "reason": "invalid_signature"})

    try:
        body_json: dict[str, Any] = await request.json()
    except Exception as exc:
        log.warning("moyasar_webhook_parse_failed", error=str(exc))
        return JSONResponse({"received": True, "processed": False, "reason": "parse_error"})

    # Normalise webhook body
    try:
        from dealix.commercial.payment_events import (
            PaymentEventProcessor,
            normalize_moyasar_webhook,
        )

        event = normalize_moyasar_webhook(body_json)
        if event is None:
            log.info("moyasar_webhook_not_actionable")
            return JSONResponse({"received": True, "processed": False, "reason": "not_actionable"})
    except Exception as exc:
        log.warning("moyasar_webhook_normalize_failed", error=str(exc))
        return JSONResponse({"received": True, "processed": False, "reason": "normalize_error"})

    # Process event (ZATCA + onboarding)
    result = None
    try:
        processor = PaymentEventProcessor()
        result = await processor.process(event)
    except Exception as exc:
        log.warning("moyasar_webhook_process_failed", error=str(exc))

    # Persist to DB and create founder alert
    alert_id: str = ""
    payment_record_id: str | None = None
    try:
        from db.session import async_session_factory
        from db.repositories.wave17_repos import FounderAlertRepository, PaymentRepository

        async with async_session_factory()() as session:
            # Create founder alert first (APPROVAL_FIRST gate)
            if event.status == "paid":
                alert_repo = FounderAlertRepository(session)
                tier_label = event.service_tier or str(int(event.amount_sar)) + " SAR"
                alert_id = await alert_repo.create_alert(
                    alert_type="payment",
                    title_ar=f"دفعة جديدة مؤكدة — {tier_label}",
                    title_en=f"New payment confirmed — {tier_label}",
                    body_ar=(
                        f"باقة: {tier_label}\n"
                        f"المبلغ: {event.amount_sar:.0f} ريال\n"
                        f"Payment ID: {event.payment_id}\n"
                        "الإجراء التالي: راجع وأرسل رسالة الترحيب بعد الموافقة."
                    ),
                    body_en=(
                        f"Tier: {tier_label}\n"
                        f"Amount: {event.amount_sar:.0f} SAR\n"
                        f"Payment ID: {event.payment_id}\n"
                        "Next action: review and send welcome email after approval."
                    ),
                    priority="high",
                    payment_id=event.payment_id,
                    account_id=event.account_id or None,
                    amount_sar=event.amount_sar,
                ) or ""

            # Persist payment record
            pay_repo = PaymentRepository(session)
            zatca_result = result.zatca_result if result else {}
            onboarding_id = result.onboarding_id if result else ""
            payment_record_id = await pay_repo.save_payment(
                event=event,
                zatca_result=zatca_result,
                onboarding_id=onboarding_id,
                alert_id=alert_id,
            )
            await session.commit()
    except Exception as exc:
        log.warning("moyasar_webhook_persist_failed", error=str(exc))

    log.info(
        "moyasar_webhook_completed",
        payment_id=event.payment_id,
        status=event.status,
        alert_created=bool(alert_id),
        payment_persisted=bool(payment_record_id),
    )
    return JSONResponse({"received": True, "processed": True})
