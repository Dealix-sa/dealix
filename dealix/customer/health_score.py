"""خادم العميل — CustomerHealthScorer."""

from __future__ import annotations

from datetime import datetime, timedelta
from decimal import Decimal
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from dealix.hermes.core.outcomes import Outcome, OutcomeKind
from dealix.hermes.core.schemas import utcnow


class HealthBand(StrEnum):
    GREEN = "green"
    AMBER = "amber"
    RED = "red"


class CustomerHealth(BaseModel):
    """A customer's overall health, broken into four components."""

    model_config = ConfigDict(extra="forbid")

    customer_id: str = Field(..., min_length=1, max_length=128)
    score: float = Field(..., ge=0.0, le=5.0)
    band: HealthBand
    components: dict[str, float] = Field(default_factory=dict)
    flags: list[str] = Field(default_factory=list, max_length=10)


class CustomerHealthScorer:
    """Combine usage, payment, support and engagement signals."""

    def score(
        self,
        customer_meta: dict[str, Any],
        outcomes: list[Outcome],
        now: datetime | None = None,
    ) -> CustomerHealth:
        ref = now or utcnow()
        customer_id = str(customer_meta.get("customer_id") or "unknown")
        usage_score = self._usage_score(customer_meta)
        payment_score = self._payment_score(customer_meta)
        support_score = self._support_score(customer_meta)
        engagement_score = self._engagement_score(customer_meta, outcomes, ref)

        components = {
            "usage": round(usage_score, 3),
            "payment": round(payment_score, 3),
            "support": round(support_score, 3),
            "engagement": round(engagement_score, 3),
        }
        score = round(
            (usage_score * 0.30)
            + (payment_score * 0.30)
            + (support_score * 0.20)
            + (engagement_score * 0.20),
            3,
        )
        if score >= 4.0:
            band = HealthBand.GREEN
        elif score >= 2.5:
            band = HealthBand.AMBER
        else:
            band = HealthBand.RED
        flags: list[str] = []
        if usage_score < 2.0:
            flags.append("usage_decline")
        if payment_score < 2.0:
            flags.append("payment_risk")
        if support_score < 2.0:
            flags.append("support_volume_high")
        if engagement_score < 2.0:
            flags.append("disengaged")
        return CustomerHealth(
            customer_id=customer_id,
            score=score,
            band=band,
            components=components,
            flags=flags,
        )

    @staticmethod
    def _usage_score(meta: dict[str, Any]) -> float:
        # Active feature ratio, 0..1.
        ratio = float(meta.get("usage_ratio", 0.5))
        return max(0.0, min(5.0, ratio * 5.0))

    @staticmethod
    def _payment_score(meta: dict[str, Any]) -> float:
        # Days past due — 0 days = 5, 30+ days = 0.
        days_past_due = int(meta.get("days_past_due", 0))
        score = max(0.0, 5.0 - (days_past_due / 6.0))
        if meta.get("payment_blocked"):
            score = min(score, 1.0)
        return min(5.0, score)

    @staticmethod
    def _support_score(meta: dict[str, Any]) -> float:
        # Tickets per week — 0 = 5, 5+ = 0.
        tickets = int(meta.get("support_tickets_week", 0))
        return max(0.0, min(5.0, 5.0 - tickets))

    @staticmethod
    def _engagement_score(
        meta: dict[str, Any],
        outcomes: list[Outcome],
        ref: datetime,
    ) -> float:
        last_engagement = meta.get("last_engagement_at")
        if isinstance(last_engagement, str):
            try:
                last_engagement = datetime.fromisoformat(last_engagement)
            except ValueError:
                last_engagement = None
        recent_outcomes = sum(
            1 for o in outcomes
            if o.kind in {OutcomeKind.MONEY, OutcomeKind.PARTNER}
            and (ref - o.created_at) <= timedelta(days=30)
        )
        score = min(5.0, 2.0 + recent_outcomes)
        if isinstance(last_engagement, datetime):
            gap_days = (ref - last_engagement).days
            score -= gap_days / 30.0
        return max(0.0, min(5.0, score))


__all__ = ["CustomerHealth", "CustomerHealthScorer", "HealthBand"]
