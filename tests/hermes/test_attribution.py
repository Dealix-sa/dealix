from __future__ import annotations

import pytest

from dealix.hermes.growth.attribution import (
    AgentAttribution,
    AssetAttribution,
    CampaignAttribution,
    ChannelAttribution,
    GEOAttribution,
    MessageAttribution,
    PartnerAttribution,
    TrustSignalAttribution,
    build_attribution_record,
)


def test_full_attribution_record_round_trip():
    record = build_attribution_record(
        25000,
        ChannelAttribution(channel="direct_outreach", confidence=0.9),
        campaign=CampaignAttribution(campaign_id="ai_trust_kit_saudi_b2b", confidence=0.8),
        message=MessageAttribution(
            variant_id="executive_control_angle",
            confidence=0.7,
            angle="executive_control",
        ),
        asset=AssetAttribution(asset_id="ai_governance_checklist", confidence=0.6),
        agent=AgentAttribution(agent_id="proposal_factory", confidence=0.7),
        partner=PartnerAttribution(partner_id="agency_xyz", confidence=0.5),
        geo=GEOAttribution(surface_id="answer_engine_page_001", confidence=0.4),
        trust_signal=TrustSignalAttribution(
            signal_id="evidence_pack_sample", confidence=0.55
        ),
    )
    out = record.to_dict()
    assert out["verified_revenue_sar"] == 25000
    assert out["channel"] == "direct_outreach"
    assert 0 < out["confidence"] <= 1


def test_attribution_requires_channel():
    with pytest.raises(ValueError):
        ChannelAttribution(channel="", confidence=0.5)


def test_confidence_bounds_enforced():
    with pytest.raises(ValueError):
        ChannelAttribution(channel="x", confidence=1.2)
