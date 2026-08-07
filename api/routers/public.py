"""
Public endpoints — no auth, CORS-open. Used by the landing page.

Routes:
  POST /api/v1/public/demo-request   — landing form submission
    Body: {name, company, email, phone, sector?, size?, message?, consent, website(honeypot)}
    Returns: {ok: true, calendly_url: "...", lead_id?: "..."}
"""

from __future__ import annotations

import logging
import os
from typing import Any

from fastapi import APIRouter, HTTPException, Request

from dealix.analytics import FUNNEL_EVENTS, capture_event

log = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/public", tags=["public"])


CALENDLY_URL = os.getenv(
    "CALENDLY_URL",
    "https://calendly.com/sami-assiri11/dealix-demo",
)


def _is_free_diagnostic_source(source: str) -> bool:
    """Return True only for the canonical free-diagnostic intake surfaces."""
    normalized = source.strip().lower().replace("_", "-")
    return normalized in {"landing/diagnostic", "landing/free-diagnostic"}


def _intake_response(
    *, source: str, lead_id: str | None, transactional_status: str
) -> dict[str, Any]:
    """Keep the free-first funnel explicit and machine-verifiable."""
    free_diagnostic = _is_free_diagnostic_source(source)
    return {
        "ok": True,
        "calendly_url": None if free_diagnostic else CALENDLY_URL,
        "message": (
            "تم استلام الفحص المجاني للمراجعة البشرية — لا دفع أو تفعيل تلقائي"
            if free_diagnostic
            else "تم استلام طلبك للمراجعة خلال ساعات العمل"
        ),
        "lead_id": lead_id,
        "transactional_confirmation": transactional_status,
        "funnel_stage": "free_diagnostic" if free_diagnostic else "demo_request",
        "next_step": "human_review" if free_diagnostic else "optional_booking",
        "payment_required": False,
        "external_action_allowed": False,
        "governance_decision": "allow",
    }


@router.post("/demo-request")
async def demo_request(req: Request) -> dict[str, Any]:
    """Public landing form — captures demo request and returns Calendly booking URL."""
    try:
        body = await req.json()
    except Exception as e:
        raise HTTPException(status_code=400, detail="invalid_json") from e

    source = str(body.get("source") or "landing.demo_form")

    # Honeypot: if "website" field is filled, silently drop
    if body.get("website"):
        log.info("demo_request_honeypot_triggered")
        return _intake_response(
            source=source,
            lead_id=None,
            transactional_status="skipped_honeypot",
        )

    name = str(body.get("name") or "").strip()
    company = str(body.get("company") or "").strip()
    email = str(body.get("email") or "").strip()
    phone = str(body.get("phone") or "").strip()
    sector = str(body.get("sector") or "").strip()
    size = str(body.get("size") or "").strip()
    message = str(body.get("message") or "").strip()
    consent = bool(body.get("consent"))

    if not name or not company or "@" not in email or not phone:
        raise HTTPException(status_code=422, detail="missing_required_fields")
    if not consent:
        raise HTTPException(status_code=422, detail="consent_required")

    # Fire PostHog event (fire-and-forget — never blocks response)
    try:
        event = (
            FUNNEL_EVENTS.DIAGNOSTIC_REQUESTED
            if _is_free_diagnostic_source(source)
            else FUNNEL_EVENTS.DEMO_REQUESTED
        )
        await capture_event(
            event,
            distinct_id=email,
            properties={
                "name": name,
                "company": company,
                "email": email,
                "phone": phone,
                "sector": sector,
                "size": size,
                "message_len": len(message),
                "source": source,
            },
        )
    except Exception:
        log.exception("posthog_capture_failed")

    # Persist to local lead-inbox (gitignored var/lead-inbox.jsonl) so the
    # founder can review every inquiry in /api/v1/founder/leads — completes
    # the previous TODO. Best-effort: failure never 5xx the public form.
    lead_id: str | None = None
    try:
        from auto_client_acquisition import lead_inbox
        rec = lead_inbox.append({
            "name": name,
            "company": company,
            "email": email,
            "phone": phone,
            "sector": sector,
            "size": size,
            "message": message,
            "consent": consent,
            "source": source,
            "ref": str(body.get("ref") or ""),
        })
        lead_id = rec.get("id")
    except Exception:
        log.exception("lead_inbox_append_failed")

    # No PII / no user-controlled strings in logs (non-negotiable #6 +
    # CodeQL py/log-injection): record only lengths + a persisted flag.
    log.info(
        "demo_request_accepted email_len=%d company_len=%d sector_len=%d persisted=%s",
        len(email),
        len(company),
        len(sector),
        bool(lead_id),
    )

    # Wave 14B activation: fire transactional confirmation email — best-effort,
    # never blocks the 200 response. Whitelisted kind only; Gmail OAuth
    # configured via env. If Gmail isn't set up, this no-ops gracefully.
    transactional_status = "skipped_not_configured"
    try:
        from auto_client_acquisition.email.transactional import (
            render_diagnostic_intake_confirmation,
            send_transactional,
        )
        subject, body_plain = render_diagnostic_intake_confirmation(
            customer_name=name, sector=sector or "b2b_services"
        )
        send_result = await send_transactional(
            kind="diagnostic_intake_confirmation",
            to_email=email,
            subject=subject,
            body_plain=body_plain,
        )
        transactional_status = send_result.reason_code
    except Exception:
        log.exception("transactional_confirmation_failed")
        transactional_status = "exception_caught"

    return _intake_response(
        source=source,
        lead_id=lead_id,
        transactional_status=transactional_status,
    )


@router.post("/custom-ai-request")
async def custom_ai_request(req: Request) -> dict[str, Any]:
    """Public Custom AI Service intake (commercial ladder Rung 4).

    Captures a bespoke AI project request from the landing page and stores it
    as a governed lead for founder review. No external action is taken without
    approval — this only records the inquiry and returns a confirmation.

    Body: {name, company, email, phone, sector?, use_case?, data_readiness?,
           budget_band?, timeline?, description?, consent, website(honeypot)}
    Returns: {ok, lead_id?, governance_decision: "allow"}
    """
    try:
        body = await req.json()
    except Exception as e:
        raise HTTPException(status_code=400, detail="invalid_json") from e

    # Honeypot: if "website" field is filled, silently drop
    if body.get("website"):
        log.info("custom_ai_request_honeypot_triggered")
        return {"ok": True, "governance_decision": "allow"}

    name = str(body.get("name") or "").strip()
    company = str(body.get("company") or "").strip()
    email = str(body.get("email") or "").strip()
    phone = str(body.get("phone") or "").strip()
    sector = str(body.get("sector") or "").strip()
    use_case = str(body.get("use_case") or "").strip()
    data_readiness = str(body.get("data_readiness") or "").strip()
    budget_band = str(body.get("budget_band") or "").strip()
    timeline = str(body.get("timeline") or "").strip()
    description = str(body.get("description") or "").strip()
    consent = bool(body.get("consent"))

    if not name or not company or "@" not in email or not phone:
        raise HTTPException(status_code=422, detail="missing_required_fields")
    if not consent:
        raise HTTPException(status_code=422, detail="consent_required")

    # Fire PostHog event (fire-and-forget — never blocks response)
    try:
        await capture_event(
            "custom_ai_requested",
            distinct_id=email,
            properties={
                "company": company,
                "sector": sector,
                "use_case": use_case[:120],
                "budget_band": budget_band,
                "timeline": timeline,
                "data_readiness": data_readiness,
                "description_len": len(description),
                "source": "landing.custom_ai_form",
            },
        )
    except Exception:
        log.exception("posthog_capture_failed")

    # Persist to local lead-inbox (gitignored var/lead-inbox.jsonl) so the
    # founder reviews every custom-AI inquiry in /api/v1/founder/leads.
    # Best-effort: failure never 5xx the public form.
    lead_id: str | None = None
    try:
        from auto_client_acquisition import lead_inbox
        rec = lead_inbox.append({
            "name": name,
            "company": company,
            "email": email,
            "phone": phone,
            "sector": sector,
            "message": description,
            "consent": consent,
            "source": str(body.get("source") or "landing.custom_ai_form"),
            "ref": str(body.get("ref") or ""),
            "offer_interest": "custom_ai",
            "custom_ai": {
                "use_case": use_case,
                "data_readiness": data_readiness,
                "budget_band": budget_band,
                "timeline": timeline,
            },
        })
        lead_id = rec.get("id")
    except Exception:
        log.exception("lead_inbox_append_failed")

    # No PII / no user-controlled strings in logs (non-negotiable #6 +
    # CodeQL py/log-injection): record only lengths + a persisted flag.
    log.info(
        "custom_ai_request_accepted email_len=%d company_len=%d sector_len=%d budget_len=%d persisted=%s",
        len(email),
        len(company),
        len(sector),
        len(budget_band),
        bool(lead_id),
    )

    # Wave: transactional confirmation — best-effort, never blocks the 200.
    # Reuses the whitelisted diagnostic-intake confirmation kind. No-ops if
    # Gmail OAuth isn't configured. transactional_status is set on every
    # path below (success or except), so no pre-initialization is needed.
    try:
        from auto_client_acquisition.email.transactional import (
            render_diagnostic_intake_confirmation,
            send_transactional,
        )
        subject, body_plain = render_diagnostic_intake_confirmation(
            customer_name=name, sector=sector or "b2b_services"
        )
        send_result = await send_transactional(
            kind="diagnostic_intake_confirmation",
            to_email=email,
            subject=subject,
            body_plain=body_plain,
        )
        transactional_status = send_result.reason_code
    except Exception:
        log.exception("transactional_confirmation_failed")
        transactional_status = "exception_caught"

    return {
        "ok": True,
        "message": (
            "تم استلام طلب مشروع AI المخصص — سنتواصل خلال 4 ساعات عمل / "
            "Custom AI request received — we will contact you within 4 business hours"
        ),
        "lead_id": lead_id,
        "transactional_confirmation": transactional_status,
        "governance_decision": "allow",
    }


@router.get("/health")
async def public_health() -> dict[str, Any]:
    """Unauthenticated health probe for landing page to show live status."""
    return {"ok": True, "service": "dealix-api"}


@router.post("/partner-application")
async def partner_application(req: Request) -> dict[str, Any]:
    """Public partner signup — for agencies/freelancers/consultants."""
    try:
        body = await req.json()
    except Exception:
        # Also accept form-urlencoded submissions from Formspree-style forms
        form = await req.form()
        body = dict(form)

    name = str(body.get("name") or "").strip()
    company = str(body.get("company") or "").strip()
    email = str(body.get("email") or "").strip()
    phone = str(body.get("phone") or "").strip()
    ptype = str(body.get("partnership_type") or body.get("type") or "referral").strip()
    services = str(body.get("services") or "").strip()
    active_clients = str(body.get("active_clients") or body.get("clients") or "0")
    why = str(body.get("why") or "").strip()

    if not name or not company or "@" not in email:
        raise HTTPException(status_code=422, detail="missing_required_fields")

    log.info(
        "partner_application_received company=%s type=%s clients=%s",
        company,
        ptype,
        active_clients,
    )

    try:
        await capture_event(
            "partner_application_submitted",
            distinct_id=email or company or "anonymous",
            properties={
                "company": company,
                "partnership_type": ptype,
                "active_clients": active_clients,
                "has_phone": bool(phone),
                "has_services": bool(services),
                "has_why": bool(why),
                "source": "dealix.partners_page",
            },
        )
    except Exception:
        log.warning("posthog_capture_failed", exc_info=True)

    return {
        "ok": True,
        "message": "وصلنا طلبك. سنتواصل خلال 48 ساعة.",
        "next_step": "email_review",
    }
