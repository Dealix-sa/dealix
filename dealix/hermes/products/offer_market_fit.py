"""
Offer-Market Fit metrics.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class OfferMarketFit:
    offer_id: str
    score: float
    band: str
    breakdown: dict[str, float]
    notes: list[str]


def _rate(numerator: int, denominator: int) -> float:
    if denominator <= 0:
        return 0.0
    return numerator / denominator


def score_offer_market_fit(
    offer_id: str,
    *,
    outreach_count: int,
    reply_count: int,
    qualified_call_count: int,
    proposal_count: int,
    win_count: int,
    payment_count: int,
    retainer_conversion_count: int,
    referral_count: int,
    delivery_margin_pct: float,
) -> OfferMarketFit:
    reply_rate = _rate(reply_count, outreach_count)
    qualified_rate = _rate(qualified_call_count, reply_count)
    proposal_rate = _rate(proposal_count, qualified_call_count)
    win_rate = _rate(win_count, proposal_count)
    payment_rate = _rate(payment_count, win_count)
    retainer_rate = _rate(retainer_conversion_count, payment_count)
    referral_rate = _rate(referral_count, payment_count)

    breakdown = {
        "reply_rate": reply_rate * 10,
        "qualified_rate": qualified_rate * 15,
        "proposal_rate": proposal_rate * 10,
        "win_rate": win_rate * 20,
        "payment_rate": payment_rate * 15,
        "retainer_rate": retainer_rate * 15,
        "referral_rate": referral_rate * 5,
        "delivery_margin": max(0.0, delivery_margin_pct / 2),
    }
    raw = sum(breakdown.values())
    score = max(0.0, min(100.0, round(raw, 2)))
    if score < 25:
        band = "kill"
    elif score < 45:
        band = "reposition"
    elif score < 65:
        band = "iterate"
    elif score < 80:
        band = "scale"
    else:
        band = "double_down"

    notes: list[str] = []
    if win_rate < 0.2 and proposal_count >= 5:
        notes.append("proposal-to-win conversion is weak; tighten qualification")
    if delivery_margin_pct < 30:
        notes.append("delivery margin below 30% — reprice")
    if retainer_rate < 0.2 and payment_count >= 5:
        notes.append("low retainer conversion — design a sticky follow-on")

    return OfferMarketFit(
        offer_id=offer_id,
        score=score,
        band=band,
        breakdown={k: round(v, 2) for k, v in breakdown.items()},
        notes=notes,
    )
