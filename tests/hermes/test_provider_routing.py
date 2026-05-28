"""HERMES_PROVIDER env switches engine + strategy to the right provider."""

from __future__ import annotations

import pytest

from dealix.hermes import HermesOrchestrator, HermesTask
from dealix.hermes.agents import route_to_agent_executor
from dealix.llm.engine import DealixEngine, Gear, active_provider
from dealix.llm.strategy import LLMStrategyRouter, TaskType


def test_default_provider_is_openrouter(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("HERMES_PROVIDER", raising=False)
    assert active_provider() == "openrouter"
    cfg = DealixEngine.get(Gear.DAILY)
    assert cfg.provider == "openrouter"
    assert cfg.model_id == "deepseek/deepseek-chat"


def test_direct_deepseek_rewrites_model_id(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("HERMES_PROVIDER", "direct_deepseek")
    assert active_provider() == "direct_deepseek"
    cfg = DealixEngine.get(Gear.DAILY)
    assert cfg.provider == "direct_deepseek"
    assert cfg.model_id == "deepseek-chat"
    # Cost reflects direct-provider pricing, not OpenRouter mark-up.
    assert cfg.cost_per_1m_input == pytest.approx(0.014)
    assert cfg.cost_per_1m_output == pytest.approx(0.028)


def test_direct_deepseek_falls_back_for_minimax_models(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("HERMES_PROVIDER", "direct_deepseek")
    # Power gear is Minimax — not serviceable by DeepSeek-direct, must fall back.
    cfg = DealixEngine.get(Gear.POWER)
    assert cfg.provider == "openrouter"
    assert cfg.model_id.startswith("minimax/")


def test_strategy_router_respects_active_provider(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("HERMES_PROVIDER", "direct_deepseek")
    chain = LLMStrategyRouter().resolve(TaskType.DATA_ENRICHMENT)
    # LIGHT tier is DeepSeek → should route direct.
    light = chain[0]
    assert light.provider == "direct_deepseek"
    assert light.model_id == "deepseek-chat"


def test_unknown_provider_defaults_to_openrouter(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("HERMES_PROVIDER", "bogus_provider_x")
    assert active_provider() == "openrouter"


def test_orchestrator_passes_provider_into_route(
    monkeypatch: pytest.MonkeyPatch, tmp_path
) -> None:
    monkeypatch.setenv("HERMES_PROVIDER", "direct_deepseek")
    monkeypatch.setenv("HERMES_AUDIT_PATH", str(tmp_path / "audit.jsonl"))
    orch = HermesOrchestrator(executor=route_to_agent_executor)
    result = orch.dispatch(HermesTask(intent="refactor router"))
    assert result.route is not None
    # Engineering routes to POWER gear → falls back to openrouter for minimax model.
    assert result.route.gear_config.provider == "openrouter"
    # But content (DOCUMENTATION = DAILY = deepseek) stays direct.
    result2 = orch.dispatch(HermesTask(intent="write docs for the bilingual report"))
    assert result2.route is not None
    assert result2.route.gear_config.provider == "direct_deepseek"
    assert result2.route.gear_config.model_id == "deepseek-chat"
