"""
Support Desk API.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from api.security.auth_deps import get_current_user
from db.session import get_db as get_db_session
from dealix.erp.service import ERPService
from dealix.feature_gating.service import FeatureGate

router = APIRouter(prefix="/api/v1/erp/support", tags=["ERP — Support"])


class TicketCreate(BaseModel):
    subject: str
    description: str = ""
    priority: str = "medium"
    category: str | None = None
    requester_email: str | None = None
    requester_name: str | None = None


class CommentCreate(BaseModel):
    body: str
    is_internal: bool = False


@router.post("/tickets", dependencies=[Depends(FeatureGate("support"))])
async def create_ticket(
    req: TicketCreate,
    session: AsyncSession = Depends(get_db_session),
    current_user=Depends(get_current_user),
) -> dict[str, Any]:
    svc = ERPService(session)
    t = await svc.create_ticket(current_user.tenant_id, {
        **req.dict(exclude_none=True),
        "assigned_to": current_user.id,
    })
    await session.commit()
    return {"id": t.id, "ticket_number": t.ticket_number, "status": t.status}


@router.get("/tickets")
async def list_tickets(
    status: str | None = None,
    session: AsyncSession = Depends(get_db_session),
    current_user=Depends(get_current_user),
) -> list[dict[str, Any]]:
    svc = ERPService(session)
    tickets = await svc.list_tickets(current_user.tenant_id, status)
    return [{"id": t.id, "subject": t.subject, "status": t.status, "priority": t.priority} for t in tickets]


@router.post("/tickets/{ticket_id}/comments")
async def add_comment(
    ticket_id: str,
    req: CommentCreate,
    session: AsyncSession = Depends(get_db_session),
    current_user=Depends(get_current_user),
) -> dict[str, Any]:
    svc = ERPService(session)
    c = await svc.add_ticket_comment(current_user.tenant_id, ticket_id, {
        **req.dict(),
        "author_id": current_user.id,
    })
    await session.commit()
    return {"id": c.id, "created_at": c.created_at}
