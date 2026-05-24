"""Follow-up Commander — plans a 3-touch follow-up cadence.

Drafts only — every send must be approved. Cadence is intentionally
simple: day 0, day 3, day 7. We pre-write the messages, vet them, and
attach them to the opportunity.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta, timezone

from dealix.hermes.core.schemas import Opportunity, TrustCheckOutcome
from dealix.hermes.sovereignty import SovereigntyLevel
from dealix.hermes.trust.guardrails import TrustContext, trust_check


@dataclass
class FollowUpStep:
    day_offset: int
    scheduled_at: datetime
    channel: str
    draft: str
    sovereignty_level: SovereigntyLevel
    requires_approval: bool
    blocked_reason: str | None = None


@dataclass
class FollowUpPlan:
    opportunity_id: str
    client_name: str
    steps: list[FollowUpStep]


def _draft_for(step_index: int, client_name: str, offer: str) -> str:
    if step_index == 0:
        return (
            f"{client_name} — sending over the {offer} summary so you can "
            "scan it before our call. Happy to tailor if anything is off."
        )
    if step_index == 1:
        return (
            f"{client_name} — circling back on the {offer} pilot. Is the "
            "scope still the right shape for this quarter?"
        )
    return (
        f"{client_name} — closing the loop on the {offer} thread. If timing "
        "is wrong, no pressure; want me to park it for next quarter?"
    )


def plan_followups(
    opportunity: Opportunity,
    client_name: str,
    offer: str,
    starting_at: datetime | None = None,
    channel: str = "email",
) -> FollowUpPlan:
    start = starting_at or datetime.now(UTC)
    offsets = (0, 3, 7)
    steps: list[FollowUpStep] = []
    for i, offset in enumerate(offsets):
        draft = _draft_for(i, client_name, offer)
        check = trust_check(
            TrustContext(
                target_id=opportunity.id,
                target_kind="message",
                text=draft,
                payload={"price_sar": opportunity.estimated_value_sar},
                action="send_external",
            )
        )
        blocked = (
            "; ".join(check.violations)
            if check.outcome == TrustCheckOutcome.DENY
            else None
        )
        steps.append(
            FollowUpStep(
                day_offset=offset,
                scheduled_at=start + timedelta(days=offset),
                channel=channel,
                draft=draft,
                sovereignty_level=SovereigntyLevel.L4_EXTERNAL_APPROVAL,
                requires_approval=True,
                blocked_reason=blocked,
            )
        )
    return FollowUpPlan(
        opportunity_id=opportunity.id, client_name=client_name, steps=steps
    )
