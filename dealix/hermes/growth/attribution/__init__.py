"""
Multi-layer attribution.

A single revenue event is attributed across:

- channel
- campaign
- message variant
- asset
- agent
- partner
- GEO surface
- trust signal

Each layer returns a confidence-weighted attribution row; the union is
the AttributionRecord that the dashboard renders.
"""

from __future__ import annotations

from dealix.hermes.growth.attribution.agent import AgentAttribution
from dealix.hermes.growth.attribution.asset import AssetAttribution
from dealix.hermes.growth.attribution.campaign import CampaignAttribution
from dealix.hermes.growth.attribution.channel import ChannelAttribution
from dealix.hermes.growth.attribution.geo import GEOAttribution
from dealix.hermes.growth.attribution.message import MessageAttribution
from dealix.hermes.growth.attribution.partner import PartnerAttribution
from dealix.hermes.growth.attribution.trust_signal import TrustSignalAttribution

from dealix.hermes.growth.attribution._record import (
    AttributionRecord,
    build_attribution_record,
)

__all__ = [
    "ChannelAttribution",
    "CampaignAttribution",
    "MessageAttribution",
    "AssetAttribution",
    "AgentAttribution",
    "PartnerAttribution",
    "GEOAttribution",
    "TrustSignalAttribution",
    "AttributionRecord",
    "build_attribution_record",
]
