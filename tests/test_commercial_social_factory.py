"""Tests for the Social & Media review-only factory."""

from __future__ import annotations

from dealix.commercial_launch.social import (
    REQUIRED_POST_FIELDS,
    generate_social,
    load_social_config,
    validate_post_invariants,
)


def test_meets_minimum_posts() -> None:
    cfg = load_social_config()
    result = generate_social(seed=1, run_date="2026-01-01")
    assert result.total_accepted >= cfg["total_minimum"]


def test_every_post_has_required_fields() -> None:
    result = generate_social(seed=2, run_date="2026-01-01")
    for p in result.accepted[:40]:
        for f in REQUIRED_POST_FIELDS:
            assert f in p, f"missing {f}"


def test_every_post_is_review_only() -> None:
    result = generate_social(seed=3, run_date="2026-01-01")
    for p in result.accepted:
        assert p["post_allowed"] is False
        assert p["external_post_blocked"] is True
        assert p["requires_founder_approval"] is True
        assert p["status"] == "founder_review"
        assert validate_post_invariants(p) == []


def test_scores_in_range() -> None:
    result = generate_social(seed=4, run_date="2026-01-01")
    for p in result.accepted:
        assert 70 <= p["quality_score"] <= 100
        assert 70 <= p["compliance_score"] <= 100


def test_platform_targets_met() -> None:
    cfg = load_social_config()
    result = generate_social(seed=5, run_date="2026-01-01")
    counts: dict[str, int] = {}
    for p in result.accepted:
        counts[p["platform"]] = counts.get(p["platform"], 0) + 1
    for platform, target in cfg["daily_targets_by_platform"].items():
        assert counts.get(platform, 0) >= target, f"{platform}: {counts.get(platform, 0)} < {target}"


def test_bilingual() -> None:
    result = generate_social(seed=6, run_date="2026-01-01")
    langs = {p["language"] for p in result.accepted}
    assert "ar" in langs and "en" in langs


def test_x_posts_within_length() -> None:
    cfg = load_social_config()
    maxc = next(p["max_chars"] for p in cfg["platforms"] if p["id"] == "x_post")
    result = generate_social(seed=7, run_date="2026-01-01")
    for p in result.accepted:
        if p["platform"] == "x_post":
            assert p["char_count"] <= maxc


def test_no_ad_spend_flag() -> None:
    result = generate_social(seed=8, run_date="2026-01-01")
    for p in result.accepted:
        # never a truthy auto-post/spend flag
        for banned in ("auto_post", "scheduled_post", "api_post", "ad_spend"):
            assert not p.get(banned)


def test_config_blocks_posting_and_spend() -> None:
    cfg = load_social_config()
    gp = cfg["global_policy"]
    assert gp["external_post"] == "BLOCKED"
    assert gp["auto_post"] == "BLOCKED"
    assert gp["ad_spend"] == "BLOCKED"


def test_no_banned_terms_in_accepted() -> None:
    cfg = load_social_config()
    result = generate_social(seed=9, run_date="2026-01-01")
    for p in result.accepted:
        low = p["body"].lower()
        for term in cfg["banned_terms"]:
            assert term.lower() not in low, f"banned term '{term}' in {p['post_id']}"
