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

    Every externally-visible output returns as ``pending_approval`` — it
    must still be approved via /api/v1/approvals before anything is sent.
    """
    run_date = payload.get("run_date")
    context = payload.get("context") or {}
    if not isinstance(context, dict):
        raise HTTPException(status_code=422, detail="context must be an object")

    report = run_daily_cycle(run_date=run_date, context=context)
    log.info(
        "agent_org_cycle",
        cycle_id=report.cycle_id,
        agents_run=report.agents_run,
        pending_approval=report.items_pending_approval,
    )
    return report.to_dict()
