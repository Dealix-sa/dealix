"""Business NOW — unified operating snapshot for founder/CTO."""

from __future__ import annotations

import json
import logging
from typing import Any

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from api.security.api_key import require_admin_key
from dealix.business_now.commercial_strategy import (
    build_commercial_strategy_simulate,
    build_commercial_strategy_snapshot,
)
from dealix.business_now.founder_signals import build_operator_signals
from dealix.business_now.snapshot_builder import build_business_now_snapshot

log = logging.getLogger(__name__)

router = APIRouter(prefix="/business-now", tags=["business-now"])

_SNAPSHOT_CACHE_KEY = "business_now:snapshot:v1"
_SNAPSHOT_CACHE_TTL = 900  # 15 minutes


def _get_redis():
    try:
        import redis as _redis
        from core.config.settings import get_settings
        url = get_settings().redis_url
        if not url or url == "redis://localhost:6379/0":
            return None
        return _redis.from_url(url, socket_timeout=2, decode_responses=True)
    except Exception:
        return None


class CommercialStrategySimulateRequest(BaseModel):
    industry: str = "clinics"
    city: str = "Riyadh"
    company_size: str = "sme"
    monthly_budget_sar: float = Field(default=2500.0, ge=0, le=50_000_000)
    goal: str = "pipeline"


@router.get("/snapshot")
def business_now_snapshot() -> dict[str, Any]:
    """All business pillars — read-only from repo YAML + catalog. Redis-cached 15 min."""
    rc = _get_redis()
    if rc is not None:
        try:
            cached = rc.get(_SNAPSHOT_CACHE_KEY)
            if cached:
                data = json.loads(cached)
                data["_cache_hit"] = True
                return data
        except Exception:
            log.debug("snapshot_cache_read_failed")

    result = build_business_now_snapshot(run_verify=False)

    if rc is not None:
        try:
            rc.setex(_SNAPSHOT_CACHE_KEY, _SNAPSHOT_CACHE_TTL, json.dumps(result, default=str))
        except Exception:
            log.debug("snapshot_cache_write_failed")

    return result


@router.post("/snapshot/invalidate", dependencies=[Depends(require_admin_key)])
def invalidate_snapshot_cache() -> dict[str, Any]:
    """Force-expire the Business NOW snapshot cache (admin only)."""
    rc = _get_redis()
    if rc is not None:
        try:
            deleted = rc.delete(_SNAPSHOT_CACHE_KEY)
            return {"status": "invalidated", "keys_deleted": deleted}
        except Exception:
            log.warning("cache_invalidate_failed")
            return {"status": "error", "detail": "cache invalidation failed"}
    return {"status": "no_cache", "detail": "Redis not configured"}


@router.get("/commercial-strategy")
def business_now_commercial_strategy() -> dict[str, Any]:
    """Full commercial strategy — GTM, ladder, offers, upsell (no invented CRM)."""
    return build_commercial_strategy_snapshot()


@router.post("/commercial-strategy/simulate")
def business_now_commercial_strategy_simulate(
    body: CommercialStrategySimulateRequest,
) -> dict[str, Any]:
    """Simulate vertical + plan recommendation from founder inputs (deterministic)."""
    return build_commercial_strategy_simulate(
        industry=body.industry,
        city=body.city,
        company_size=body.company_size,
        monthly_budget_sar=body.monthly_budget_sar,
        goal=body.goal,
    )


@router.get("/operator-signals", dependencies=[Depends(require_admin_key)])
def business_now_operator_signals() -> dict[str, Any]:
    """Founder ops slice — admin key required."""
    return build_operator_signals()
