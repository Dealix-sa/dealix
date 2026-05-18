"""
ARQ async task worker — registers all background job functions.
عامل المهام غير المتزامن — يسجّل جميع وظائف المهام الخلفية.

ARQ (async Redis Queue) provides:
  - Redis-backed job queue (no extra broker infra beyond Redis)
  - Automatic retry with exponential backoff
  - Job deduplication
  - Cron scheduling

Startup command:
    arq core.tasks.worker.WorkerSettings

Job submission from FastAPI:
    from arq import create_pool
    redis = await create_pool(RedisSettings.from_url(settings.redis_url))
    await redis.enqueue_job("run_lead_scoring", lead_id="abc123", tenant_id="t1")
"""

from __future__ import annotations

from datetime import timedelta
from typing import Any

from arq import cron
from arq.connections import RedisSettings

from core.config.settings import get_settings
from core.logging import get_logger

logger = get_logger(__name__)


# ── Job Functions ─────────────────────────────────────────────────

async def run_lead_scoring(ctx: dict[str, Any], lead_id: str, tenant_id: str) -> dict[str, Any]:
    """
    Score a lead using the ICP fit + urgency heuristics + LLM enrichment.
    تقييم العميل المحتمل باستخدام نماذج الذكاء الاصطناعي.
    """
    from core.agents.lead_scoring import LeadScoringAgent
    from db.session import AsyncSessionLocal

    logger.info("job_lead_scoring_start", lead_id=lead_id, tenant_id=tenant_id)
    async with AsyncSessionLocal() as session:
        agent = LeadScoringAgent(session=session)
        result = await agent.score(lead_id=lead_id, tenant_id=tenant_id)
    logger.info("job_lead_scoring_done", lead_id=lead_id, score=result.get("fit_score"))
    return result


async def run_proposal_draft(
    ctx: dict[str, Any],
    deal_id: str,
    tenant_id: str,
    lang: str = "ar",
) -> dict[str, Any]:
    """
    Draft a localised proposal for a deal using the Proposal agent.
    صياغة عرض سعر محلّي للصفقة باستخدام وكيل المقترحات.
    """
    from core.agents.proposal import ProposalAgent
    from db.session import AsyncSessionLocal

    logger.info("job_proposal_draft_start", deal_id=deal_id, lang=lang)
    async with AsyncSessionLocal() as session:
        agent = ProposalAgent(session=session)
        result = await agent.draft(deal_id=deal_id, tenant_id=tenant_id, lang=lang)
    logger.info("job_proposal_draft_done", deal_id=deal_id)
    return result


async def run_outreach_batch(
    ctx: dict[str, Any],
    batch_id: str,
    tenant_id: str,
) -> dict[str, Any]:
    """
    Execute a personalised outreach email batch.
    تنفيذ دفعة بريد إلكتروني للتواصل المخصّص.
    """
    from core.agents.outreach import OutreachAgent
    from db.session import AsyncSessionLocal

    logger.info("job_outreach_batch_start", batch_id=batch_id)
    async with AsyncSessionLocal() as session:
        agent = OutreachAgent(session=session)
        result = await agent.execute_batch(batch_id=batch_id, tenant_id=tenant_id)
    logger.info("job_outreach_batch_done", batch_id=batch_id, sent=result.get("sent"))
    return result


async def run_account_enrichment(
    ctx: dict[str, Any],
    account_id: str,
    tenant_id: str,
) -> dict[str, Any]:
    """
    Enrich an account profile from public data sources.
    إثراء ملف الحساب من مصادر البيانات العامة.
    """
    from core.agents.enrichment import EnrichmentAgent
    from db.session import AsyncSessionLocal

    logger.info("job_enrichment_start", account_id=account_id)
    async with AsyncSessionLocal() as session:
        agent = EnrichmentAgent(session=session)
        result = await agent.enrich_account(account_id=account_id, tenant_id=tenant_id)
    logger.info("job_enrichment_done", account_id=account_id)
    return result


async def run_embedding_refresh(
    ctx: dict[str, Any],
    entity_type: str,
    entity_id: str,
    tenant_id: str,
) -> dict[str, Any]:
    """
    Re-embed an entity into the Revenue Memory vector store.
    إعادة تضمين كيان في مخزن المتجهات — ذاكرة الإيرادات.
    """
    from core.memory.embedding_service import EmbeddingService
    from db.session import AsyncSessionLocal

    logger.info("job_embedding_refresh", entity_type=entity_type, entity_id=entity_id)
    async with AsyncSessionLocal() as session:
        svc = EmbeddingService(session=session)
        result = await svc.refresh(entity_type=entity_type, entity_id=entity_id, tenant_id=tenant_id)
    return result


async def run_zatca_clearance(
    ctx: dict[str, Any],
    invoice_id: str,
    tenant_id: str,
) -> dict[str, Any]:
    """
    Submit invoice to ZATCA for Phase 2 clearance/reporting.
    إرسال الفاتورة إلى هيئة الزكاة والضريبة والجمارك للمقاصة.
    """
    from integrations.zatca import ZATCAClient
    from db.session import AsyncSessionLocal

    logger.info("job_zatca_clearance_start", invoice_id=invoice_id)
    async with AsyncSessionLocal() as session:
        client = ZATCAClient(session=session, tenant_id=tenant_id)
        result = await client.submit_for_clearance(invoice_id=invoice_id)
    logger.info("job_zatca_clearance_done", invoice_id=invoice_id, status=result.get("status"))
    return result


# ── Cron Jobs ─────────────────────────────────────────────────────

async def daily_pipeline_refresh(ctx: dict[str, Any]) -> None:
    """
    Nightly pipeline health check — re-score stale leads, refresh embeddings.
    فحص صحة خط الأنابيب الليلي — إعادة تقييم العملاء المحتملين القديمين.
    """
    logger.info("cron_daily_pipeline_refresh_start")
    # Implementation: query leads older than 7d with status=new and re-enqueue scoring
    pass


# ── Governed Autopilot daily motion ───────────────────────────────
# These cron jobs automate drafting / scoring / scheduling / queuing only.
# Prospect outreach is NEVER auto-sent here: the daily-targeting job queues
# drafts into the durable approval queue (approval_required=True). The
# founder's approval tap remains the only send trigger for prospects.
#
# ARQ cron runs in UTC; Riyadh is UTC+3 (AST). The UTC hour for an AST
# target hour H is (H - 3) mod 24.

async def daily_lead_prep(ctx: dict[str, Any]) -> dict[str, Any]:
    """
    Daily lead-prep — find stale unscored accounts and fan out scoring jobs.
    Runs 06:00 AST (03:00 UTC).
    """
    from auto_client_acquisition.automation.daily_runner import run_lead_prep_core

    logger.info("cron_daily_lead_prep_start")
    result = await run_lead_prep_core()
    redis = ctx.get("redis")
    enqueued = 0
    if redis is not None and result.get("status") == "ok":
        for account_id in result.get("unscored_account_ids", []):
            await redis.enqueue_job(
                "run_lead_scoring", lead_id=account_id, tenant_id="default"
            )
            enqueued += 1
    logger.info(
        "cron_daily_lead_prep_done",
        needs_scoring=result.get("needs_scoring", 0),
        scoring_jobs_enqueued=enqueued,
    )
    return {**result, "scoring_jobs_enqueued": enqueued}


async def daily_targeting(ctx: dict[str, Any]) -> dict[str, Any]:
    """
    Daily-targeting — queue the TOP-50 personalised outreach drafts into the
    durable approval queue (approval_required=True). NEVER auto-sends.
    Runs 07:00 AST (04:00 UTC).
    """
    from auto_client_acquisition.automation.daily_runner import (
        run_daily_targeting_core,
    )

    logger.info("cron_daily_targeting_start")
    result = await run_daily_targeting_core(daily_target_count=50)
    logger.info(
        "cron_daily_targeting_done",
        selected=result.get("selected_count", 0),
        status=result.get("status", "ok"),
    )
    return result


async def daily_followups(ctx: dict[str, Any]) -> dict[str, Any]:
    """
    Follow-ups — queue +2/+5/+10 follow-up drafts for unanswered sent emails.
    Drafts only; approval_required=True. Runs 08:00 AST (05:00 UTC).
    """
    from auto_client_acquisition.automation.daily_runner import run_followups_core

    logger.info("cron_daily_followups_start")
    result = await run_followups_core()
    logger.info(
        "cron_daily_followups_done",
        followups_created=result.get("followups_created", 0),
    )
    return result


async def founder_daily_brief(ctx: dict[str, Any]) -> dict[str, Any]:
    """
    Founder daily brief — email the founder a summary of today's queued
    drafts, pending approvals, and follow-ups. Runs 08:30 AST (05:30 UTC).

    Emails via the existing EmailClient. The brief is an internal
    transactional message to the founder — not prospect outreach.
    """
    from auto_client_acquisition.approval_center import get_default_approval_store
    from core.config.settings import get_settings
    from integrations.email import EmailClient

    logger.info("cron_founder_daily_brief_start")
    settings = get_settings()

    pending = get_default_approval_store().list_pending()
    pending_email_drafts = sum(
        1 for r in pending
        if r.action_type == "draft_email" and (r.channel or "") == "email"
    )
    pending_blocked = sum(
        1 for r in pending
        if (r.channel or "").lower() in {"whatsapp", "linkedin", "phone"}
    )

    subject = f"Dealix daily brief — {len(pending)} approvals waiting"
    lines = [
        "Dealix Governed Autopilot — daily brief",
        "",
        f"Pending approvals: {len(pending)}",
        f"  email drafts (executable on approve): {pending_email_drafts}",
        f"  blocked-channel drafts (draft-only):  {pending_blocked}",
        "",
        "Action: review and batch-approve in the Approval Command Center.",
        "Prospect sends only happen after your approval tap.",
    ]
    body_text = "\n".join(lines)

    sent = False
    try:
        result = await EmailClient().send(
            to=settings.dealix_founder_email,
            subject=subject,
            body_text=body_text,
        )
        sent = result.success
    except Exception as exc:  # noqa: BLE001
        logger.warning("cron_founder_daily_brief_email_failed", error=str(exc))

    logger.info(
        "cron_founder_daily_brief_done",
        pending=len(pending),
        email_sent=sent,
    )
    return {
        "status": "ok",
        "pending_total": len(pending),
        "pending_email_drafts": pending_email_drafts,
        "pending_blocked_drafts": pending_blocked,
        "brief_emailed": sent,
    }


async def cron_own_brand_publish(ctx: dict[str, Any]) -> dict[str, Any]:
    """
    Own-brand publish — read cleared weekly-calendar slots for Dealix's OWN
    LinkedIn / X accounts and publish each via ``publish_own_brand``.

    Own-brand publishing may bypass the founder approval queue (the owner
    has authorized automated posting to Dealix's own accounts) but NEVER
    bypasses the safety gate: ``publish_own_brand`` runs the
    ``safe_publishing_gate`` text check first and routes flagged copy to
    the approval queue instead of publishing. Prospect / cold channels are
    rejected by the publisher itself. Runs 09:00 AST (06:00 UTC).
    """
    from auto_client_acquisition.gtm_os.content_calendar import (
        build_weekly_calendar,
    )
    from auto_client_acquisition.self_growth_os.social_publisher import (
        OWN_BRAND_CHANNELS,
        publish_own_brand,
    )

    logger.info("cron_own_brand_publish_start")
    calendar = build_weekly_calendar()
    own_brand_slots = [
        s for s in calendar.get("slots", [])
        if str(s.get("channel", "")) in OWN_BRAND_CHANNELS
    ]
    published = 0
    routed = 0
    dry_run = 0
    for slot in own_brand_slots:
        result = publish_own_brand(slot)
        outcome = result.get("outcome")
        if outcome == "published":
            published += 1
        elif outcome == "routed_to_approval":
            routed += 1
        elif outcome == "dry_run":
            dry_run += 1
    logger.info(
        "cron_own_brand_publish_done",
        own_brand_slots=len(own_brand_slots),
        published=published,
        routed_to_approval=routed,
        dry_run=dry_run,
    )
    return {
        "status": "ok",
        "own_brand_slots": len(own_brand_slots),
        "published": published,
        "routed_to_approval": routed,
        "dry_run": dry_run,
    }


async def expire_stale_approvals(ctx: dict[str, Any]) -> dict[str, Any]:
    """
    Stale-approval expire-sweep — flip pending approvals past expires_at to
    expired. Terminal transition; no send. Runs hourly.
    """
    from auto_client_acquisition.automation.daily_runner import (
        expire_stale_approvals as _expire,
    )

    logger.info("cron_expire_stale_approvals_start")
    result = _expire()
    logger.info(
        "cron_expire_stale_approvals_done",
        expired=result.get("expired_count", 0),
    )
    return result


# ── Worker lifecycle ──────────────────────────────────────────────

async def worker_on_startup(ctx: dict[str, Any]) -> None:
    """
    ARQ worker startup hook — rehydrate the in-memory approval queue from
    the durable ``approval_records`` table so a worker restart does not
    lose the founder's pending approvals. Degrades gracefully (no crash)
    when Postgres is unreachable.
    """
    try:
        from auto_client_acquisition.approval_center import durable_mirror

        count = await durable_mirror.hydrate()
        logger.info("worker_approval_rehydrate_done", rehydrated=count)
    except Exception as exc:  # noqa: BLE001
        logger.warning("worker_approval_rehydrate_skipped", error=str(exc))


# ── ARQ Worker Settings ───────────────────────────────────────────

class WorkerSettings:
    """
    ARQ WorkerSettings class — consumed by: arq core.tasks.worker.WorkerSettings
    إعدادات عامل ARQ.
    """

    functions = [
        run_lead_scoring,
        run_proposal_draft,
        run_outreach_batch,
        run_account_enrichment,
        run_embedding_refresh,
        run_zatca_clearance,
    ]

    # ARQ cron is UTC. Riyadh (AST) = UTC+3, so UTC hour = AST hour - 3.
    cron_jobs = [
        cron(daily_pipeline_refresh, hour=2, minute=0),     # 05:00 AST
        cron(daily_lead_prep, hour=3, minute=0),            # 06:00 AST
        cron(daily_targeting, hour=4, minute=0),            # 07:00 AST
        cron(daily_followups, hour=5, minute=0),            # 08:00 AST
        cron(founder_daily_brief, hour=5, minute=30),       # 08:30 AST
        cron(cron_own_brand_publish, hour=6, minute=0),     # 09:00 AST
        cron(expire_stale_approvals, minute=0),             # hourly, on the hour
    ]

    on_startup = worker_on_startup

    @staticmethod
    def redis_settings() -> RedisSettings:
        settings = get_settings()
        return RedisSettings.from_url(settings.redis_url)

    max_jobs = 20
    job_timeout = timedelta(minutes=10)
    keep_result = timedelta(hours=24)
    retry_jobs = True
    max_tries = 3
