"""Intelligence router."""

from __future__ import annotations

from fastapi import APIRouter

from dealix.hermes.intelligence.market_radar import MarketRadar, RadarSignal
from dealix.hermes.intelligence.trend_to_offer import trend_to_offer


router = APIRouter(prefix="/api/v1/hermes/intelligence", tags=["hermes-intelligence"])
_radar = MarketRadar()


@router.post("/radar")
def emit(signal: RadarSignal):
    return _radar.emit(signal)


@router.get("/radar")
def list_signals():
    return _radar.recent()


@router.get("/trend-to-offer")
def trend(trend: str, buyer: str, pain: str):
    return trend_to_offer(trend=trend, buyer=buyer, pain=pain)
