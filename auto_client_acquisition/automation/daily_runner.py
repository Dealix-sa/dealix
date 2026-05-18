"""Shared daily-motion logic for the Governed Autopilot.

Pure-ish async functions extracted from ``api/routers/automation.py`` so the
HTTP endpoints and the ARQ cron worker share one implementation.

Functions here open their own DB sessions and persist results to Postgres
(``OutreachQueueRecord``). They NEVER auto-send prospect outreach: targeting
and follow-up runners only queue drafts with ``approval_required=True``.

Doctrine constraint: prospect channels (whatsapp/linkedin/phone) are draft+
approve only. "Autopilot" means automated drafting / scheduling / queuing —
the founder's approval tap remains the only send trigger.
"""

from __future__ import annotations

import logging
import uuid
from datetime import datetime, timedelta, timezone
from typing import Any

from sqlalchemy import select

from auto_client_acquisition.email.compliance import (
    append_opt_out_line,
    get_daily_limit,
)
from auto_client_acquisition.email.daily_targeting import (
    DailyTargetingResult,
    compute_followup_schedule,
    llm_personalize,
    render_email_template,
    select_top_n_diversified,
)
from db.models import (
    AccountRecord,
    ContactRecord,
    EmailSendLog,
    LeadScoreRecord,
    OutreachQueueRecord,
    SuppressionRecord,
)
from db.session import async_session_factory

log = logging.getLogger(__name__)

# Top-N outreach drafts queued per daily-targeting run. The compliance gate
# (auto_client_acquisition/email/compliance.py) still enforces the real send
# cap; this is the queueing target only.
DEFAULT_TARGET_COUNT = 50

_PERSONAL_EMAIL_DOMAINS = ("@gmail.com", "@hotmail.com", "@yahoo.com", "@outlook.com")


def _new_id(prefix: str = "") -> str:
    return f"{prefix}{uuid.uuid4().hex[:24]}" if prefix else uuid.uuid4().hex[:24]


def _utcnow() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


def followup_template(step: int, prev_subject: str = "") -> str:
    """Return the Arabic follow-up body for step 2 / 5 / 10."""
    if step == 2:
        return (
            "متابعة سريعة لرسالتي السابقة بخصوص Pilot Dealix.\n\n"
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


async def run_daily_targeting_core(
    *,
    target_date: str | None = None,
    daily_target_count: int | None = None,
    candidate_pool_size: int | None = None,
    sectors: list[str] | None = None,
    cities: list[str] | None = None,
    personalize_with_llm: bool = True,
) -> dict[str, Any]:
    """Generate today's TOP-N personalised outbound rows and queue them.

    Pulls compliant candidates from the lead graph, filters opt-out /
    suppressed / high-risk / recently-contacted, diversifies the selection,
    drafts a per-account email, and persists ``OutreachQueueRecord`` rows
    with ``approval_required=True`` and ``status='queued'``.

    No send happens here. Returns a ``DailyTargetingResult`` dict.
    """
    target_date = target_date or _utcnow().date().isoformat()
    daily_target = int(daily_target_count or DEFAULT_TARGET_COUNT)
    pool_size = int(candidate_pool_size or max(200, daily_target * 4))

    excluded = {
        "opt_out": 0, "suppressed": 0, "recently_contacted": 0,
        "high_risk": 0, "no_allowed_use": 0, "personal_email_only": 0,
    }
    async with async_session_factory()() as session:
        try:
            q = select(AccountRecord).where(AccountRecord.status.in_(["enriched", "new"]))
            if sectors:
                q = q.where(AccountRecord.sector.in_(sectors))
            if cities:
                q = q.where(AccountRecord.city.in_(cities))
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

            recent_cutoff = _utcnow() - timedelta(days=14)
            recent_logs = (await session.execute(
                select(EmailSendLog.account_id).where(
                    EmailSendLog.sent_at >= recent_cutoff
                ).distinct()
            )).scalars().all() if ids else []
            recently_contacted = set(recent_logs)
        except Exception as exc:  # noqa: BLE001
            return {"status": "skipped_db_unreachable", "error": str(exc)}

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
        ac_contacts = contacts_by_acc.get(a.id, [])
        if any(c.opt_out for c in ac_contacts):
            excluded["opt_out"] += 1
            continue
        business_email = next(
            (c.email for c in ac_contacts
             if c.email and c.email.lower() not in sup_emails
             and not any(p in c.email.lower() for p in _PERSONAL_EMAIL_DOMAINS)),
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

    selected = select_top_n_diversified(candidates, target_count=daily_target)

    selected_out: list[dict[str, Any]] = []
    sector_split: dict[str, int] = {}
    for acc in selected:
        base = render_email_template(acc, acc.get("priority") or "P2")
        if personalize_with_llm:
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

    queued_count = 0
    async with async_session_factory()() as session:
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
            f"personalize_with_llm={personalize_with_llm}",
        ],
    )
    return result.to_dict()


async def run_followups_core() -> dict[str, Any]:
    """Create +2 / +5 / +10 follow-up queue rows for unanswered sent emails.

    Walks ``EmailSendLog`` rows where ``status='sent'`` and no reply, and
    queues follow-up ``OutreachQueueRecord`` rows (``approval_required=True``).
    """
    now = _utcnow()
    created = 0
    skipped_replied = 0
    async with async_session_factory()() as session:
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
                        message=followup_template(step, log_row.subject),
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


async def run_lead_prep_core() -> dict[str, Any]:
    """Daily lead-prep: re-enqueue stale unscored accounts for scoring.

    Finds accounts in ``new`` / ``enriched`` status that have no recent
    ``LeadScoreRecord`` and reports them so the cron can fan out scoring
    jobs. Read-only; never sends anything.
    """
    async with async_session_factory()() as session:
        try:
            accounts = (await session.execute(
                select(AccountRecord).where(
                    AccountRecord.status.in_(["new", "enriched"])
                ).limit(500)
            )).scalars().all()
            ids = [a.id for a in accounts]
            scored = set((await session.execute(
                select(LeadScoreRecord.account_id).where(
                    LeadScoreRecord.account_id.in_(ids)
                )
            )).scalars().all()) if ids else set()
        except Exception as exc:  # noqa: BLE001
            return {"status": "skipped_db_unreachable", "error": str(exc)}

    unscored = [a.id for a in accounts if a.id not in scored]
    return {
        "status": "ok",
        "accounts_scanned": len(accounts),
        "unscored_account_ids": unscored,
        "needs_scoring": len(unscored),
    }


def expire_stale_approvals() -> dict[str, Any]:
    """Sweep pending approvals whose ``expires_at`` has passed.

    Delegates to the shared ``ApprovalStore`` so the cron and the HTTP
    ``/expire-sweep`` endpoint share one implementation. Returns the
    expired count. This is a terminal transition; no send happens.
    """
    from auto_client_acquisition.approval_center import get_default_approval_store

    expired = get_default_approval_store().expire_overdue()
    return {"status": "ok", "expired_count": expired}
