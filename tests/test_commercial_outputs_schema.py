"""Founder-facing outputs are written with the expected files and schema."""

from __future__ import annotations

import json
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import commercial_launch_lib as lib  # noqa: E402

EXPECTED_FILES = [
    "draft_queue.jsonl",
    "founder_review.csv",
    "founder_review.md",
    "top_50_priority.md",
    "rejected_drafts.jsonl",
    "needs_research.jsonl",
    "compliance_report.json",
    "quality_report.json",
    "safety_audit.json",
    "daily_metrics.json",
    "next_actions.md",
    "batch_manifest.json",
    "approved_manual_sends.example.csv",
]


def test_outputs_written(tmp_path, monkeypatch):
    monkeypatch.setattr(lib, "OUTPUT_ROOT", tmp_path)
    drafts = lib.generate_drafts(target=400)
    out = lib.write_outputs(drafts, lib.load_all_config(), date="2026-06-04")
    for fname in EXPECTED_FILES:
        assert (out / fname).exists(), f"missing {fname}"


def test_draft_queue_records_safe(tmp_path, monkeypatch):
    monkeypatch.setattr(lib, "OUTPUT_ROOT", tmp_path)
    drafts = lib.generate_drafts(target=400)
    out = lib.write_outputs(drafts, lib.load_all_config(), date="2026-06-04")
    count = 0
    with (out / "draft_queue.jsonl").open(encoding="utf-8") as fh:
        for line in fh:
            rec = json.loads(line)
            count += 1
            assert rec["send_allowed"] is False
            assert rec["no_auto_send"] is True
            assert "_vertical_names" not in rec  # internal helper keys stripped
    assert count >= 400


def test_batch_manifest_schema(tmp_path, monkeypatch):
    monkeypatch.setattr(lib, "OUTPUT_ROOT", tmp_path)
    drafts = lib.generate_drafts(target=400)
    out = lib.write_outputs(drafts, lib.load_all_config(), date="2026-06-04")
    manifest = json.loads((out / "batch_manifest.json").read_text(encoding="utf-8"))
    assert manifest["total"] >= 400
    assert manifest["safety_flags"]["send_allowed"] is False
    assert "golden_rule" in manifest


def test_safety_audit_json_pass(tmp_path, monkeypatch):
    monkeypatch.setattr(lib, "OUTPUT_ROOT", tmp_path)
    drafts = lib.generate_drafts(target=400)
    out = lib.write_outputs(drafts, lib.load_all_config(), date="2026-06-04")
    audit = json.loads((out / "safety_audit.json").read_text(encoding="utf-8"))
    assert audit["verdict"] == "PASS"
    assert audit["all_send_allowed_false"] is True
