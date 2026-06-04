import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import json
from _v5util import ensure_chain


def test_all_expected_output_files_exist():
    d = ensure_chain()
    for name in ["draft_queue.jsonl", "founder_review.csv", "founder_review.md",
                 "top_50_priority.md", "rejected_drafts.jsonl", "needs_research.jsonl",
                 "compliance_report.json", "quality_report.json", "safety_audit.json",
                 "daily_metrics.json", "next_actions.md", "batch_manifest.json",
                 "approved_manual_sends.example.csv"]:
        assert (d / name).exists(), f"missing output {name}"


def test_manifest_safety_flags():
    d = ensure_chain()
    m = json.loads((d / "batch_manifest.json").read_text())
    assert m["safety_flags"]["external_send_blocked"] is True
    assert m["safety_flags"]["send_allowed"] is False
