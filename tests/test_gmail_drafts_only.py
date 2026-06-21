"""Test that Gmail adapter creates drafts only, never sends."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_gmail_draft_script_dry_run() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/email/create_gmail_drafts_safe.py", "--outbox-dir", "outbox/2026-06-15"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "DRY-RUN" in result.stdout
    assert "No drafts created" in result.stdout


def test_gmail_script_has_no_send_call() -> None:
    path = REPO_ROOT / "scripts" / "email" / "create_gmail_drafts_safe.py"
    text = path.read_text(encoding="utf-8")
    # The safe adapter must never call a send function directly.
    assert "send_email(" not in text
    assert "GMAIL_SEND_URL" not in text
    # It must call create_draft only.
    assert "create_draft" in text
