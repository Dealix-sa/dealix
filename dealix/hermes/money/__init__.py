"""
Money layer.

Counts only verified revenue. Scores revenue quality. Tracks delivery
margin. Treats founder time as a finite, accountable cost.
"""

from __future__ import annotations

from dealix.hermes.money.delivery_margin import (
    DeliveryMarginMetrics,
    compute_delivery_margin,
)
from dealix.hermes.money.founder_time_cost import (
    FounderTimeCost,
    score_founder_time_cost,
)
from dealix.hermes.money.revenue_quality import (
    RevenueQualityScore,
    score_revenue_quality,
)
from dealix.hermes.money.verified_revenue import (
    VERIFIED_REVENUE_SOURCES,
    RevenueEvent,
    is_verified,
    sum_verified_revenue,
)

__all__ = [
    "RevenueEvent",
    "VERIFIED_REVENUE_SOURCES",
    "is_verified",
    "sum_verified_revenue",
    "RevenueQualityScore",
    "score_revenue_quality",
    "FounderTimeCost",
    "score_founder_time_cost",
    "DeliveryMarginMetrics",
    "compute_delivery_margin",
]
