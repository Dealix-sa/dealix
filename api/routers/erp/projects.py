"""
Projects & Tasks API.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from api.security.auth_deps import get_current_user
from db.session import get_db as get_db_session
from dealix.erp.service import ERPService
from dealix.feature_gating.service import FeatureGate

router = APIRouter(prefix="/api/v1/erp/projects", tags=["ERP — Projects"])


class ProjectCreate(BaseModel):
    name: str
    description: str | None = None
    priority: str = "medium"
    start_date: str | None = None
    end_date: str | None = None
    budget_sar: float | None = None
    deal_id: str | None = None


class TaskCreate(BaseModel):
    name: str
    description: str | None = None
    status: str = "todo"
    priority: str = "medium"
    assigned_to: str | None = None
    due_date: str | None = None
    estimated_hours: float | None = None
    parent_task_id: str | None = None


@router.post("", dependencies=[Depends(FeatureGate("projects"))])
async def create_project(
    req: ProjectCreate,
    session: AsyncSession = Depends(get_db_session),
    current_user=Depends(get_current_user),
) -> dict[str, Any]:
    svc = ERPService(session)
    p = await svc.create_project(current_user.tenant_id, {
        **req.dict(exclude_none=True),
        "created_by": current_user.id,
    })
    await session.commit()
    return {"id": p.id, "name": p.name, "status": "created"}


@router.get("")
async def list_projects(
    status: str | None = None,
    session: AsyncSession = Depends(get_db_session),
    current_user=Depends(get_current_user),
) -> list[dict[str, Any]]:
    svc = ERPService(session)
    projects = await svc.list_projects(current_user.tenant_id, status)
    return [{"id": p.id, "name": p.name, "status": p.status, "priority": p.priority} for p in projects]


@router.post("/{project_id}/tasks", dependencies=[Depends(FeatureGate("projects"))])
async def create_task(
    project_id: str,
    req: TaskCreate,
    session: AsyncSession = Depends(get_db_session),
    current_user=Depends(get_current_user),
) -> dict[str, Any]:
    svc = ERPService(session)
    t = await svc.create_task(current_user.tenant_id, project_id, {
        **req.dict(exclude_none=True),
        "created_by": current_user.id,
    })
    await session.commit()
    return {"id": t.id, "name": t.name, "status": t.status}


@router.get("/{project_id}/tasks")
async def list_tasks(
    project_id: str,
    session: AsyncSession = Depends(get_db_session),
    current_user=Depends(get_current_user),
) -> list[dict[str, Any]]:
    svc = ERPService(session)
    tasks = await svc.list_tasks(current_user.tenant_id, project_id)
    return [{"id": t.id, "name": t.name, "status": t.status, "priority": t.priority} for t in tasks]
