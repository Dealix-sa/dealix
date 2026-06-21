"""Tests for company.ai_router.router module — no live network calls."""
from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from unittest.mock import patch

from company.ai_router.router import (
    AIResponse,
    ProviderConfig,
    PROVIDERS,
    _get_provider_order,
    _budget_remaining,
    ai_complete,
    health_check,
)


class TestProviderRegistry:
    def test_all_known_providers_registered(self):
        for name in ("openai", "deepseek", "openrouter", "groq", "minimax", "kimi"):
            assert name in PROVIDERS

    def test_each_provider_has_api_key_env(self):
        for name, cfg in PROVIDERS.items():
            assert cfg.api_key_env, f"{name} missing api_key_env"

    def test_each_provider_has_base_url(self):
        for name, cfg in PROVIDERS.items():
            assert cfg.base_url.startswith("https://"), f"{name} base_url not HTTPS"

    def test_each_provider_has_default_model(self):
        for name, cfg in PROVIDERS.items():
            assert cfg.default_model, f"{name} missing default_model"

    def test_provider_config_dataclass(self):
        cfg = PROVIDERS["openai"]
        assert isinstance(cfg, ProviderConfig)
        assert cfg.name == "openai"


class TestGetProviderOrder:
    def test_default_order_contains_deepseek(self):
        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop("AI_PROVIDER_ORDER", None)
            order = _get_provider_order()
        assert "deepseek" in order

    def test_custom_order_from_env(self):
        with patch.dict(os.environ, {"AI_PROVIDER_ORDER": "groq,openai"}):
            order = _get_provider_order()
        assert order == ["groq", "openai"]

    def test_strips_whitespace(self):
        with patch.dict(os.environ, {"AI_PROVIDER_ORDER": " openai , groq "}):
            order = _get_provider_order()
        assert order == ["openai", "groq"]


class TestBudgetRemaining:
    def test_full_budget_when_no_log(self):
        with patch("company.ai_router.router.USAGE_LOG", Path("/tmp/nonexistent_usage_dealix.json")):
            remaining = _budget_remaining()
        assert remaining > 0

    def test_budget_deducted_by_spent_amount(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump({"calls": [{"cost_usd": 1.0}, {"cost_usd": 0.5}]}, f)
            tmp_path = Path(f.name)
        try:
            with patch("company.ai_router.router.USAGE_LOG", tmp_path):
                with patch.dict(os.environ, {"AI_DAILY_BUDGET_USD": "5.0"}):
                    remaining = _budget_remaining()
            assert abs(remaining - 3.5) < 0.001
        finally:
            tmp_path.unlink(missing_ok=True)

    def test_returns_full_budget_on_corrupt_log(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            f.write("NOT_JSON")
            tmp_path = Path(f.name)
        try:
            with patch("company.ai_router.router.USAGE_LOG", tmp_path):
                with patch.dict(os.environ, {"AI_DAILY_BUDGET_USD": "5.0"}):
                    remaining = _budget_remaining()
            assert remaining == 5.0
        finally:
            tmp_path.unlink(missing_ok=True)

    def test_custom_budget_limit(self):
        with patch("company.ai_router.router.USAGE_LOG", Path("/tmp/nonexistent_usage_dealix.json")):
            with patch.dict(os.environ, {"AI_DAILY_BUDGET_USD": "10.0"}):
                remaining = _budget_remaining()
        assert remaining == 10.0


class TestHealthCheck:
    def test_returns_status_for_all_providers(self):
        status = health_check()
        for name in PROVIDERS:
            assert name in status

    def test_unconfigured_shows_no_key(self):
        clean = {k: v for k, v in os.environ.items() if "_API_KEY" not in k}
        with patch.dict(os.environ, clean, clear=True):
            status = health_check()
        for name in PROVIDERS:
            assert status.get(name) in ("configured", "no_key")

    def test_budget_remaining_in_status(self):
        status = health_check()
        assert "budget_remaining_usd" in status


class TestAiComplete:
    def test_returns_none_when_no_providers(self):
        clean = {k: v for k, v in os.environ.items() if "_API_KEY" not in k}
        clean["OLLAMA_BASE_URL"] = "http://127.0.0.1:1"  # unreachable
        clean["AI_PROVIDER_ORDER"] = "local"
        with patch.dict(os.environ, clean, clear=True):
            result = ai_complete("Hello", task="test", timeout=1, max_retries=0)
        assert result is None

    def test_returns_none_when_budget_exhausted(self):
        with patch("company.ai_router.router._budget_remaining", return_value=0.0):
            result = ai_complete("Hello")
        assert result is None


class TestAIResponse:
    def test_defaults(self):
        r = AIResponse(text="hello", provider="openai", model="gpt-4o-mini")
        assert r.prompt_tokens == 0
        assert r.completion_tokens == 0
        assert r.cost_usd == 0.0

    def test_custom_fields(self):
        r = AIResponse(text="test", provider="groq", model="llama", cost_usd=0.001)
        assert r.cost_usd == 0.001
