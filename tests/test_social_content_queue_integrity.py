"""Integrity tests for the canonical social content queue."""

from __future__ import annotations

from dealix.commercial_ops.paths import SOCIAL_QUEUE_YAML
from dealix.commercial_ops.social_queue import load_social_queue


def test_social_content_queue_loads_all_28_weeks() -> None:
    data = load_social_queue(SOCIAL_QUEUE_YAML)
    posts = data["posts"]

    assert data["cycle_weeks"] == 28
    assert len(posts) >= 140
    assert {int(post["week"]) for post in posts} == set(range(1, 29))
    assert all((post.get("body_ar") or "").strip() for post in posts)


def test_social_content_queue_has_one_post_per_weekday() -> None:
    posts = load_social_queue(SOCIAL_QUEUE_YAML)["posts"]
    slots = [(int(post["week"]), int(post["day"])) for post in posts]

    assert len(slots) == len(set(slots))
    assert all(day in {0, 1, 2, 3, 4} for _, day in slots)
