"""Next-action recommender — decides what draft to queue next per prospect.

Doctrine:
  - Output is a RECOMMENDATION, not an action
  - Recommended drafts go to approval_center (Doctrine #1)
  - Founder approves + sends manually
  - Decision logic transparent (every recommendation cites the rule)

State machine:
  prospect_state + days_in_state + buying_intent + sequence_progress
  → NextActionRecommendation

Recommendation outputs:
  - send_touch_2: queue Touch 2 draft (Day 3 nudge)
  - send_touch_3: queue Touch 3 draft (Day 7 decision)
  - send_demo_invite: high intent + no demo yet
  - send_proposal_draft: demo done + 48h silence
  - send_decision_moment: proposal sent + 72h silence
  - move_to_nurture: 14+ days silence + no signal
  - schedule_followup_call: replied positive
  - no_action: cooling period (90-day nurture)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any


@dataclass
class NextActionRecommendation:
    prospect_brief_id: str
    recommended_action: str
    reason: str
    confidence: str  # "high" | "medium" | "low"
    suggested_channel: str | None = None
    suggested_offer: str | None = None
    computed_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())
    doctrine_note: str = "Recommendation only. Founder approves before any send."

    def to_dict(self) -> dict[str, Any]:
        return {
            "prospect_brief_id": self.prospect_brief_id,
            "recommended_action": self.recommended_action,
            "reason": self.reason,
            "confidence": self.confidence,
            "suggested_channel": self.suggested_channel,
            "suggested_offer": self.suggested_offer,
            "computed_at": self.computed_at,
            "doctrine_note": self.doctrine_note,
        }


def recommend_next_action(
    *,
    prospect_brief_id: str,
    current_state: str,  # "touch_1_sent" | "touch_2_sent" | "touch_3_sent" |
                          # "replied" | "demo_booked" | "demo_done" |
                          # "proposal_sent" | "stalled" | "nurture"
    days_in_state: int,
    buying_intent_score: int = 0,
    sequence_progress: int = 1,  # which touch is the prospect on
) -> NextActionRecommendation:
    """Apply decision rules to recommend next action."""

    # Rule 1: high intent + no demo → push demo invite
    if buying_intent_score >= 70 and current_state != "demo_booked":
        return NextActionRecommendation(
            prospect_brief_id=prospect_brief_id,
            recommended_action="send_demo_invite",
            reason=f"Buying intent score {buying_intent_score} (>=70). Send demo invite immediately.",
            confidence="high",
            suggested_channel="email",
        )

    # Rule 2: replied positive → schedule call
    if current_state == "replied":
        return NextActionRecommendation(
            prospect_brief_id=prospect_brief_id,
            recommended_action="schedule_followup_call",
            reason="Prospect replied positively. Schedule 15-min call within 24h.",
            confidence="high",
            suggested_channel="same_as_reply_channel",
        )

    # Rule 3: demo done + 48h silence → send proposal
    if current_state == "demo_done" and days_in_state >= 2:
        return NextActionRecommendation(
            prospect_brief_id=prospect_brief_id,
            recommended_action="send_proposal_draft",
            reason=f"Demo completed {days_in_state} days ago, no follow-up. Send proposal.",
            confidence="high",
            suggested_offer="from_sector_brief",
        )

    # Rule 4: proposal sent + 72h silence → decision moment
    if current_state == "proposal_sent" and days_in_state >= 3:
        return NextActionRecommendation(
            prospect_brief_id=prospect_brief_id,
            recommended_action="send_decision_moment",
            reason=f"Proposal sent {days_in_state} days ago, no response. Use Touch 3 pattern.",
            confidence="medium",
            suggested_channel="email",
        )

    # Rule 5: touch 1 sent, no reply, day 3 → queue touch 2
    if current_state == "touch_1_sent" and days_in_state >= 2 and sequence_progress < 2:
        return NextActionRecommendation(
            prospect_brief_id=prospect_brief_id,
            recommended_action="send_touch_2",
            reason="Touch 1 sent 3+ days ago. Queue Day-3 value-add nudge.",
            confidence="medium",
            suggested_channel="same_as_touch_1",
        )

    # Rule 6: touch 2 sent, no reply, day 7 → queue touch 3
    if current_state == "touch_2_sent" and days_in_state >= 4 and sequence_progress < 3:
        return NextActionRecommendation(
            prospect_brief_id=prospect_brief_id,
            recommended_action="send_touch_3",
            reason="Touch 2 sent 4+ days ago. Queue Day-7 decision moment.",
            confidence="medium",
            suggested_channel="same_as_touch_2",
        )

    # Rule 7: 14+ days silence with no signal → nurture
    if days_in_state >= 14 and buying_intent_score < 30:
        return NextActionRecommendation(
            prospect_brief_id=prospect_brief_id,
            recommended_action="move_to_nurture",
            reason=f"{days_in_state} days silence, intent {buying_intent_score}. 90-day cooldown.",
            confidence="high",
        )

    # Default: no action — let cool
    return NextActionRecommendation(
        prospect_brief_id=prospect_brief_id,
        recommended_action="no_action",
        reason="In cooling period. No recommendation today.",
        confidence="medium",
    )


__all__ = [
    "NextActionRecommendation",
    "recommend_next_action",
]
