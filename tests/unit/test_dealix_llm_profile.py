"""Tests for MiniMax-first DEALIX_LLM_PROFILE routing."""

from __future__ import annotations

import pytest

from core.config.models import (
    Provider,
    Task,
    effective_dealix_llm_profile,
    get_provider_for_task,
    smart_route,
)
from core.config.settings import get_settings


@pytest.fixture(autouse=True)
def _clear_settings(monkeypatch):
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()


def test_effective_profile_explicit_minimax(monkeypatch):
    monkeypatch.setenv("DEALIX_LLM_PROFILE", "minimax")
    assert effective_dealix_llm_profile() == "minimax"


def test_effective_profile_auto_minimax_no_anthropic(monkeypatch):
    monkeypatch.delenv("DEALIX_LLM_PROFILE", raising=False)
    monkeypatch.setenv("MINIMAX_API_KEY", "sk-api-test")
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    assert effective_dealix_llm_profile() == "minimax"


def test_get_provider_reasoning_minimax_profile(monkeypatch):
    monkeypatch.setenv("DEALIX_LLM_PROFILE", "minimax")
    monkeypatch.setenv("MINIMAX_API_KEY", "sk-api-test")
    assert get_provider_for_task(Task.REASONING) == Provider.MINIMAX
    assert get_provider_for_task(Task.ARABIC_TASKS) == Provider.MINIMAX


def test_get_provider_code_deepseek_when_keyed(monkeypatch):
    monkeypatch.setenv("DEALIX_LLM_PROFILE", "minimax")
    monkeypatch.setenv("MINIMAX_API_KEY", "sk-api-test")
    monkeypatch.setenv("DEEPSEEK_API_KEY", "ds-test")
    assert get_provider_for_task(Task.CODE) == Provider.DEEPSEEK


def test_smart_route_critical_minimax(monkeypatch):
    monkeypatch.setenv("DEALIX_LLM_PROFILE", "minimax")
    monkeypatch.setenv("MINIMAX_API_KEY", "sk-api-test")
    cfg = smart_route(Task.PROPOSAL, critical=True)
    assert cfg.provider == Provider.MINIMAX


def test_smart_route_arabic_minimax(monkeypatch):
    monkeypatch.setenv("DEALIX_LLM_PROFILE", "minimax")
    monkeypatch.setenv("MINIMAX_API_KEY", "sk-api-test")
    arabic = "مرحبا " * 20
    cfg = smart_route(Task.SUMMARY, text_sample=arabic)
    assert cfg.provider == Provider.MINIMAX
