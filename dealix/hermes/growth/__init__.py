"""
growth — Verified-Revenue First growth engine.

Vanity stops here: views, likes, "interested" meetings cannot become
verified revenue without payment + signed agreement + activation.
"""

from dealix.hermes.growth.campaign_quality import score_campaign
from dealix.hermes.growth.channel_quality import score_channel
from dealix.hermes.growth.growth_scale_kill import GrowthDecision, decide_for_offer
from dealix.hermes.growth.message_quality import score_message
from dealix.hermes.growth.offer_market_fit import OfferMarketFit, score as omf_score
from dealix.hermes.growth.trust_signals import TrustSignal, TrustSignalLedger
from dealix.hermes.growth.verified_revenue_loop import (
    REVENUE_VERIFICATION_POLICY,
    RevenueEvent,
    VerifiedRevenueLoop,
)

__all__ = [
    "GrowthDecision",
    "OfferMarketFit",
    "REVENUE_VERIFICATION_POLICY",
    "RevenueEvent",
    "TrustSignal",
    "TrustSignalLedger",
    "VerifiedRevenueLoop",
    "decide_for_offer",
    "omf_score",
    "score_campaign",
    "score_channel",
    "score_message",
]
