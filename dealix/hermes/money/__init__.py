"""
money — revenue quality, cost intelligence, margin analysis, pricing.

The platform never optimizes for revenue volume in isolation. Every
decision joins revenue with margin, risk, and repeatability.
"""

from dealix.hermes.money.cost_intelligence import (
    CostBreakdown,
    register_cost,
    total_cost,
)
from dealix.hermes.money.margin_analysis import MarginReport, analyse_margin
from dealix.hermes.money.pricing_engine import (
    PricingInputs,
    PricingRecommendation,
    recommend_price,
)
from dealix.hermes.money.revenue_quality import RevenueQualityScore, score_revenue_quality

__all__ = [
    "CostBreakdown",
    "MarginReport",
    "PricingInputs",
    "PricingRecommendation",
    "RevenueQualityScore",
    "analyse_margin",
    "recommend_price",
    "register_cost",
    "score_revenue_quality",
    "total_cost",
]
