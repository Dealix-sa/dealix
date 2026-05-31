"""
GrowthScaleKill — combine offer-market-fit, channel quality, and trust
signals to make a single scale / hold / kill decision for an offer.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from dealix.hermes.growth.channel_quality import ChannelQualityScore
from dealix.hermes.growth.offer_market_fit import OfferMarketFit


class GrowthAction(StrEnum):
    SCALE = "scale"
    HOLD = "hold"
    REPOSITION = "reposition"
    REPRICE = "reprice"
    KILL = "kill"


@dataclass
class GrowthDecision:
    offer_id: str
    action: GrowthAction
    confidence: float
    reasons: tuple[str, ...]


def decide_for_offer(
    omf: OfferMarketFit,
    *,
    best_channel: ChannelQualityScore | None,
    trust_signal_count: int,
) -> GrowthDecision:
    reasons: list[str] = []

    if omf.decision == "kill":
        return GrowthDecision(omf.offer_id, GrowthAction.KILL, 0.9, ("offer market fit very low",))
    if best_channel is None or best_channel.grade in ("C", "D"):
        reasons.append("no channel with grade B or better")
    if trust_signal_count < 3:
        reasons.append("insufficient trust signals to scale")
    if omf.decision == "scale" and best_channel and best_channel.grade in ("A", "B") and trust_signal_count >= 3:
        return GrowthDecision(omf.offer_id, GrowthAction.SCALE, 0.85, ("OMF=scale", "channel viable", "trust signals present"))
    if omf.decision == "reposition":
        return GrowthDecision(omf.offer_id, GrowthAction.REPOSITION, 0.7, ("OMF=reposition",) + tuple(reasons))
    if omf.decision == "reprice_or_bundle":
        return GrowthDecision(omf.offer_id, GrowthAction.REPRICE, 0.7, ("OMF=reprice/bundle",) + tuple(reasons))
    if omf.decision == "niche_down":
        return GrowthDecision(omf.offer_id, GrowthAction.HOLD, 0.6, ("OMF=niche_down",) + tuple(reasons))
    return GrowthDecision(omf.offer_id, GrowthAction.HOLD, 0.5, tuple(reasons) or ("default hold",))
