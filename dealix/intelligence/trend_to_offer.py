"""خادم الذكاء — TrendToOfferTranslator.

Heuristic mapping from short trend phrases ("AI governance", "PDPL
compliance", "agency consolidation", "vertical SaaS rebound") to
suggested offer ideas. Returns a list of OfferIdea records the operator
can promote into the catalog.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class OfferIdea(BaseModel):
    """A suggested offer derived from a market trend."""

    model_config = ConfigDict(extra="forbid")

    name: str = Field(..., min_length=1, max_length=120)
    buyer: str = Field(..., min_length=1, max_length=120)
    rationale: str = Field(..., min_length=1, max_length=400)
    suggested_price_band_sar: tuple[int, int]


_TREND_MAP: dict[str, list[OfferIdea]] = {
    "ai governance": [
        OfferIdea(
            name="AI Trust Kit",
            buyer="CTO / Head of AI",
            rationale="Trend pushes regulators to demand evidence-pack discipline.",
            suggested_price_band_sar=(12000, 24000),
        ),
        OfferIdea(
            name="Agent Risk Audit",
            buyer="Chief Risk Officer",
            rationale="High-risk agent estates need a third-party audit.",
            suggested_price_band_sar=(8000, 16000),
        ),
    ],
    "pdpl compliance": [
        OfferIdea(
            name="PDPL Readiness Sprint",
            buyer="DPO / Legal counsel",
            rationale="2-week sprint to align data handling with PDPL.",
            suggested_price_band_sar=(6000, 12000),
        ),
    ],
    "agency consolidation": [
        OfferIdea(
            name="Agency White-label Kit",
            buyer="Agency owner",
            rationale="Smaller agencies need a defensible technology layer.",
            suggested_price_band_sar=(9000, 18000),
        ),
    ],
    "vertical saas rebound": [
        OfferIdea(
            name="Vertical Launch Sprint",
            buyer="Vertical SaaS founder",
            rationale="Vertical launches need ICP + ProofPack in two weeks.",
            suggested_price_band_sar=(7500, 15000),
        ),
    ],
    "renewal pressure": [
        OfferIdea(
            name="Renewal & Upsell Pack",
            buyer="Customer success lead",
            rationale="Retention is the cheapest growth lever this quarter.",
            suggested_price_band_sar=(3500, 8000),
        ),
    ],
}


class TrendToOfferTranslator:
    """Map short trend phrases to OfferIdea suggestions."""

    def translate(self, trend: str) -> list[OfferIdea]:
        key = trend.lower().strip()
        if key in _TREND_MAP:
            return list(_TREND_MAP[key])
        # Loose match — return any trend whose key is a substring.
        for known, ideas in _TREND_MAP.items():
            if known in key or key in known:
                return list(ideas)
        return []

    def known_trends(self) -> list[str]:
        return sorted(_TREND_MAP.keys())


__all__ = ["OfferIdea", "TrendToOfferTranslator"]
