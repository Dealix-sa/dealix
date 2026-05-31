"""Hermes API routers — composed in api.routers.hermes.composite."""

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

__all__ = [
    "assets_router",
    "customers_router",
    "growth_router",
    "intelligence_router",
    "kernel_router",
    "money_router",
    "observability_router",
    "partners_router",
    "products_router",
    "sovereign_router",
    "training_router",
    "trust_router",
    "ventures_router",
]
