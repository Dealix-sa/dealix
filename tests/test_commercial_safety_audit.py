"""Tests for the Commercial Launch safety audit."""

from __future__ import annotations

import json
from pathlib import Path

from dealix.commercial_launch.engine import generate_drafts, write_outputs
from dealix.commercial_launch.safety import (
    audit_outputs_dir,
    scan_files,
    write_safety_audit,
)


def test_source_scan_is_clean() -> None:
    report = scan_files()
    assert report.passed, [f.__dict__ for f in report.findings]
    assert report.scanned_files > 0


def test_scan_detects_active_send(tmp_path: Path) -> None:
    # Build a fake repo layout with an offending script.
    (tmp_path / "scripts").mkdir()
    (tmp_path / "dealix" / "commercial_launch").mkdir(parents=True)
    bad = tmp_path / "scripts" / "commercial_bad.py"
    # Construct the offending token at runtime so this test file itself is clean.
    token = "smtp" + "lib"
    bad.write_text(f"import {token}\n", encoding="utf-8")
    report = scan_files(tmp_path)
    assert report.passed is False
    assert any(f.rule == "smtp_client" for f in report.findings)


def test_scan_detects_send_allowed_true(tmp_path: Path) -> None:
    (tmp_path / "dealix" / "commercial_launch").mkdir(parents=True)
    bad = tmp_path / "dealix" / "commercial_launch" / "x.py"
    bad.write_text('cfg = {"send_allowed": True}\n', encoding="utf-8")
    report = scan_files(tmp_path)
    assert report.passed is False
    assert any(f.rule == "send_allowed_true" for f in report.findings)


def test_allow_marker_is_respected(tmp_path: Path) -> None:
    (tmp_path / "dealix" / "commercial_launch").mkdir(parents=True)
    f = tmp_path / "dealix" / "commercial_launch" / "x.py"
    token = "smtp" + "lib"
    f.write_text(f"import {token}  # safety-audit-allow\n", encoding="utf-8")
    report = scan_files(tmp_path)
    assert report.passed is True


def test_audit_outputs_dir_passes_on_generated(tmp_path: Path) -> None:
    result = generate_drafts(target=400, seed=11, run_date="2026-01-02")
    write_outputs(result, base_dir=tmp_path)
    report = audit_outputs_dir("2026-01-02", base_dir=tmp_path)
    assert report.drafts_checked >= 400
    assert report.passed, report.draft_violations
    out = write_safety_audit(report, "2026-01-02", base_dir=tmp_path)
    data = json.loads(Path(out).read_text(encoding="utf-8"))
    assert data["passed"] is True


def test_audit_detects_tampered_draft(tmp_path: Path) -> None:
    result = generate_drafts(target=400, seed=12, run_date="2026-01-03")
    # Tamper: flip one draft to allow sending.
    result.accepted[0]["send_allowed"] = True
    result.accepted[0]["external_send_blocked"] = False
    write_outputs(result, base_dir=tmp_path)
    report = audit_outputs_dir("2026-01-03", base_dir=tmp_path)
    assert report.passed is False
    assert report.draft_violations
