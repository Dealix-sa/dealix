"""Founder review report builds all review artifacts (review-only)."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "scripts" / "lib"))

import commercial_founder_review_report as frr  # noqa: E402
import commercial_generate_400_drafts as gen  # noqa: E402
from startup_os_common import output_day_dir, write_jsonl  # noqa: E402

TEST_DAY = "2099-06-01"


def test_review_artifacts_built():
    d = output_day_dir(TEST_DAY)
    write_jsonl(d / "draft_queue.jsonl", gen.generate(400, TEST_DAY))
    frr.run(TEST_DAY)
    for f in ("founder_review.csv", "founder_review.md", "top_50_priority.md",
              "approved_manual_sends.example.csv", "next_actions.md"):
        assert (d / f).exists(), f"missing {f}"


def test_approval_template_defaults_to_not_sent():
    d = output_day_dir(TEST_DAY)
    write_jsonl(d / "draft_queue.jsonl", gen.generate(400, TEST_DAY))
    frr.run(TEST_DAY)
    text = (d / "approved_manual_sends.example.csv").read_text(encoding="utf-8")
    # Header + example rows; every example row marks sent_manually=NO.
    assert "sent_manually" in text
    assert "YES" not in text
