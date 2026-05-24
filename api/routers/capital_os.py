"""Wave 15.1 — Capital OS HTTP surface.

Exposes capital asset ledger, investment readiness, and PMF scoring:
  GET  /api/v1/capital-os/status           — layer health + hard gates
  POST /api/v1/capital-os/assets/add       — record a new capital asset
  GET  /api/v1/capital-os/assets/list      — list capital assets
  GET  /api/v1/capital-os/readiness-score  — investor readiness (0–100)
  POST /api/v1/capital-os/pmf-score        — Product-Market Fit score
  GET  /api/v1/capital-os/funding-checklist — funding readiness checklist
  GET  /api/v1/capital-os/valuation-drivers — key valuation driver list
  POST /api/v1/capital-os/exit-valuation   — exit/IPO valuation estimate

Hard rules:
- no_fake_revenue: exit valuation requires positive ARR
- is_estimate_always_true: all valuations carry is_estimate=True
- approval_required: no external sharing without founder sign-off
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

from auto_client_acquisition.capital_os import (
    CapitalAssetType,
    add_asset,
    list_assets,
)
from auto_client_acquisition.investment_os import (
    FUNDING_READINESS_ITEMS,
    VALUATION_DRIVERS,
    PmfScoreInputs,
    compute_pmf_score,
    pmf_band,
)

router = APIRouter(prefix="/api/v1/capital-os", tags=["Capital OS"])

_HARD_GATES: dict[str, bool] = {
    "no_fake_revenue": True,
    "is_estimate_always_true": True,
    "approval_required_for_external_share": True,
    "no_exit_valuation_without_arr": True,
}


# ─── Status ──────────────────────────────────────────────────────────────────

@router.get("/status")
async def status() -> dict[str, Any]:
    return {
        "service": "capital_os",
        "version": "v1",
        "hard_gates": _HARD_GATES,
        "asset_types": [t.value for t in CapitalAssetType],
    }


# ─── Capital asset ledger ─────────────────────────────────────────────────────

class AddAssetRequest(BaseModel):
    customer_id: str = Field(..., min_length=1)
    engagement_id: str = Field(..., min_length=1)
    asset_type: CapitalAssetType = Field(
        ..., description="One of the CapitalAssetType values"
    )
    owner: str = ""
    reusable: bool = True
    asset_ref: str = ""
    notes: str = ""


@router.post("/assets/add")
async def assets_add(req: AddAssetRequest) -> dict[str, Any]:
    """Record a new reusable capital asset in the ledger."""
    try:
        asset = add_asset(
            customer_id=req.customer_id,
            engagement_id=req.engagement_id,
            asset_type=req.asset_type,
            owner=req.owner,
            reusable=req.reusable,
            asset_ref=req.asset_ref,
            notes=req.notes,
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return asset.to_dict()


@router.get("/assets/list")
async def assets_list(
    customer_id: str | None = None,
    engagement_id: str | None = None,
    limit: int = Query(default=100, ge=1, le=500),
) -> dict[str, Any]:
    """List capital assets, optionally filtered."""
    rows = list_assets(
        customer_id=customer_id,
        engagement_id=engagement_id,
        limit=min(limit, 500),
    )
    return {
        "assets": [a.to_dict() for a in rows],
        "count": len(rows),
    }


# ─── Investor readiness score ─────────────────────────────────────────────────

class ReadinessScoreRequest(BaseModel):
    has_arr: bool = False
    arr_sar: float = Field(0.0, ge=0)
    team_complete: bool = False
    product_live: bool = False
    revenue_12mo_sar: float = Field(0.0, ge=0)
    governance_docs_ready: bool = False
    proof_library_count: int = Field(0, ge=0)
    retainer_customers: int = Field(0, ge=0)


@router.get("/readiness-score")
async def readiness_score_get() -> dict[str, Any]:
    """Return readiness score derived from ledger state."""
    assets = list_assets(limit=500)
    has_arr = any(
        getattr(a, "asset_type", None) in ("arr_contract", "retainer_contract")
        for a in assets
    )
    retainer_count = sum(
        1 for a in assets
        if getattr(a, "asset_type", None) == "retainer_contract"
    )
    proof_count = sum(
        1 for a in assets
        if getattr(a, "asset_type", None) == "proof_asset"
    )
    inputs = {
        "has_arr": has_arr,
        "arr_sар": 0.0,
        "team_complete": False,
        "product_live": True,
        "revenue_12mo_sar": 0.0,
        "governance_docs_ready": False,
        "proof_library_count": proof_count,
        "retainer_customers": retainer_count,
    }
    return _compute_readiness(inputs)


@router.post("/readiness-score")
async def readiness_score_post(req: ReadinessScoreRequest) -> dict[str, Any]:
    """Compute investor readiness score (0–100) from supplied signals."""
    return _compute_readiness(req.model_dump())


def _compute_readiness(inputs: dict[str, Any]) -> dict[str, Any]:
    score = 0
    breakdown: dict[str, Any] = {}

    # ARR exists (30 pts)
    arr_pts = 30 if inputs.get("has_arr") else 0
    score += arr_pts
    breakdown["arr_exists"] = arr_pts

    # Team completeness (20 pts)
    team_pts = 20 if inputs.get("team_complete") else 0
    score += team_pts
    breakdown["team_complete"] = team_pts

    # Product live (20 pts)
    prod_pts = 20 if inputs.get("product_live") else 0
    score += prod_pts
    breakdown["product_live"] = prod_pts

    # Revenue 12mo > 500K SAR (20 pts)
    rev_pts = 20 if inputs.get("revenue_12mo_sar", 0) >= 500_000 else 0
    score += rev_pts
    breakdown["revenue_12mo"] = rev_pts

    # Governance docs (10 pts)
    gov_pts = 10 if inputs.get("governance_docs_ready") else 0
    score += gov_pts
    breakdown["governance_docs"] = gov_pts

    band = "seed" if score < 40 else ("pre_series_a" if score < 70 else "series_a_ready")
    return {
        "readiness_score": score,
        "band": band,
        "breakdown": breakdown,
        "is_estimate": True,
        "hard_gates": _HARD_GATES,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }


# ─── PMF score ────────────────────────────────────────────────────────────────

class PmfRequest(BaseModel):
    paying_customers: int = Field(0, ge=0)
    nps_score: float = Field(0.0, ge=-100, le=100)
    churn_rate_pct: float = Field(0.0, ge=0.0, le=100.0)
    expansion_revenue_pct: float = Field(0.0, ge=0.0, le=100.0)
    repeat_purchase_rate_pct: float = Field(0.0, ge=0.0, le=100.0)


@router.post("/pmf-score")
async def pmf_score_endpoint(req: PmfRequest) -> dict[str, Any]:
    """Compute Product-Market Fit score."""
    inputs = PmfScoreInputs(
        paying_customers=req.paying_customers,
        nps_score=req.nps_score,
        churn_rate_pct=req.churn_rate_pct,
        expansion_revenue_pct=req.expansion_revenue_pct,
        repeat_purchase_rate_pct=req.repeat_purchase_rate_pct,
    )
    result = compute_pmf_score(inputs)
    band = pmf_band(result)
    return {
        "pmf_score": result,
        "band": band.value if hasattr(band, "value") else str(band),
        "is_estimate": True,
        "hard_gates": _HARD_GATES,
    }


# ─── Funding checklist ────────────────────────────────────────────────────────

@router.get("/funding-checklist")
async def funding_checklist() -> dict[str, Any]:
    """Return the 10-item funding readiness checklist."""
    return {
        "checklist": list(FUNDING_READINESS_ITEMS),
        "total_items": len(FUNDING_READINESS_ITEMS),
        "source": "investment_os.funding_readiness",
    }


# ─── Valuation drivers ────────────────────────────────────────────────────────

@router.get("/valuation-drivers")
async def valuation_drivers() -> dict[str, Any]:
    """Return key SaaS/services valuation drivers."""
    return {
        "drivers": VALUATION_DRIVERS,
        "source": "investment_os.valuation_drivers",
    }


# ─── Exit valuation ────────────────────────────────────────────────────────────

_VALID_BUSINESS_TYPES: frozenset[str] = frozenset(
    {"saas", "services", "marketplace", "hardware"}
)


class ExitValuationRequest(BaseModel):
    arr_sar: float = Field(..., gt=0, description="Annual Recurring Revenue in SAR")
    business_type: str = Field(
        default="saas",
        description="One of: saas, services, marketplace, hardware",
    )
    growth_rate_pct: float = Field(0.0, ge=0.0, le=500.0)
    gross_margin_pct: float = Field(0.0, ge=0.0, le=100.0)


@router.post("/exit-valuation")
async def exit_valuation(req: ExitValuationRequest) -> dict[str, Any]:
    """Estimate exit/IPO valuation from ARR and business type.

    Hard gate: ARR must be positive (enforced by pydantic gt=0).
    """
    if req.business_type not in _VALID_BUSINESS_TYPES:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "invalid_business_type",
                "message": (
                    f"business_type '{req.business_type}' is not supported. "
                    f"Valid values: {sorted(_VALID_BUSINESS_TYPES)}"
                ),
            },
        )
    if req.business_type == "saas":
        # Base multiple 5x, premium for growth + margin
        base_multiple = 5.0
        growth_bonus = min(req.growth_rate_pct / 100, 2.0)
        margin_bonus = max(0, (req.gross_margin_pct - 60) / 100)
        multiple = min(base_multiple + growth_bonus + margin_bonus, 15.0)
        low = req.arr_sar * 5.0
        mid = req.arr_sar * multiple
        high = req.arr_sar * min(multiple * 1.5, 15.0)
    else:
        # Services: 1-3x ARR
        multiple = 1.5 + min(req.gross_margin_pct / 100, 1.5)
        low = req.arr_sar * 1.0
        mid = req.arr_sar * multiple
        high = req.arr_sar * 3.0

    return {
        "arr_sar": req.arr_sar,
        "business_type": req.business_type,
        "revenue_multiple": round(multiple, 2),
        "valuation_low_sar": round(low, 0),
        "valuation_mid_sar": round(mid, 0),
        "valuation_high_sar": round(high, 0),
        "is_estimate": True,
        "hard_gates": _HARD_GATES,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }
