"""Unit tests for Dealix runtime AI router (primary → fallback)."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest

from core.config.models import Provider
from core.config.settings import get_settings
from core.llm.base import LLMResponse, Message
from core.llm.runtime_router import (
    RuntimeLLMRouter,
    _sanitize_error,
    parse_provider_name,
    reset_runtime_router,
)


def test_parse_provider_name():
    assert parse_provider_name("deepseek") == Provider.DEEPSEEK
    assert parse_provider_name("MINIMAX") == Provider.MINIMAX


def test_parse_provider_name_invalid():
    with pytest.raises(ValueError, match="Unknown AI provider"):
        parse_provider_name("unknown-vendor")


def test_sanitize_error_redacts_sk_like_tokens():
    msg = _sanitize_error(Exception("Bearer sk-abc1234567890abcdef failed"))
    assert "sk-abc" not in msg
    assert "[redacted]" in msg


@pytest.mark.asyncio
async def test_runtime_router_primary_success(monkeypatch):
    monkeypatch.setenv("AI_PRIMARY_PROVIDER", "deepseek")
    monkeypatch.setenv("AI_FALLBACK_PROVIDER", "minimax")
    get_settings.cache_clear()
    reset_runtime_router()

    mock_router = MagicMock()
    deepseek_client = AsyncMock()
    deepseek_client.chat.return_value = LLMResponse(
        content="ok",
        provider="deepseek",
        model="deepseek-chat",
        input_tokens=1,
        output_tokens=2,
    )
    mock_router.get_client.side_effect = lambda p: (
        deepseek_client if p == Provider.DEEPSEEK else None
    )

    runtime = RuntimeLLMRouter(model_router=mock_router)
    out = await runtime.chat("hello")
    assert out.content == "ok"
    deepseek_client.chat.assert_awaited_once()


@pytest.mark.asyncio
async def test_runtime_router_falls_back_on_primary_failure(monkeypatch):
    monkeypatch.setenv("AI_PRIMARY_PROVIDER", "deepseek")
    monkeypatch.setenv("AI_FALLBACK_PROVIDER", "minimax")
    get_settings.cache_clear()
    reset_runtime_router()

    mock_router = MagicMock()
    deepseek_client = AsyncMock()
    deepseek_client.chat.side_effect = RuntimeError("upstream 503")
    minimax_client = AsyncMock()
    minimax_client.chat.return_value = LLMResponse(
        content="fallback ok",
        provider="minimax",
        model="MiniMax-M2.7",
    )

    def _client(provider: Provider):
        if provider == Provider.DEEPSEEK:
            return deepseek_client
        if provider == Provider.MINIMAX:
            return minimax_client
        return None

    mock_router.get_client.side_effect = _client
    runtime = RuntimeLLMRouter(model_router=mock_router)
    out = await runtime.chat("hello")
    assert out.content == "fallback ok"
    minimax_client.chat.assert_awaited_once()


@pytest.mark.asyncio
async def test_runtime_router_all_fail_raises_sanitized(monkeypatch):
    monkeypatch.setenv("AI_PRIMARY_PROVIDER", "deepseek")
    monkeypatch.setenv("AI_FALLBACK_PROVIDER", "minimax")
    get_settings.cache_clear()

    mock_router = MagicMock()
    client = AsyncMock()
    client.chat.side_effect = RuntimeError("Bearer sk-secret1234567890")
    mock_router.get_client.return_value = client

    runtime = RuntimeLLMRouter(model_router=mock_router)
    with pytest.raises(RuntimeError, match="AI runtime failed") as exc_info:
        await runtime.chat("hello")
    assert "sk-secret" not in str(exc_info.value)


def test_ai_runtime_status_endpoint(monkeypatch):
    from fastapi.testclient import TestClient

    from api.main import app

    monkeypatch.setenv("ADMIN_API_KEYS", "test_admin_ai_runtime")
    monkeypatch.setenv("AI_PRIMARY_PROVIDER", "minimax")
    monkeypatch.setenv("AI_FALLBACK_PROVIDER", "openai")
    monkeypatch.setenv("DEALIX_LLM_PROFILE", "minimax")
    monkeypatch.setenv("MINIMAX_API_KEY", "test-minimax")
    get_settings.cache_clear()
    reset_runtime_router()

    # Reset model router singleton so new env keys are picked up
    import core.llm.router as router_mod

    router_mod._router_instance = None

    client = TestClient(app)
    resp = client.get(
        "/api/v1/ai-runtime/status",
        headers={"X-Admin-API-Key": "test_admin_ai_runtime"},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["primary_provider"] == "minimax"
    assert body["fallback_provider"] == "openai"
    assert body["dealix_llm_profile"] == "minimax"
    assert "sk-" not in resp.text
