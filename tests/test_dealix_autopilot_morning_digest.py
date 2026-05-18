"""Tests for scripts/dealix_autopilot_morning_digest.py (WS-E).

Covers the consolidated morning digest glue script: data aggregation from
the two existing approval surfaces, digest rendering, overdue counting, and
the print/dry-run/send paths. Also asserts the WS-E workflow wiring.
"""
from __future__ import annotations

import asyncio
import importlib.util
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path
from unittest.mock import AsyncMock, patch

REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / "scripts" / "dealix_autopilot_morning_digest.py"
sys.path.insert(0, str(REPO))


def _load():
    spec = importlib.util.spec_from_file_location(
        "dealix_autopilot_morning_digest", str(SCRIPT)
    )
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


digest = _load()


def test_subject_includes_today():
    today = datetime.now(UTC).strftime("%Y-%m-%d")
    assert today in digest._build_subject()


def test_count_overdue_counts_past_expiry_only():
    now = datetime.now(UTC)
    past = (now - timedelta(hours=2)).isoformat()
    future = (now + timedelta(hours=2)).isoformat()
    pending = {
        "pending": [
            {"id": "a", "expires_at": past},
            {"id": "b", "expires_at": future},
            {"id": "c"},  # no expiry — not counted
            {"id": "d", "expires_at": past},
        ]
    }
    assert digest._count_overdue(pending) == 2


def test_count_overdue_handles_empty_and_malformed():
    assert digest._count_overdue({}) == 0
    assert digest._count_overdue({"pending": "not-a-list"}) == 0
    assert digest._count_overdue({"pending": [{"expires_at": "garbage"}]}) == 0


def test_collect_digest_data_aggregates_both_queues():
    def _fake_get(base, path, api_key):
        if "approvals/pending" in path:
            return {"count": 2, "pending": [
                {"id": "x", "expires_at": (datetime.now(UTC) - timedelta(hours=1)).isoformat()},
            ]}
        if "revenue-machine/today" in path:
            return {
                "gmail_drafts": {"total": 50, "remaining_to_review": 50},
                "linkedin_drafts": {"total": 20},
                "approval_queue_open": 70,
            }
        return {"_error": "unexpected"}

    def _fake_post(base, path, api_key):
        return {"metrics": {"followups_due": 8, "revenue_actual": 499, "revenue_target": 2999}}

    with patch.object(digest, "_get_json", side_effect=_fake_get), \
         patch.object(digest, "_post_json", side_effect=_fake_post):
        data = digest.collect_digest_data("https://api.example", "key")

    q = data["approval_queue"]
    # Both surfaces aggregated; total is the sum.
    assert q["pending_approval_center"] == 2
    assert q["pending_drafts"] == 70
    assert q["pending_total"] == 72
    assert q["overdue"] == 1
    assert data["followups_due"] == 8
    assert data["revenue"]["actual"] == 499
    assert data["revenue"]["target"] == 2999


def test_render_digest_contains_required_sections():
    data = {
        "date": "2026-05-18",
        "drafts": {"gmail_total": 50, "gmail_remaining": 50, "linkedin_total": 20},
        "followups_due": 8,
        "approval_queue": {
            "pending_approval_center": 2,
            "pending_drafts": 70,
            "pending_total": 72,
            "overdue": 1,
        },
        "revenue": {"actual": 499, "target": 2999},
        "_errors": {},
    }
    text = digest.render_digest(data)
    assert "Morning Autopilot Digest" in text
    assert "Drafts generated today" in text
    assert "Follow-ups" in text
    assert "Founder approval queue" in text
    assert "TOTAL pending approval: 72" in text
    assert "Overdue approvals (expired): 1" in text
    assert "Revenue vs target" in text
    # Doctrine: nothing auto-sends.
    assert "nothing was auto-sent" in text
    # No guarantee language.
    assert "guaranteed" not in text.lower() or "not guaranteed" in text.lower()


def test_render_digest_surfaces_data_warnings():
    data = {
        "date": "2026-05-18",
        "drafts": {"gmail_total": 0, "gmail_remaining": 0, "linkedin_total": 0},
        "followups_due": "n/a",
        "approval_queue": {"pending_approval_center": 0, "pending_drafts": 0,
                           "pending_total": 0, "overdue": 0},
        "revenue": {"actual": "n/a", "target": "n/a"},
        "_errors": {"approvals_pending": "ConnectionError: boom"},
    }
    text = digest.render_digest(data)
    assert "Data warnings" in text
    assert "ConnectionError: boom" in text


def test_build_morning_digest_no_credentials():
    with patch.dict("os.environ", {"DEALIX_API_BASE": "", "DEALIX_API_KEY": ""},
                    clear=False):
        text = digest.build_morning_digest()
    assert "API credentials not configured" in text


def test_print_only_mode(capsys):
    sys.argv = ["dealix_autopilot_morning_digest.py", "--print"]
    args = digest.parse_args()
    with patch.object(digest, "build_morning_digest", return_value="# rendered body"):
        result = asyncio.run(digest._build_and_send(args))
    out = capsys.readouterr().out
    assert "# rendered body" in out
    assert result.success is True
    assert result.provider == "print_only"


def test_dry_run_does_not_send():
    sys.argv = ["dealix_autopilot_morning_digest.py", "--dry-run"]
    args = digest.parse_args()
    with patch.object(digest, "build_morning_digest", return_value="# body"), \
         patch.object(digest, "EmailClient") as MockClient:
        instance = MockClient.return_value
        instance.send = AsyncMock(side_effect=AssertionError("must not send in dry-run"))
        result = asyncio.run(digest._build_and_send(args))
    assert result.success is True
    assert result.provider == "dry_run"
    instance.send.assert_not_called()


def test_send_mode_emails_founder_only():
    sys.argv = ["dealix_autopilot_morning_digest.py"]
    args = digest.parse_args()
    captured = {}

    async def _capture(**kwargs):
        captured.update(kwargs)
        from integrations.email import EmailResult
        return EmailResult(success=True, provider="resend", message_id="m1")

    with patch.object(digest, "build_morning_digest", return_value="# body"), \
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
    sys.argv = ["dealix_autopilot_morning_digest.py"]
    args = digest.parse_args()
    with patch.object(digest, "get_settings") as mock_get:
        mock_settings = type("S", (), {})()
        mock_settings.dealix_founder_email = ""
        mock_settings.email_provider = "resend"
        mock_get.return_value = mock_settings
        result = asyncio.run(digest._build_and_send(args))
    assert result.success is False
    assert "founder_email_not_configured" in (result.error or "")


def test_morning_workflow_has_consolidated_digest_step():
    workflow = REPO / ".github" / "workflows" / "daily-revenue-machine.yml"
    text = workflow.read_text(encoding="utf-8")
    assert "scripts/dealix_autopilot_morning_digest.py" in text
    assert "Consolidated founder digest" in text
    # Doctrine: the daily run stays draft-only.
    assert '"approval_mode": "draft_only"' in text


def test_evening_workflow_exists_and_wired():
    workflow = REPO / ".github" / "workflows" / "daily-evening-digest.yml"
    assert workflow.exists()
    text = workflow.read_text(encoding="utf-8")
    # 16:00 UTC = 19:00 KSA
    assert 'cron: "0 16 * * *"' in text
    assert "scripts/dealix_evening_digest.py" in text
    assert "secrets_present" in text  # skip-gracefully pattern


def test_weekly_workflow_exists_and_wired():
    workflow = REPO / ".github" / "workflows" / "weekly-review.yml"
    assert workflow.exists()
    text = workflow.read_text(encoding="utf-8")
    assert 'cron: "0 5 * * 0"' in text
    assert "scripts/weekly_brief_runner.py" in text
    assert "scripts/verify_dealix_ready.py" in text
    assert "scripts/verify_governance.py" in text
