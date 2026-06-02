"""Tests for scripts/dealix_morning_digest.py (P4)."""
from __future__ import annotations

import asyncio
import importlib.util
import sys
from datetime import UTC, datetime
from pathlib import Path
from unittest.mock import AsyncMock, patch

import pytest

REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / "scripts" / "dealix_morning_digest.py"
sys.path.insert(0, str(REPO))


def _load():
    spec = importlib.util.spec_from_file_location(
        "dealix_morning_digest", str(SCRIPT)
    )
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


digest = _load()


def test_subject_includes_today():
    today = datetime.now(UTC).strftime("%Y-%m-%d")
    assert today in digest._build_subject()


def test_print_only_mode_writes_to_stdout(capsys):
    sys.argv = ["dealix_morning_digest.py", "--print"]
    args = digest.parse_args()

    fake_loop = {
        "schema_version": 1,
        "generated_at": "2026-05-04T07:00:00+00:00",
        "decisions": [{"title_ar": "tester", "title_en": "tester"}],
        "service_to_promote": {},
        "partner_focus": {},
        "seo_gap_pages": [],
        "perimeter_status": {},
        "open_loops": [],
        "guardrails": {
            "no_live_send": True,
            "no_scraping": True,
            "no_cold_outreach": True,
            "approval_required_for_external_actions": True,
        },
    }
    with patch.object(digest.daily_growth_loop, "build_today", return_value=fake_loop):
        result = asyncio.run(digest._build_and_send(args))

    out = capsys.readouterr().out
    assert "Daily Growth Loop" in out
    assert result.success is True
    assert result.provider == "print_only"


def test_dry_run_logs_but_does_not_send(capsys):
    sys.argv = ["dealix_morning_digest.py", "--dry-run"]
    args = digest.parse_args()

    with patch.object(digest, "EmailClient") as MockClient:
        instance = MockClient.return_value
        instance.send = AsyncMock(side_effect=AssertionError("must not send in dry-run"))
        result = asyncio.run(digest._build_and_send(args))

    out = capsys.readouterr().out
    assert "[dry-run]" in out
    assert result.success is True
    assert result.provider == "dry_run"
    # Verify the mock was NEVER called
    instance.send.assert_not_called()


def test_send_mode_calls_email_client():
    sys.argv = ["dealix_morning_digest.py"]
    args = digest.parse_args()

    captured = {}

    async def _capture(**kwargs):
        captured.update(kwargs)
        from integrations.email import EmailResult
        return EmailResult(success=True, provider="resend", message_id="msg_1")

    with patch.object(digest, "EmailClient") as MockClient:
        instance = MockClient.return_value
        instance.send = AsyncMock(side_effect=_capture)
        result = asyncio.run(digest._build_and_send(args))

    assert result.success is True
    assert result.provider == "resend"
    # Subject contains today's date
    today = datetime.now(UTC).strftime("%Y-%m-%d")
    assert today in captured["subject"]
    # Body is the markdown digest
    assert "Daily Growth Loop" in captured["body_text"]
    # Contains key sections per to_markdown()
    assert "Hard guardrails" in captured["body_text"]
    # Recipient is the founder, never anyone else
    assert captured["to"] == "sami.assiri11@gmail.com"


def test_no_recipient_returns_failure(monkeypatch):
    """If DEALIX_FOUNDER_EMAIL is empty AND not in dry-run/print-only,
    return an explicit failure rather than sending blindly."""
    sys.argv = ["dealix_morning_digest.py"]
    args = digest.parse_args()

    with patch.object(digest, "get_settings") as mock_get:
        mock_settings = type("S", (), {})()
        mock_settings.dealix_founder_email = ""
        mock_settings.email_provider = "resend"
        mock_get.return_value = mock_settings
        result = asyncio.run(digest._build_and_send(args))

    assert result.success is False
    assert "founder_email_not_configured" in (result.error or "")


def test_workflow_file_exists_and_has_correct_cron():
    # Consolidated into the single founder-daily workflow (offline brief,
    # no external send). The standalone daily_digest.yml was removed when the
    # ~19 founder ops workflows were folded into founder-daily / founder-weekly.
    workflow = REPO / ".github" / "workflows" / "founder-daily.yml"
    assert workflow.exists()
    text = workflow.read_text(encoding="utf-8")
    # 05:00 UTC Sun-Thu = ~08:00 KSA
    assert 'cron: "0 5 * * 0-4"' in text
    # Calls the unified runner with python3 (never the Windows py -3 launcher)
    assert "python3 scripts/run_dealix_complete_autonomous_day.py" in text
    assert "py -3" not in text
    # Has manual trigger too
    assert "workflow_dispatch" in text
