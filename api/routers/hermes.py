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
from fastapi.responses import JSONResponse
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


def _read_audit_ledger() -> list[dict[str, Any]]:
    """Lazy-read the JSONL audit ledger (small enough to scan in-process)."""
    from pathlib import Path
    import json
    import os
    p = Path(os.environ.get("HERMES_AUDIT_PATH", "var/hermes-runs.jsonl"))
    if not p.is_absolute():
        from dealix.hermes import audit as _audit  # noqa: PLC0415
        p = _audit._path()  # noqa: SLF001
    if not p.is_file():
        return []
    rows: list[dict[str, Any]] = []
    for line in p.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return rows


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
        # The HTTP contract documented in the docstring promises 202 for
        # approval-queued runs. JSONResponse lets us return the structured
        # body alongside the non-default status code so callers can branch
        # on the status as well as on `governance_decision.decision`.
        return JSONResponse(status_code=202, content=body)
    if not result.success:
        raise HTTPException(status_code=500, detail=body)
    return body


@router.get("/metrics")
async def metrics(window_days: int = 7) -> dict[str, Any]:
    """Aggregate counts over the last ``window_days`` of audit rows.

    Useful for the founder cockpit and for the CTO weekly anchor. No PII;
    aggregates only. ``window_days`` is clamped to [1, 90]; the response
    echoes the clamped value so the body and the data agree.
    """
    from datetime import UTC, datetime, timedelta

    clamped_window = max(1, min(window_days, 90))
    rows = _read_audit_ledger()
    cutoff = (datetime.now(UTC) - timedelta(days=clamped_window)).isoformat()
    recent = [r for r in rows if r.get("occurred_at", "") >= cutoff]

    by_decision: dict[str, int] = {}
    by_sub_agent: dict[str, int] = {}
    by_provider: dict[str, int] = {}
    success_count = 0
    for r in recent:
        gd = r.get("governance_decision") or {}
        decision = gd.get("decision", "unknown")
        by_decision[decision] = by_decision.get(decision, 0) + 1
        sub = r.get("sub_agent") or "unrouted"
        by_sub_agent[sub] = by_sub_agent.get(sub, 0) + 1
        prov = r.get("provider") or "none"
        by_provider[prov] = by_provider.get(prov, 0) + 1
        if r.get("success"):
            success_count += 1

    return {
        "window_days": clamped_window,
        "window_days_requested": window_days,
        "total_runs": len(recent),
        "success_runs": success_count,
        "by_decision": by_decision,
        "by_sub_agent": by_sub_agent,
        "by_provider": by_provider,
        "ledger_size": len(rows),
    }
