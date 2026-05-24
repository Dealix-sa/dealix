"""Tests for `dealix.money.followup.FollowUpScheduler`."""

from __future__ import annotations

from datetime import datetime, timedelta

from dealix.hermes.core.opportunities import Opportunity, OpportunityType
from dealix.hermes.core.schemas import utcnow
from dealix.money.followup import FollowUpScheduler


def _opp(urgency: int, **kwargs) -> Opportunity:
    return Opportunity(
        signal_id="sig_f",
        opp_type=kwargs.pop("opp_type", OpportunityType.REVENUE),
        title="t",
        narrative="n",
        urgency=urgency,
        fit_score=3,
        sensitive=kwargs.pop("sensitive", False),
    )


def test_next_action_for_high_urgency_picks_short_wait_email() -> None:
    scheduler = FollowUpScheduler()
    last = utcnow()
    action = scheduler.next_action(_opp(urgency=5), last_touch_at=last)
    assert action.channel == "email"
    # Urgency 5 → 6 hours.
    assert (action.send_at - last) == timedelta(hours=6)
    assert action.requires_approval is True
    assert action.draft_template_id


def test_next_action_for_sensitive_opportunity_picks_internal_note() -> None:
    scheduler = FollowUpScheduler()
    action = scheduler.next_action(_opp(urgency=3, sensitive=True))
    assert action.channel == "internal_note"
    assert action.requires_approval is False


def test_next_action_for_low_urgency_picks_long_wait() -> None:
    scheduler = FollowUpScheduler()
    last = utcnow()
    action = scheduler.next_action(_opp(urgency=1), last_touch_at=last)
    assert (action.send_at - last) == timedelta(hours=96)
