"""Tests for the founder daily action list."""
from __future__ import annotations

import datetime as dt

from auto_client_acquisition.approval_center.approval_store import (
    get_default_approval_store,
)
from auto_client_acquisition.content_os.action_list import build_action_list
from auto_client_acquisition.content_os.drafting import draft_daily_social_posts
from auto_client_acquisition.content_os.queue_bridge import enqueue_social_drafts


def _has_arabic(text: str) -> bool:
    return any("؀" <= ch <= "ۿ" for ch in text)


def test_action_list_is_bilingual_markdown():
    md = build_action_list()
    assert md.lstrip().startswith("#")
    assert "## العربية" in md
    assert "## English" in md
    assert _has_arabic(md)


def test_action_list_contains_all_four_items():
    md = build_action_list()
    # 1. approvals waiting
    assert "موافقات بانتظارك" in md and "Approvals waiting" in md
    # 2. social posts to review
    assert "بوستات سوشل" in md and "Social posts" in md
    # 3. the single number
    assert "الرقم الوحيد" in md and "single number" in md
    # 4. founder hours
    assert "ساعات المؤسس" in md and "Founder hours" in md


def test_action_list_reflects_pending_social_posts():
    store = get_default_approval_store()
    store.clear()
    try:
        assert "جاهزة للمراجعة: **0**" in build_action_list()

        drafts = draft_daily_social_posts(date=dt.date(2026, 5, 17))
        enqueue_social_drafts(drafts)  # default store
        assert f"جاهزة للمراجعة: **{len(drafts)}**" in build_action_list()
    finally:
        store.clear()
