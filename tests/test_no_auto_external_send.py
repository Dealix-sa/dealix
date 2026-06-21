"""Test that no ungated auto external send patterns exist."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_no_auto_external_send_script() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/verify_no_auto_external_send.py"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_outreach_drafts_contain_opt_out() -> None:
    outbox = REPO_ROOT / "outbox"
    if not outbox.exists():
        return
    for path in outbox.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        assert any(word in text.lower() for word in ["إيقاف", "unsubscribe", "stop", "إلغاء"]), (
            f"{path} missing opt-out"
        )


def test_no_send_in_new_revenue_scripts() -> None:
    forbidden = ["send_email(", "send_whatsapp(", "send_sms(", "auto_send = True"]
    for path in (REPO_ROOT / "scripts" / "revenue").glob("*.py"):
        if path.name.startswith("_"):
            continue
        text = path.read_text(encoding="utf-8")
        for pat in forbidden:
            assert pat not in text, f"{path} contains {pat}"
