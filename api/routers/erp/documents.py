"""
Document Management API.
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

router = APIRouter(prefix="/api/v1/erp/documents", tags=["ERP — Documents"])


class FolderCreate(BaseModel):
    name: str
    parent_id: str | None = None


class DocumentCreate(BaseModel):
    name: str
    folder_id: str | None = None
    size_bytes: int = 0
    mime_type: str = ""
    storage_key: str = ""


@router.post("/folders", dependencies=[Depends(FeatureGate("documents"))])
async def create_folder(
    req: FolderCreate,
    session: AsyncSession = Depends(get_db_session),
    current_user=Depends(get_current_user),
) -> dict[str, Any]:
    svc = ERPService(session)
    f = await svc.create_folder(current_user.tenant_id, {
        **req.dict(exclude_none=True),
        "created_by": current_user.id,
    })
    await session.commit()
    return {"id": f.id, "name": f.name}


@router.post("", dependencies=[Depends(FeatureGate("documents"))])
async def create_document(
    req: DocumentCreate,
    session: AsyncSession = Depends(get_db_session),
    current_user=Depends(get_current_user),
) -> dict[str, Any]:
    svc = ERPService(session)
    d = await svc.create_document(current_user.tenant_id, {
        **req.dict(exclude_none=True),
        "created_by": current_user.id,
    })
    await session.commit()
    return {"id": d.id, "name": d.name}


@router.get("")
async def list_documents(
    folder_id: str | None = None,
    session: AsyncSession = Depends(get_db_session),
    current_user=Depends(get_current_user),
) -> list[dict[str, Any]]:
    svc = ERPService(session)
    docs = await svc.list_documents(current_user.tenant_id, folder_id)
    return [{"id": d.id, "name": d.name, "size_bytes": d.size_bytes, "mime_type": d.mime_type} for d in docs]
