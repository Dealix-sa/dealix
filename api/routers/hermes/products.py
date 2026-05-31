"""Products router — offer library and readiness."""

from __future__ import annotations

from fastapi import APIRouter, Depends

from api.routers.hermes._dependencies import get_hermes
from dealix.hermes.orchestrator import HermesOrchestrator
from dealix.hermes.products.offer_library import OfferLibrary, check_readiness


router = APIRouter(prefix="/api/v1/hermes/products", tags=["hermes-products"])
_library = OfferLibrary()


@router.get("/offers")
def offers():
    return _library.list()


@router.get("/offers/{offer_id}/readiness")
def readiness(offer_id: str):
    if not _library.exists(offer_id):
        return {"ready": False, "missing_fields": ["offer_id_unknown"]}
    return check_readiness(_library.get(offer_id))
