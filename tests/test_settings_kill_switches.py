"""Tests for the Settings kill-switch properties."""
from __future__ import annotations

import pytest

from core.config.settings import get_settings


def test_is_live_send_allowed_default_false(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("APP_ENV", raising=False)
    monkeypatch.delenv("WHATSAPP_ALLOW_LIVE_SEND", raising=False)
    monkeypatch.delenv("WHATSAPP_MOCK_MODE", raising=False)
    get_settings.cache_clear()
    try:
        s = get_settings()
        assert s.is_live_send_allowed is False
    finally:
        get_settings.cache_clear()


def test_is_live_send_allowed_requires_production(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("APP_ENV", "staging")
    monkeypatch.setenv("WHATSAPP_ALLOW_LIVE_SEND", "true")
    monkeypatch.setenv("WHATSAPP_MOCK_MODE", "false")
    get_settings.cache_clear()
    try:
        s = get_settings()
        assert s.is_live_send_allowed is False, "non-production must never enable live send"
    finally:
        get_settings.cache_clear()


def test_is_live_send_allowed_blocked_by_mock_mode(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("APP_ENV", "production")
    monkeypatch.setenv("WHATSAPP_ALLOW_LIVE_SEND", "true")
    monkeypatch.setenv("WHATSAPP_MOCK_MODE", "true")  # contradicts; mock wins
    get_settings.cache_clear()
    try:
        s = get_settings()
        assert s.is_live_send_allowed is False
    finally:
        get_settings.cache_clear()


def test_is_live_send_allowed_true_only_when_all_three(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("APP_ENV", "production")
    monkeypatch.setenv("WHATSAPP_ALLOW_LIVE_SEND", "true")
    monkeypatch.setenv("WHATSAPP_MOCK_MODE", "false")
    get_settings.cache_clear()
    try:
        s = get_settings()
        assert s.is_live_send_allowed is True
    finally:
        get_settings.cache_clear()


def test_internal_token_value_none_when_unset(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("DEALIX_INTERNAL_TOKEN", raising=False)
    get_settings.cache_clear()
    try:
        s = get_settings()
        assert s.internal_token_value is None
    finally:
        get_settings.cache_clear()


def test_internal_token_value_string(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DEALIX_INTERNAL_TOKEN", "secret-token-xyz")
    get_settings.cache_clear()
    try:
        s = get_settings()
        assert s.internal_token_value == "secret-token-xyz"
    finally:
        get_settings.cache_clear()
