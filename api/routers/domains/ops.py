"""Operating System domain router aggregator.

Bundles all /api/v1/ops/* routers.
"""

from __future__ import annotations

from fastapi import APIRouter

from api.routers import (
    ops_communication,
    ops_customer_success,
    ops_growth,
    ops_health,
    ops_knowledge,
    ops_negotiation,
    ops_research,
    ops_sales,
)


def get_routers() -> list[APIRouter]:
    return [
        ops_negotiation.router,
        ops_research.router,
        ops_knowledge.router,
        ops_communication.router,
        ops_sales.router,
        ops_growth.router,
        ops_customer_success.router,
        ops_health.router,
    ]
