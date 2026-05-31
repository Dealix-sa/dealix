"""Tests for core.email.invites — doctrine gate + bilingual rendering."""

from __future__ import annotations

from unittest.mock import patch

import pytest

from core.email.invites import (
    InviteEmailResult,
    _render_invite_html,
    _render_invite_text,
    send_invite_email,
)


def test_render_html_includes_both_languages() -> None:
    html = _render_invite_html(
        invited_by_name="Sami",
        accept_url="https://dealix.me/invite?token=abc",
    )
    assert 'lang="ar"' in html
    assert 'dir="rtl"' in html
    assert "دعوة" in html
    assert "Dealix" in html
    assert "Sami" in html
    assert "https://dealix.me/invite?token=abc" in html


def test_render_text_includes_both_languages() -> None:
    txt = _render_invite_text(
        invited_by_name="Sami",
        accept_url="https://dealix.me/invite?token=abc",
    )
    assert "دعاك Sami" in txt
    assert "Sami invited" in txt
    assert "https://dealix.me/invite?token=abc" in txt


@pytest.mark.asyncio
async def test_send_invite_blocked_when_policy_off() -> None:
    """Default settings (email_allow_live_send=False) → blocked_by_policy."""
    from core.config.settings import Settings

    fake_settings = Settings(email_allow_live_send=False)
    with patch("core.email.invites.get_settings", return_value=fake_settings):
        result = await send_invite_email(
            to_email="acceptor@example.sa",
            invite_token="t123",
            invited_by_name="Sami",
            accept_url="https://dealix.me/invite?token=t123",
        )
    assert isinstance(result, InviteEmailResult)
    assert result.blocked_by_policy is True
    assert result.delivered is False
    assert "email_allow_live_send" in (result.error or "")


@pytest.mark.asyncio
async def test_send_invite_delegates_when_policy_on() -> None:
    """When the policy is open, the helper hits EmailClient.send."""
    from core.config.settings import Settings

    fake_settings = Settings(email_allow_live_send=True, email_provider="resend")

    class FakeResult:
        success = True
        provider = "resend"
        message_id = "msg_abc"
        error = None

    async def fake_send(**kwargs):
        # Verify the helper passes bilingual content + correct subject
        assert "دعوة" in kwargs["subject"] or "invitation" in kwargs["subject"]
        assert kwargs["to"] == "acceptor@example.sa"
        return FakeResult()

    with (
        patch("core.email.invites.get_settings", return_value=fake_settings),
        patch("integrations.email.EmailClient.send", side_effect=fake_send),
    ):
        result = await send_invite_email(
            to_email="acceptor@example.sa",
            invite_token="t123",
            invited_by_name="Sami",
            accept_url="https://dealix.me/invite?token=t123",
        )
    assert result.delivered is True
    assert result.blocked_by_policy is False
    assert result.message_id == "msg_abc"
