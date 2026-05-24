"""Churn risk classifier — purely informational; drives renewal actions."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ChurnRisk:
    level: str            # low|medium|high
    rationale: str


class ChurnRiskScorer:
    def assess(self, *, health_score: float, days_since_value_report: int) -> ChurnRisk:
        if health_score < 0.35 or days_since_value_report > 45:
            return ChurnRisk("high", f"health={health_score:.2f}, last_report={days_since_value_report}d ago")
        if health_score < 0.55 or days_since_value_report > 30:
            return ChurnRisk("medium", f"health={health_score:.2f}, last_report={days_since_value_report}d ago")
        return ChurnRisk("low", f"health={health_score:.2f}, last_report={days_since_value_report}d ago")


__all__ = ["ChurnRisk", "ChurnRiskScorer"]
