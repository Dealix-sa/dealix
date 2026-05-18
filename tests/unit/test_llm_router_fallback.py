"""
Unit tests — LLM ModelRouter fallback chain.
اختبارات الوحدة — سلسلة الاحتياط لمُوجّه النموذج.

Tests that when a provider raises an exception the router correctly
falls back to the next provider in the FALLBACK_CHAIN.

The router's public entrypoint is ``ModelRouter.run(task, messages)`` and
it dispatches to each client's ``chat(...)`` coroutine. These tests mock
``chat`` directly so no network call is made.
"""

from __future__ import annotations

import asyncio
from unittest.mock import AsyncMock, MagicMock

import pytest

from core.config.models import FALLBACK_CHAIN, Provider, Task
from core.llm.base import LLMResponse, Message
from core.llm.router import ModelRouter

# Task.REASONING routes to ANTHROPIC as its primary provider; the configured
# fallback chain is [OPENAI, GLM]. The fixture below leaves OPENAI unconfigured
# so the effective chain is ANTHROPIC -> GLM.
_TASK = Task.REASONING
_PRIMARY = Provider.ANTHROPIC


# ── Fixtures ───────────────────────────────────────────────────────

@pytest.fixture()
def mock_settings() -> MagicMock:
    settings = MagicMock()
    settings.anthropic_api_key.get_secret_value.return_value = "sk-test-anthropic"
    settings.deepseek_api_key.get_secret_value.return_value = "sk-test-deepseek"
    settings.groq_api_key.get_secret_value.return_value = "sk-test-groq"
    settings.glm_api_key.get_secret_value.return_value = "sk-test-glm"
    settings.google_api_key.get_secret_value.return_value = "sk-test-google"
    settings.openai_api_key.get_secret_value.return_value = ""
    settings.openai_api_key.__bool__ = lambda self: False
    return settings


def _make_response(provider: Provider, content: str = "OK") -> LLMResponse:
    return LLMResponse(
        content=content,
        provider=provider,
        model="test-model",
        input_tokens=10,
        output_tokens=5,
    )


def _chain_for(router: ModelRouter, primary: Provider) -> list[Provider]:
    """Effective fallback chain — primary plus configured fallbacks."""
    chain = [primary] + [p for p in FALLBACK_CHAIN.get(primary, []) if p != primary]
    return [p for p in chain if p in router._clients]


# ── Tests ──────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_router_uses_primary_provider(mock_settings: MagicMock) -> None:
    """Router calls the primary provider and returns its response."""
    router = ModelRouter(settings=mock_settings)

    mock_client = AsyncMock()
    mock_client.chat.return_value = _make_response(_PRIMARY, "primary response")
    router._clients[_PRIMARY] = mock_client

    messages = [Message(role="user", content="hello")]
    response = await router.run(task=_TASK, messages=messages)

    assert response.content == "primary response"
    mock_client.chat.assert_called_once()


@pytest.mark.asyncio
async def test_router_falls_back_on_provider_error(mock_settings: MagicMock) -> None:
    """When the primary provider raises, router tries the next in fallback chain."""
    router = ModelRouter(settings=mock_settings)
    chain = _chain_for(router, _PRIMARY)
    assert len(chain) >= 2, "test needs primary + at least one fallback configured"

    success_content = "fallback response"

    # Every provider in the chain fails except the last one.
    for provider in chain[:-1]:
        mock_fail = AsyncMock()
        mock_fail.chat.side_effect = Exception(f"Provider {provider} unavailable")
        router._clients[provider] = mock_fail

    last_provider = chain[-1]
    mock_ok = AsyncMock()
    mock_ok.chat.return_value = _make_response(last_provider, success_content)
    router._clients[last_provider] = mock_ok

    messages = [Message(role="user", content="test")]
    response = await router.run(task=_TASK, messages=messages)

    assert response.content == success_content


@pytest.mark.asyncio
async def test_router_raises_when_all_providers_fail(mock_settings: MagicMock) -> None:
    """Router raises RuntimeError when every provider in the chain fails."""
    router = ModelRouter(settings=mock_settings)

    for provider in list(router._clients.keys()):
        mock_fail = AsyncMock()
        mock_fail.chat.side_effect = Exception("unavailable")
        router._clients[provider] = mock_fail

    messages = [Message(role="user", content="test")]
    with pytest.raises(RuntimeError):
        await router.run(task=_TASK, messages=messages)


@pytest.mark.asyncio
async def test_router_increments_fallback_counter(mock_settings: MagicMock) -> None:
    """After a fallback the primary provider's fallbacks_triggered is incremented."""
    router = ModelRouter(settings=mock_settings)
    chain = _chain_for(router, _PRIMARY)
    assert len(chain) >= 2, "test needs primary + at least one fallback configured"

    primary, secondary = chain[0], chain[1]

    mock_fail = AsyncMock()
    mock_fail.chat.side_effect = Exception("timeout")
    router._clients[primary] = mock_fail

    mock_ok = AsyncMock()
    mock_ok.chat.return_value = _make_response(secondary)
    router._clients[secondary] = mock_ok

    await router.run(task=_TASK, messages=[Message(role="user", content="x")])

    assert router.usage[primary].fallbacks_triggered >= 1


@pytest.mark.asyncio
async def test_router_usage_records_are_updated(mock_settings: MagicMock) -> None:
    """Usage records are incremented on successful completion."""
    router = ModelRouter(settings=mock_settings)

    mock_client = AsyncMock()
    mock_client.chat.return_value = _make_response(_PRIMARY, "ok")
    router._clients[_PRIMARY] = mock_client

    initial_calls = router.usage[_PRIMARY].calls
    await router.run(task=_TASK, messages=[Message(role="user", content="test")])
    assert router.usage[_PRIMARY].calls == initial_calls + 1


@pytest.mark.asyncio
async def test_router_concurrent_safety(mock_settings: MagicMock) -> None:
    """Concurrent run calls don't corrupt usage counters (asyncio.Lock)."""
    router = ModelRouter(settings=mock_settings)

    call_count = 0

    async def _increment_and_respond(**kwargs: object) -> LLMResponse:
        nonlocal call_count
        call_count += 1
        await asyncio.sleep(0)  # yield — simulates I/O
        return _make_response(_PRIMARY)

    mock_client = MagicMock()
    mock_client.chat = _increment_and_respond
    router._clients[_PRIMARY] = mock_client

    messages = [Message(role="user", content="concurrent")]
    tasks = [router.run(task=_TASK, messages=messages) for _ in range(10)]
    responses = await asyncio.gather(*tasks)

    assert len(responses) == 10
    assert router.usage[_PRIMARY].calls == 10
