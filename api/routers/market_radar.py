"""
Market Radar API — autonomous Saudi SME market intelligence.

  GET  /api/v1/market-radar/weekly-brief
  POST /api/v1/market-radar/acquisition-targets
  POST /api/v1/market-radar/competitor-threat
  GET  /api/v1/market-radar/opportunity-map
"""

from __future__ import annotations

import logging
from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel

from dealix.intelligence.market_radar import MarketRadar

router = APIRouter(prefix="/api/v1/market-radar", tags=["market-radar"])
log = logging.getLogger(__name__)

_radar = MarketRadar()


class AcquisitionScanRequest(BaseModel):
    sectors: list[str] | None = None
    min_score: float = 60.0
    max_results: int = 10


class CompetitorThreatRequest(BaseModel):
    competitor_name: str
    competitor_sector: str
    has_ai_product: bool = False
    market_share_pct: float = 0.0
    has_saudi_presence: bool = True
    funding_raised_sar: float = 0.0


@router.get("/weekly-brief")
async def weekly_brief() -> dict[str, Any]:
    """Return this week's auto-generated market intelligence brief."""
    brief = _radar.weekly_market_brief()
    log.info("market_radar_weekly_brief_generated date=%s", brief["brief_date"])
    return brief


@router.post("/acquisition-targets")
async def scan_targets(req: AcquisitionScanRequest) -> dict[str, Any]:
    """Scan and score Saudi SME acquisition targets."""
    result = _radar.scan_acquisition_targets(
        sectors=req.sectors,
        min_score=req.min_score,
        max_results=req.max_results,
    )
    log.info(
        "market_radar_scan_complete sectors=%s found=%s",
        req.sectors,
        result["total_targets_found"],
    )
    return result


@router.post("/competitor-threat")
async def competitor_threat(req: CompetitorThreatRequest) -> dict[str, Any]:
    """Score competitive threat level for a named competitor."""
    result = _radar.competitive_threat_score(
        competitor_name=req.competitor_name,
        competitor_sector=req.competitor_sector,
        has_ai_product=req.has_ai_product,
        market_share_pct=req.market_share_pct,
        has_saudi_presence=req.has_saudi_presence,
        funding_raised_sar=req.funding_raised_sar,
    )
    log.info(
        "market_radar_threat_scored competitor=%s score=%s",
        req.competitor_name,
        result["threat_score"],
    )
    return result


@router.get("/opportunity-map")
async def opportunity_map(
    horizon_months: int = 12,
) -> dict[str, Any]:
    """Return revenue opportunity map across all Saudi SME sectors."""
    result = _radar.revenue_opportunity_map(planning_horizon_months=horizon_months)
    log.info("market_radar_opportunity_map horizon=%s months", horizon_months)
    return result
