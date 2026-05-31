"""Offer/ICP fit captures industry, region and pain overlap."""

from __future__ import annotations

from dealix.hermes.growth.icp_registry import ICP
from dealix.hermes.growth.offer_market_fit import Offer, score


def test_offer_market_fit_score_high_when_pains_overlap() -> None:
    icp = ICP(
        icp_id="icp_x",
        name="x",
        industry="logistics",
        region="SA",
        company_size="medium",
        pain_points=("manual_routing", "idle_drivers"),
    )
    offer = Offer(
        offer_id="of_1",
        name="route_ai",
        addresses_pains=("manual_routing", "idle_drivers"),
        price_band="mid",
        industries=("logistics",),
        regions=("SA",),
    )
    fit = score(offer, icp)
    assert fit.fit_score >= 0.9
