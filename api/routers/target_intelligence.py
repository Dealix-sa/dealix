"""Target Company Intelligence API — dossiers + daily targeting brief.

Thin router over :mod:`auto_client_acquisition.revenue_os.target_company_intelligence`
and :mod:`auto_client_acquisition.revenue_os.daily_targeting_brief`. All facts come
from declared inputs (no scraping); all outreach is draft-only. Doctrine violations
map to HTTP 403.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from auto_client_acquisition.revenue_os.daily_targeting_brief import (
    build_daily_targeting_brief,
)
from auto_client_acquisition.revenue_os.target_company_intelligence import (
    WEAKNESS_CATALOG,
    build_company_dossier,
)

router = APIRouter(prefix="/api/v1/target-intelligence", tags=["target-intelligence"])


def _frozen(values: list[str] | None) -> frozenset[str] | None:
    if not values:
        return None
    return frozenset(values)


class DossierRequest(BaseModel):
    company: dict[str, Any] = Field(..., description="Declared company fields.")
    icp_sectors: list[str] | None = None
    icp_cities: list[str] | None = None


class DailyBriefRequest(BaseModel):
    companies: list[dict[str, Any]] = Field(..., description="Declared companies.")
    top_n: int = 10
    icp_sectors: list[str] | None = None
    icp_cities: list[str] | None = None
    date_iso: str | None = None


@router.get("/weakness-catalog")
def get_weakness_catalog() -> dict[str, Any]:
    """Return the deterministic weakness catalog."""
    return {"weakness_catalog": WEAKNESS_CATALOG}


@router.post("/dossier")
def post_dossier(req: DossierRequest) -> dict[str, Any]:
    """Build a deterministic, estimate-labeled dossier from declared inputs only."""
    try:
        return build_company_dossier(
            req.company,
            icp_sectors=_frozen(req.icp_sectors),
            icp_cities=_frozen(req.icp_cities),
        )
    except ValueError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc


@router.post("/daily-brief")
def post_daily_brief(req: DailyBriefRequest) -> dict[str, Any]:
    """Build a ranked, governed daily targeting brief (draft-only outreach)."""
    try:
        return build_daily_targeting_brief(
            req.companies,
            top_n=req.top_n,
            date_iso=req.date_iso,
            icp_sectors=_frozen(req.icp_sectors),
            icp_cities=_frozen(req.icp_cities),
        )
    except ValueError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc


__all__ = ["router"]
