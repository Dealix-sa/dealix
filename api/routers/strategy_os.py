"""Wave 17.0 — Strategy OS + Competitive Moat HTTP surface.

Hard gates:
  - is_estimate_always_true: all scored outputs carry is_estimate=True
  - no_fake_revenue: use cases ranked by real impact, never inflated
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from auto_client_acquisition.moat_os import (
    GOVERNANCE_TO_MOAT_STAGES,
    PROOF_TO_MOAT_STAGES,
    MoatScoreDimensions,
    detect_anti_moat_risks,
    governance_moat_loop_complete,
    governance_to_moat_progress,
    moat_compound_index,
    moat_tier,
    proof_moat_loop_complete,
    proof_to_moat_progress,
    weighted_moat_score,
)
from auto_client_acquisition.strategy_os import (
    UseCaseScores,
    compute_ai_readiness,
    rank_use_cases,
    roadmap_buckets,
)

router = APIRouter(prefix="/api/v1/strategy", tags=["Wave 17 — Strategy OS"])

_HARD_GATES: dict[str, bool] = {
    "is_estimate_always_true": True,
    "no_fake_revenue": True,
}


# ── Pydantic models ────────────────────────────────────────────────────────────


class AIReadinessRequest(BaseModel):
    data: float = 0.5
    process: float = 0.5
    governance: float = 0.5
    people: float = 0.5
    tech: float = 0.5


class UseCaseItem(BaseModel):
    name: str
    revenue_impact: float = 0.5
    time_save: float = 0.5
    data_readiness: float = 0.5
    ease: float = 0.5
    low_risk: float = 0.5


class RankUseCasesRequest(BaseModel):
    use_cases: list[UseCaseItem]


class MoatScoreRequest(BaseModel):
    governance_depth: int = 0
    proof_strength: int = 0
    product_reuse: int = 0
    saudi_arabic_differentiation: int = 0
    capital_assets_created: int = 0
    partner_academy_distribution: int = 0
    market_language_adoption: int = 0


class AntiMoatRisksRequest(BaseModel):
    every_engagement_custom_scope: bool = False
    delivery_without_proof_pack: bool = False
    output_without_governance_status: bool = False
    arabic_quality_fail: bool = False
    priced_as_commodity_task: bool = False
    shipped_public_saas_before_internal_use: bool = False


# ── Endpoints ─────────────────────────────────────────────────────────────────


@router.get("/status")
async def status() -> dict[str, Any]:
    """Layer health + hard gates (no I/O)."""
    return {
        "module": "strategy_os",
        "version": "17.0",
        "endpoints": 6,
        "hard_gates": _HARD_GATES,
        "is_estimate": False,
    }


@router.post("/ai-readiness")
async def ai_readiness(body: AIReadinessRequest) -> dict[str, Any]:
    """Compute AI readiness score across five axes."""
    result = compute_ai_readiness(axes=body.model_dump())
    return {**result, "is_estimate": True}


@router.post("/rank-use-cases")
async def rank_use_cases_endpoint(body: RankUseCasesRequest) -> dict[str, Any]:
    """Rank AI use cases by composite score and assign to a 30/60/90-day roadmap."""
    if not body.use_cases:
        raise HTTPException(status_code=400, detail="use_cases must not be empty")

    scored_items = [
        UseCaseScores(
            name=item.name,
            revenue_impact=item.revenue_impact,
            time_save=item.time_save,
            data_readiness=item.data_readiness,
            ease=item.ease,
            low_risk=item.low_risk,
        )
        for item in body.use_cases
    ]
    ranked = rank_use_cases(scored_items)
    top_names = [name for name, _ in ranked]
    roadmap = roadmap_buckets(top_names)
    return {
        "ranked": ranked,
        "roadmap": roadmap,
        "is_estimate": True,
    }


@router.post("/moat-score")
async def moat_score(body: MoatScoreRequest) -> dict[str, Any]:
    """Compute weighted moat score, compound index, and tier."""
    try:
        dims = MoatScoreDimensions(**body.model_dump())
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    score = weighted_moat_score(dims)
    tier = moat_tier(score)
    compound = moat_compound_index(dims)
    return {
        "weighted_score": score,
        "compound_index": compound,
        "tier": tier,
        "dimensions": body.model_dump(),
        "is_estimate": False,
    }


@router.post("/anti-moat-risks")
async def anti_moat_risks(body: AntiMoatRisksRequest) -> dict[str, Any]:
    """Detect anti-moat risks from boolean condition flags."""
    hits = detect_anti_moat_risks(
        every_engagement_custom_scope=body.every_engagement_custom_scope,
        delivery_without_proof_pack=body.delivery_without_proof_pack,
        output_without_governance_status=body.output_without_governance_status,
        arabic_quality_fail=body.arabic_quality_fail,
        priced_as_commodity_task=body.priced_as_commodity_task,
        shipped_public_saas_before_internal_use=body.shipped_public_saas_before_internal_use,
    )
    return {
        "risks_detected": len(hits),
        "hits": [{"risk": h.risk, "remedy_key": h.remedy_key} for h in hits],
        "is_estimate": False,
    }


@router.get("/moat-progress")
async def moat_progress(
    proof_stage: str = Query(default=""),
    governance_stage: str = Query(default=""),
) -> dict[str, Any]:
    """Return proof-to-moat and governance-to-moat progress for the given completed stages."""
    proof_completed = (
        frozenset(s.strip() for s in proof_stage.split(",") if s.strip())
        if proof_stage.strip()
        else frozenset()
    )
    gov_completed = (
        frozenset(s.strip() for s in governance_stage.split(",") if s.strip())
        if governance_stage.strip()
        else frozenset()
    )

    proof_result: dict[str, Any] = {}
    if proof_stage.strip():
        done, missing = proof_to_moat_progress(proof_completed)
        complete = proof_moat_loop_complete(proof_completed)
        proof_result = {"done": done, "missing": list(missing), "loop_complete": complete}

    gov_result: dict[str, Any] = {}
    if governance_stage.strip():
        done, missing = governance_to_moat_progress(gov_completed)
        complete = governance_moat_loop_complete(gov_completed)
        gov_result = {"done": done, "missing": list(missing), "loop_complete": complete}

    return {
        "proof_stages": list(PROOF_TO_MOAT_STAGES),
        "governance_stages": list(GOVERNANCE_TO_MOAT_STAGES),
        "proof_progress": proof_result,
        "governance_progress": gov_result,
        "is_estimate": False,
    }
