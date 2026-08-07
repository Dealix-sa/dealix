"""
Finance GL API.
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

router = APIRouter(prefix="/api/v1/erp/finance", tags=["ERP — Finance"])


class AccountCreate(BaseModel):
    account_code: str
    account_name: str
    account_type: str
    parent_id: str | None = None
    is_bank_account: bool = False
    bank_name: str | None = None
    iban: str | None = None
    opening_balance: float = 0.0
    currency: str = "SAR"


class JournalEntryCreate(BaseModel):
    date: str
    description: str = ""
    reference_type: str | None = None
    reference_id: str | None = None
    lines: list[dict]


@router.post("/accounts", dependencies=[Depends(FeatureGate("finance"))])
async def create_account(
    req: AccountCreate,
    session: AsyncSession = Depends(get_db_session),
    current_user=Depends(get_current_user),
) -> dict[str, Any]:
    svc = ERPService(session)
    a = await svc.create_gl_account(current_user.tenant_id, {
        **req.dict(exclude_none=True),
    })
    await session.commit()
    return {"id": a.id, "account_code": a.account_code, "account_name": a.account_name}


@router.get("/accounts")
async def list_accounts(
    session: AsyncSession = Depends(get_db_session),
    current_user=Depends(get_current_user),
) -> list[dict[str, Any]]:
    svc = ERPService(session)
    accounts = await svc.list_gl_accounts(current_user.tenant_id)
    return [{"id": a.id, "code": a.account_code, "name": a.account_name, "type": a.account_type, "balance": a.current_balance} for a in accounts]


@router.post("/journal-entries", dependencies=[Depends(FeatureGate("finance"))])
async def create_journal_entry(
    req: JournalEntryCreate,
    session: AsyncSession = Depends(get_db_session),
    current_user=Depends(get_current_user),
) -> dict[str, Any]:
    svc = ERPService(session)
    je = await svc.create_journal_entry(current_user.tenant_id, {
        **req.dict(exclude_none=True),
        "created_by": current_user.id,
    })
    await session.commit()
    return {"id": je.id, "entry_number": je.entry_number, "total_debit": je.total_debit, "total_credit": je.total_credit}


@router.get("/trial-balance")
async def get_trial_balance(
    session: AsyncSession = Depends(get_db_session),
    current_user=Depends(get_current_user),
) -> list[dict[str, Any]]:
    svc = ERPService(session)
    return await svc.get_trial_balance(current_user.tenant_id)
