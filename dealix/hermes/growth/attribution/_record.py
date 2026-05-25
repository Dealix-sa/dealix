"""
Composite attribution record.
"""

from __future__ import annotations

from dataclasses import dataclass

from dealix.hermes.growth.attribution.agent import AgentAttribution
from dealix.hermes.growth.attribution.asset import AssetAttribution
from dealix.hermes.growth.attribution.campaign import CampaignAttribution
from dealix.hermes.growth.attribution.channel import ChannelAttribution
from dealix.hermes.growth.attribution.geo import GEOAttribution
from dealix.hermes.growth.attribution.message import MessageAttribution
from dealix.hermes.growth.attribution.partner import PartnerAttribution
from dealix.hermes.growth.attribution.trust_signal import TrustSignalAttribution


@dataclass
class AttributionRecord:
    verified_revenue_sar: float
    channel: ChannelAttribution
    campaign: CampaignAttribution | None
    message: MessageAttribution | None
    asset: AssetAttribution | None
    agent: AgentAttribution | None
    partner: PartnerAttribution | None
    geo: GEOAttribution | None
    trust_signal: TrustSignalAttribution | None
    confidence: float

    def to_dict(self) -> dict[str, object]:
        return {
            "verified_revenue_sar": self.verified_revenue_sar,
            "channel": self.channel.channel,
            "campaign": self.campaign.campaign_id if self.campaign else None,
            "message_variant": self.message.variant_id if self.message else None,
            "asset": self.asset.asset_id if self.asset else None,
            "agent": self.agent.agent_id if self.agent else None,
            "partner": self.partner.partner_id if self.partner else None,
            "geo_surface": self.geo.surface_id if self.geo else None,
            "trust_signal": (
                self.trust_signal.signal_id if self.trust_signal else None
            ),
            "confidence": self.confidence,
        }


def _weighted_confidence(
    parts: list[float | None],
) -> float:
    present = [p for p in parts if p is not None]
    if not present:
        return 0.0
    return round(sum(present) / len(present), 4)


def build_attribution_record(
    verified_revenue_sar: float,
    channel: ChannelAttribution,
    *,
    campaign: CampaignAttribution | None = None,
    message: MessageAttribution | None = None,
    asset: AssetAttribution | None = None,
    agent: AgentAttribution | None = None,
    partner: PartnerAttribution | None = None,
    geo: GEOAttribution | None = None,
    trust_signal: TrustSignalAttribution | None = None,
) -> AttributionRecord:
    if verified_revenue_sar < 0:
        raise ValueError("verified_revenue_sar must be >= 0")
    confidence = _weighted_confidence(
        [
            channel.confidence,
            campaign.confidence if campaign else None,
            message.confidence if message else None,
            asset.confidence if asset else None,
            agent.confidence if agent else None,
            partner.confidence if partner else None,
            geo.confidence if geo else None,
            trust_signal.confidence if trust_signal else None,
        ]
    )
    return AttributionRecord(
        verified_revenue_sar=verified_revenue_sar,
        channel=channel,
        campaign=campaign,
        message=message,
        asset=asset,
        agent=agent,
        partner=partner,
        geo=geo,
        trust_signal=trust_signal,
        confidence=confidence,
    )
