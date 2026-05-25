"""
Products — offer-market-fit, experimentation, readiness gates.
"""

from __future__ import annotations

from dealix.hermes.products.experiment_metrics import (
    ExperimentMetrics,
    score_experiment,
)
from dealix.hermes.products.from_asset import (
    AssetCandidate,
    is_productization_candidate,
)
from dealix.hermes.products.offer_market_fit import (
    OfferMarketFit,
    score_offer_market_fit,
)
from dealix.hermes.products.readiness_gate import (
    OfferReadinessGate,
    check_offer_readiness,
)
from dealix.hermes.products.repositioning import (
    RepositioningRecommendation,
    recommend_repositioning,
)

__all__ = [
    "OfferMarketFit",
    "score_offer_market_fit",
    "ExperimentMetrics",
    "score_experiment",
    "RepositioningRecommendation",
    "recommend_repositioning",
    "OfferReadinessGate",
    "check_offer_readiness",
    "AssetCandidate",
    "is_productization_candidate",
]
