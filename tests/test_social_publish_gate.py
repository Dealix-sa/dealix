"""Tests for the social publishing gate — the required proof test.

Proves that an approved social post cannot be handed to n8n unless
(a) the live flag is ON and (b) the post is founder-APPROVED.
"""
from __future__ import annotations

from unittest.mock import AsyncMock, patch

import pytest

from auto_client_acquisition.approval_center.schemas import (
    ApprovalRequest,
    ApprovalStatus,
)
from auto_client_acquisition.content_os.publish_gate import (
    assert_publishable,
    is_publishable,
)
from core.config.settings import Settings
from integrations.n8n import N8NResult
from integrations.social_publish import SocialPublishClient


def _social_request(status: ApprovalStatus) -> ApprovalRequest:
    return ApprovalRequest(
        object_type="social_post",
        object_id="linkedin:proof_not_promises",
        action_type="draft_social_post",
        action_mode="draft_only",
        channel="social",
        status=status,
    )


# ── Gate default ──────────────────────────────────────────────────
def test_social_publish_off_by_default():
    assert Settings().social_publish_allow_live is False


# ── Flag OFF → blocked, n8n never called ──────────────────────────
async def test_blocked_when_flag_off(monkeypatch):
    client = SocialPublishClient()
    monkeypatch.setattr(client.settings, "social_publish_allow_live", False)
    monkeypatch.setattr(client.settings, "n8n_webhook_url", "https://example.com/hook")
    req = _social_request(ApprovalStatus.APPROVED)

    with patch("integrations.social_publish.N8NClient") as mock_n8n:
        send = AsyncMock()
        mock_n8n.return_value.send_event = send
        result = await client.publish_approved_post(
            approval_request=req, platform="linkedin",
            locale="ar", body_ar="نص", body_en="text",
        )

    assert result.success is False
    assert result.error == "social_publish_allow_live_false"
    send.assert_not_called()


# ── Flag ON but not approved → blocked, n8n never called ──────────
async def test_blocked_when_not_approved(monkeypatch):
    client = SocialPublishClient()
    monkeypatch.setattr(client.settings, "social_publish_allow_live", True)
    monkeypatch.setattr(client.settings, "n8n_webhook_url", "https://example.com/hook")
    req = _social_request(ApprovalStatus.PENDING)

    with patch("integrations.social_publish.N8NClient") as mock_n8n:
        send = AsyncMock()
        mock_n8n.return_value.send_event = send
        result = await client.publish_approved_post(
            approval_request=req, platform="linkedin",
            locale="ar", body_ar="نص", body_en="text",
        )

    assert result.success is False
    assert result.error == "post_not_approved"
    send.assert_not_called()


# ── Flag ON + approved → fires exactly once ───────────────────────
async def test_fires_only_after_approval(monkeypatch):
    client = SocialPublishClient()
    monkeypatch.setattr(client.settings, "social_publish_allow_live", True)
    monkeypatch.setattr(client.settings, "n8n_webhook_url", "https://example.com/hook")
    req = _social_request(ApprovalStatus.APPROVED)

    with patch("integrations.social_publish.N8NClient") as mock_n8n:
        send = AsyncMock(return_value=N8NResult(success=True, status_code=200))
        mock_n8n.return_value.send_event = send
        result = await client.publish_approved_post(
            approval_request=req, platform="linkedin",
            locale="ar", body_ar="نص", body_en="text",
        )

    assert result.success is True
    assert result.handoff == "n8n"
    send.assert_called_once()
    assert send.call_args.args[0] == "social_post_approved"


# ── publish_gate chokepoint ───────────────────────────────────────
def test_assert_publishable_rejects_pending():
    with pytest.raises(ValueError):
        assert_publishable(_social_request(ApprovalStatus.PENDING))


def test_assert_publishable_rejects_non_social():
    req = ApprovalRequest(
        object_type="email",
        object_id="e1",
        action_type="draft_email",
        status=ApprovalStatus.APPROVED,
    )
    with pytest.raises(ValueError):
        assert_publishable(req)


def test_is_publishable_true_only_for_approved_social():
    assert is_publishable(_social_request(ApprovalStatus.APPROVED)) is True
    assert is_publishable(_social_request(ApprovalStatus.PENDING)) is False
