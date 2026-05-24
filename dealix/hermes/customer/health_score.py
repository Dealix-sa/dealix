"""Customer Health — scores usage, outcome, communication, value."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class CustomerHealth:
    customer_id: str
    usage_score: int
    outcome_score: int
    communication_score: int
    value_score: int
    renewal_risk: str
    upsell_potential: str
    next_action: str


class CustomerHealthScorer:
    def score(
        self,
        *,
        customer_id: str,
        usage_score: int,
        outcome_score: int,
        communication_score: int,
        value_score: int,
        suggested_upsell: str = "AI Governance OS",
    ) -> CustomerHealth:
        avg = (usage_score + outcome_score + communication_score + value_score) / 4
        if avg >= 4.0:
            risk = "low"
            action = "Send monthly value report + propose upsell"
        elif avg >= 3.0:
            risk = "medium"
            action = "Send monthly value report"
        else:
            risk = "high"
            action = "Escalate to Sami — at risk of churn"
        return CustomerHealth(
            customer_id=customer_id,
            usage_score=usage_score,
            outcome_score=outcome_score,
            communication_score=communication_score,
            value_score=value_score,
            renewal_risk=risk,
            upsell_potential=suggested_upsell,
            next_action=action,
        )
