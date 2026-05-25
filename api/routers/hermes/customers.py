"""Customers router."""

from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel

from dealix.hermes.customer.churn_risk import evaluate_churn_risk
from dealix.hermes.customer.health_score import compute_health_score


router = APIRouter(prefix="/api/v1/hermes/customers", tags=["hermes-customers"])


class HealthRequest(BaseModel):
    customer_id: str
    usage_score: float
    nps_score: float
    paid_on_time: bool
    open_tickets: int


@router.post("/health-score")
def health(body: HealthRequest):
    return compute_health_score(**body.model_dump())


class ChurnRequest(BaseModel):
    customer_id: str
    health_score: float
    days_since_last_activity: int
    open_tickets_critical: int
    payment_late_days: int


@router.post("/churn-risk")
def churn(body: ChurnRequest):
    return evaluate_churn_risk(**body.model_dump())
