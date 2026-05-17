"""Tests for the content_os social drafting engine."""
from __future__ import annotations

import datetime as dt

from auto_client_acquisition.content_os.drafting import (
    SUPPORTED_PLATFORMS,
    SocialPostDraft,
    draft_daily_social_posts,
)
from auto_client_acquisition.governance_os.policy_check import policy_check_draft

_FIXED_DATE = dt.date(2026, 5, 17)


def test_drafts_one_post_per_platform():
    drafts = draft_daily_social_posts(date=_FIXED_DATE, count=1)
    platforms = {d.platform for d in drafts}
    assert platforms == set(SUPPORTED_PLATFORMS)
    assert all(isinstance(d, SocialPostDraft) for d in drafts)


def test_drafts_are_bilingual():
    drafts = draft_daily_social_posts(date=_FIXED_DATE)
    assert drafts, "expected at least one draft"
    for d in drafts:
        assert d.body_ar.strip(), "Arabic body must be non-empty"
        assert d.body_en.strip(), "English body must be non-empty"
        assert d.locale_primary == "ar"
        # Arabic body must actually contain Arabic script.
        assert any("؀" <= ch <= "ۿ" for ch in d.body_ar)


def test_drafting_is_deterministic_for_a_fixed_date():
    first = draft_daily_social_posts(date=_FIXED_DATE)
    second = draft_daily_social_posts(date=_FIXED_DATE)
    assert [d.to_dict() for d in first] == [d.to_dict() for d in second]


def test_every_draft_passes_governance_pre_check():
    drafts = draft_daily_social_posts(date=_FIXED_DATE)
    for d in drafts:
        verdict = policy_check_draft(f"{d.body_ar}\n{d.body_en}")
        assert verdict.allowed, f"draft tripped governance: {verdict.issues}"


def test_no_draft_contains_forbidden_language():
    drafts = draft_daily_social_posts(date=_FIXED_DATE)
    for d in drafts:
        blob = f"{d.body_ar}\n{d.body_en}".lower()
        assert "linkedin automation" not in blob
        assert "guarantee" not in blob
        assert "نضمن" not in blob
        assert "scrap" not in blob


def test_internal_sources_only():
    drafts = draft_daily_social_posts(date=_FIXED_DATE)
    for d in drafts:
        assert d.internal_sources
        # No external/scraped source labels.
        for src in d.internal_sources:
            assert src in {"content_cadence", "pricing_catalog"}
