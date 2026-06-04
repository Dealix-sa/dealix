"""Commercial Draft Factory — generates 400+ review-only drafts with safe flags."""

from __future__ import annotations

import json

from scripts.commercial_generate_400_drafts import build_outputs
from scripts.commercial_launch_core import (
    ALLOWED_STATUSES,
    FORBIDDEN_STATUSES,
    MANDATORY_FLAGS,
)


def _generate(tmp_path):
    out_dir = tmp_path / "2026-06-04"
    build_outputs(target=400, leads_path=None, run_date="2026-06-04", out_dir=out_dir)
    drafts = [
        json.loads(ln)
        for ln in (out_dir / "draft_queue.jsonl").read_text(encoding="utf-8").splitlines()
        if ln.strip()
    ]
    return out_dir, drafts


def test_generates_at_least_400(tmp_path):
    _, drafts = _generate(tmp_path)
    assert len(drafts) >= 400


def test_every_draft_has_mandatory_safe_flags(tmp_path):
    _, drafts = _generate(tmp_path)
    for d in drafts:
        for flag, expected in MANDATORY_FLAGS.items():
            assert d[flag] is expected, f"{d['draft_id']} {flag}"


def test_statuses_are_allowed_and_never_forbidden(tmp_path):
    _, drafts = _generate(tmp_path)
    for d in drafts:
        assert d["status"] in ALLOWED_STATUSES
        assert d["status"] not in FORBIDDEN_STATUSES


def test_core_output_files_created(tmp_path):
    out_dir, _ = _generate(tmp_path)
    for name in (
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
    ):
        assert (out_dir / name).exists(), name


def test_target_floor_with_placeholder_leads(tmp_path):
    """Even with no real leads, the floor of 400 is met (placeholders → needs_research)."""
    out_dir = tmp_path / "d"
    leads = tmp_path / "empty.jsonl"
    leads.write_text("", encoding="utf-8")
    summary = build_outputs(400, leads, "2026-06-04", out_dir)
    assert summary["total"] >= 400
