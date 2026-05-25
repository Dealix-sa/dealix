"""
Growth Workspace summary — Section 52 sections (revenue by offer / channel /
campaign, pipeline by ICP, reply rates, etc.) projected from the graphs.
"""

from __future__ import annotations

from typing import Any

from ...hermes.intelligence_plane.attribution_graph import (
    AttributionDimension,
    AttributionGraph,
)
from ...hermes.intelligence_plane.learning_engine import LearningEngine
from ...hermes.intelligence_plane.revenue_graph import RevenueGraph


def build_summary(
    *,
    revenue: RevenueGraph,
    attribution: AttributionGraph,
    learning: LearningEngine,
) -> dict[str, Any]:
    return {
        "revenue_by_offer_sar": revenue.total_by_offer(),
        "revenue_by_customer_sar": revenue.total_by_customer(),
        "attribution": {
            dim.value: attribution.attributed_to(dim)
            for dim in AttributionDimension
        },
        "insights": [
            {
                "kind": i.kind.value,
                "dimension": i.dimension.value,
                "value": i.dimension_value,
                "confidence": i.confidence,
                "evidence": i.evidence,
                "recommendation": i.recommendation,
            }
            for i in learning.insights_by_channel()
        ],
    }


__all__ = ["build_summary"]
