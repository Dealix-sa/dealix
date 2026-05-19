"""Tests for the Full Ops runtime agent pyramid (Wave 19)."""

from __future__ import annotations

import pytest

from auto_client_acquisition.agent_os import (
    FORBIDDEN_TOOLS_MVP,
    AutonomyLevel,
    clear_agent_registry_for_tests,
    get_agent,
    kill_agent,
)
from auto_client_acquisition.full_ops_os import audit_store
from auto_client_acquisition.full_ops_os.agents import (
    CONDUCTOR_ID,
    FULL_OPS_AGENT_SPECS,
    register_full_ops_agents,
)
from auto_client_acquisition.full_ops_os.auto_exec import (
    APPROVAL_REQUIRED,
    AUTO_EXECUTE,
    BLOCKED,
    governed_dispatch,
)
from auto_client_acquisition.full_ops_os.dispatcher import (
    agent_for_stage,
    verify_agent_pyramid_integrity,
)
from auto_client_acquisition.full_ops_os.stages import STAGES, Stage


@pytest.fixture(autouse=True)
def _isolated(tmp_path, monkeypatch):
    monkeypatch.setenv("DEALIX_AGENT_REGISTRY_PATH", str(tmp_path / "agents.jsonl"))
    monkeypatch.setenv("DEALIX_FULL_OPS_AUDIT_PATH", str(tmp_path / "audit.jsonl"))
    clear_agent_registry_for_tests()
    audit_store.clear_for_test()
    yield
    clear_agent_registry_for_tests()
    audit_store.clear_for_test()


def test_registers_full_pyramid() -> None:
    cards = register_full_ops_agents()
    assert len(cards) == 18
    assert len(FULL_OPS_AGENT_SPECS) == 18


def test_register_is_idempotent() -> None:
    register_full_ops_agents()
    cards = register_full_ops_agents()
    assert len(cards) == 18  # no duplicate-registration error


def test_conductor_is_l4_with_kill_switch() -> None:
    register_full_ops_agents()
    conductor = get_agent(CONDUCTOR_ID)
    assert conductor is not None
    assert conductor.autonomy_level == int(AutonomyLevel.L4_AUTO_WITH_AUDIT)
    assert conductor.kill_switch_owner.strip() != ""


def test_tier2_workers_capped_at_l2() -> None:
    register_full_ops_agents()
    for spec in FULL_OPS_AGENT_SPECS:
        if spec.tier != 2:
            continue
        card = get_agent(spec.agent_id)
        assert card is not None
        assert card.autonomy_level <= int(AutonomyLevel.L2_DRAFT)


def test_no_agent_holds_a_forbidden_tool() -> None:
    register_full_ops_agents()
    for spec in FULL_OPS_AGENT_SPECS:
        card = get_agent(spec.agent_id)
        assert card is not None
        assert not (set(card.allowed_tools) & FORBIDDEN_TOOLS_MVP)


def test_integrity_clean_after_registration() -> None:
    register_full_ops_agents()
    assert verify_agent_pyramid_integrity() == []


def test_integrity_flags_unregistered_pyramid() -> None:
    issues = verify_agent_pyramid_integrity()
    assert len(issues) >= 18  # nothing registered yet


def test_integrity_flags_killed_agent() -> None:
    register_full_ops_agents()
    kill_agent("scoring-agent", reason="test")
    issues = verify_agent_pyramid_integrity()
    assert any(i.agent_id == "scoring-agent" for i in issues)


def test_every_stage_maps_to_a_registered_worker() -> None:
    register_full_ops_agents()
    for spec in STAGES:
        worker = agent_for_stage(spec.stage)
        assert get_agent(worker) is not None


def test_governed_dispatch_auto_executes_internal_stage() -> None:
    register_full_ops_agents()
    decision = governed_dispatch(Stage.SIGNAL_INTAKE)
    assert decision.mode == AUTO_EXECUTE
    assert decision.worker_agent == "lead-intake-agent"
    assert decision.conductor_agent == CONDUCTOR_ID


def test_governed_dispatch_gates_external_stage() -> None:
    register_full_ops_agents()
    decision = governed_dispatch(Stage.APPROVAL_GATE)
    assert decision.mode == APPROVAL_REQUIRED


def test_governed_dispatch_blocks_when_worker_killed() -> None:
    register_full_ops_agents()
    kill_agent("lead-intake-agent", reason="test")
    decision = governed_dispatch(Stage.SIGNAL_INTAKE)
    assert decision.mode == BLOCKED
    assert "worker_killed" in decision.reason


def test_governed_dispatch_blocks_when_conductor_killed() -> None:
    register_full_ops_agents()
    kill_agent(CONDUCTOR_ID, reason="test")
    decision = governed_dispatch(Stage.SIGNAL_INTAKE)
    assert decision.mode == BLOCKED
    assert "conductor_killed" in decision.reason
