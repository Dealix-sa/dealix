import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import json
from pathlib import Path
from _v5util import run, ROOT


def test_calendar_generates_and_verifies():
    assert run("media_social_calendar_generate.py").returncode == 0
    assert run("media_social_verify.py").returncode == 0


def test_calendar_is_manual_only():
    cal = json.loads((ROOT / "config" / "media_social_calendar.json").read_text())
    assert len(cal["days"]) >= 30
    assert all(day["auto_post"] is False for day in cal["days"])


def test_ads_seed_not_live():
    ads = json.loads((ROOT / "config" / "ad_campaigns_seed.json").read_text())
    assert ads["live_launch"] is False
    assert ads["status"] == "PLANNING_ONLY"
