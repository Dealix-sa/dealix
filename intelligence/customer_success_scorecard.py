"""
Customer Success Scorecard

Scores existing customer health based on engagement, delivery, payment,
and expansion signals. Predicts churn risk and upsell readiness.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any


class HealthTier(str, Enum):
    EXCELLENT = "excellent"
    GOOD = "good"
    AT_RISK = "at_risk"
    CRITICAL = "critical"


@dataclass
class CustomerHealthScore:
    customer_id: str
    customer_name: str
    overall_score: float
    tier: HealthTier
    engagement_score: float
    delivery_score: float
    payment_score: float
    expansion_score: float
    risk_flags: list[str]
    recommended_actions: list[str]


class CustomerSuccessScorecard:
    """Deterministic customer health scoring for Dealix customers."""

    def score(
        self,
        customer_id: str,
        customer_name: str,
        last_activity_days: int,
        deliverables_completed: int,
        deliverables_total: int,
        payments_on_time: int,
        payments_total: int,
        support_tickets_open: int,
        nps_score: float | None,
        expansion_signals: list[str] | None = None,
    ) -> CustomerHealthScore:
        """Calculate customer health score."""
        expansion_signals = expansion_signals or []

        # Engagement (0-25)
        if last_activity_days <= 7:
            engagement = 25
        elif last_activity_days <= 14:
            engagement = 18
        elif last_activity_days <= 30:
            engagement = 10
        else:
            engagement = 0

        # Delivery (0-25)
        if deliverables_total > 0:
            delivery = (deliverables_completed / deliverables_total) * 25
        else:
            delivery = 12.5

        # Payment (0-25)
        if payments_total > 0:
            payment = (payments_on_time / payments_total) * 25
        else:
            payment = 25

        # Expansion / sentiment (0-25)
        expansion = 0
        if nps_score is not None and nps_score >= 50:
            expansion += 10
        if nps_score is not None and nps_score >= 70:
            expansion += 5
        expansion += min(len(expansion_signals) * 5, 10)

        overall = engagement + delivery + payment + expansion

        risk_flags: list[str] = []
        if last_activity_days > 14:
            risk_flags.append(f"No activity for {last_activity_days} days")
        if deliverables_total > 0 and deliverables_completed / deliverables_total < 0.5:
            risk_flags.append("Delivery completion below 50%")
        if payments_total > 0 and payments_on_time / payments_total < 0.8:
            risk_flags.append("Payment history concerns")
        if support_tickets_open > 3:
            risk_flags.append(f"{support_tickets_open} open support tickets")

        if overall >= 80:
            tier = HealthTier.EXCELLENT
        elif overall >= 60:
            tier = HealthTier.GOOD
        elif overall >= 40:
            tier = HealthTier.AT_RISK
        else:
            tier = HealthTier.CRITICAL

        actions: list[str] = []
        if tier in (HealthTier.AT_RISK, HealthTier.CRITICAL):
            actions.append("Schedule executive check-in within 48 hours")
        if support_tickets_open > 3:
            actions.append("Escalate open support tickets")
        if expansion >= 20 and tier in (HealthTier.EXCELLENT, HealthTier.GOOD):
            actions.append("Initiate upsell conversation")
        if not actions:
            actions.append("Continue regular cadence")

        return CustomerHealthScore(
            customer_id=customer_id,
            customer_name=customer_name,
            overall_score=round(overall, 1),
            tier=tier,
            engagement_score=engagement,
            delivery_score=round(delivery, 1),
            payment_score=round(payment, 1),
            expansion_score=expansion,
            risk_flags=risk_flags,
            recommended_actions=actions,
        )

    def batch_score(self, customers: list[dict[str, Any]]) -> list[CustomerHealthScore]:
        return [self.score(**c) for c in customers]
