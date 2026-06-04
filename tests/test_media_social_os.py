"""Media/social calendar generates 30+ bilingual items with no auto-post."""

from __future__ import annotations

import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "scripts" / "lib"))

import media_social_calendar_generate as mscg  # noqa: E402
import media_social_verify as msv  # noqa: E402


def test_calendar_has_30_items():
    cal = mscg.generate(date(2026, 1, 1), 30)
    assert len(cal["calendar"]) == 30
    assert cal["_meta"]["auto_post"] is False


def test_calendar_items_bilingual_and_no_autopost():
    cal = mscg.generate(date(2026, 1, 1), 30)
    for it in cal["calendar"]:
        assert it["hook_ar"] and it["hook_en"]
        assert it["body_ar"] and it["body_en"]
        assert it["auto_post"] is False
        assert it["requires_founder_approval"] is True


def test_verify_passes():
    # Ensure the on-disk calendar verifies (regenerates if needed).
    assert msv.verify() == []
