"""Executive Orchestrator API — status, latest brief, and the tick.

The orchestrator queues and prepares; it never sends or charges.

  * ``GET  /api/v1/executive/status`` — read-only; always 200.
  * ``GET  /api/v1/executive/brief``  — read-only; latest brief or
    ``no_brief_yet``.
  * ``POST /api/v1/executive/tick``   — admin-gated and feature-flag
    gated; runs one tick and best-effort spawns internal jobs.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query, status

from api.security.api_key import require_admin_key

router = APIRouter(prefix="/api/v1/executive", tags=["executive-orchestrator"])

_CANONICAL_ACTION_TYPES = [
    "prepare_diagnostic",
    "draft_email",
    "draft_linkedin_manual",
    "call_script",
    "follow_up_task",
    "support_reply_draft",
    "payment_reminder",
    "delivery_task",
    "proof_request",
    "upsell_recommendation",
    "partner_intro",
]


def _orchestrator_enabled() -> bool:
    from core.config.settings import get_settings

    return bool(get_settings().executive_orchestrator_enabled)


@router.get("/status")
async def executive_status() -> dict[str, Any]:
    """Declare guardrails, autonomy ceiling, and flag state. Always 200."""
    from auto_client_acquisition.executive_os.schemas import GUARDRAILS

    return {
        "agent_id": "executive_orchestrator",
        "autonomy_level": 3,
        "autonomy_label": "L3_RECOMMEND",
        "enabled": _orchestrator_enabled(),
        "guardrails": GUARDRAILS,
        "canonical_action_types": _CANONICAL_ACTION_TYPES,
        "promise_ar": "يَصفّ ويُحضّر — لا يُرسل ولا يَخصم أبداً.",
        "promise_en": "Queues and prepares — never sends, never charges.",
    }


@router.get("/brief")
async def executive_brief() -> dict[str, Any]:
    """Return the latest executive brief, or ``no_brief_yet``."""
    from auto_client_acquisition.executive_os import load_latest_brief

    latest = load_latest_brief()
    if latest is None:
        return {"data_status": "no_brief_yet"}
    return {"data_status": "ok", "brief": latest}


@router.post("/tick", dependencies=[Depends(require_admin_key)])
async def executive_tick(dry_run: bool = Query(False)) -> dict[str, Any]:
    """Run one executive tick. Admin-gated; 404 when the flag is off."""
    if not _orchestrator_enabled():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="executive orchestrator is disabled",
        )
    from fastapi.concurrency import run_in_threadpool

    from auto_client_acquisition.executive_os import (
        run_executive_tick,
        spawn_internal_jobs,
    )
    from auto_client_acquisition.executive_os.schemas import ExecutiveTickResult

    result: ExecutiveTickResult = await run_in_threadpool(run_executive_tick, dry_run=dry_run)
    spawned: list[dict[str, Any]] = []
    if result.ok and not dry_run and result.intended_jobs:
        spawned = await spawn_internal_jobs(result.intended_jobs)
    payload: dict[str, Any] = result.to_dict()
    payload["spawned_jobs_result"] = spawned
    return payload
