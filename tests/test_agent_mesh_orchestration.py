"""Tests for the agent_os mesh, task router, and runner."""

from __future__ import annotations

import pytest

from auto_client_acquisition.agent_os import (
    AGENT_ICP,
    AGENT_PAIN,
    AGENT_PROPOSAL,
    AGENT_QUALIFICATION,
    AGENT_SECTOR_INTEL,
    AgentCard,
    AgentLifecycleState,
    AgentMesh,
    AgentRun,
    AgentStatus,
    AutonomyLevel,
    MeshTrace,
    TaskPlan,
    agents_required_for_tier,
    new_card,
    plan_for_offer,
    run_agent,
    supported_offer_tiers,
)


def _active_card(agent_id: str) -> AgentCard:
    base = new_card(
        agent_id=agent_id,
        name=agent_id,
        owner="test_owner",
        purpose=f"test handler for {agent_id}",
        autonomy_level=AutonomyLevel.L2_DRAFT,
    )
    return AgentCard(
        agent_id=base.agent_id,
        name=base.name,
        owner=base.owner,
        purpose=base.purpose,
        autonomy_level=base.autonomy_level,
        status=AgentStatus.ACTIVE.value,
        allowed_tools=base.allowed_tools,
        kill_switch_owner=base.kill_switch_owner,
        notes=base.notes,
        created_at=base.created_at,
        killed_reason=base.killed_reason,
    )


class TestTaskRouter:
    def test_all_five_offer_tiers_are_planned(self) -> None:
        tiers = supported_offer_tiers()
        for expected in (
            "free_diagnostic",
            "sprint_499",
            "data_pack_1500",
            "managed_ops",
            "custom_ai",
        ):
            assert expected in tiers

    def test_plan_for_free_diagnostic_has_two_steps(self) -> None:
        plan = plan_for_offer(
            offer_tier="free_diagnostic",
            base_payload={"x": 1},
        )
        assert plan.offer_tier == "free_diagnostic"
        assert len(plan.tasks) == 2
        agent_ids = [t.agent_id for t in plan.tasks]
        assert AGENT_ICP in agent_ids
        assert AGENT_PAIN in agent_ids

    def test_plan_for_unknown_tier_raises(self) -> None:
        with pytest.raises(ValueError, match="unknown offer_tier"):
            plan_for_offer(offer_tier="unknown", base_payload={})

    def test_managed_ops_includes_retainer_recommendation(self) -> None:
        plan = plan_for_offer(
            offer_tier="managed_ops",
            base_payload={"x": 1},
        )
        agent_ids = [t.agent_id for t in plan.tasks]
        assert "retainer_recommend" in agent_ids

    def test_agents_required_for_tier_matches_plan(self) -> None:
        for tier in supported_offer_tiers():
            plan = plan_for_offer(offer_tier=tier, base_payload={})
            assert agents_required_for_tier(tier) == tuple(
                t.agent_id for t in plan.tasks
            )

    def test_sector_intel_is_optional_in_sprint_data_pack(self) -> None:
        plan = plan_for_offer(offer_tier="data_pack_1500", base_payload={})
        sector_tasks = [t for t in plan.tasks if t.agent_id == AGENT_SECTOR_INTEL]
        assert len(sector_tasks) == 1
        assert sector_tasks[0].optional is True


class TestAgentRunner:
    def test_runner_captures_ok_status(self) -> None:
        card = _active_card("a1")

        def handler(payload):
            return {"summary": "did the thing", "n": 7}

        run = run_agent(card=card, handler=handler, payload={"x": 1})
        assert run.status == "ok"
        assert run.error is None
        assert "did the thing" in run.output_summary

    def test_runner_captures_error(self) -> None:
        card = _active_card("a1")

        def boom(payload):
            raise RuntimeError("oh no")

        run = run_agent(card=card, handler=boom, payload={})
        assert run.status == "error"
        assert run.error == "oh no"

    def test_runner_blocks_killed_agent(self) -> None:
        card = AgentCard(
            agent_id="x",
            name="X",
            owner="o",
            purpose="p",
            status=AgentStatus.KILLED.value,
            killed_reason="testing",
        )
        run = run_agent(card=card, handler=lambda p: {}, payload={})
        assert run.status == "blocked"
        assert run.error == "agent_killed"

    def test_runner_blocks_non_production_lifecycle(self) -> None:
        card = _active_card("a2")
        run = run_agent(
            card=card,
            handler=lambda p: {},
            payload={},
            lifecycle_state=AgentLifecycleState.DRAFT,
        )
        assert run.status == "blocked"
        assert run.error == "lifecycle_blocked"


class TestAgentMesh:
    def test_mesh_registers_and_lists(self) -> None:
        mesh = AgentMesh()
        card = _active_card(AGENT_ICP)
        mesh.register(card=card, handler=lambda p: {"summary": "ok"})
        assert AGENT_ICP in mesh.registered_agents()
        assert mesh.has_agent(AGENT_ICP)

    def test_mesh_executes_full_plan(self) -> None:
        mesh = AgentMesh()
        for agent_id in (AGENT_ICP, AGENT_PAIN):
            mesh.register(
                card=_active_card(agent_id),
                handler=lambda payload, a=agent_id: {
                    "summary": f"ok from {a}",
                    "ar": f"تم من {a}",
                    "en": f"ok from {a}",
                },
            )
        plan = plan_for_offer(offer_tier="free_diagnostic", base_payload={})
        trace = mesh.execute(plan)
        assert isinstance(trace, MeshTrace)
        assert trace.all_ok
        assert len(trace.runs) == 2
        assert not trace.halted

    def test_mesh_halts_on_required_task_error(self) -> None:
        mesh = AgentMesh()
        mesh.register(
            card=_active_card(AGENT_ICP),
            handler=lambda p: (_ for _ in ()).throw(RuntimeError("boom")),
        )
        mesh.register(
            card=_active_card(AGENT_PAIN),
            handler=lambda p: {"summary": "ok"},
        )
        plan = plan_for_offer(offer_tier="free_diagnostic", base_payload={})
        trace = mesh.execute(plan)
        assert trace.halted
        assert trace.halt_reason is not None
        assert AGENT_ICP in trace.halt_reason

    def test_mesh_continues_on_optional_task_failure(self) -> None:
        mesh = AgentMesh()
        for agent_id in (AGENT_ICP, AGENT_PAIN, AGENT_QUALIFICATION, AGENT_PROPOSAL):
            mesh.register(
                card=_active_card(agent_id),
                handler=lambda p, a=agent_id: {"summary": f"ok from {a}"},
            )
        # The sector_intel agent is optional in the data_pack_1500 pipeline.
        mesh.register(
            card=_active_card(AGENT_SECTOR_INTEL),
            handler=lambda p: (_ for _ in ()).throw(RuntimeError("sector down")),
        )
        plan = plan_for_offer(offer_tier="data_pack_1500", base_payload={})
        trace = mesh.execute(plan)
        # Should NOT halt — sector_intel failure is optional.
        assert not trace.halted
        sector_runs = trace.by_agent_id(AGENT_SECTOR_INTEL)
        assert len(sector_runs) == 1
        assert sector_runs[0].status == "error"

    def test_mesh_blocks_on_missing_handler(self) -> None:
        mesh = AgentMesh()
        # No handlers registered.
        plan = plan_for_offer(offer_tier="free_diagnostic", base_payload={})
        trace = mesh.execute(plan)
        assert trace.halted
        assert "missing_handler" in (trace.halt_reason or "")
