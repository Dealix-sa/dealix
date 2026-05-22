"""
Offer Ladder API — expose the 5-rung commercial service ladder.
Read-only catalog + upgrade recommendation engine.
"""

from __future__ import annotations

from fastapi import APIRouter

from dealix.commercial_ops.five_rung_ladder import (
    OFFER_LADDER,
    LadderContext,
    calculate_pipeline_value,
    get_offer,
    get_upgrade_path_for_all,
    recommend_upgrade,
)

router = APIRouter(prefix="/api/v1/offer-ladder", tags=["offer-ladder"])


@router.get("/rungs")
async def list_rungs() -> dict:
    """Return the full 5-rung offer catalog."""
    return {
        "total_rungs": len(OFFER_LADDER),
        "currency": "SAR",
        "rungs": OFFER_LADDER,
    }


@router.get("/upgrade-path")
async def upgrade_path() -> dict:
    """Return simplified upgrade path visualization."""
    return {"path": get_upgrade_path_for_all()}


@router.get("/rung/{tier}")
async def get_rung(tier: str) -> dict:
    """Return details for a specific offer tier."""
    try:
        return get_offer(tier)  # type: ignore[arg-type]
    except KeyError:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail=f"Tier '{tier}' not found")


@router.post("/recommend-upgrade")
async def recommend_upgrade_endpoint(ctx: dict) -> dict:
    """
    Given client context, return upgrade readiness score and recommendation.
    Body: {current_tier, months_active, total_paid_sar, data_volume_records?,
           nps_score?, support_tickets_open?, last_interaction_days?}
    """
    try:
        ladder_ctx = LadderContext(
            current_tier=ctx["current_tier"],
            months_active=int(ctx.get("months_active", 1)),
            total_paid_sar=float(ctx.get("total_paid_sar", 0)),
            data_volume_records=int(ctx.get("data_volume_records", 0)),
            nps_score=ctx.get("nps_score"),
            support_tickets_open=int(ctx.get("support_tickets_open", 0)),
            last_interaction_days=int(ctx.get("last_interaction_days", 7)),
        )
        return recommend_upgrade(ladder_ctx)
    except (KeyError, ValueError) as e:
        from fastapi import HTTPException
        raise HTTPException(status_code=422, detail=str(e))


@router.post("/pipeline-value")
async def pipeline_value(active_clients: dict) -> dict:
    """
    Calculate MRR, ARR, and 24-month LTV for current client distribution.
    Body: {tier_name: client_count, ...}
    e.g. {"free_diagnostic": 10, "sprint_499": 5, "managed_ops": 2}
    """
    try:
        result = calculate_pipeline_value(active_clients)  # type: ignore[arg-type]
        return result
    except KeyError as e:
        from fastapi import HTTPException
        raise HTTPException(status_code=422, detail=f"Unknown tier: {e}")
