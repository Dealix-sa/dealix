"""Unit tests for core.llm.dealix_chat."""

from __future__ import annotations

from unittest.mock import AsyncMock, patch

import pytest

from core.config.settings import get_settings
from core.llm.base import LLMResponse, Message
from core.llm.dealix_chat import dealix_chat
from core.llm.runtime_router import reset_runtime_router


@pytest.mark.asyncio
async def test_dealix_chat_uses_runtime_when_minimax_primary(monkeypatch):
    monkeypatch.setenv("AI_PRIMARY_PROVIDER", "minimax")
    monkeypatch.setenv("MINIMAX_API_KEY", "sk-api-test")
    get_settings.cache_clear()
    reset_runtime_router()

    mock_response = LLMResponse(
        content="ok",
        provider="minimax",
        model="MiniMax-M2.7",
    )
    with patch(
        "core.llm.dealix_chat.get_runtime_router"
    ) as mock_get:
        runtime = AsyncMock()
        runtime.chat.return_value = mock_response
        mock_get.return_value = runtime

        out = await dealix_chat("hello", max_tokens=32)
        assert out.content == "ok"
        runtime.chat.assert_awaited_once()
