"""Agent Organization HTTP surface.

Exposes the Dealix Agent Organization — the org chart, per-role detail,
the structural integrity check, and the daily executive cycle.

Hard rules:
  - The daily cycle does work but sends nothing; external outputs come
    back as ``pending_approval`` and must flow through /api/v1/approvals.
  - Read endpoints are pure; the cycle endpoint is deterministic given
    its input context.
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Body, HTTPException

from auto_client_acquisition.agent_org.approval_routing import (
    route_report_to_approvals,
)
from auto_client_acquisition.agent_org.cycle_store import get_default_cycle_store
from auto_client_acquisition.agent_org.org_chart import (
    get_role,
    has_role,
    org_chart_dict,
    all_roles,
    validate_org,
)
from auto_client_acquisition.agent_org.orchestrator import run_daily_cycle
from core.logging import get_logger

router = APIRouter(prefix="/api/v1/agent-org", tags=["agent-org"])
log = get_logger(__name__)


@router.get("/status")
async def status() -> dict[str, Any]:
    roles = all_roles()
    return {
        "module": "agent_org",
        "headcount": len(roles),
        "tiers": {
            "chief": sum(1 for r in roles if r.tier == 0),
            "directors": sum(1 for r in roles if r.tier == 1),
            "operators": sum(1 for r in roles if r.tier == 2),
        },
        "guardrails": {
            "governed_autonomy": True,
            "external_output_is_draft_only": True,
            "no_auto_send": True,
            "no_scraping": True,
            "max_autonomy_for_external": "L2_DRAFT",
        },
        "endpoints": [
            "/chart",
            "/agents",
            "/agents/{agent_id}",
            "/validate",
            "/daily-cycle/run",
            "/cycles",
            "/cycles/latest",
            "/cycles/{cycle_id}",
        ],
    }


@router.get("/chart")
async def chart() -> dict[str, Any]:
    """The full org pyramid — chief -> directors -> operators."""
    return org_chart_dict()


@router.get("/agents")
async def agents() -> dict[str, Any]:
    roles = all_roles()
    return {"count": len(roles), "agents": [r.to_dict() for r in roles]}


@router.get("/agents/{agent_id}")
async def agent_detail(agent_id: str) -> dict[str, Any]:
    if not has_role(agent_id):
        raise HTTPException(status_code=404, detail=f"unknown agent {agent_id!r}")
    return get_role(agent_id).to_dict()


@router.get("/validate")
async def validate() -> dict[str, Any]:
    """Structural integrity check of the organization."""
    problems = validate_org()
    return {"healthy": not problems, "problems": problems}


@router.post("/daily-cycle/run")
async def daily_cycle_run(
    payload: dict[str, Any] = Body(default_factory=dict),
) -> dict[str, Any]:
    """Run one daily executive cycle.

    Optional body:
      - ``run_date``: ISO date string for the cycle (defaults to today).
      - ``context``: light inputs (account targets, sprints in flight, …).
      - ``route_to_approvals``: bool (default ``true``) — push every
        external draft into ``/api/v1/approvals`` for one-click review.
      - ``persist``: bool (default ``true``) — store the report in the
        cycle history so /cycles endpoints can return it.

    Every externally-visible output returns as ``pending_approval`` — it
    must still be approved via /api/v1/approvals before anything is sent.
    """
    run_date = payload.get("run_date")
    context = payload.get("context") or {}
    if not isinstance(context, dict):
        raise HTTPException(status_code=422, detail="context must be an object")
    route_flag = bool(payload.get("route_to_approvals", True))
    persist_flag = bool(payload.get("persist", True))

    report = run_daily_cycle(run_date=run_date, context=context)

    routed = 0
    if route_flag:
        created = route_report_to_approvals(report)
        routed = len(created)

    if persist_flag:
        get_default_cycle_store().add(report)

    log.info(
        "agent_org_cycle",
        cycle_id=report.cycle_id,
        agents_run=report.agents_run,
        pending_approval=report.items_pending_approval,
        routed_to_approvals=routed,
        persisted=persist_flag,
    )
    body = report.to_dict()
    body["routed_to_approvals"] = routed
    body["persisted"] = persist_flag
    return body


@router.get("/cycles")
async def cycles_list(limit: int = 20) -> dict[str, Any]:
    """Recent cycles, most-recent first. Capped at 60 in memory."""
    if limit < 1 or limit > 60:
        raise HTTPException(status_code=422, detail="limit must be in [1, 60]")
    store = get_default_cycle_store()
    recent = store.list_recent(limit=limit)
    return {
        "count": len(recent),
        "stored": len(store),
        "cycles": [
            {
                "cycle_id": r.cycle_id,
                "run_date": r.run_date,
                "agents_run": r.agents_run,
                "items_total": r.items_total,
                "items_pending_approval": r.items_pending_approval,
                "items_internal": r.items_internal,
                "escalations": len(r.escalations),
            }
            for r in recent
        ],
    }


@router.get("/cycles/latest")
async def cycles_latest() -> dict[str, Any]:
    """Full report for the most recent cycle, or 404 if none."""
    latest = get_default_cycle_store().latest()
    if latest is None:
        raise HTTPException(status_code=404, detail="no cycles run yet")
    return latest.to_dict()


@router.get("/cycles/{cycle_id}")
async def cycles_detail(cycle_id: str) -> dict[str, Any]:
    """Full report for one cycle by id."""
    report = get_default_cycle_store().get(cycle_id)
    if report is None:
        raise HTTPException(status_code=404, detail=f"unknown cycle {cycle_id!r}")
    return report.to_dict()
