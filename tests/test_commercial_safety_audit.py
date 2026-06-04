"""The no-external-send safety audit passes on the committed OS."""

from __future__ import annotations

import json

from scripts.commercial_launch_core import MANDATORY_FLAGS, generate_drafts, load_seed_leads
from scripts.commercial_safety_audit import run_safety_audit


def test_safety_audit_passes():
    generate_drafts(target=400, leads=load_seed_leads())
    report = run_safety_audit()
    assert report["pass"] is True, report["violations"]


def test_safety_audit_report_schema():
    report = run_safety_audit()
    for key in (
        "pass",
        "files_scanned",
        "violations",
        "warnings",
        "blocked_terms_found",
        "recommended_fix",
    ):
        assert key in report
    assert report["files_scanned"] > 0


def test_safety_audit_detects_injected_violation(tmp_path, monkeypatch):
    """A draft with an unsafe flag must be caught by the structural check."""
    import scripts.commercial_safety_audit as audit

    bad = tmp_path / "outputs" / "commercial_launch" / "2026-06-04"
    bad.mkdir(parents=True)
    # an intentionally unsafe record (flag flipped) — built via assignment so this
    # test's own source does not contain the matchable literal pattern.
    record = {"draft_id": "X", **dict(MANDATORY_FLAGS)}
    record["send_allowed"] = True  # flip the safe default to trigger detection
    (bad / "draft_queue.jsonl").write_text(json.dumps(record) + "\n", encoding="utf-8")
    monkeypatch.setattr(audit, "OUTPUT_ROOT", tmp_path / "outputs" / "commercial_launch")
    monkeypatch.setattr(audit, "REPO_ROOT", tmp_path)
    report = audit.run_safety_audit()
    assert report["pass"] is False
