"""
Repositioning recommender — converts an OfferMarketFit band into an
explicit go-forward decision.
"""

from __future__ import annotations

from dataclasses import dataclass

from dealix.hermes.products.offer_market_fit import OfferMarketFit


@dataclass
class RepositioningRecommendation:
    offer_id: str
    decision: str  # "scale" | "reprice" | "reposition" | "niche_down" | "bundle" | "pause" | "kill"
    reason: str


def recommend_repositioning(fit: OfferMarketFit) -> RepositioningRecommendation:
    notes = " | ".join(fit.notes)
    if fit.band == "double_down":
        return RepositioningRecommendation(fit.offer_id, "scale", "fit score in double-down band")
    if fit.band == "scale":
        return RepositioningRecommendation(fit.offer_id, "scale", "fit score in scale band")
    if fit.band == "iterate":
        if fit.breakdown.get("delivery_margin", 0) < 10:
            return RepositioningRecommendation(fit.offer_id, "reprice", notes)
        if fit.breakdown.get("retainer_rate", 0) < 5:
            return RepositioningRecommendation(fit.offer_id, "bundle", notes)
        return RepositioningRecommendation(fit.offer_id, "niche_down", notes)
    if fit.band == "reposition":
        return RepositioningRecommendation(fit.offer_id, "reposition", notes)
    return RepositioningRecommendation(fit.offer_id, "kill", notes or "low fit score")
