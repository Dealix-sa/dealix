"""Draft factory: produces >=400 drafts with the right mix and hard safety flags."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "scripts" / "lib"))

import commercial_generate_400_drafts as gen  # noqa: E402

TEST_DAY = "2099-01-01"


def test_generates_at_least_400():
    drafts = gen.generate(400, TEST_DAY)
    assert len(drafts) >= 400


def test_channel_mix():
    drafts = gen.generate(400, TEST_DAY)
    counts = {c: sum(1 for d in drafts if d["channel"] == c) for c in gen.CHANNEL_MIX}
    assert counts["cold_email"] == 175
    assert counts["follow_up"] == 100
    assert counts["linkedin_manual"] == 75
    assert counts["website_form"] == 50


def test_every_draft_blocks_external_send():
    drafts = gen.generate(400, TEST_DAY)
    for d in drafts:
        assert d["send_allowed"] is False
        assert d["external_send_blocked"] is True
        assert d["requires_founder_approval"] is True
        assert d["no_auto_send"] is True


def test_scaling_above_400():
    drafts = gen.generate(800, TEST_DAY)
    assert len(drafts) == 800
