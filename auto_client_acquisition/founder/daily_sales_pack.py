"""Aggregate founder morning sales pack — read-only composition."""
from __future__ import annotations

from datetime import UTC, datetime
from typing import Any


def _safe(fn, default: Any) -> Any:
    try:
        return fn()
    except BaseException as exc:  # noqa: BLE001
        return {"_error": True, "_message": str(exc)[:200], "_default": default}


async def fetch_outreach_queue_sample(*, limit: int = 25) -> dict[str, Any]:
    try:
        from sqlalchemy import select

        from db.models import OutreachQueueRecord
        from db.session import async_session_factory

        async with async_session_factory() as session:
            rows = (
                await session.execute(
                    select(OutreachQueueRecord)
                    .where(OutreachQueueRecord.status.in_(["queued", "approved"]))
                    .order_by(OutreachQueueRecord.created_at.desc())
                    .limit(limit)
                )
            ).scalars().all()
        pending = [r for r in rows if r.status == "queued"]
        return {
            "total_sampled": len(rows),
            "pending_count": len(pending),
            "items": [
                {
                    "id": r.id,
                    "status": r.status,
                    "channel": r.channel,
                    "approval_required": r.approval_required,
                    "leadops_id": (r.meta_json or {}).get("leadops_id"),
                }
                for r in rows
            ],
        }
    except Exception as exc:  # noqa: BLE001
        return {"pending_count": 0, "items": [], "note": str(exc)[:120]}


def build_daily_sales_pack(
    *,
    outreach_queue: dict[str, Any] | None = None,
    leads_limit: int = 15,
) -> dict[str, Any]:
    from auto_client_acquisition.personal_operator.operator import (
        build_daily_brief,
        launch_readiness_score,
    )
    from auto_client_acquisition import lead_inbox
    from auto_client_acquisition.approval_center import list_pending

    brief = build_daily_brief().to_dict()
    readiness = launch_readiness_score()
    pending = list_pending()

    leads_payload = {
        "leads": lead_inbox.list_leads(limit=leads_limit),
        "stats": lead_inbox.stats(),
    }

    return {
        "schema_version": 1,
        "generated_at": datetime.now(UTC).isoformat(),
        "read_only": True,
        "hard_gates": {
            "no_cold_whatsapp": True,
            "no_linkedin_automation": True,
            "approval_required_for_external_send": True,
        },
        "daily_brief": brief,
        "launch_readiness": readiness,
        "pending_approvals": {
            "count": len(pending),
            "first_5": [p.model_dump(mode="json") for p in pending[:5]],
        },
        "founder_leads": leads_payload,
        "outreach_queue": outreach_queue or {"pending_count": 0, "items": []},
        "gtm_content_calendar_url": "/api/v1/gtm/content-calendar",
        "next_urls": {
            "approvals_ui": "/ar/approvals",
            "operator_ui": "/ar/operator",
            "command_center_ui": "/ar/command-center",
        },
    }
