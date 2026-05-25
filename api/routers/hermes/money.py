"""Money router — dashboard, revenue assurance, pricing, deals."""

from __future__ import annotations

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from api.routers.hermes._dependencies import get_hermes
from dealix.hermes.money.cashflow import build_cashflow_brief
from dealix.hermes.money.dashboard import MoneyDashboard
from dealix.hermes.money.revenue_assurance import RevenueAssurance
from dealix.hermes.orchestrator import HermesOrchestrator


router = APIRouter(prefix="/api/v1/hermes/money", tags=["hermes-money"])


@router.get("/dashboard")
def dashboard(orch: HermesOrchestrator = Depends(get_hermes)) -> MoneyDashboard:
    brief = build_cashflow_brief(streams=[], fastest_cash_action="follow up on outstanding proposals")
    return MoneyDashboard.from_inputs(cashflow=brief, deals=[])


class RevenueQualityRequest(BaseModel):
    margin_ratio: float
    repeatability: float
    retainer_potential: float
    data_moat: float
    partner_potential: float
    delivery_burden: float


@router.post("/revenue-assurance")
def revenue_quality(body: RevenueQualityRequest):
    return RevenueAssurance.quality_score(
        margin_ratio=body.margin_ratio,
        repeatability=body.repeatability,
        retainer_potential=body.retainer_potential,
        data_moat=body.data_moat,
        partner_potential=body.partner_potential,
        delivery_burden=body.delivery_burden,
    )
