"""
Revenue Forecasting Engine

Forecasts revenue from current pipeline using stage probabilities
and historical conversion patterns.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from intelligence.revenue_intelligence import Deal, RevenueIntelligenceEngine


@dataclass
class RevenueForecast:
    period: str
    expected_revenue_sar: float
    best_case_sar: float
    worst_case_sar: float
    forecast_confidence: float
    assumptions: list[str]


class RevenueForecastingEngine:
    """Simple but grounded revenue forecasting from pipeline."""

    def __init__(self):
        self.engine = RevenueIntelligenceEngine()

    def forecast(
        self,
        deals: list[Deal],
        period_days: int = 90,
    ) -> RevenueForecast:
        """Forecast revenue for the next N days."""
        self.engine.load_deals(deals)
        intel = self.engine.analyze()

        weighted = intel.weighted_pipeline_sar
        # Simple time-based decay: assume 30% of weighted pipeline closes in period
        expected = weighted * 0.30
        best_case = intel.total_pipeline_sar * 0.45
        worst_case = expected * 0.40

        confidence = intel.pipeline_health / 100

        assumptions = [
            f"Forecast horizon: {period_days} days",
            f"Based on weighted pipeline of SAR {weighted:,.0f}",
            "Assumes 30% of weighted pipeline closes within period",
            f"Pipeline health: {intel.pipeline_health:.0f}/100",
        ]

        return RevenueForecast(
            period=f"next_{period_days}_days",
            expected_revenue_sar=round(expected, 2),
            best_case_sar=round(best_case, 2),
            worst_case_sar=round(worst_case, 2),
            forecast_confidence=round(confidence, 2),
            assumptions=assumptions,
        )

    def to_dict(self, forecast: RevenueForecast) -> dict[str, Any]:
        return {
            "period": forecast.period,
            "expected_revenue_sar": forecast.expected_revenue_sar,
            "best_case_sar": forecast.best_case_sar,
            "worst_case_sar": forecast.worst_case_sar,
            "forecast_confidence": forecast.forecast_confidence,
            "assumptions": forecast.assumptions,
        }
