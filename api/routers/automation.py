"""
Automation router — daily targeting, follow-ups, compliance gate, replies.

Endpoints:
    POST /api/v1/automation/daily-targeting/run    — generate today's 50
    POST /api/v1/automation/followups/run          — schedule +2/+5/+10
    POST /api/v1/compliance/check-outreach         — single-row gate
    POST /api/v1/automation/reply/classify         — classify a reply text
    GET  /api/v1/automation/status                 — health + counts
    GET  /api/v1/automation/today                  — today's queued plan
"""

from __future__ import annotations

import logging
import os
import uuid
from datetime import datetime, timedelta, timezone
from typing import Any

from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import func, select

from auto_client_acquisition.automation.daily_runner import (
    run_daily_targeting_core,
    run_followups_core,
)
from auto_client_acquisition.email.compliance import (
    check_outreach,
    get_batch_interval_seconds,
    get_batch_size,
    get_daily_limit,
)
from auto_client_acquisition.email.reply_classifier import (
    classify_reply,
)
from db.models import (
    EmailSendLog,
    OutreachQueueRecord,
    SuppressionRecord,
)
from db.session import async_session_factory

router = APIRouter(prefix="/api/v1", tags=["automation"])
log = logging.getLogger(__name__)


def _new_id(prefix: str = "") -> str:
    return f"{prefix}{uuid.uuid4().hex[:24]}" if prefix else uuid.uuid4().hex[:24]


def _utcnow() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


# ── Compliance check single-row ───────────────────────────────────
@router.post("/compliance/check-outreach")
async def compliance_check(body: dict[str, Any] = Body(...)) -> dict[str, Any]:
    """
    Check a single outreach candidate against all gates.
    Body must include: to_email; optional: contact_opt_out, risk_score, allowed_use,
                      bounced_before, sent_today_count, sent_in_current_batch,
                      seconds_since_last_batch, is_partner_warm.
    """
    # Pull suppression list
    sup_emails: set[str] = set()
    sup_domains: set[str] = set()
    sup_phones: set[str] = set()
    async with async_session_factory() as session:
        try:
            rows = (await session.execute(select(SuppressionRecord))).scalars().all()
            for r in rows:
                if r.email: sup_emails.add(r.email.lower())
                if r.domain: sup_domains.add(r.domain.lower())
                if r.phone: sup_phones.add(r.phone)
        except Exception as exc:  # noqa: BLE001
            log.warning("suppression_load_failed err=%s", exc)

    chk = check_outreach(
        to_email=body.get("to_email"),
        contact_opt_out=bool(body.get("contact_opt_out")),
        risk_score=float(body.get("risk_score") or 0),
        allowed_use=body.get("allowed_use"),
        suppression_emails=sup_emails,
        suppression_domains=sup_domains,
        suppression_phones=sup_phones,
        bounced_before=bool(body.get("bounced_before")),
        sent_today_count=int(body.get("sent_today_count") or 0),
        sent_in_current_batch=int(body.get("sent_in_current_batch") or 0),
        seconds_since_last_batch=body.get("seconds_since_last_batch"),
        is_partner_warm=bool(body.get("is_partner_warm")),
    )
    return chk.to_dict()


# ── Daily targeting ───────────────────────────────────────────────
@router.post("/automation/daily-targeting/run")
async def run_daily_targeting(body: dict[str, Any] = Body(default={})) -> dict[str, Any]:
    """
    Generate today's 50 personalized outbound rows.

    Body (all optional):
        target_date: ISO date (default today UTC)
        daily_target_count: int (default = DAILY_EMAIL_LIMIT env)
        candidate_pool_size: int (default 200 — pulled from accounts)
        personalize_with_llm: bool (default True if Groq exists)
        sectors: list[str] | null  — filter (default: all)
        cities: list[str] | null
    """
    return await run_daily_targeting_core(
        target_date=body.get("target_date"),
        daily_target_count=(
            int(body["daily_target_count"]) if body.get("daily_target_count") else None
        ),
        candidate_pool_size=(
            int(body["candidate_pool_size"]) if body.get("candidate_pool_size") else None
        ),
        sectors=body.get("sectors") or None,
        cities=body.get("cities") or None,
        personalize_with_llm=bool(body.get("personalize_with_llm", True)),
    )


# ── Follow-ups: schedule +2/+5/+10 from sent logs ─────────────────
@router.post("/automation/followups/run")
async def run_followups(body: dict[str, Any] = Body(default={})) -> dict[str, Any]:
    """
    Walk EmailSendLog rows where status='sent' and create follow-up
    OutreachQueueRecord rows at days 2/5/10 — only if no reply yet.
    """
    return await run_followups_core()


# ── Reply classifier endpoint ─────────────────────────────────────
@router.post("/automation/reply/classify")
async def classify_reply_endpoint(body: dict[str, Any] = Body(...)) -> dict[str, Any]:
    """
    Classify a reply text into one of 13 categories + draft response.
    Body: text (required), prefer_llm (default True), thread_id (optional)
    """
    text = str(body.get("text") or "").strip()
    if not text:
        raise HTTPException(400, "text_required")
    prefer_llm = bool(body.get("prefer_llm", True))
    classification = await classify_reply(text, prefer_llm=prefer_llm)
    return classification.to_dict()


# ── Status + today's plan ─────────────────────────────────────────
@router.get("/automation/status")
async def automation_status() -> dict[str, Any]:
    """Health summary — counts of today's sends, replies, suppressions."""
    today_start = _utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    counts: dict[str, int] = {"sent_today": 0, "queued_total": 0,
                              "replied_today": 0, "bounced_today": 0,
                              "suppression_total": 0}
    async with async_session_factory() as session:
        try:
            counts["sent_today"] = int(
                (await session.execute(
                    select(func.count()).select_from(EmailSendLog).where(
                        EmailSendLog.sent_at >= today_start
                    )
                )).scalar() or 0
            )
            counts["queued_total"] = int(
                (await session.execute(
                    select(func.count()).select_from(OutreachQueueRecord).where(
                        OutreachQueueRecord.status == "queued"
                    )
                )).scalar() or 0
            )
            counts["replied_today"] = int(
                (await session.execute(
                    select(func.count()).select_from(EmailSendLog).where(
                        EmailSendLog.reply_received_at >= today_start
                    )
                )).scalar() or 0
            )
            counts["bounced_today"] = int(
                (await session.execute(
                    select(func.count()).select_from(EmailSendLog).where(
                        EmailSendLog.status == "bounced",
                        EmailSendLog.updated_at >= today_start,
                    )
                )).scalar() or 0
            )
            counts["suppression_total"] = int(
                (await session.execute(
                    select(func.count()).select_from(SuppressionRecord)
                )).scalar() or 0
            )
        except Exception as exc:  # noqa: BLE001
            return {"status": "skipped_db_unreachable", "error": str(exc)}

    return {
        "status": "ok",
        "limits": {
            "daily_email_limit": get_daily_limit(),
            "batch_size": get_batch_size(),
            "batch_interval_seconds": get_batch_interval_seconds(),
        },
        "counts": counts,
        "remaining_today": max(0, get_daily_limit() - counts["sent_today"]),
        "gmail_configured": bool(
            os.getenv("GMAIL_CLIENT_ID") and os.getenv("GMAIL_REFRESH_TOKEN")
            and os.getenv("GMAIL_SENDER_EMAIL")
        ),
        "llm_configured": bool(
            os.getenv("GROQ_API_KEY") or os.getenv("ANTHROPIC_API_KEY")
            or os.getenv("OPENAI_API_KEY")
        ),
    }
