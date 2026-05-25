"""
Aggregate Hermes router — mount on the main FastAPI app to expose
the full Hermes surface under /api/v1/hermes/*.
"""

from __future__ import annotations

from fastapi import APIRouter

from api.routers.hermes import (
    assets as assets_router,
    customers as customers_router,
    growth as growth_router,
    intelligence as intelligence_router,
    kernel as kernel_router,
    money as money_router,
    observability as observability_router,
    partners as partners_router,
    products as products_router,
    sovereign as sovereign_router,
    training as training_router,
    trust as trust_router,
    ventures as ventures_router,
)


def build_hermes_router() -> APIRouter:
    composite = APIRouter()
    for module in (
        kernel_router,
        sovereign_router,
        trust_router,
        money_router,
        growth_router,
        products_router,
        partners_router,
        customers_router,
        intelligence_router,
        training_router,
        ventures_router,
        assets_router,
        observability_router,
    ):
        composite.include_router(module.router)
    return composite
