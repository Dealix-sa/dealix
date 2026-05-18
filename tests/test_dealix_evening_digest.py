"""Tests for scripts/dealix_evening_digest.py (WS-E).

Covers the close-of-day founder digest glue script: subject formatting,
digest composition (reusing the scorecard), and the print/dry-run/send
paths. Asserts the evening digest emails the founder only.
"""
from __future__ import annotations

import asyncio
import importlib.util
import sys
from datetime import UTC, datetime
from pathlib import Path
from unittest.mock import AsyncMock, patch

REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / "scripts" / "dealix_evening_digest.py"
sys.path.insert(0, str(REPO))


def _load():
    spec = importlib.util.spec_from_file_location(
        "dealix_evening_digest", str(SCRIPT)
    )
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


digest = _load()


def test_subject_includes_today():
    today = datetime.now(UTC).strftime("%Y-%m-%d")
    assert today in digest._build_subject()


def test_build_evening_digest_contains_required_sections():
    with patch.object(digest, "_run_scorecard", return_value="(stub scorecard)"):
        text = digest.build_evening_digest()
    assert "Evening Digest" in text
    assert "Close-of-day scorecard" in text
    assert "(stub scorecard)" in text
    # Doctrine: nothing was auto-sent.
    assert "nothing was auto-sent" in text
    # Mentions tomorrow's setup.
    assert "Tomorrow" in text


def test_print_only_mode(capsys):
    sys.argv = ["dealix_evening_digest.py", "--print"]
    args = digest.parse_args()
    with patch.object(digest, "build_evening_digest", return_value="# evening body"):
        result = asyncio.run(digest._build_and_send(args))
    out = capsys.readouterr().out
    assert "# evening body" in out
    assert result.success is True
    assert result.provider == "print_only"


def test_dry_run_does_not_send():
    sys.argv = ["dealix_evening_digest.py", "--dry-run"]
    args = digest.parse_args()
    with patch.object(digest, "build_evening_digest", return_value="# body"), \
         patch.object(digest, "EmailClient") as MockClient:
        instance = MockClient.return_value
        instance.send = AsyncMock(side_effect=AssertionError("must not send in dry-run"))
        result = asyncio.run(digest._build_and_send(args))
    assert result.success is True
    assert result.provider == "dry_run"
    instance.send.assert_not_called()


def test_send_mode_emails_founder_only():
    sys.argv = ["dealix_evening_digest.py"]
    args = digest.parse_args()
    captured = {}

    async def _capture(**kwargs):
        captured.update(kwargs)
        from integrations.email import EmailResult
        return EmailResult(success=True, provider="resend", message_id="m1")

    with patch.object(digest, "build_evening_digest", return_value="# body"), \
         patch.object(digest, "EmailClient") as MockClient:
        instance = MockClient.return_value
        instance.send = AsyncMock(side_effect=_capture)
        result = asyncio.run(digest._build_and_send(args))

    assert result.success is True
    # Recipient is the founder, never a prospect.
    assert captured["to"] == "sami.assiri11@gmail.com"
    today = datetime.now(UTC).strftime("%Y-%m-%d")
    assert today in captured["subject"]


def test_no_recipient_returns_failure():
    sys.argv = ["dealix_evening_digest.py"]
    args = digest.parse_args()
    with patch.object(digest, "get_settings") as mock_get:
        mock_settings = type("S", (), {})()
        mock_settings.dealix_founder_email = ""
        mock_settings.email_provider = "resend"
        mock_get.return_value = mock_settings
        result = asyncio.run(digest._build_and_send(args))
    assert result.success is False
    assert "founder_email_not_configured" in (result.error or "")
