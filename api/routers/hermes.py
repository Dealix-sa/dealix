"""Hermes HTTP surface — `/api/v1/hermes/*`.

Single dispatcher endpoint that lets the founder (or an authed automation
like n8n / WhatsApp Decision Bot / Railway cron) trigger a Hermes run
remotely while preserving every doctrine guarantee:

  - All endpoints sit behind ``require_admin_key`` (X-Admin-API-Key).
  - The orchestrator's governance gate runs unchanged. The HTTP layer
    never bypasses a refusal.
  - No external send happens here. ``needs_approval`` returns the
    placeholder and a pointer to the approval_center queue.
  - Audit + friction_log writes happen inside ``HermesOrchestrator``.

This router intentionally exposes only a thin shell; the heavy lifting
lives in ``dealix/hermes/``.
"""
from __future__ import annotations

from typing import Any, Optional

from fastapi import APIRouter, Body, Depends, HTTPException
from pydantic import BaseModel, ConfigDict, Field

from api.security.api_key import require_admin_key
from core.logging import get_logger
from dealix.hermes import HermesOrchestrator, HermesTask
from dealix.hermes.agents import route_to_agent_executor
from dealix.hermes.governance_gate import Decision
from dealix.hermes.identity import HermesIdentity
from dealix.hermes.router import TaskClass
from dealix.llm.engine import active_provider, fallback_provider


router = APIRouter(
    prefix="/api/v1/hermes",
    tags=["hermes"],
    dependencies=[Depends(require_admin_key)],
)
log = get_logger(__name__)


class HermesDispatchRequest(BaseModel):
    """Inbound dispatch payload."""
    model_config = ConfigDict(extra="forbid")

    intent: str = Field(..., min_length=1, max_length=2000)
    customer_id: str = Field(default="dealix_internal", max_length=128)
    channel: str = Field(default="", max_length=32)
    hint: Optional[str] = Field(
        default=None,
        description="One of: pm, engineering, content, sales, delivery. "
                    "When omitted, the router classifies from the intent.",
    )


def _hint_to_taskclass(hint: Optional[str]) -> Optional[TaskClass]:
    if not hint:
        return None
    try:
        return TaskClass(hint.strip().lower())
    except ValueError as exc:
        raise HTTPException(
            status_code=422,
            detail=f"Unknown hint '{hint}'. Allowed: {[t.value for t in TaskClass]}",
        ) from exc


@router.get("/status")
async def status() -> dict[str, Any]:
    identity = HermesIdentity.current()
    return {
        "module": "hermes",
        "agent_id": identity.agent_id,
        "version": identity.version,
        "kill_switch": identity.kill_switch,
        "provider": active_provider(),
        "fallback_provider": fallback_provider(),
        "guardrails": {
            "no_live_send": True,
            "no_scraping": True,
            "no_cold_outreach": True,
            "approval_center_gated_externals": True,
        },
        "endpoints": [
            "/status",
            "/dispatch",
        ],
    }


@router.post("/dispatch")
async def dispatch(
    payload: HermesDispatchRequest = Body(...),
) -> dict[str, Any]:
    """Run a single Hermes dispatch and return the structured result.

    HTTP semantics:
      - 200: governance approved, executor reported ok.
      - 202: needs_approval — drafted and queued; nothing was sent.
      - 403: rejected by doctrine (cold outreach / scraping / fabrication).
      - 409: kill switch active (HERMES_KILL_SWITCH=1).
      - 500: executor crashed; orchestrator captured the error.
    """
    hint = _hint_to_taskclass(payload.hint)
    orch = HermesOrchestrator(executor=route_to_agent_executor)
    result = orch.dispatch(
        HermesTask(
            intent=payload.intent,
            customer_id=payload.customer_id,
            channel=payload.channel,
            hint=hint,
        )
    )
    body = result.to_dict()

    log.info(
        "hermes_dispatch",
        run_id=result.run_id,
        decision=result.decision.decision,
        sub_agent=(result.route.sub_agent if result.route else None),
    )

    decision = result.decision.decision
    if decision == Decision.REJECTED.value:
        raise HTTPException(status_code=403, detail=body)
    if decision == Decision.KILL_SWITCHED.value:
        raise HTTPException(status_code=409, detail=body)
    if decision == Decision.NEEDS_APPROVAL.value:
        # FastAPI converts 200 → 202 only via status_code in decorator; emit body
        # with explicit hint so callers can branch on result["governance_decision"].
        return {"http_hint_status": 202, **body}
    if not result.success:
        raise HTTPException(status_code=500, detail=body)
    return body
