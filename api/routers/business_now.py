"""Business NOW — unified operating snapshot for founder/CTO."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Body, Depends

from api.security.api_key import require_admin_key
from dealix.business_now.commercial_strategy import (
    build_commercial_strategy_simulate,
    build_commercial_strategy_snapshot,
)
from dealix.business_now.founder_signals import build_operator_signals
from dealix.business_now.snapshot_builder import build_business_now_snapshot

router = APIRouter(prefix="/business-now", tags=["business-now"])


@router.get("/snapshot")
def business_now_snapshot() -> dict[str, Any]:
    """All business pillars — read-only from repo YAML + catalog (fast; verdicts from cache)."""
    return build_business_now_snapshot(run_verify=False)


@router.get("/commercial-strategy")
def business_now_commercial_strategy() -> dict[str, Any]:
    """Full commercial strategy — GTM, ladder, offers, upsell (no invented CRM)."""
    return build_commercial_strategy_snapshot()


@router.post("/commercial-strategy/simulate")
def business_now_commercial_strategy_simulate(
    body: dict[str, Any] = Body(default_factory=dict),
) -> dict[str, Any]:
    """Simulate vertical + plan recommendation from founder inputs (deterministic)."""
    return build_commercial_strategy_simulate(
        industry=str(body.get("industry", "clinics")),
        city=str(body.get("city", "Riyadh")),
        company_size=str(body.get("company_size", "sme")),
        monthly_budget_sar=float(body.get("monthly_budget_sar", 2500)),
        goal=str(body.get("goal", "pipeline")),
    )


@router.get("/operator-signals", dependencies=[Depends(require_admin_key)])
def business_now_operator_signals() -> dict[str, Any]:
    """Founder ops slice — admin key required."""
    return build_operator_signals()
