"""خادم المال — FollowUpScheduler.

Computes when and how to follow up on a given Opportunity. Pure
function — no scheduling side effects. The caller is expected to
hand the resulting FollowUpAction off to the trust queue.
"""

from __future__ import annotations

from datetime import datetime, timedelta

from pydantic import BaseModel, ConfigDict, Field

from dealix.hermes.core.opportunities import Opportunity, OpportunityType
from dealix.hermes.core.schemas import utcnow


class FollowUpAction(BaseModel):
    """A scheduled next-touch with the buyer."""

    model_config = ConfigDict(extra="forbid")

    channel: str = Field(..., min_length=1, max_length=64)
    send_at: datetime
    draft_template_id: str = Field(..., min_length=1, max_length=128)
    requires_approval: bool = True
    rationale: str = Field(..., min_length=1, max_length=400)


# ─────────────────────────────────────────────────────────────
# Scheduler
# ─────────────────────────────────────────────────────────────


_TEMPLATE_BY_TYPE: dict[OpportunityType, str] = {
    OpportunityType.REVENUE: "tpl_revenue_followup_v1",
    OpportunityType.PARTNER: "tpl_partner_followup_v1",
    OpportunityType.PRODUCT: "tpl_product_followup_v1",
    OpportunityType.KNOWLEDGE: "tpl_knowledge_followup_v1",
    OpportunityType.RISK_AVOIDANCE: "tpl_risk_followup_v1",
}

# Forbidden channels — Dealix never schedules these (carry-over guard).
_FORBIDDEN_CHANNELS: frozenset[str] = frozenset({"cold_whatsapp", "linkedin_dm"})


class FollowUpScheduler:
    """Compute the next follow-up action for an opportunity."""

    def next_action(
        self,
        opportunity: Opportunity,
        last_touch_at: datetime | None = None,
    ) -> FollowUpAction:
        baseline = last_touch_at or utcnow()
        wait_hours = self._wait_hours(opportunity)
        send_at = baseline + timedelta(hours=wait_hours)
        channel = self._channel_for(opportunity)
        if channel in _FORBIDDEN_CHANNELS:
            raise ValueError(f"forbidden follow-up channel: {channel}")
        template = _TEMPLATE_BY_TYPE.get(
            opportunity.opp_type,
            "tpl_generic_followup_v1",
        )
        rationale = (
            f"urgency={opportunity.urgency}, fit={opportunity.fit_score}, "
            f"opp_type={opportunity.opp_type.value} → wait {wait_hours}h, "
            f"channel={channel}"
        )
        # External channels always require an approval ticket per doctrine.
        requires_approval = channel != "internal_note"
        return FollowUpAction(
            channel=channel,
            send_at=send_at,
            draft_template_id=template,
            requires_approval=requires_approval,
            rationale=rationale,
        )

    @staticmethod
    def _wait_hours(opportunity: Opportunity) -> int:
        # Higher urgency → shorter wait. Map urgency 1..5 → 96..6 hours.
        urgency = max(1, min(5, opportunity.urgency))
        return {1: 96, 2: 48, 3: 24, 4: 12, 5: 6}[urgency]

    @staticmethod
    def _channel_for(opportunity: Opportunity) -> str:
        # Sensitive signals get reviewed internally first.
        if opportunity.sensitive:
            return "internal_note"
        if opportunity.opp_type == OpportunityType.RISK_AVOIDANCE:
            return "internal_note"
        if opportunity.opp_type == OpportunityType.KNOWLEDGE:
            return "email"
        return "email"


__all__ = ["FollowUpAction", "FollowUpScheduler"]
