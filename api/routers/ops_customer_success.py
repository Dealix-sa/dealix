"""Customer Success OS API.

Success plans, health dashboards, renewal forecasts, expansion signals.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from intelligence.bilingual import LanguageCode, get_lang
from intelligence.customer_success_ops import CustomerSuccessOperatingSystem

router = APIRouter(prefix="/api/v1/ops/cs", tags=["Customer Success OS"])
_os = CustomerSuccessOperatingSystem()


class SuccessPlanRequest(BaseModel):
    customer_id: str = Field(..., min_length=1)
    customer_name: str = Field(..., min_length=1)
    goals_en: list[str] = Field(..., min_length=1)
    goals_ar: list[str] = Field(..., min_length=1)
    package_sku: str = Field(..., min_length=1)
    renewal_date: str | None = None
    lang: LanguageCode = "both"


class MilestoneUpdateRequest(BaseModel):
    milestone_name_en: str = Field(..., min_length=1)
    completed: bool
    evidence: list[str] = Field(default_factory=list)


class CustomerHealthRequest(BaseModel):
    customers: list[dict[str, Any]] = Field(..., min_length=1)
    lang: LanguageCode = "both"


class UsageSignalsRequest(BaseModel):
    usage_data: dict[str, Any]
    lang: LanguageCode = "both"


@router.post("/success-plan")
async def create_success_plan(payload: SuccessPlanRequest) -> dict[str, Any]:
    return _os.create_success_plan(
        customer_id=payload.customer_id,
        customer_name=payload.customer_name,
        goals_en=payload.goals_en,
        goals_ar=payload.goals_ar,
        package_sku=payload.package_sku,
        renewal_date=payload.renewal_date,
        lang=payload.lang,
    )


@router.get("/success-plan/{plan_id}")
async def get_success_plan(plan_id: str, lang: LanguageCode = Depends(get_lang)) -> dict[str, Any]:
    try:
        return _os.get_success_plan(plan_id, lang)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/success-plan/{plan_id}/milestone")
async def update_milestone(plan_id: str, payload: MilestoneUpdateRequest) -> dict[str, Any]:
    try:
        return _os.update_milestone(plan_id, payload.milestone_name_en, payload.completed, payload.evidence)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/health-dashboard")
async def health_dashboard(payload: CustomerHealthRequest) -> dict[str, Any]:
    return _os.health_dashboard(payload.customers, payload.lang)


@router.post("/renewals/forecast")
async def renewal_forecast(payload: CustomerHealthRequest) -> dict[str, Any]:
    return _os.forecast_renewals(payload.customers, payload.lang)


@router.post("/expansion-signals/{customer_id}")
async def expansion_signals(customer_id: str, payload: UsageSignalsRequest) -> dict[str, Any]:
    return _os.detect_expansion_signals(customer_id, payload.usage_data, payload.lang)


@router.post("/customer-brief/{customer_id}")
async def customer_brief(customer_id: str, payload: CustomerHealthRequest) -> dict[str, Any]:
    if not payload.customers:
        raise HTTPException(status_code=422, detail="customers required")
    return _os.customer_brief(customer_id, payload.customers[0], payload.lang)
