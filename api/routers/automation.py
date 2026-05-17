"""
Automation router — daily targeting, follow-ups, compliance gate, replies.

Endpoints:
    POST /api/v1/automation/daily-targeting/run    — generate today's 50
    POST /api/v1/automation/followups/run          — schedule +2/+5/+10
    POST /api/v1/automation/social/draft           — queue governed social posts
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

from auto_client_acquisition.email.daily_targeting import (
    DailyTargetingResult,
    compute_followup_schedule,
    llm_personalize,
    render_email_template,
    select_top_n_diversified,
)
from auto_client_acquisition.email.compliance import (
    append_opt_out_line,
    check_outreach,
    get_batch_interval_seconds,
    get_batch_size,
    get_daily_limit,
)
from auto_client_acquisition.email.reply_classifier import (
    classify_reply,
)
from auto_client_acquisition.approval_center import (
    ApprovalRequest,
    get_default_approval_store,
)
from auto_client_acquisition.approval_center import persistence
from auto_client_acquisition.growth_beast.content_engine import draft_content
from db.models import (
    AccountRecord,
    ContactRecord,
    EmailSendLog,
    LeadScoreRecord,
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
    target_date = body.get("target_date") or _utcnow().date().isoformat()
    daily_target = int(body.get("daily_target_count") or get_daily_limit())
    pool_size = int(body.get("candidate_pool_size") or max(200, daily_target * 4))
    sectors_filter = body.get("sectors") or None
    cities_filter = body.get("cities") or None
    personalize = bool(body.get("personalize_with_llm", True))

    # 1. Pull candidates from the lead graph
    excluded = {
        "opt_out": 0, "suppressed": 0, "recently_contacted": 0,
        "high_risk": 0, "no_allowed_use": 0, "personal_email_only": 0,
    }
    async with async_session_factory() as session:
        try:
            q = select(AccountRecord).where(AccountRecord.status.in_(["enriched", "new"]))
            if sectors_filter:
                q = q.where(AccountRecord.sector.in_(sectors_filter))
            if cities_filter:
                q = q.where(AccountRecord.city.in_(cities_filter))
            q = q.order_by(AccountRecord.data_quality_score.desc()).limit(pool_size)
            accounts = (await session.execute(q)).scalars().all()

            ids = [a.id for a in accounts]
            scores = (await session.execute(
                select(LeadScoreRecord).where(LeadScoreRecord.account_id.in_(ids))
            )).scalars().all() if ids else []
            score_map: dict[str, LeadScoreRecord] = {}
            for s in scores:
                if s.account_id not in score_map or s.created_at > score_map[s.account_id].created_at:
                    score_map[s.account_id] = s

            contacts_q = (await session.execute(
                select(ContactRecord).where(ContactRecord.account_id.in_(ids))
            )).scalars().all() if ids else []
            contacts_by_acc: dict[str, list[ContactRecord]] = {}
            for c in contacts_q:
                contacts_by_acc.setdefault(c.account_id, []).append(c)

            sup_rows = (await session.execute(select(SuppressionRecord))).scalars().all()
            sup_emails = {s.email.lower() for s in sup_rows if s.email}
            sup_domains = {s.domain.lower() for s in sup_rows if s.domain}

            # Recently contacted: any send in last 14 days
            recent_cutoff = _utcnow() - timedelta(days=14)
            recent_logs = (await session.execute(
                select(EmailSendLog.account_id).where(
                    EmailSendLog.sent_at >= recent_cutoff
                ).distinct()
            )).scalars().all() if ids else []
            recently_contacted = set(recent_logs)
        except Exception as exc:  # noqa: BLE001
            return {"status": "skipped_db_unreachable", "error": str(exc)}

    # 2. Filter
    candidates: list[dict[str, Any]] = []
    for a in accounts:
        if a.id in recently_contacted:
            excluded["recently_contacted"] += 1
            continue
        if (a.risk_level or "").lower() == "high":
            excluded["high_risk"] += 1
            continue
        allowed_use = (a.extra or {}).get("allowed_use")
        if not allowed_use or allowed_use in {"unknown", ""}:
            excluded["no_allowed_use"] += 1
            continue
        if a.domain and a.domain.lower() in sup_domains:
            excluded["suppressed"] += 1
            continue
        # Pick best contact email
        ac_contacts = contacts_by_acc.get(a.id, [])
        any_opt_out = any(c.opt_out for c in ac_contacts)
        if any_opt_out:
            excluded["opt_out"] += 1
            continue
        business_email = next(
            (c.email for c in ac_contacts
             if c.email and c.email.lower() not in sup_emails
             and not any(p in c.email.lower() for p in
                         ["@gmail.com", "@hotmail.com", "@yahoo.com", "@outlook.com"])),
            None,
        )
        any_phone = next((c.phone for c in ac_contacts if c.phone), None)
        if not business_email and not any_phone:
            excluded["personal_email_only"] += 1
            continue

        score = score_map.get(a.id)
        candidates.append({
            "id": a.id, "company_name": a.company_name,
            "domain": a.domain, "website": a.website,
            "city": a.city, "city_ar": a.city, "sector": a.sector,
            "sector_ar": (a.extra or {}).get("source_url"),
            "google_place_id": a.google_place_id,
            "data_quality_score": a.data_quality_score,
            "risk_level": a.risk_level,
            "best_email": business_email,
            "best_phone": any_phone,
            "allowed_use": allowed_use,
            "total_score": score.total_score if score else 0,
            "priority": score.priority if score else "P3",
            "recommended_channel": score.recommended_channel if score else None,
        })

    # 3. Diversified select
    selected = select_top_n_diversified(candidates, target_count=daily_target)

    # 4. Generate per-account email (LLM if available)
    selected_out: list[dict[str, Any]] = []
    sector_split: dict[str, int] = {}
    for acc in selected:
        base = render_email_template(acc, acc.get("priority") or "P2")
        if personalize:
            base = await llm_personalize(acc, base)
        body_with_optout = append_opt_out_line(base["body_ar"])
        sched = compute_followup_schedule(_utcnow())
        out = {
            **acc,
            "subject_ar": base["subject_ar"],
            "body_ar": body_with_optout,
            "personalized_by_llm": base.get("personalized_by_llm") == "true",
            "approval_required": True,
            "send_status": "queued_for_human_approval",
            "channel": "email" if acc.get("best_email") else "phone_task",
            "followups": sched,
        }
        selected_out.append(out)
        sec = (acc.get("sector") or "other").lower()
        sector_split[sec] = sector_split.get(sec, 0) + 1

    # 5. Persist queue rows (approval_required=True; no auto-send here)
    queued_count = 0
    async with async_session_factory() as session:
        for o in selected_out:
            qr = OutreachQueueRecord(
                id=_new_id("oq_"),
                lead_id=o["id"],
                channel=o["channel"],
                message=o["body_ar"],
                approval_required=True,
                status="queued",
                due_at=_utcnow() + timedelta(hours=2),
                risk_reason=None,
            )
            session.add(qr)
            queued_count += 1
        try:
            await session.commit()
        except Exception as exc:  # noqa: BLE001
            await session.rollback()
            log.warning("daily_targeting_commit_failed err=%s", exc)

    result = DailyTargetingResult(
        generated_at=_utcnow().isoformat(),
        target_date=target_date,
        candidates_evaluated=len(accounts),
        excluded_opt_out=excluded["opt_out"],
        excluded_suppressed=excluded["suppressed"],
        excluded_recently_contacted=excluded["recently_contacted"],
        excluded_high_risk=excluded["high_risk"],
        excluded_no_allowed_use=excluded["no_allowed_use"],
        excluded_personal_email_phone_only=excluded["personal_email_only"],
        selected_count=len(selected_out),
        selected=selected_out[:daily_target],
        sector_split=sector_split,
        daily_email_limit=get_daily_limit(),
        notes=[
            f"queued {queued_count} OutreachQueueRecord rows (approval_required=True)",
            f"personalize_with_llm={personalize}",
        ],
    )
    return result.to_dict()


# ── Follow-ups: schedule +2/+5/+10 from sent logs ─────────────────
@router.post("/automation/followups/run")
async def run_followups(body: dict[str, Any] = Body(default={})) -> dict[str, Any]:
    """
    Walk EmailSendLog rows where status='sent' and create follow-up
    OutreachQueueRecord rows at days 2/5/10 — only if no reply yet.
    """
    now = _utcnow()
    created = 0
    skipped_replied = 0
    async with async_session_factory() as session:
        try:
            sent_logs = (await session.execute(
                select(EmailSendLog).where(
                    EmailSendLog.status == "sent",
                    EmailSendLog.sent_at >= now - timedelta(days=15),
                )
            )).scalars().all()
        except Exception as exc:  # noqa: BLE001
            return {"status": "skipped_db_unreachable", "error": str(exc)}

        for log_row in sent_logs:
            if log_row.reply_received_at is not None:
                skipped_replied += 1
                continue
            if not log_row.sent_at:
                continue
            days_since = (now - log_row.sent_at).days
            for step, days in [(2, 2), (5, 5), (10, 10)]:
                if days_since == days and log_row.sequence_step < step:
                    fq = OutreachQueueRecord(
                        id=_new_id("oq_"),
                        lead_id=log_row.account_id,
                        channel="email_followup",
                        message=_followup_template(step, log_row.subject),
                        approval_required=True,
                        status="queued",
                        due_at=now,
                        risk_reason=None,
                    )
                    session.add(fq)
                    log_row.sequence_step = step
                    created += 1
                    break
        try:
            await session.commit()
        except Exception as exc:  # noqa: BLE001
            await session.rollback()
            return {"status": "commit_failed", "error": str(exc)}

    return {
        "status": "ok",
        "followups_created": created,
        "skipped_already_replied": skipped_replied,
        "scanned": len(sent_logs),
    }


def _followup_template(step: int, prev_subject: str) -> str:
    if step == 2:
        return (
            f"متابعة سريعة لرسالتي السابقة بخصوص Pilot Dealix.\n\n"
            "هل عندكم سؤال محدد قبل ما نبدأ؟ أو الوقت غير مناسب الأسبوع هذا؟\n\n"
            "سامي\n— لإلغاء الاستلام: ردّ بـ STOP."
        )
    if step == 5:
        return (
            "أرسل لكم مثال سريع: عميل عقاري في الرياض شغّل Pilot أسبوع، رد على 23 lead، "
            "حجز 4 demos، صفقة واحدة من الأسبوع الأول. تجربتكم غالباً مشابهة.\n\n"
            "تبغوا تجربة 7 أيام بـ 499 ريال؟\n\n"
            "سامي\n— لإلغاء الاستلام: ردّ بـ STOP."
        )
    if step == 10:
        return (
            "آخر متابعة قبل ما أتوقف عن المراسلة. لو الوقت ما يناسب، نقدر نلتقي بعد شهر.\n\n"
            "لو غير ذلك، شكراً لوقتكم وحظاً موفقاً.\n\n"
            "سامي\n— لإلغاء الاستلام نهائياً: ردّ بـ STOP."
        )
    return ""


# ── Social content drafts (governed) ──────────────────────────────

# A week's rotation of content types so the founder gets variety, not
# seven identical posts. Pure templates — see content_engine.draft_content.
_SOCIAL_ROTATION: list[tuple[str, str]] = [
    ("linkedin_post", "بطء الردّ على العملاء المحتملين"),
    ("diagnostic_cta", "تشخيص مجاني خلال 24 ساعة"),
    ("sector_insight", "غياب نظام تشغيل أسبوعي واضح"),
    ("objection_post", "جرّبنا أدوات كثيرة وما نفعت"),
    ("case_snippet", "أسبوع واحد من Proof Sprint"),
    ("linkedin_post", "قرارات بدون أدلّة موثّقة"),
    ("diagnostic_cta", "ابدأ بخطوة صغيرة بلا التزام"),
]

_DEFAULT_SOCIAL_SECTORS = ["real_estate", "logistics", "retail", "professional_services"]


@router.post("/automation/social/draft")
async def run_social_drafts(body: dict[str, Any] = Body(default={})) -> dict[str, Any]:
    """Generate a governed batch of social-media post drafts and queue
    them in the Approval Command Center.

    Doctrine: draft-and-queue ONLY. Nothing is published. Every draft
    lands as a pending approval the founder reviews — and then posts
    manually. There is no auto-publish path and none may be added.

    Body (all optional):
        count: int = 7         — how many posts to draft (one per day)
        sectors: list[str]     — sector rotation (default: 4 Saudi sectors)
        start_date: ISO date   — first suggested publish date (default tomorrow)
    """
    count = max(1, min(int(body.get("count") or 7), 30))
    sectors = body.get("sectors") or _DEFAULT_SOCIAL_SECTORS
    if not isinstance(sectors, list) or not sectors:
        sectors = _DEFAULT_SOCIAL_SECTORS

    start_raw = body.get("start_date")
    if start_raw:
        try:
            start = datetime.fromisoformat(str(start_raw))
        except ValueError:
            start = _utcnow() + timedelta(days=1)
    else:
        start = _utcnow() + timedelta(days=1)

    store = get_default_approval_store()
    queued: list[ApprovalRequest] = []
    for i in range(count):
        content_type, angle = _SOCIAL_ROTATION[i % len(_SOCIAL_ROTATION)]
        sector = sectors[i % len(sectors)]
        draft = draft_content(sector=sector, angle=angle, content_type=content_type)
        publish_at = start + timedelta(days=i)
        req = ApprovalRequest(
            object_type="social_post",
            object_id=_new_id("soc_"),
            action_type="social_post",
            action_mode="draft_only",
            summary_ar=draft["draft_ar"],
            summary_en=draft["draft_en"],
            risk_level="low",
            proof_impact=f"social:{content_type}:{sector}",
            due_date=publish_at,
        )
        queued.append(store.create(req))

    persisted = await persistence.upsert_many(queued)

    return {
        "status": "ok",
        "drafted": len(queued),
        "persisted": persisted,
        "approval_mode": "draft_only",
        "note": "queued in the Approval Command Center; founder reviews then posts manually",
        "approvals": [
            {
                "approval_id": r.approval_id,
                "content_type": r.proof_impact,
                "suggested_publish_date": r.due_date.isoformat() if r.due_date else None,
            }
            for r in queued
        ],
    }


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
