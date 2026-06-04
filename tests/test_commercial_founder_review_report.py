"""Founder review report summarizes the draft queue and writes a digest."""

from __future__ import annotations

from scripts.commercial_founder_review_report import summarize, write_report
from scripts.commercial_launch_core import generate_drafts, load_seed_leads, strip_internal


def _drafts():
    result = generate_drafts(target=400, leads=load_seed_leads())
    return [strip_internal(d) for d in result.drafts]


def test_summarize_shape():
    summary = summarize(_drafts())
    assert summary["total"] >= 400
    assert len(summary["top_50_ids"]) <= 50
    assert "by_status" in summary
    assert "by_channel" in summary


def test_write_report_creates_file(tmp_path):
    path = write_report(_drafts(), tmp_path)
    assert path.exists()
    text = path.read_text(encoding="utf-8")
    assert "Founder Review Report" in text
    assert "No external sending" in text
