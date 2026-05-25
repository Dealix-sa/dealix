"""Campaign attribution aggregates verified revenue per campaign_id."""

from __future__ import annotations

from dealix.hermes.growth.attribution import _base, campaign


def test_campaign_attribution_aggregates() -> None:
    _base.reset()
    campaign.attribute("cam_1", 8_000, evidence_pack_id="ep_1")
    campaign.attribute("cam_1", 2_000, evidence_pack_id="ep_2")
    assert campaign.total("cam_1") == 10_000
