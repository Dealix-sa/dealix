from __future__ import annotations

import asyncio
from unittest.mock import AsyncMock, Mock, patch

import pytest

from core.config.models import Provider, Task
from core.llm.base import LLMResponse
from core.llm.inference import NoLLMProviderConfigured, complete_with_router


def test_complete_with_router_calls_router_run_for_single_provider() -> None:
    router = Mock()
    router.run = AsyncMock()
    router.available_providers.return_value = [Provider.OPENAI]
    router.run.return_value = LLMResponse(
        content="model output",
        provider="openai",
        model="gpt-test",
    )

    async def exercise() -> tuple[str, str]:
        with patch("core.llm.router.get_router", return_value=router):
            return await complete_with_router("system", "user")

    content, model = asyncio.run(exercise())

    assert content == "model output"
    assert model == "gpt-test"
    kwargs = router.run.await_args.kwargs
    assert kwargs["task"] is Task.ARABIC_TASKS
    assert kwargs["preferred_provider"] is Provider.OPENAI
    assert kwargs["system"] == "system"


def test_complete_with_router_blocks_without_provider() -> None:
    router = Mock()
    router.run = AsyncMock()
    router.available_providers.return_value = []

    async def exercise() -> None:
        with patch("core.llm.router.get_router", return_value=router):
            await complete_with_router("system", "user")

    with pytest.raises(NoLLMProviderConfigured, match="no_llm_provider_configured"):
        asyncio.run(exercise())
    router.run.assert_not_awaited()


def test_command_bus_uses_the_shared_router_adapter() -> None:
    from api.routers import command_bus

    completion = AsyncMock(return_value=("draft", "test-model"))

    async def exercise() -> tuple[str, str]:
        with patch("core.llm.inference.complete_with_router", completion):
            return await command_bus._call_llm("system", "user")

    assert asyncio.run(exercise()) == ("draft", "test-model")
    completion.assert_awaited_once_with(
        "system",
        "user",
        max_tokens=command_bus.MAX_OUTPUT_TOKENS,
        temperature=0.4,
        timeout_seconds=command_bus.LLM_TIMEOUT_SECONDS,
    )
