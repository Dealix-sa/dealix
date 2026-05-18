"""Founder agent task queue API — governed daily fleet (no external send)."""

from __future__ import annotations

from typing import Any, Literal

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from api.security.api_key import require_admin_key

router = APIRouter(prefix="/api/v1/founder", tags=["founder-agent-queue"])

TaskStatusLiteral = Literal["pending", "in_progress", "done", "blocked", "skipped"]


class AgentQueuePatchBody(BaseModel):
    status: TaskStatusLiteral


@router.get("/agent-queue", dependencies=[Depends(require_admin_key)])
async def get_agent_queue() -> dict[str, Any]:
    from dealix.commercial_ops.founder_agent_tasks import build_queue_status

    return build_queue_status()


@router.post("/agent-queue/seed-today", dependencies=[Depends(require_admin_key)])
async def seed_agent_queue_today() -> dict[str, Any]:
    from dealix.commercial_ops.founder_agent_tasks import build_queue_status, seed_today_queue

    seed_today_queue(force=True)
    out = build_queue_status()
    out["seeded"] = True
    return out


@router.get("/agent-fleet/today-pack", dependencies=[Depends(require_admin_key)])
async def agent_fleet_today_pack() -> dict[str, Any]:
    from dealix.commercial_ops.agent_fleet_tasks import build_agent_fleet_today_pack
    from dealix.commercial_ops.ceo_gtm_operating_system import build_ceo_gtm_status
    from dealix.commercial_ops.doctrine import build_soaen_daily

    return {
        "soaen": build_soaen_daily(),
        "agent_fleet": build_agent_fleet_today_pack(),
        "ceo_gtm_status": build_ceo_gtm_status(api_base=False),
    }


@router.patch("/agent-queue/tasks/{task_id}", dependencies=[Depends(require_admin_key)])
async def patch_agent_queue_task(task_id: str, body: AgentQueuePatchBody) -> dict[str, Any]:
    from dealix.commercial_ops.founder_agent_tasks import update_task_status

    result = update_task_status(task_id, body.status)
    if not result.get("ok"):
        raise HTTPException(status_code=404, detail=result.get("error", "task_not_found"))
    return result
