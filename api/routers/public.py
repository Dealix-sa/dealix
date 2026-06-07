"""
Public endpoints — no auth, CORS-open. Used by the landing page + web app.

Routes:
  POST /api/v1/public/demo-request    — landing form submission
    Body: {name, company, email, phone, sector?, size?, message?, consent, website(honeypot)}
    Returns: {ok: true, calendly_url: "...", lead_id?: "..."}
  POST /api/v1/public/custom-request  — bespoke ("custom solution") intake
    Body: {name, company, email, phone?, what_to_build(required), budget_range?,
           timeline?, sector?, consent, website(honeypot)}
    Returns: {ok: true, calendly_url: "...", lead_id?: "..."}
  POST /api/v1/public/partner-application — agency/partner signup (persisted to lead-inbox)

All inbound here is DRAFT-ONLY: leads are persisted to the gitignored lead-inbox
so the daily lead-prep engine + founder review can pick them up. Nothing is ever
auto-sent (NO_LIVE_SEND) — the founder approves and sends manually.
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


@router.post("/demo-request")
async def demo_request(req: Request) -> dict[str, Any]:
    """Public landing form — captures demo request and returns Calendly booking URL."""
    try:
        body = await req.json()
    except Exception as e:
        raise HTTPException(status_code=400, detail="invalid_json") from e

    # Honeypot: if "website" field is filled, silently drop
    if body.get("website"):
        log.info("demo_request_honeypot_triggered")
        return {"ok": True, "calendly_url": CALENDLY_URL}

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
        await capture_event(
            (
                FUNNEL_EVENTS.DEMO_REQUESTED
                if hasattr(FUNNEL_EVENTS, "DEMO_REQUESTED")
                else "demo_requested"
            ),
            distinct_id=email,
            properties={
                "name": name,
                "company": company,
                "email": email,
                "phone": phone,
                "sector": sector,
                "size": size,
                "message_len": len(message),
                "source": "landing.demo_form",
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
            "source": str(body.get("source") or "landing.demo_form"),
            "ref": str(body.get("ref") or ""),
        })
        lead_id = rec.get("id")
    except Exception:
        log.exception("lead_inbox_append_failed")

    log.info(
        "demo_request_accepted email=%s company=%s sector=%s lead_id=%s",
        email,
        company,
        sector,
        lead_id,
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

    return {
        "ok": True,
        "calendly_url": CALENDLY_URL,
        "message": "تم استلام طلبك — سنتواصل خلال 4 ساعات عمل",
        "lead_id": lead_id,
        "transactional_confirmation": transactional_status,
        "governance_decision": "allow",
    }


@router.post("/custom-request")
async def custom_request(req: Request) -> dict[str, Any]:
    """Public 'custom solution' intake — prospect describes what they want Dealix
    to build/do. Captured as a lead (DRAFT-ONLY) for founder review. No auto-send.
    """
    try:
        body = await req.json()
    except Exception as e:
        raise HTTPException(status_code=400, detail="invalid_json") from e

    # Honeypot: if "website" field is filled, silently drop
    if body.get("website"):
        log.info("custom_request_honeypot_triggered")
        return {"ok": True, "calendly_url": CALENDLY_URL}

    name = str(body.get("name") or "").strip()
    company = str(body.get("company") or "").strip()
    email = str(body.get("email") or "").strip()
    phone = str(body.get("phone") or "").strip()
    sector = str(body.get("sector") or "").strip()
    what_to_build = str(body.get("what_to_build") or body.get("message") or "").strip()
    budget_range = str(body.get("budget_range") or "").strip()
    timeline = str(body.get("timeline") or "").strip()
    consent = bool(body.get("consent"))

    if not name or not company or "@" not in email:
        raise HTTPException(status_code=422, detail="missing_required_fields")
    if not what_to_build:
        raise HTTPException(status_code=422, detail="what_to_build_required")
    if not consent:
        raise HTTPException(status_code=422, detail="consent_required")

    # Fire PostHog event (fire-and-forget — never blocks response)
    try:
        await capture_event(
            "custom_request_submitted",
            distinct_id=email,
            properties={
                "name": name,
                "company": company,
                "email": email,
                "sector": sector,
                "budget_range": budget_range,
                "timeline": timeline,
                "what_to_build_len": len(what_to_build),
                "source": "web.custom_form",
            },
        )
    except Exception:
        log.exception("posthog_capture_failed")

    # Persist to the gitignored lead-inbox so the daily engine + founder review
    # pick it up. Best-effort — a disk hiccup never 5xx the public form.
    lead_id: str | None = None
    try:
        from auto_client_acquisition import lead_inbox
        rec = lead_inbox.append({
            "name": name,
            "company": company,
            "email": email,
            "phone": phone,
            "sector": sector,
            "size": "",
            "message": what_to_build,
            "budget_range": budget_range,
            "timeline": timeline,
            "consent": consent,
            "source": str(body.get("source") or "landing.custom_form"),
            "request_kind": "custom_solution",
            "ref": str(body.get("ref") or ""),
        })
        lead_id = rec.get("id")
    except Exception:
        log.exception("lead_inbox_append_failed")

    log.info(
        "custom_request_accepted email=%s company=%s budget=%s lead_id=%s",
        email,
        company,
        budget_range or "—",
        lead_id,
    )

    return {
        "ok": True,
        "calendly_url": CALENDLY_URL,
        "message": "تم استلام طلبك المخصّص — سنراجع المتطلبات ونتواصل خلال 4 ساعات عمل",
        "lead_id": lead_id,
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

    # Persist to the gitignored lead-inbox so partner applications are not lost
    # (previously only logged). Best-effort — never 5xx the public form.
    partner_lead_id: str | None = None
    try:
        from auto_client_acquisition import lead_inbox
        rec = lead_inbox.append({
            "name": name,
            "company": company,
            "email": email,
            "phone": phone,
            "sector": "agency_partner",
            "message": why or services,
            "partnership_type": ptype,
            "active_clients": active_clients,
            "source": str(body.get("source") or "dealix.partners_page"),
            "request_kind": "partner_application",
        })
        partner_lead_id = rec.get("id")
    except Exception:
        log.exception("lead_inbox_append_failed")

    return {
        "ok": True,
        "message": "وصلنا طلبك. سنتواصل خلال 48 ساعة.",
        "next_step": "email_review",
        "lead_id": partner_lead_id,
    }
