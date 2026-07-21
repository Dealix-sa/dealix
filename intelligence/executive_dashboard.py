"""
Executive Dashboard Data Provider

Aggregates all commercial intelligence into a single executive view.
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from intelligence.revenue_intelligence import RevenueIntelligenceEngine
from intelligence.saudi_market_intelligence import SaudiMarketIntelligence
from intelligence.competitor_battlecards import CompetitorBattlecards
from intelligence.customer_success_scorecard import CustomerSuccessScorecard
from intelligence.pricing_engine import PricingEngine
from intelligence.product_led_growth import ProductLedGrowthFlow
from intelligence.revenue_forecasting import RevenueForecastingEngine
from intelligence.saudi_lead_machine import SaudiLeadMachine


class ExecutiveDashboardData:
    """Provides unified data for the Dealix executive dashboard."""

    PROSPECTS_PATH = Path("data/commercial/saudi_prospects_sample.json")
    PIPELINE_PATH = Path("data/commercial/pipeline_sample.json")

    def __init__(self):
        self.lead_machine = SaudiLeadMachine()
        self.pricing = PricingEngine()
        self.success = CustomerSuccessScorecard()
        self.battlecards = CompetitorBattlecards()
        self.plg = ProductLedGrowthFlow()
        self.forecasting = RevenueForecastingEngine()
        self.market_intel = SaudiMarketIntelligence()

    def snapshot(self) -> dict[str, Any]:
        """Return a complete executive snapshot."""
        prospects = self._load_prospects()
        deals = self._load_deals()

        enriched = self.lead_machine.enrich_batch(prospects)
        priority_leads = self.lead_machine.export_priority_list(enriched, top_n=5)

        self.forecasting.engine.load_deals(deals)
        forecast = self.forecasting.forecast(deals)

        revenue_intel = RevenueIntelligenceEngine()
        revenue_intel.load_deals(deals)
        pipeline = revenue_intel.analyze()

        sample_customer = self.success.score(
            customer_id="c1",
            customer_name="Najm Tech",
            last_activity_days=5,
            deliverables_completed=3,
            deliverables_total=4,
            payments_on_time=2,
            payments_total=2,
            support_tickets_open=1,
            nps_score=65,
            expansion_signals=["asked about add-on", "increased usage"],
        )

        return {
            "generated_at": datetime.utcnow().isoformat(),
            "priority_leads": priority_leads,
            "pipeline": {
                "health": pipeline.pipeline_health,
                "total_sar": pipeline.total_pipeline_sar,
                "weighted_sar": pipeline.weighted_pipeline_sar,
                "at_risk_sar": pipeline.revenue_at_risk_sar,
                "actions": pipeline.recommended_actions,
            },
            "forecast": {
                "expected_90d_sar": forecast.expected_revenue_sar,
                "best_case_sar": forecast.best_case_sar,
                "worst_case_sar": forecast.worst_case_sar,
                "confidence": forecast.forecast_confidence,
            },
            "customer_health": {
                "customer": sample_customer.customer_name,
                "score": sample_customer.overall_score,
                "tier": sample_customer.tier.value,
                "risk_flags": sample_customer.risk_flags,
                "actions": sample_customer.recommended_actions,
            },
            "competitive_position": self.battlecards.to_dict(self.battlecards.get("generic_crm")),
            "plg_preview": self.plg.run("Demo Co", "software", "Riyadh", 60).to_dict(),
            "sector_momentum": [
                {"sector": s, "momentum": self.market_intel.sector_momentum(s).value}
                for s in ["fintech", "logistics", "software", "healthcare_tech", "proptech"]
            ],
        }

    def _load_prospects(self) -> list[dict[str, Any]]:
        if not self.PROSPECTS_PATH.exists():
            return []
        return json.loads(self.PROSPECTS_PATH.read_text(encoding="utf-8"))

    def _load_deals(self) -> list:
        from intelligence import Deal
        if not self.PIPELINE_PATH.exists():
            return []
        raw = json.loads(self.PIPELINE_PATH.read_text(encoding="utf-8"))
        now = datetime.utcnow()
        return [
            Deal(
                deal_id=d["deal_id"],
                company_name=d["company_name"],
                stage=d["stage"],
                value_sar=d["value_sar"],
                created_at=datetime.fromisoformat(d.get("created_at", now.isoformat())),
                last_activity_at=datetime.fromisoformat(d.get("last_activity_at", now.isoformat())),
                activities_count=d.get("activities_count", 0),
                days_in_stage=d.get("days_in_stage", 0),
            )
            for d in raw
        ]
