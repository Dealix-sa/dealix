"""Contract: writing outputs creates the daily review pack with a stable schema."""

from __future__ import annotations

import csv
import json

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[1] / "scripts"))

import commercial_launch_core as core

# Isolate all runtime writes to a unique temp dir so parallel (-n auto) test
# workers never race on or pollute the repo's outputs/ tree.
import tempfile as _tempfile
import commercial_launch_core as _clc_isolate
_clc_isolate.OUTPUT_ROOT = _Path(_tempfile.mkdtemp(prefix='cl_test_out_'))

DATE = "2026-01-05"


def _build_outputs():
    cfg = core.load_all_configs()
    drafts = core.generate_drafts(target=400, leads=core.load_seed_leads(),
                                  configs=cfg, date_str=DATE)
    out = core.write_outputs(drafts, cfg, DATE)
    return out, drafts


def test_required_output_files_exist():
    out, _ = _build_outputs()
    for name in [
        "draft_queue.jsonl", "founder_review.csv", "founder_review.md",
        "top_50_priority.md", "rejected_drafts.jsonl", "needs_research.jsonl",
        "compliance_report.json", "quality_report.json", "daily_metrics.json",
        "next_actions.md", "batch_manifest.json",
    ]:
        assert (out / name).exists(), f"missing output {name}"


def test_draft_queue_schema_is_stable():
    out, _ = _build_outputs()
    with (out / "draft_queue.jsonl").open(encoding="utf-8") as fh:
        for line in fh:
            d = json.loads(line)
            assert list(d.keys()) == core.DRAFT_FIELDS
            assert d["send_allowed"] is False
            assert d["external_send_blocked"] is True


def test_founder_review_md_has_sections():
    out, _ = _build_outputs()
    text = (out / "founder_review.md").read_text(encoding="utf-8")
    for marker in ["Executive summary", "Top 50 priority", "Go / No-Go by channel",
                   "Rejection reasons"]:
        assert marker in text


def test_top_50_is_present_and_capped():
    out, _ = _build_outputs()
    text = (out / "top_50_priority.md").read_text(encoding="utf-8")
    # headings like "## 1." ... at most 50
    count = text.count("\n## ")
    assert 0 < count <= 50


def test_metrics_report_consistent():
    out, drafts = _build_outputs()
    metrics = json.loads((out / "daily_metrics.json").read_text(encoding="utf-8"))
    assert metrics["drafts_generated"] == len(drafts)
    assert metrics["all_send_blocked"] is True
    assert metrics["all_send_disallowed"] is True


def test_founder_csv_parses():
    out, _ = _build_outputs()
    with (out / "founder_review.csv").open(encoding="utf-8") as fh:
        rows = list(csv.reader(fh))
    assert rows[0][0] == "rank"
    assert len(rows) >= 1
