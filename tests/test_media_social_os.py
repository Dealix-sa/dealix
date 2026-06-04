"""Media & social OS: 30-day calendar is planning-only, manual posting."""

from __future__ import annotations

import json

from tests._lc_util import REPO_ROOT

from launch_os.media_social import generate_calendar, write_calendar, CHANNELS, PILLARS


def test_calendar_has_30_items():
    cal = generate_calendar(days=30)
    assert len(cal["items"]) == 30


def test_calendar_is_manual_only():
    cal = generate_calendar(days=30)
    assert cal["auto_post_enabled"] is False
    assert cal["publish_method"] == "manual_only"
    for item in cal["items"]:
        assert item["auto_post"] is False
        assert item["requires_founder_approval"] is True
        assert item["publish_method"] == "manual_only"


def test_calendar_covers_channels_and_pillars():
    cal = generate_calendar(days=30)
    used_channels = {i["channel"] for i in cal["items"]}
    used_pillars = {i["pillar"] for i in cal["items"]}
    assert used_channels == set(CHANNELS)
    assert used_pillars == {p["key"] for p in PILLARS}


def test_write_calendar(tmp_path):
    path = write_calendar(generate_calendar(), tmp_path)
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["auto_post_enabled"] is False


def test_config_file_is_manual_only():
    cfg = json.loads((REPO_ROOT / "config" / "media_social_calendar.json").read_text(encoding="utf-8"))
    assert cfg["auto_post_enabled"] is False
    assert cfg["publish_method"] == "manual_only"
