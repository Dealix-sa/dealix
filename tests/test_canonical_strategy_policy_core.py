"""Tests for the canonical strategy-policy core."""

from __future__ import annotations

from pathlib import Path

import pytest

from dealix.strategy_core import (
    ActionKind,
    ModelRouter,
    Route,
    StrategyDefinition,
    StrategyRegistry,
    StrategyRegistryError,
    StrategyStep,
    evaluate_step,
    learning_summary,
)


def test_strategy_parsing_treats_string_false_as_false() -> None:
    strategy = StrategyDefinition.from_dict(
        {
            "id": "revenue_sprint",
            "name": "Revenue Sprint",
            "goal": "Prepare evidence-first commercial work.",
            "enabled": "false",
            "priority": "80",
            "guardrails": ["draft_only"],
            "steps": [{"action": "prepare_brief", "kind": "internal_draft", "requires_approval": "false"}],
        }
    )

    assert strategy.enabled is False
    assert strategy.steps[0].requires_approval is False


def test_invalid_risk_kind_priority_and_empty_steps_are_rejected() -> None:
    with pytest.raises(ValueError, match="risk"):
        StrategyStep.from_dict({"action": "bad", "risk": 1.2})
    with pytest.raises(ValueError, match="unsupported"):
        StrategyStep.from_dict({"action": "bad", "kind": "magic"})
    with pytest.raises(ValueError, match="priority"):
        StrategyDefinition.from_dict(
            {"id": "bad_priority", "name": "Bad", "goal": "Bad", "priority": 101, "steps": [{"action": "x"}]}
        )
    with pytest.raises(ValueError, match="at least one step"):
        StrategyDefinition.from_dict({"id": "empty_steps", "name": "Empty", "goal": "Empty", "steps": []})


def test_registry_orders_active_and_rejects_duplicate_ids(tmp_path: Path) -> None:
    (tmp_path / "a.yaml").write_text(
        """
id: strategy_a
name: A
goal: Do A
enabled: true
priority: 20
steps:
  - action: analyze_a
    kind: analyze
""".strip(),
        encoding="utf-8",
    )
    (tmp_path / "b.yaml").write_text(
        """
id: strategy_b
name: B
goal: Do B
enabled: true
priority: 90
steps:
  - action: draft_b
    kind: internal_draft
""".strip(),
        encoding="utf-8",
    )

    registry = StrategyRegistry.from_directory(tmp_path)

    assert [item.definition.strategy_id for item in registry.active()] == ["strategy_b", "strategy_a"]

    (tmp_path / "c.yaml").write_text((tmp_path / "a.yaml").read_text(encoding="utf-8"), encoding="utf-8")
    with pytest.raises(StrategyRegistryError, match="duplicate"):
        StrategyRegistry.from_directory(tmp_path)


def test_registry_fails_on_missing_or_empty_directory(tmp_path: Path) -> None:
    with pytest.raises(StrategyRegistryError, match="does not exist"):
        StrategyRegistry.from_directory(tmp_path / "missing")
    with pytest.raises(StrategyRegistryError, match="contains no YAML"):
        StrategyRegistry.from_directory(tmp_path)


def test_safety_routes_internal_work_by_autonomy_and_risk() -> None:
    draft = StrategyStep(action="prepare_brief", kind=ActionKind.INTERNAL_DRAFT, risk=0.1)
    write = StrategyStep(action="write_report", kind=ActionKind.INTERNAL_WRITE, risk=0.1)
    risky = StrategyStep(action="analyze_contract", kind=ActionKind.ANALYZE, risk=0.6)

    assert evaluate_step(draft, autonomy_level=2).route == Route.INTERNAL_EXECUTE
    assert evaluate_step(write, autonomy_level=2).route == Route.APPROVAL
    assert evaluate_step(write, autonomy_level=3).route == Route.INTERNAL_EXECUTE
    assert evaluate_step(risky, autonomy_level=4).route == Route.APPROVAL


def test_safety_never_auto_authorizes_external_irreversible_or_forbidden_actions() -> None:
    external = StrategyStep(action="prepare_customer_email", kind=ActionKind.EXTERNAL_DRAFT, channel="email")
    merge = StrategyStep(action="merge_main", kind=ActionKind.MERGE)
    production = StrategyStep(action="redeploy_production", kind=ActionKind.PRODUCTION)
    forbidden = StrategyStep(action="run_mass_send_campaign", kind=ActionKind.INTERNAL_DRAFT)

    assert evaluate_step(external, autonomy_level=4).route == Route.APPROVAL
    assert evaluate_step(merge, autonomy_level=4).route == Route.APPROVAL
    assert evaluate_step(production, autonomy_level=4).route == Route.APPROVAL
    assert evaluate_step(forbidden, autonomy_level=4).route == Route.BLOCKED
    assert evaluate_step(external, autonomy_level=4).external_action_allowed is False


def test_model_router_requires_explicit_local_health() -> None:
    unhealthy = ModelRouter({"ENABLE_LOCAL_LLM": "true", "OLLAMA_HOST": "http://127.0.0.1:11434"}).route("code")
    healthy = ModelRouter(
        {
            "ENABLE_LOCAL_LLM": "true",
            "LOCAL_LLM_HEALTHY": "true",
            "OLLAMA_HOST": "http://127.0.0.1:11434",
        }
    ).route("code")

    assert unhealthy.executable is False
    assert healthy.provider == "ollama"
    assert healthy.executable is True
    assert healthy.model == "qwen2.5-coder:7b-64k"


def test_hosted_fallback_is_explicit_and_does_not_expose_credentials() -> None:
    target = ModelRouter(
        {
            "ALLOW_HOSTED_MODEL_FALLBACK": "true",
            "OPENROUTER_API_KEY": "secret-value-never-returned",
            "OPENROUTER_MODEL": "configured/model",
        }
    ).route("strategy")
    summary = target.to_dict()

    assert target.provider == "openrouter"
    assert target.model == "configured/model"
    assert target.executable is True
    assert "secret-value-never-returned" not in str(summary)


def test_no_model_configuration_returns_non_executable_target() -> None:
    target = ModelRouter({}).route("classify")

    assert target.provider == "none"
    assert target.model is None
    assert target.executable is False


def test_learning_is_transparent_and_never_mutates_policy() -> None:
    summary = learning_summary(
        [
            {"event_type": "draft_prepared", "payload": {"strategy_id": "revenue"}},
            {"event_type": "approval_requested", "payload": {"strategy_id": "revenue"}},
            {"event_type": "approval_decided", "payload": {"strategy_id": "revenue", "approved": True}},
            {"event_type": "step_blocked", "payload": {"strategy_id": "revenue"}},
            {"event_type": "outcome_recorded", "payload": {"strategy_id": "revenue"}},
        ]
    )

    metrics = summary["strategies"][0]
    assert metrics["approval_rate"] == 1.0
    assert metrics["blocked"] == 1
    assert metrics["outcomes_recorded"] == 1
    assert summary["automatic_strategy_mutation"] is False
    assert summary["requires_human_review_for_policy_change"] is True
