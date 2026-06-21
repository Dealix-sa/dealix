from pathlib import Path
import os
import subprocess
import sys


def test_daily_outreach_generates_drafts_without_live_send():
    result = subprocess.run(
        [
            sys.executable,
            "scripts/outreach/run_daily_outreach.py",
            "--targets",
            "data/outreach/target_accounts.example.csv",
            "--date",
            "2099-01-01",
        ],
        text=True,
        capture_output=True,
        check=False,
        env={**os.environ, "PYTHONPATH": "."},
    )

    assert result.returncode == 0, result.stderr
    assert Path("outbox/2099-01-01/roadlink_email_step1.md").exists()
    assert Path("outbox/2099-01-01/roadlink_whatsapp_buttons.json").exists()
    assert Path("reports/outreach/2099-01-01/daily_outreach_summary.md").exists()


def test_daily_outreach_whatsapp_blocks_without_opt_in(monkeypatch):
    from app.outreach.policy import can_send_whatsapp

    monkeypatch.setenv("WHATSAPP_SEND_ENABLED", "true")
    monkeypatch.setenv("WHATSAPP_ALLOW_LIVE_SEND", "true")

    row = {
        "company": "X",
        "phone": "+966500000000",
        "whatsapp_opt_in": "false",
        "source_url": "https://example.com",
        "status": "new",
    }

    decision = can_send_whatsapp(row)
    assert decision.allowed is False
    assert "whatsapp_opt_in is not true" in decision.reasons


def test_daily_outreach_email_blocks_without_env(monkeypatch):
    from app.outreach.policy import can_send_email

    monkeypatch.setenv("EMAIL_SEND_ENABLED", "false")

    row = {
        "company": "X",
        "email": "person@example.com",
        "email_opt_in": "true",
        "source_url": "https://example.com",
        "status": "new",
    }

    decision = can_send_email(row)
    assert decision.allowed is False
    assert "EMAIL_SEND_ENABLED is not true" in decision.reasons
