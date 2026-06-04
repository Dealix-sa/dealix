"""Contract: the safety audit detects external-send enablement and code
signatures, and writes a safety report. This file names blocked terms to drive
the detector and is allow-listed in SELF_REFERENTIAL."""

from __future__ import annotations

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[1] / "scripts"))

import commercial_safety_audit as audit


def test_audit_runs_and_reports(tmp_path):
    report = audit.run_audit(date_str="2026-01-02", out_dir=tmp_path)
    assert (tmp_path / "safety_audit.json").exists()
    assert set(["pass", "files_scanned", "violations", "warnings",
                "recommended_fix"]).issubset(report)


def test_clean_repo_passes():
    report = audit.run_audit(date_str="2026-01-02")
    assert report["pass"] is True


def test_enablement_pattern_detects_true_flag():
    import re
    rx = [re.compile(p, re.IGNORECASE) for p in audit.ENABLEMENT_PATTERNS]
    assert any(r.search("send_allowed=true") for r in rx)
    assert any(r.search("external_send_blocked: false") for r in rx)
    assert any(r.search("no_auto_send = false") for r in rx)


def test_code_pattern_detects_smtplib():
    import re
    rx = [re.compile(p, re.IGNORECASE) for p in audit.CODE_PATTERNS]
    assert any(r.search("import smtplib") for r in rx)
    assert any(r.search("client.send_email(to)") for r in rx)


def test_draft_flag_audit_catches_bad_flag(tmp_path):
    # Write a draft_queue with a bad flag and confirm the draft audit catches it.
    import commercial_launch_core as core
    out = core.output_dir_for("2026-01-09")
    out.mkdir(parents=True, exist_ok=True)
    import json
    bad = {"draft_id": "X", "send_allowed": True, "external_send_blocked": True,
           "no_auto_send": True, "requires_founder_approval": True, "status": "founder_review"}
    (out / "draft_queue.jsonl").write_text(json.dumps(bad) + "\n", encoding="utf-8")
    result = audit.audit_drafts("2026-01-09")
    assert result["draft_flag_issues"], "should flag send_allowed True"
    # cleanup
    (out / "draft_queue.jsonl").unlink()
