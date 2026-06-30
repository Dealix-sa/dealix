"""Media/social OS: 30-day calendar, planning-only, no auto-post."""
import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
CAL = REPO / "outputs" / "media_social" / "calendar_30_day.json"


@pytest.fixture(scope="module", autouse=True)
def _gen():
    subprocess.run([sys.executable, str(REPO / "scripts" / "media_social_calendar_generate.py")],
                   check=True, cwd=REPO)


def test_thirty_days():
    cal = json.loads(CAL.read_text(encoding="utf-8"))
    assert cal["total_days"] == 30
    assert len(cal["days"]) == 30


def test_auto_post_disabled():
    cal = json.loads(CAL.read_text(encoding="utf-8"))
    assert cal["auto_post"] is False
    for day in cal["days"]:
        assert day["auto_post"] is False


def test_ads_not_live():
    cal = json.loads(CAL.read_text(encoding="utf-8"))
    assert cal["ads"]["live_launch_allowed"] is False
