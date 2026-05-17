"""Tests for content_os → approval queue bridge."""
from __future__ import annotations

import datetime as dt

from auto_client_acquisition.approval_center.approval_store import ApprovalStore
from auto_client_acquisition.approval_center.schemas import ApprovalStatus
from auto_client_acquisition.content_os.drafting import draft_daily_social_posts
from auto_client_acquisition.content_os.queue_bridge import enqueue_social_drafts

_FIXED_DATE = dt.date(2026, 5, 17)


def test_enqueue_creates_draft_social_post_requests():
    store = ApprovalStore()
    drafts = draft_daily_social_posts(date=_FIXED_DATE)
    created = enqueue_social_drafts(drafts, store=store)

    assert len(created) == len(drafts)
    for req in created:
        assert req.action_type == "draft_social_post"
        assert req.action_mode == "draft_only"
        assert req.channel == "social"
        assert req.object_type == "social_post"
        assert req.summary_ar.strip()
        assert req.summary_en.strip()
        assert req.risk_level == "low"


def test_enqueued_drafts_are_pending_in_the_store():
    store = ApprovalStore()
    drafts = draft_daily_social_posts(date=_FIXED_DATE)
    enqueue_social_drafts(drafts, store=store)

    pending = store.list_pending()
    assert len(pending) == len(drafts)
    assert all(ApprovalStatus(r.status) == ApprovalStatus.PENDING for r in pending)
    assert all(r.action_type == "draft_social_post" for r in pending)


def test_social_channel_is_not_linkedin():
    """Social posts use channel 'social' — the LinkedIn outreach channel
    hard-blocks stay reserved for actual outreach drafts."""
    store = ApprovalStore()
    enqueue_social_drafts(draft_daily_social_posts(date=_FIXED_DATE), store=store)
    for req in store.list_pending():
        assert req.channel != "linkedin"
