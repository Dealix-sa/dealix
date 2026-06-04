"""Media & Social OS: calendar generation, verification, and no auto-post."""

from __future__ import annotations

import media_social_calendar_generate as cal
import media_social_verify as verify
from _commercial_common import load_config
from _launch_util import ROOT


def test_calendar_generates_30_days():
    calendar = cal.generate("2099-01-01")
    assert calendar["days"] == 30
    assert len(calendar["items"]) == 30
    assert calendar["auto_post"] is False
    for item in calendar["items"]:
        assert item["auto_post"] is False
        assert item["hook_en"] and item["hook_ar"]


def test_media_verify_passes():
    assert verify.verify() == []


def test_calendar_config_no_auto_post():
    cfg = load_config("media_social_calendar.json")
    assert cfg["auto_post"] is False


def test_ads_are_plan_only():
    ads = load_config("ad_campaigns_seed.json")
    assert ads["live_launch_allowed"] is False
    assert ads["launch_no_go_conditions"]
