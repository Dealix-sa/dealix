"""The draft factory produces 400+ review-only drafts with correct distribution."""

from __future__ import annotations

import commercial_generate_400_drafts as gen
from _launch_util import SEED, TEST_DAY


def _result():
    return gen.generate(target=400, day=TEST_DAY, seed_path=SEED)


def test_at_least_400_drafts():
    drafts = _result()["drafts"]
    assert len(drafts) >= 400


def test_channel_distribution():
    drafts = _result()["drafts"]
    by_channel: dict[str, int] = {}
    for d in drafts:
        by_channel[d["channel"]] = by_channel.get(d["channel"], 0) + 1
    assert by_channel["cold_email"] == 175
    assert by_channel["follow_up"] == 100
    assert by_channel["linkedin_manual"] == 75
    assert by_channel["website_contact_form"] == 50


def test_every_draft_has_required_fields():
    from _commercial_common import load_config

    required = load_config("commercial_quality_gates.json")["required_fields"]
    for d in _result()["drafts"]:
        for field in required:
            assert field in d, f"missing {field}"


def test_write_outputs_creates_files(tmp_path):
    result = _result()
    gen.write_outputs(result, tmp_path)
    for name in [
        "draft_queue.jsonl",
        "founder_review.csv",
        "founder_review.md",
        "top_50_priority.md",
        "rejected_drafts.jsonl",
        "needs_research.jsonl",
        "compliance_report.json",
        "quality_report.json",
        "daily_metrics.json",
        "next_actions.md",
        "batch_manifest.json",
        "approved_manual_sends.example.csv",
    ]:
        assert (tmp_path / name).exists(), name


def test_drafts_are_ranked_and_scored():
    for d in _result()["drafts"]:
        assert 0 <= d["quality_score"] <= 100
        assert 0 <= d["compliance_score"] <= 100
        assert d["risk_level"] in {"low", "medium", "high"}
