"""
AI Co-Pilot API.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.security.auth_deps import get_current_user
from db.session import get_db as get_db_session
from dealix.ai_copilot.service import AICopilotService

router = APIRouter(prefix="/api/v1/ai-copilot", tags=["AI Co-Pilot"])


@router.get("/daily-brief")
async def daily_brief(
    session: AsyncSession = Depends(get_db_session),
    current_user=Depends(get_current_user),
) -> dict[str, Any]:
    svc = AICopilotService(session)
    return await svc.generate_daily_brief(current_user.tenant_id)


@router.get("/pipeline-analysis")
async def pipeline_analysis(
    session: AsyncSession = Depends(get_db_session),
    current_user=Depends(get_current_user),
) -> dict[str, Any]:
    svc = AICopilotService(session)
    return await svc.analyze_pipeline(current_user.tenant_id)


@router.get("/financial-health")
async def financial_health(
    session: AsyncSession = Depends(get_db_session),
    current_user=Depends(get_current_user),
) -> dict[str, Any]:
    svc = AICopilotService(session)
    return await svc.financial_health(current_user.tenant_id)


@router.get("/inventory-forecast/{item_id}")
async def inventory_forecast(
    item_id: str,
    session: AsyncSession = Depends(get_db_session),
    current_user=Depends(get_current_user),
) -> dict[str, Any]:
    svc = AICopilotService(session)
    return await svc.forecast_inventory(current_user.tenant_id, item_id)
