"""Growth-attribution doctrine: every campaign has offer; every revenue has attribution."""

from __future__ import annotations

import pytest

from dealix.hermes.growth.attribution import AttributionLink, RevenueAttribution
from dealix.hermes.growth.campaigns import Campaign, CampaignStore


def test_campaign_requires_offer():
    """No 10: لا Campaign بلا Attribution — starts with: every campaign has an offer."""
    store = CampaignStore()
    with pytest.raises(ValueError):
        store.create(Campaign(
            name="naked campaign", target_icp="ksa_sme", offer_id="", channel="linkedin",
        ))


def test_attribution_links_revenue_to_campaign():
    """No 10: لا Campaign بلا Attribution."""
    attr = RevenueAttribution()
    attr.link(AttributionLink(
        revenue_id="rev_1", campaign_id="cmp_1", offer_id="ai_trust_kit", amount_sar=25_000,
    ))
    links = attr.for_campaign("cmp_1")
    assert len(links) == 1
    assert links[0].amount_sar == 25_000


def test_attribution_coverage_ratio():
    attr = RevenueAttribution()
    attr.link(AttributionLink(revenue_id="rev_1", campaign_id="cmp_1"))
    attr.link(AttributionLink(revenue_id="rev_2"))
    assert attr.coverage_ratio(["rev_1", "rev_2", "rev_3"]) == pytest.approx(0.6667, abs=0.001)
