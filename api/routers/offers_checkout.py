"""Offers self-serve checkout — Phase 1 (autonomous lead-to-cash).

Public, no-auth endpoints that allow a warm inbound visitor to:
  1. List the 5 productized offers (catalog).
  2. Start a checkout for one of them.

Gated by Settings.offers_self_serve_enabled — defaults False.
Returns 503 (feature_disabled) when the flag is off so the surface area
stays inert in production until the founder flips the switch.

Doctrine compliance:
  - Non-Neg #10: Source Passport mandatory in request body.
  - Non-Neg #4/#5/#1: SelfServeIntakeGuard runs before any Moyasar call.
  - Non-Neg #6: Moyasar HPP URL returned; charge happens on customer click.
  - Non-Neg #7: No external send; idempotent service is pure orchestration.
"""

from __future__ import annotations

import logging
import os
from typing import Any

from fastapi import APIRouter, HTTPException, Request

from auto_client_acquisition.governance_os.self_serve_intake_guard import (
    ALLOWED_OFFER_IDS,
)
from dealix.payments.checkout import (
    OFFER_CATALOG,
    InMemoryCheckoutStore,
    OfferCheckoutService,
)
from dealix.payments.moyasar import MoyasarClient

log = logging.getLogger(__name__)

router = APIRouter(tags=["offers"])

# Process-local singletons. Replaced with DI in api/deps.py when Phase 3
# Postgres-backed store ships.
_store = InMemoryCheckoutStore()
_service: OfferCheckoutService | None = None


def _get_service() -> OfferCheckoutService:
    """Lazy singleton — built on first request to avoid boot-time IO."""
    global _service
    if _service is None:
        callback_base = os.getenv("APP_URL", "https://api.dealix.me")
        moyasar = MoyasarClient()

        async def _factory(**kwargs: Any) -> dict[str, Any]:
            return await moyasar.create_hosted_payment(**kwargs)

        _service = OfferCheckoutService(
            store=_store,
            hosted_payment_factory=_factory,
            callback_base_url=callback_base,
        )
    return _service


def reset_service_for_tests() -> None:
    """Test hook — drops the singleton so a fresh DI build runs next request."""
    global _service
    _service = None
    _store.__init__()  # type: ignore[misc]


def _feature_enabled() -> bool:
    try:
        from core.config.settings import get_settings

        return bool(get_settings().offers_self_serve_enabled)
    except Exception:  # noqa: BLE001 — settings optional in some test contexts
        return False


@router.get("/api/v1/offers/catalog")
async def offers_catalog() -> dict[str, Any]:
    """Public read of the 5 productized offers."""
    return {
        "offers": [
            {
                "offer_id": oid,
                "amount_halalas": int(spec["amount_halalas"]),
                "currency": str(spec["currency"]),
                "requires_payment": bool(spec["requires_payment"]),
                "approval_class": str(spec["approval_class"]),
            }
            for oid, spec in OFFER_CATALOG.items()
        ],
        "allowed_offer_ids": list(ALLOWED_OFFER_IDS),
    }


@router.post("/api/v1/offers/{offer_id}/checkout")
async def offer_checkout(offer_id: str, req: Request) -> dict[str, Any]:
    """
    Body shape:
      {
        "source_passport_id": "passport_...",     // Non-Neg #10 — required
        "lawful_basis": "consent" | "contract" | ...,
        "consent_given": true,
        "customer_handle": "ahmad",               // optional
        "locale": "ar" | "en",                    // default "ar"
        "free_text": "..."                        // optional context for guard
      }

    Returns CheckoutResult.to_dict() with one of:
      status="free"      — diagnostic_free, no charge needed
      status="ok"        — hosted_payment_url ready for customer click
      status="escalated" — managed_ops/custom_ai routed to founder pitch
      status="rejected"  — doctrine violation; verdict carries reasons
    """
    if not _feature_enabled():
        raise HTTPException(
            status_code=503,
            detail={
                "error": "feature_disabled",
                "reasons": {
                    "ar": "البوابة الذاتية غير مُفعّلة بعد — يتطلّب موافقة المؤسس.",
                    "en": "Self-serve offers gate is disabled — founder must enable.",
                },
            },
        )

    try:
        body = await req.json()
    except Exception as exc:
        raise HTTPException(status_code=400, detail="invalid_json") from exc

    source_passport_id = str(body.get("source_passport_id") or "").strip()
    lawful_basis_raw = body.get("lawful_basis", "consent")
    consent_given = bool(body.get("consent_given") is True)
    customer_handle = body.get("customer_handle")
    locale = str(body.get("locale") or "ar")
    free_text = str(body.get("free_text") or "")

    svc = _get_service()

    try:
        # The service will run the intake guard and short-circuit on violations.
        result = await svc.checkout(
            offer_id=offer_id,
            source_passport_id=source_passport_id,
            lawful_basis=lawful_basis_raw,
            consent_given=consent_given,
            customer_handle=customer_handle,
            free_text=free_text,
            locale=locale,
        )
    except RuntimeError as exc:
        # Misconfiguration (e.g. missing hosted_payment_factory).
        # offer_id is restricted to the closed ALLOWED_OFFER_IDS set; coerce
        # to a short, log-safe token to prevent CRLF/log injection (CWE-117).
        safe_offer_id = offer_id if offer_id in ALLOWED_OFFER_IDS else "unknown"
        log.exception("offer_checkout_misconfigured offer_id=%s", safe_offer_id)
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    if result.status == "rejected":
        # 422 carries the bilingual reasons.
        raise HTTPException(status_code=422, detail=result.to_dict())

    return result.to_dict()
