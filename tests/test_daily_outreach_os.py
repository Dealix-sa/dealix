from pathlib import Path
import os
import shutil
import subprocess
import sys


def test_daily_outreach_generates_drafts_without_live_send():
    test_date = "2099-01-01"

    generated_paths = [
        Path(f"outbox/{test_date}"),
        Path(f"reports/outreach/{test_date}"),
        Path(f"data/outreach/approval_queue/{test_date}"),
    ]

    for path in generated_paths:
        shutil.rmtree(path, ignore_errors=True)

    try:
        result = subprocess.run(
            [
                sys.executable,
                "scripts/outreach/run_daily_outreach.py",
                "--targets",
                "data/outreach/target_accounts.example.csv",
                "--date",
                test_date,
            ],
            text=True,
            capture_output=True,
            check=False,
            env={**os.environ, "PYTHONPATH": "."},
        )

        assert result.returncode == 0, result.stderr
        assert Path(f"outbox/{test_date}/roadlink_email_step1.md").exists()
        assert Path(f"outbox/{test_date}/roadlink_whatsapp_buttons.json").exists()
        assert Path(f"reports/outreach/{test_date}/daily_outreach_summary.md").exists()
        assert Path(f"data/outreach/approval_queue/{test_date}/roadlink_approval.json").exists()
    finally:
        for path in generated_paths:
            shutil.rmtree(path, ignore_errors=True)


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
