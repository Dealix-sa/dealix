"""The safety audit passes on the real repo and fails on planted violations."""

from __future__ import annotations

import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import commercial_launch_lib as lib  # noqa: E402
import commercial_safety_audit as audit  # noqa: E402


def test_audit_passes_on_repo():
    # Ensure a fresh batch exists so the batch scan has data.
    drafts = lib.generate_drafts(target=400)
    lib.write_outputs(drafts, lib.load_all_config())
    result = audit.run_audit()
    assert result["verdict"] == "PASS", result["code_violations"] + result["batch_violations"]
    assert result["drafts_checked"] >= 400


def test_scan_ignores_prose_mentions(tmp_path):
    # WhatsApp/LinkedIn appearing in config prose must NOT be flagged.
    terms = audit._load_terms()
    code_patterns = terms["import_send_patterns"] + terms["call_send_patterns"]
    # None of the code patterns should be plain prose words.
    assert "whatsapp" not in [p.lower() for p in code_patterns]
    assert "linkedin" not in [p.lower() for p in code_patterns]


def test_forbidden_flag_state_detected(tmp_path, monkeypatch):
    bad = tmp_path / "scripts"
    bad.mkdir(parents=True)
    (bad / "commercial_bad.py").write_text('cfg = {"send_allowed": true}\n'.replace("true", "True").lower(), encoding="utf-8")
    # Write a file literally containing the forbidden flag string.
    (bad / "commercial_bad2.py").write_text('x = \'"send_allowed": true\'\n', encoding="utf-8")
    monkeypatch.setattr(audit, "REPO_ROOT", tmp_path)
    terms = {
        "import_send_patterns": [],
        "call_send_patterns": [],
        "forbidden_flag_states": ['"send_allowed": true'],
        "scan_globs": ["scripts/commercial_*.py"],
        "scan_exclude": [],
    }
    violations = audit._scan_files(terms)
    assert any(v["type"] == "forbidden_flag" for v in violations)


def test_send_code_detected(tmp_path, monkeypatch):
    bad = tmp_path / "scripts"
    bad.mkdir(parents=True)
    (bad / "commercial_bad.py").write_text("import smtplib\nsmtplib.SMTP('x')\n", encoding="utf-8")
    monkeypatch.setattr(audit, "REPO_ROOT", tmp_path)
    terms = {
        "import_send_patterns": ["import smtplib"],
        "call_send_patterns": ["smtplib.smtp"],
        "forbidden_flag_states": [],
        "scan_globs": ["scripts/commercial_*.py"],
        "scan_exclude": [],
    }
    violations = audit._scan_files(terms)
    assert any(v["type"] == "send_code" for v in violations)
