"""Media & Social OS produces a 30-day plan and never auto-publishes."""

from __future__ import annotations

import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
ROOT = Path(__file__).resolve().parents[1]
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import media_social_calendar_generate as cal  # noqa: E402


def test_calendar_has_30_days():
    calendar = cal.build_calendar()
    assert len(calendar) == 30


def test_calendar_is_bilingual_and_no_autopublish():
    calendar = cal.build_calendar()
    for item in calendar:
        assert item["post_ar"]
        assert item["post_en"]
        assert item["auto_publish"] is False
        assert item["platform"] in {"linkedin", "x", "instagram", "tiktok", "youtube_shorts"}


def test_media_os_docs_exist():
    for doc in [
        "docs/media-social-os/00_MEDIA_SOCIAL_OS.md",
        "docs/media-social-os/03_30_DAY_CONTENT_CALENDAR.md",
        "docs/media-social-os/10_ADS_OS.md",
    ]:
        assert (ROOT / doc).exists(), f"missing {doc}"


def test_ads_config_does_not_autolaunch():
    import json

    ads = json.loads((ROOT / "config" / "ad_campaigns_seed.json").read_text(encoding="utf-8"))
    assert "No paid ads are launched" in ads["note"]
