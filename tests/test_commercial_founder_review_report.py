"""Founder review report renders the executive summary and top-50 queue."""

from __future__ import annotations

import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import commercial_launch_lib as lib  # noqa: E402


def test_founder_md_has_sections(tmp_path, monkeypatch):
    monkeypatch.setattr(lib, "OUTPUT_ROOT", tmp_path)
    drafts = lib.generate_drafts(target=400)
    out = lib.write_outputs(drafts, lib.load_all_config(), date="2026-06-04")
    md = (out / "founder_review.md").read_text(encoding="utf-8")
    for heading in [
        "## Executive Summary",
        "## Channel Distribution",
        "## Vertical Distribution",
        "## Language Distribution",
        "## Top 10 Highest-Value Opportunities",
        "## Go / No-Go by Channel",
    ]:
        assert heading in md, f"missing {heading}"


def test_top_50_has_ranked_entries(tmp_path, monkeypatch):
    monkeypatch.setattr(lib, "OUTPUT_ROOT", tmp_path)
    drafts = lib.generate_drafts(target=400)
    out = lib.write_outputs(drafts, lib.load_all_config(), date="2026-06-04")
    top = (out / "top_50_priority.md").read_text(encoding="utf-8")
    assert "## 1." in top
    assert "Manual action:" in top
    assert "Draft preview:" in top


def test_review_csv_ranked(tmp_path, monkeypatch):
    import csv

    monkeypatch.setattr(lib, "OUTPUT_ROOT", tmp_path)
    drafts = lib.generate_drafts(target=400)
    out = lib.write_outputs(drafts, lib.load_all_config(), date="2026-06-04")
    with (out / "founder_review.csv").open(encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    assert rows
    scores = [float(r["priority_score"]) for r in rows]
    assert scores == sorted(scores, reverse=True)
