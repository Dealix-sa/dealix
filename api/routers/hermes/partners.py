"""Partners router."""

from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel

from dealix.hermes.partners.fit_score import score_partner_fit


router = APIRouter(prefix="/api/v1/hermes/partners", tags=["hermes-partners"])


class PartnerFitRequest(BaseModel):
    client_base_score: int
    sales_capability: int
    delivery_capability: int
    trust_level: int
    sector_fit: int
    risk_level: int


@router.post("/fit-score")
def fit_score(body: PartnerFitRequest):
    fit = score_partner_fit(**body.model_dump())
    return {"score": fit.score, "components": fit.components}
