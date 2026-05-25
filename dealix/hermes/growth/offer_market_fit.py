"""
OfferMarketFit — does this offer actually fit the market?

Inputs are funnel rates that the growth engine measures from end to end.
Output drives the scale / reposition / reprice / kill decision.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class OfferMarketFit:
    offer_id: str
    reply_rate: float
    call_rate: float
    proposal_rate: float
    win_rate: float
    payment_rate: float
    retainer_conversion: float
    delivery_margin: float
    score: float
    decision: str


def score(
    *,
    offer_id: str,
    reply_rate: float,
    call_rate: float,
    proposal_rate: float,
    win_rate: float,
    payment_rate: float,
    retainer_conversion: float,
    delivery_margin: float,
) -> OfferMarketFit:
    s = round(
        0.08 * reply_rate
        + 0.1 * call_rate
        + 0.15 * proposal_rate
        + 0.2 * win_rate
        + 0.22 * payment_rate
        + 0.15 * retainer_conversion
        + 0.1 * max(0.0, delivery_margin),
        4,
    )
    if s >= 0.45 and delivery_margin >= 0.4:
        decision = "scale"
    elif s >= 0.3:
        decision = "reposition"
    elif s >= 0.15:
        decision = "reprice_or_bundle"
    elif s >= 0.05:
        decision = "niche_down"
    else:
        decision = "kill"
    return OfferMarketFit(
        offer_id=offer_id,
        reply_rate=reply_rate,
        call_rate=call_rate,
        proposal_rate=proposal_rate,
        win_rate=win_rate,
        payment_rate=payment_rate,
        retainer_conversion=retainer_conversion,
        delivery_margin=delivery_margin,
        score=s,
        decision=decision,
    )
