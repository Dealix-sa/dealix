"""
Learning Engine — يستخرج "ما الذي يجب توسيعه؟" و "ما الذي يجب قتله؟"
من الـ graphs الأربعة. لا LLM هنا — خوارزميات بسيطة قابلة للتفسير.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from .attribution_graph import AttributionDimension, AttributionGraph
from .outcome_graph import OutcomeGraph, OutcomeKind
from .revenue_graph import RevenueGraph


class InsightKind(StrEnum):
    EXPAND = "expand"  # double down
    KILL = "kill"  # stop investing
    INVESTIGATE = "investigate"  # ambiguous


@dataclass
class LearningInsight:
    kind: InsightKind
    dimension: AttributionDimension
    dimension_value: str
    confidence: float  # 0..1
    evidence: dict[str, float | int]
    recommendation: str


class LearningEngine:
    def __init__(
        self,
        *,
        revenue: RevenueGraph,
        attribution: AttributionGraph,
        outcomes: OutcomeGraph,
    ) -> None:
        self._revenue = revenue
        self._attribution = attribution
        self._outcomes = outcomes

    def insights_by_channel(
        self, *, min_revenue_sar: int = 5_000
    ) -> list[LearningInsight]:
        stats = self._attribution.attributed_to(AttributionDimension.CHANNEL)
        # convert weights to attributed revenue
        total_revenue = sum(r.amount_sar for r in self._revenue.all())
        if total_revenue == 0 or not stats:
            return []

        attributed_revenue: dict[str, float] = {
            channel: weight_sum * total_revenue / max(sum(stats.values()), 1e-9)
            for channel, weight_sum in stats.items()
        }

        insights: list[LearningInsight] = []
        for channel, revenue in attributed_revenue.items():
            if revenue >= min_revenue_sar * 2:
                insights.append(
                    LearningInsight(
                        kind=InsightKind.EXPAND,
                        dimension=AttributionDimension.CHANNEL,
                        dimension_value=channel,
                        confidence=min(1.0, revenue / (min_revenue_sar * 5)),
                        evidence={"attributed_revenue_sar": revenue},
                        recommendation=(
                            f"double the experiment budget on `{channel}`"
                        ),
                    )
                )
            elif revenue < min_revenue_sar / 2:
                insights.append(
                    LearningInsight(
                        kind=InsightKind.KILL,
                        dimension=AttributionDimension.CHANNEL,
                        dimension_value=channel,
                        confidence=0.7,
                        evidence={"attributed_revenue_sar": revenue},
                        recommendation=(
                            f"freeze spend on `{channel}` until evidence improves"
                        ),
                    )
                )
            else:
                insights.append(
                    LearningInsight(
                        kind=InsightKind.INVESTIGATE,
                        dimension=AttributionDimension.CHANNEL,
                        dimension_value=channel,
                        confidence=0.5,
                        evidence={"attributed_revenue_sar": revenue},
                        recommendation=(
                            f"run a small structured experiment on `{channel}`"
                        ),
                    )
                )
        return insights

    def execution_without_outcome_count(
        self, executions: list[str]
    ) -> int:
        """Count executions that produced no outcome (CTRL-OPS-001 violation)."""
        missing = 0
        for execution_id in executions:
            if not self._outcomes.for_execution(execution_id):
                missing += 1
        return missing


__all__ = ["InsightKind", "LearningEngine", "LearningInsight"]
