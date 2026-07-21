"""
Revenue Intelligence Dashboard

Computes intelligent revenue signals from pipeline data:
- Pipeline health score
- Win probability by stage
- Revenue at risk
- Recommended next actions
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any


@dataclass
class Deal:
    deal_id: str
    company_name: str
    stage: str
    value_sar: float
    created_at: datetime
    last_activity_at: datetime
    activities_count: int = 0
    days_in_stage: int = 0


@dataclass
class StageStats:
    stage: str
    count: int = 0
    total_value: float = 0.0
    avg_days: float = 0.0
    win_probability: float = 0.0


@dataclass
class RevenueIntelligence:
    pipeline_health: float
    total_pipeline_sar: float
    weighted_pipeline_sar: float
    revenue_at_risk_sar: float
    recommended_actions: list[str]
    stage_breakdown: list[StageStats]


class RevenueIntelligenceEngine:
    """Computes revenue intelligence from a pipeline of deals."""

    # Stage → probability of close
    STAGE_PROBABILITY: dict[str, float] = {
        "lead": 0.10,
        "qualified": 0.25,
        "diagnostic_scheduled": 0.40,
        "proposal_sent": 0.55,
        "pilot_negotiation": 0.70,
        "contract_sent": 0.85,
        "closed_won": 1.00,
        "closed_lost": 0.00,
    }

    # Max days before a deal is considered stale
    STALE_DAYS: int = 14

    def __init__(self):
        self._deals: list[Deal] = []

    def load_deals(self, deals: list[Deal]) -> None:
        self._deals = deals

    def analyze(self) -> RevenueIntelligence:
        """Run full revenue intelligence analysis."""
        if not self._deals:
            return RevenueIntelligence(
                pipeline_health=0.0,
                total_pipeline_sar=0.0,
                weighted_pipeline_sar=0.0,
                revenue_at_risk_sar=0.0,
                recommended_actions=["No active deals. Start lead generation."],
                stage_breakdown=[],
            )

        total_value = sum(d.value_sar for d in self._deals if d.stage != "closed_lost")
        weighted_value = sum(
            d.value_sar * self.STAGE_PROBABILITY.get(d.stage, 0.1)
            for d in self._deals if d.stage != "closed_lost"
        )

        at_risk = self._calculate_risk()
        health = self._calculate_health()
        breakdown = self._stage_breakdown()
        actions = self._recommendations(health, at_risk)

        return RevenueIntelligence(
            pipeline_health=round(health, 1),
            total_pipeline_sar=round(total_value, 2),
            weighted_pipeline_sar=round(weighted_value, 2),
            revenue_at_risk_sar=round(at_risk, 2),
            recommended_actions=actions,
            stage_breakdown=breakdown,
        )

    def _calculate_risk(self) -> float:
        now = datetime.utcnow()
        at_risk = 0.0
        for deal in self._deals:
            if deal.stage in ("closed_won", "closed_lost"):
                continue
            days_since_activity = (now - deal.last_activity_at).days
            if days_since_activity > self.STALE_DAYS:
                prob = self.STAGE_PROBABILITY.get(deal.stage, 0.1)
                at_risk += deal.value_sar * prob * 0.5
        return at_risk

    def _calculate_health(self) -> float:
        if not self._deals:
            return 0.0

        scores = []
        for deal in self._deals:
            if deal.stage == "closed_lost":
                continue
            score = 0.0
            prob = self.STAGE_PROBABILITY.get(deal.stage, 0.1)
            score += prob * 50  # up to 50 for stage

            days = (datetime.utcnow() - deal.last_activity_at).days
            if days <= 3:
                score += 30
            elif days <= 7:
                score += 20
            elif days <= 14:
                score += 10

            if deal.activities_count >= 3:
                score += 20
            elif deal.activities_count >= 1:
                score += 10

            scores.append(min(score, 100.0))

        return sum(scores) / len(scores) if scores else 0.0

    def _stage_breakdown(self) -> list[StageStats]:
        stats: dict[str, dict[str, Any]] = {}
        for deal in self._deals:
            if deal.stage not in stats:
                stats[deal.stage] = {"count": 0, "value": 0.0, "days": []}
            stats[deal.stage]["count"] += 1
            stats[deal.stage]["value"] += deal.value_sar
            stats[deal.stage]["days"].append(deal.days_in_stage)

        return [
            StageStats(
                stage=stage,
                count=data["count"],
                total_value=round(data["value"], 2),
                avg_days=round(sum(data["days"]) / len(data["days"]), 1) if data["days"] else 0.0,
                win_probability=round(self.STAGE_PROBABILITY.get(stage, 0.1) * 100, 1),
            )
            for stage, data in sorted(stats.items())
        ]

    def _recommendations(self, health: float, at_risk: float) -> list[str]:
        actions = []
        if health < 40:
            actions.append("Pipeline health is low. Schedule founder review of top 5 deals.")
        if at_risk > 1000:
            actions.append(f"SAR {at_risk:,.0f} at risk. Re-activate stale deals this week.")

        stage_counts = {}
        for deal in self._deals:
            stage_counts[deal.stage] = stage_counts.get(deal.stage, 0) + 1

        if stage_counts.get("lead", 0) < 10:
            actions.append("Lead count below target. Run Saudi lead generation this week.")
        if stage_counts.get("proposal_sent", 0) > 0 and stage_counts.get("pilot_negotiation", 0) == 0:
            actions.append("Proposals sent but no pilots in negotiation. Follow up within 48 hours.")

        if not actions:
            actions.append("Pipeline is healthy. Focus on converting pilots to contracts.")

        return actions
