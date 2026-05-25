"""Assets router."""

from __future__ import annotations

from fastapi import APIRouter, Depends

from api.routers.hermes._dependencies import get_hermes
from dealix.hermes.assets.commercialization import evaluate_commercialization
from dealix.hermes.kernel.scale_kill import evaluate, apply_verdict
from dealix.hermes.orchestrator import HermesOrchestrator


router = APIRouter(prefix="/api/v1/hermes/assets", tags=["hermes-assets"])


@router.get("/")
def list_assets(orch: HermesOrchestrator = Depends(get_hermes)):
    return orch.kernel.assets.list()


@router.get("/{asset_id}/scale-kill")
def scale_kill(asset_id: str, orch: HermesOrchestrator = Depends(get_hermes)):
    asset = orch.kernel.assets.get(asset_id)
    verdict = evaluate(asset)
    apply_verdict(orch.kernel.assets, asset_id, verdict)
    return {"verdict": verdict.value}


@router.get("/{asset_id}/commercial-review")
def commercial(asset_id: str, orch: HermesOrchestrator = Depends(get_hermes)):
    a = orch.kernel.assets.get(asset_id)
    review = evaluate_commercialization(
        reuse_count=a.reuse_count,
        revenue_attributed_sar=a.revenue_attributed_sar,
        quality_score=a.quality_score,
    )
    return review
