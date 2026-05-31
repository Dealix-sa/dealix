"""Auth transactional email wiring (invite + password reset).

These tests are fully offline: EmailClient.send is replaced with an AsyncMock
so no network call is ever made. They assert that:

  - the bilingual (ar+en) bodies contain the token and both languages,
  - the delivery helpers never raise and never crash on failure,
  - the invite endpoint sends only in production (not dev/test),
  - the password-reset endpoint sends only in production (not dev/test) and
    only when a matching user/token exists, while the response stays identical.

No raw token or PII is asserted via logs — only observable send behaviour.
"""
from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from api.routers import auth as auth_router
from api.routers.auth import (
    InviteRequest,
    PasswordResetRequest,
    _build_invite_email,
    _build_reset_email,
    _send_invite_email,
    _send_reset_email,
    password_reset_request,
    send_invite,
)
from core.config.settings import get_settings


@pytest.fixture(autouse=True)
def _reset_settings_cache():
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()


# ── Body builders ───────────────────────────────────────────────────

def test_build_invite_email_is_bilingual_and_carries_token() -> None:
    subject, body_text, body_html = _build_invite_email(
        invite_token="TOKEN_ABC123", expires_hours=48
    )
    assert "Dealix" in subject
    # English
    assert "You've been invited to Dealix" in subject
    assert "invited" in body_text
    # Arabic
    assert "تمت دعوتك إلى Dealix" in subject
    assert "دعوتك" in body_text
    # Token + expiry present in both representations
    assert "TOKEN_ABC123" in body_text
    assert "TOKEN_ABC123" in body_html
    assert "48" in body_text


def test_build_reset_email_is_bilingual_and_carries_token() -> None:
    subject, body_text, body_html = _build_reset_email(reset_token="RESET_XYZ789")
    assert "Reset your Dealix password" in subject
    assert "إعادة تعيين كلمة المرور" in subject
    assert "RESET_XYZ789" in body_text
    assert "RESET_XYZ789" in body_html
    # Both languages present in the text body
    assert "reset" in body_text.lower()
    assert "تعيين" in body_text


# ── Delivery helpers ────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_send_invite_email_calls_client_and_returns_true(monkeypatch) -> None:
    send_mock = AsyncMock(
        return_value=SimpleNamespace(success=True, provider="resend", error=None)
    )
    monkeypatch.setattr("integrations.email.EmailClient.send", send_mock)
    ok = await _send_invite_email(
        to_email="invitee@example.com", invite_token="T", expires_hours=24
    )
    assert ok is True
    send_mock.assert_awaited_once()
    kwargs = send_mock.await_args.kwargs
    assert kwargs["to"] == "invitee@example.com"
    assert kwargs["body_text"]


@pytest.mark.asyncio
async def test_send_reset_email_returns_false_on_unsuccessful_send(monkeypatch) -> None:
    send_mock = AsyncMock(
        return_value=SimpleNamespace(success=False, provider="resend", error="nope")
    )
    monkeypatch.setattr("integrations.email.EmailClient.send", send_mock)
    ok = await _send_reset_email(to_email="user@example.com", reset_token="T")
    assert ok is False
    send_mock.assert_awaited_once()


@pytest.mark.asyncio
async def test_send_helpers_never_crash_when_client_raises(monkeypatch) -> None:
    send_mock = AsyncMock(side_effect=RuntimeError("provider down"))
    monkeypatch.setattr("integrations.email.EmailClient.send", send_mock)
    # Must swallow and return False — endpoint robustness.
    assert await _send_invite_email(
        to_email="a@b.com", invite_token="T", expires_hours=24
    ) is False
    assert await _send_reset_email(to_email="a@b.com", reset_token="T") is False


# ── Endpoint gating: invite ──────────────────────────────────────────

def _fake_db() -> AsyncMock:
    db = AsyncMock()
    # db.execute(...) returns a result whose scalar_one_or_none() -> None
    exec_result = SimpleNamespace(
        scalar_one_or_none=lambda: None,
        scalars=lambda: SimpleNamespace(first=lambda: None),
    )
    db.execute = AsyncMock(return_value=exec_result)
    db.add = lambda *a, **k: None
    db.flush = AsyncMock(return_value=None)
    return db


@pytest.mark.asyncio
async def test_invite_endpoint_does_not_send_in_test_env(monkeypatch) -> None:
    monkeypatch.setenv("APP_ENV", "test")
    get_settings.cache_clear()
    helper = AsyncMock(return_value=True)
    monkeypatch.setattr(auth_router, "_send_invite_email", helper)

    user = SimpleNamespace(tenant_id="ten_1", id="usr_1")
    resp = await send_invite(
        body=InviteRequest(email="invitee@example.com"),
        user=user,  # type: ignore[arg-type]
        db=_fake_db(),  # type: ignore[arg-type]
    )
    helper.assert_not_awaited()
    # dev/test response shape preserved — raw token returned
    assert "invite_token" in resp
    assert "message" not in resp


@pytest.mark.asyncio
async def test_invite_endpoint_sends_in_production(monkeypatch) -> None:
    monkeypatch.setenv("APP_ENV", "production")
    get_settings.cache_clear()
    helper = AsyncMock(return_value=True)
    monkeypatch.setattr(auth_router, "_send_invite_email", helper)

    user = SimpleNamespace(tenant_id="ten_1", id="usr_1")
    resp = await send_invite(
        body=InviteRequest(email="invitee@example.com"),
        user=user,  # type: ignore[arg-type]
        db=_fake_db(),  # type: ignore[arg-type]
    )
    helper.assert_awaited_once()
    assert helper.await_args.kwargs["to_email"] == "invitee@example.com"
    # production response shape — no raw token leaked
    assert "invite_token" not in resp
    assert resp["message"]


# ── Endpoint gating: password reset ──────────────────────────────────

def _fake_db_with_user() -> AsyncMock:
    db = AsyncMock()
    user = SimpleNamespace(
        reset_token=None,
        reset_token_expires_at=None,
        email="user@example.com",
    )
    exec_result = SimpleNamespace(
        scalars=lambda: SimpleNamespace(first=lambda: user),
        scalar_one_or_none=lambda: user,
    )
    db.execute = AsyncMock(return_value=exec_result)
    db.flush = AsyncMock(return_value=None)
    db.add = lambda *a, **k: None
    return db


@pytest.mark.asyncio
async def test_reset_endpoint_does_not_send_in_test_env(monkeypatch) -> None:
    monkeypatch.setenv("APP_ENV", "test")
    get_settings.cache_clear()
    helper = AsyncMock(return_value=True)
    monkeypatch.setattr(auth_router, "_send_reset_email", helper)

    resp = await password_reset_request(
        body=PasswordResetRequest(email="user@example.com"),
        db=_fake_db_with_user(),  # type: ignore[arg-type]
    )
    helper.assert_not_awaited()
    # dev/test response shape preserved — token returned for tests
    assert "_dev_reset_token" in resp


@pytest.mark.asyncio
async def test_reset_endpoint_sends_in_production(monkeypatch) -> None:
    monkeypatch.setenv("APP_ENV", "production")
    get_settings.cache_clear()
    helper = AsyncMock(return_value=True)
    monkeypatch.setattr(auth_router, "_send_reset_email", helper)

    resp = await password_reset_request(
        body=PasswordResetRequest(email="user@example.com"),
        db=_fake_db_with_user(),  # type: ignore[arg-type]
    )
    helper.assert_awaited_once()
    assert helper.await_args.kwargs["to_email"] == "user@example.com"
    # Non-revealing: no token in the production response
    assert "_dev_reset_token" not in resp
    assert resp["message"]


@pytest.mark.asyncio
async def test_reset_endpoint_in_production_does_not_send_when_no_user(monkeypatch) -> None:
    monkeypatch.setenv("APP_ENV", "production")
    get_settings.cache_clear()
    helper = AsyncMock(return_value=True)
    monkeypatch.setattr(auth_router, "_send_reset_email", helper)

    resp = await password_reset_request(
        body=PasswordResetRequest(email="nobody@example.com"),
        db=_fake_db(),  # type: ignore[arg-type]  — first() -> None
    )
    # No user -> nothing to send, but response stays identical (non-revealing)
    helper.assert_not_awaited()
    assert "_dev_reset_token" not in resp
    assert resp["message"]
