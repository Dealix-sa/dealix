"""
Omni-Channel Growth OS API.

POST /api/v1/omni-channel/run-batch
    Process a batch of companies through the pipeline.
    Body: {companies: [...], date: "YYYY-MM-DD"}

GET  /api/v1/omni-channel/founder-queue
    List items in the founder review queue.
    ?limit=100&min_quality=65

POST /api/v1/omni-channel/founder-queue/{item_id}/approve
    Approve a queue item.

POST /api/v1/omni-channel/founder-queue/{item_id}/skip
    Skip a queue item.

POST /api/v1/omni-channel/inbound/process
    Process an inbound lead from any source.
    Body: LeadCapture dict

POST /api/v1/omni-channel/intake/submit
    Submit a website intake form.

GET  /api/v1/omni-channel/report/today
    Get today's channel report.

GET  /api/v1/omni-channel/learning/report
    Get the daily learning report.

POST /api/v1/omni-channel/learning/signal
    Record a reply/signal for a sent asset.

GET  /api/v1/omni-channel/quota/today
    Get today's quota progress.
"""
from __future__ import annotations

import logging
from typing import Any

from fastapi import APIRouter, Body, HTTPException

router = APIRouter(prefix="/api/v1/omni-channel", tags=["omni-channel"])
log = logging.getLogger(__name__)


@router.post("/run-batch")
def run_batch(body: dict[str, Any] = Body(default={})) -> dict[str, Any]:
    """
    Process a batch of companies through the omni-channel pipeline.

    Body:
        companies: list of company dicts
        date: optional YYYY-MM-DD string
    """
    try:
        from auto_client_acquisition.omni_channel_os.daily_quota_engine import DailyQuotaEngine
        from auto_client_acquisition.omni_channel_os.schemas import Company

        raw_companies = body.get("companies") or []
        date = body.get("date")

        if not isinstance(raw_companies, list):
            raise HTTPException(400, "companies_must_be_a_list")

        companies: list[Company] = []
        for raw in raw_companies:
            try:
                companies.append(Company.model_validate(raw))
            except Exception as exc:
                log.warning("run_batch.invalid_company data=%r error=%s", raw, exc)

        engine = DailyQuotaEngine()
        summary = engine.run(companies=companies, date=date)
        return {"governance_decision": "approved", **summary}
    except HTTPException:
        raise
    except Exception as exc:
        log.warning("run_batch.error error=%s", exc)
        return {"governance_decision": "error", "status": "error", "error": str(exc)}


@router.get("/founder-queue")
def list_founder_queue(
    limit: int = 100,
    min_quality: float = 65.0,
) -> dict[str, Any]:
    """List items in the founder review queue, sorted by quality score."""
    try:
        from auto_client_acquisition.omni_channel_os.founder_review_queue import FounderReviewQueue

        queue = FounderReviewQueue()
        queue.load()
        items = queue.get_top(limit=limit, min_quality=min_quality)
        formatted = [queue.format_for_founder(item) for item in items]
        return {
            "governance_decision": "approved",
            "count": len(formatted),
            "items": formatted,
        }
    except Exception as exc:
        log.warning("list_founder_queue.error error=%s", exc)
        return {
            "governance_decision": "error",
            "status": "error",
            "error": str(exc),
            "items": [],
        }


@router.post("/founder-queue/{item_id}/approve")
def approve_queue_item(item_id: str) -> dict[str, Any]:
    """Approve a founder queue item."""
    try:
        from auto_client_acquisition.omni_channel_os.founder_review_queue import FounderReviewQueue

        queue = FounderReviewQueue()
        queue.load()
        found = queue.approve(item_id)
        if not found:
            raise HTTPException(404, "queue_item_not_found")
        queue.save()
        return {"governance_decision": "approved", "item_id": item_id, "status": "approved"}
    except HTTPException:
        raise
    except Exception as exc:
        log.warning("approve_queue_item.error item_id=%s error=%s", item_id, exc)
        return {
            "governance_decision": "error",
            "status": "skipped_db_unreachable",
            "error": str(exc),
        }


@router.post("/founder-queue/{item_id}/skip")
def skip_queue_item(
    item_id: str,
    body: dict[str, Any] = Body(default={}),
) -> dict[str, Any]:
    """Skip a founder queue item."""
    reason = str(body.get("reason") or "manual_skip")[:255]
    try:
        from auto_client_acquisition.omni_channel_os.founder_review_queue import FounderReviewQueue

        queue = FounderReviewQueue()
        queue.load()
        found = queue.skip(item_id, reason=reason)
        if not found:
            raise HTTPException(404, "queue_item_not_found")
        queue.save()
        return {
            "governance_decision": "approved",
            "item_id": item_id,
            "status": "skipped",
            "reason": reason,
        }
    except HTTPException:
        raise
    except Exception as exc:
        log.warning("skip_queue_item.error item_id=%s error=%s", item_id, exc)
        return {
            "governance_decision": "error",
            "status": "skipped_db_unreachable",
            "error": str(exc),
        }


@router.post("/inbound/process")
def process_inbound(body: dict[str, Any] = Body(default={})) -> dict[str, Any]:
    """Process an inbound lead from any paid source."""
    try:
        from auto_client_acquisition.omni_channel_os.lead_capture_os import LeadCaptureOS

        source = str(body.get("source") or "website")
        os_instance = LeadCaptureOS()
        lead = os_instance.process_lead(body, source=source)
        followup = os_instance.generate_followup(lead, source=source)

        return {
            "governance_decision": "approved",
            "status": "processed",
            "lead_id": lead.lead.lead_id,
            "qualification_score": lead.qualification_score,
            "offer_route": lead.offer_route,
            "followup_draft": {
                "body": followup.body,
                "cta": followup.cta,
                "channel": followup.channel.value,
                "is_auto_sendable": followup.is_auto_sendable,
                "approval_status": followup.approval_status,
            },
        }
    except Exception as exc:
        log.warning("process_inbound.error error=%s", exc)
        return {
            "governance_decision": "error",
            "status": "error",
            "error": str(exc),
        }


@router.post("/intake/submit")
def submit_intake(body: dict[str, Any] = Body(default={})) -> dict[str, Any]:
    """Submit a website intake form and get a qualified lead + auto-reply."""
    try:
        from auto_client_acquisition.omni_channel_os.inbound_intake_os import InboundIntakeOS

        intake = InboundIntakeOS()
        lead = intake.process_submission(body)
        call_brief = intake.create_call_brief(lead)

        return {
            "governance_decision": "approved",
            "status": "processed",
            "lead_id": lead.lead.lead_id,
            "qualification_score": lead.qualification_score,
            "offer_route": lead.offer_route,
            "auto_reply_draft": lead.auto_reply_draft,
            "call_brief": call_brief,
        }
    except Exception as exc:
        log.warning("submit_intake.error error=%s", exc)
        return {
            "governance_decision": "error",
            "status": "error",
            "error": str(exc),
        }


@router.get("/report/today")
def get_today_report() -> dict[str, Any]:
    """Get today's channel report from the last batch run."""
    try:
        from auto_client_acquisition.omni_channel_os.daily_quota_engine import DailyQuotaEngine

        engine = DailyQuotaEngine()
        summary = engine.get_today_summary()
        return {"governance_decision": "approved", **summary}
    except Exception as exc:
        log.warning("get_today_report.error error=%s", exc)
        return {
            "governance_decision": "error",
            "status": "error",
            "error": str(exc),
        }


@router.get("/learning/report")
def get_learning_report() -> dict[str, Any]:
    """Get the daily learning report."""
    try:
        from auto_client_acquisition.omni_channel_os.learning_engine import LearningEngine

        engine = LearningEngine()
        report = engine.daily_learning_report()
        return {"governance_decision": "approved", **report}
    except Exception as exc:
        log.warning("get_learning_report.error error=%s", exc)
        return {
            "governance_decision": "error",
            "status": "error",
            "error": str(exc),
        }


@router.post("/learning/signal")
def record_signal(body: dict[str, Any] = Body(default={})) -> dict[str, Any]:
    """Record a reply/engagement signal for a sent asset."""
    try:
        from datetime import UTC, datetime

        from auto_client_acquisition.omni_channel_os.learning_engine import LearningEngine
        from auto_client_acquisition.omni_channel_os.schemas import LearningSignal

        signal = LearningSignal(
            company_id=str(body.get("company_id") or "unknown"),
            channel=str(body.get("channel") or "unknown"),
            asset_type=str(body.get("asset_type") or "unknown"),
            sent_at=body.get("sent_at") or datetime.now(UTC),
            response_type=str(body.get("response_type") or "no_reply"),
            response_text=body.get("response_text"),
            sector=str(body.get("sector") or "other"),
            country=str(body.get("country") or "KSA"),
            language=str(body.get("language") or "arabic"),
            offer=str(body.get("offer") or "unknown"),
            quality_score_at_send=float(body.get("quality_score_at_send") or 70.0),
        )

        engine = LearningEngine()
        engine.record_signal(signal)
        return {
            "governance_decision": "approved",
            "status": "recorded",
            "signal_id": signal.signal_id,
        }
    except Exception as exc:
        log.warning("record_signal.error error=%s", exc)
        return {
            "governance_decision": "error",
            "status": "error",
            "error": str(exc),
        }


@router.get("/quota/today")
def get_quota_today() -> dict[str, Any]:
    """Get today's quota progress from the last completed batch."""
    try:
        from auto_client_acquisition.omni_channel_os.daily_quota_engine import DailyQuotaEngine

        engine = DailyQuotaEngine()
        summary = engine.get_today_summary()
        quota_data = summary.get("quota") or summary
        return {"governance_decision": "approved", "quota": quota_data, **summary}
    except Exception as exc:
        log.warning("get_quota_today.error error=%s", exc)
        return {
            "governance_decision": "error",
            "status": "error",
            "error": str(exc),
        }
