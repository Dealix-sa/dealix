"""Unit tests for the ModelRouter routing + fallback logic."""

from __future__ import annotations

import pytest

from core.config.models import (
    FALLBACK_CHAIN,
    TASK_ROUTING,
    Provider,
    Task,
    get_fallbacks,
    get_provider_for_task,
)
from core.config.settings import get_settings


@pytest.fixture(autouse=True)
def _default_llm_profile(monkeypatch):
    """Classic routing table (not MiniMax-first)."""
    monkeypatch.setenv("DEALIX_LLM_PROFILE", "default")
    monkeypatch.delenv("MINIMAX_API_KEY", raising=False)
    monkeypatch.setenv("AI_PRIMARY_PROVIDER", "deepseek")
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()


def test_every_task_has_provider():
    for task in Task:
        assert task in TASK_ROUTING, f"Task {task} has no routing"
        assert isinstance(TASK_ROUTING[task], Provider)


def test_every_provider_has_fallback_chain():
    for provider in Provider:
        assert provider in FALLBACK_CHAIN
        chain = FALLBACK_CHAIN[provider]
        assert provider not in chain, f"{provider} should not fallback to itself"
        assert all(isinstance(p, Provider) for p in chain)


def test_get_provider_for_task():
    assert get_provider_for_task(Task.REASONING) == Provider.ANTHROPIC
    assert get_provider_for_task(Task.ARABIC_TASKS) == Provider.GLM
    assert get_provider_for_task(Task.CODE) == Provider.DEEPSEEK
    assert get_provider_for_task(Task.CLASSIFICATION) == Provider.GROQ
    assert get_provider_for_task(Task.RESEARCH) == Provider.GEMINI


def test_get_fallbacks_returns_list():
    fallbacks = get_fallbacks(Provider.ANTHROPIC)
    assert isinstance(fallbacks, list)
    assert len(fallbacks) > 0
