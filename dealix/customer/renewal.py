"""خادم العميل — RenewalEngine."""

from __future__ import annotations

from datetime import date, datetime, timedelta
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from dealix.customer.health_score import CustomerHealth, HealthBand
from dealix.hermes.core.schemas import utcnow


class RenewalRecommendation(StrEnum):
    RENEW = "renew"
    UPSELL = "upsell"
    AT_RISK = "at_risk"
    DO_NOT_RENEW = "do_not_renew"


class RenewalAssessment(BaseModel):
    """Output of the renewal engine."""

    model_config = ConfigDict(extra="forbid")

    customer_id: str = Field(..., min_length=1, max_length=128)
    recommendation: RenewalRecommendation
    confidence: float = Field(..., ge=0.0, le=1.0)
    reasons: list[str] = Field(default_factory=list, max_length=10)
    renewal_due_date: date | None = None
    requires_sami_review: bool = False


class RenewalEngine:
    """Compute a renewal recommendation from health + contract metadata."""

    def assess(
        self,
        customer: CustomerHealth,
        contract_meta: dict[str, Any],
    ) -> RenewalAssessment:
        reasons: list[str] = []
        renewal_due: date | None = None
        raw_due = contract_meta.get("renewal_due_date")
        if isinstance(raw_due, date):
            renewal_due = raw_due
        elif isinstance(raw_due, str) and raw_due:
            try:
                renewal_due = date.fromisoformat(raw_due)
            except ValueError:
                renewal_due = None

        days_to_renewal = (renewal_due - utcnow().date()).days if renewal_due else None
        if days_to_renewal is not None and days_to_renewal < 0:
            reasons.append("renewal already overdue")

        recommendation = RenewalRecommendation.RENEW
        confidence = 0.6
        requires_sami = False

        if customer.band == HealthBand.GREEN:
            recommendation = RenewalRecommendation.UPSELL
            confidence = 0.85
            reasons.append("health green — pursue upsell during renewal")
        elif customer.band == HealthBand.AMBER:
            recommendation = RenewalRecommendation.RENEW
            confidence = 0.7
            reasons.append("health amber — renew + monitor")
            if "usage_decline" in customer.flags:
                requires_sami = True
                reasons.append("usage_decline flag — flag for Sami review")
        else:  # RED
            recommendation = RenewalRecommendation.AT_RISK
            confidence = 0.6
            requires_sami = True
            reasons.append("health red — renewal at risk; Sami must approve next steps")

        if contract_meta.get("payment_blocked"):
            recommendation = RenewalRecommendation.DO_NOT_RENEW
            confidence = 0.9
            requires_sami = True
            reasons.append("payment_blocked — do not renew without resolution")

        return RenewalAssessment(
            customer_id=customer.customer_id,
            recommendation=recommendation,
            confidence=confidence,
            reasons=reasons,
            renewal_due_date=renewal_due,
            requires_sami_review=requires_sami,
        )


__all__ = [
    "RenewalAssessment",
    "RenewalEngine",
    "RenewalRecommendation",
]
