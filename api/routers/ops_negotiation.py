"""Negotiation OS API.

Bilingual objection handling, persuasion maps, deal strategy, and sales scripts.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from intelligence.bilingual import LanguageCode, get_lang
from intelligence.negotiation_engine import NegotiationEngine

router = APIRouter(prefix="/api/v1/ops/negotiation", tags=["Negotiation OS"])
_engine = NegotiationEngine()


class HandleObjectionRequest(BaseModel):
    category: str = Field(..., min_length=1)
    prospect_sector: str = "software"
    prospect_city: str = "Riyadh"
    deal_value_sar: float | None = None
    recommended_package: str | None = None
    lang: LanguageCode = "both"


class DealStrategyRequest(BaseModel):
    company_name: str = Field(..., min_length=1)
    sector: str = Field(..., min_length=1)
    city: str = Field(..., min_length=1)
    package_sku: str = Field(..., min_length=1)
    budget_hint: float | None = None
    employees: int = 50
    lang: LanguageCode = "both"


class PersuasionMapRequest(BaseModel):
    deal_id: str = Field(..., min_length=1)
    stakeholders: list[dict[str, Any]] = Field(..., min_length=1)
    lang: LanguageCode = "both"


@router.get("/objections")
async def list_objections(lang: LanguageCode = Depends(get_lang)) -> dict[str, Any]:
    return _engine.list_objections(lang)


@router.post("/handle-objection")
async def handle_objection(payload: HandleObjectionRequest) -> dict[str, Any]:
    return _engine.handle_objection(
        category=payload.category,
        context={
            "sector": payload.prospect_sector,
            "city": payload.prospect_city,
            "deal_value_sar": payload.deal_value_sar,
            "recommended_package": payload.recommended_package,
        },
        lang=payload.lang,
    )


@router.post("/persuasion-map")
async def persuasion_map(payload: PersuasionMapRequest) -> dict[str, Any]:
    return _engine.build_persuasion_map(
        deal_id=payload.deal_id,
        stakeholders=payload.stakeholders,
        lang=payload.lang,
    )


@router.post("/deal-strategy")
async def deal_strategy(payload: DealStrategyRequest) -> dict[str, Any]:
    return _engine.generate_deal_strategy(
        company_name=payload.company_name,
        sector=payload.sector,
        city=payload.city,
        package_sku=payload.package_sku,
        budget_hint=payload.budget_hint,
        employees=payload.employees,
        lang=payload.lang,
    )


@router.get("/scripts/{scenario}")
async def get_script(scenario: str, lang: LanguageCode = Depends(get_lang)) -> dict[str, Any]:
    return _engine.get_script(scenario, lang)
