"""Tests for the Dealix Autonomous Growth & Strategy Execution OS.

These assert the safety-critical guarantees: draft-only, approval-first,
forbidden actions blocked, external channels never auto-executed, and a full
orchestrator cycle producing only reviewable artifacts.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from dealix.autonomous_os import (
    AutonomousOS,
    ApprovalQueue,
    ApprovalState,
    ModelRouter,
    SafetyGate,
    StrategyRegistry,
)
from dealix.autonomous_os import integrations
from dealix.autonomous_os.execution_planner import ExecutionPlanner
from dealix.autonomous_os.growth_engine import GrowthContext, GrowthEngine
from dealix.autonomous_os.safety_gate import Route


# --------------------------- SafetyGate -----------------------------------
def test_gate_blocks_forbidden_actions():
    gate = SafetyGate(env={})
    for action in ("cold_outreach", "mass_send", "linkedin_automation", "auto_invoice"):
        decision = gate.evaluate(action=action)
        assert decision.route == Route.BLOCKED, action
        assert decision.blocked


def test_gate_routes_external_channels_to_approval():
    gate = SafetyGate(env={})
    for channel in ("whatsapp", "email", "sms", "linkedin"):
        decision = gate.evaluate(action="draft_followup", channel=channel, risk=0.1)
        assert decision.route == Route.APPROVAL, channel
        assert not decision.allowed_auto


def test_gate_high_risk_needs_approval():
    gate = SafetyGate(env={})
    assert gate.evaluate(action="draft_x", risk=0.4).route == Route.APPROVAL
    assert gate.evaluate(action="draft_x", risk=0.1).route == Route.AUTO_DRAFT


def test_gate_low_risk_internal_auto_draft():
    gate = SafetyGate(env={})
    decision = gate.evaluate(action="draft_proof_pack", kind="internal", risk=0.1)
    assert decision.route == Route.AUTO_DRAFT
    assert decision.allowed_auto


def test_gate_tripwire_raises_on_unsafe_env():
    unsafe = SafetyGate(env={"EXTERNAL_SEND_ENABLED": "true", "OUTBOUND_MODE": "draft_only"})
    with pytest.raises(RuntimeError):
        unsafe.assert_draft_only()


def test_gate_tripwire_ok_when_draft_only():
    SafetyGate(env={"OUTBOUND_MODE": "draft_only"}).assert_draft_only()  # no raise


# --------------------------- Registry -------------------------------------
def test_registry_loads_shipped_strategies():
    reg = StrategyRegistry().load()
    ids = {s.id for s in reg.all()}
    assert {"revenue_sprint", "saudi_market_access", "technical_trust"}.issubset(ids)
    # active() sorted by priority desc
    active = reg.active()
    assert active[0].priority >= active[-1].priority


def test_registry_rejects_duplicate_ids(tmp_path: Path):
    d = tmp_path / "s"
    d.mkdir()
    (d / "a.yaml").write_text("id: dup\nname: A\nsteps: []\n", encoding="utf-8")
    (d / "b.yaml").write_text("id: dup\nname: B\nsteps: []\n", encoding="utf-8")
    with pytest.raises(ValueError):
        StrategyRegistry(strategies_dir=d).load()


# --------------------------- Planner --------------------------------------
def test_planner_routes_revenue_sprint():
    reg = StrategyRegistry().load()
    planner = ExecutionPlanner(SafetyGate(env={}))
    plan = planner.plan(reg.get("revenue_sprint"))
    # internal low-risk drafts auto, whatsapp follow-up to approval
    assert len(plan.auto_steps) >= 2
    assert len(plan.approval_steps) >= 1
    assert all(s.channel != "whatsapp" for s in plan.auto_steps)


# --------------------------- Growth engine --------------------------------
def test_growth_engine_prioritises_proof_to_sprint():
    recs = GrowthEngine().recommend(GrowthContext(proof_assets_ready=3, booked_sprints=0))
    assert recs[0].offer == "transformation_diagnostic_sprint"
    assert recs[0].priority == 95


def test_growth_engine_always_returns_internal_content_action():
    recs = GrowthEngine().recommend(GrowthContext())
    assert any(r.kind == "internal" for r in recs)


# --------------------------- Model router ---------------------------------
def test_router_prefers_local_when_available():
    r = ModelRouter(env={"OLLAMA_HOST": "http://localhost:11434"})
    choice = r.route("strategy")
    assert choice.is_local
    assert choice.provider == "ollama"


def test_router_falls_back_to_hosted_when_no_local():
    r = ModelRouter(env={"DEEPSEEK_API_KEY": "present"})
    choice = r.route("draft")
    assert not choice.is_local
    assert choice.provider == "deepseek"
    assert "present" not in choice.endpoint  # never leaks the secret value


def test_router_default_is_local_target():
    choice = ModelRouter(env={}).route("default")
    assert choice.is_local  # deterministic local target for planning


# --------------------------- Approval queue -------------------------------
def test_approval_queue_submit_and_decide(tmp_path: Path):
    q = ApprovalQueue(tmp_path)
    item = q.submit(
        strategy_id="revenue_sprint",
        action="prepare_followup_drafts",
        draft="draft body",
        reason="external channel",
        channel="whatsapp",
    )
    assert len(q.list_pending()) == 1
    assert q.decide(item.id, approved=True, decided_by="founder")
    assert q.list_pending() == []
    assert q.stats()[ApprovalState.APPROVED.value] == 1


# --------------------------- Integrations ---------------------------------
def test_integrations_registry_is_honest():
    summ = integrations.summary()
    assert summ["total"] >= 40
    # No item falsely claims to be wired.
    assert integrations.by_status("wired") == []
    assert "ollama" in summ["core_stack"]


# --------------------------- Full orchestrator ----------------------------
def test_orchestrator_full_cycle_is_draft_only(tmp_path: Path):
    os_engine = AutonomousOS(runtime_root=tmp_path, env={"OUTBOUND_MODE": "draft_only"})
    summary = os_engine.run(growth_context={"proof_assets_ready": 2, "warm_leads": 5})

    assert summary["mode"] == "draft_only"
    assert summary["counters"]["drafted"] >= 1
    assert summary["counters"]["approval"] >= 1
    # Reports written.
    report_dir = tmp_path / "reports"
    assert any(report_dir.glob("autonomous-os-*.md"))
    assert any(report_dir.glob("autonomous-os-*.json"))
    # Proof trail exists and records a completed run.
    events = os_engine.proofs.read_all()
    assert any(e["event_type"] == "run_completed" for e in events)
    # Approval queue has real pending items; nothing was "sent".
    assert os_engine.approvals.stats()["pending"] >= 1


def test_orchestrator_blocks_forbidden_strategy_step(tmp_path: Path):
    strat_dir = tmp_path / "strategies"
    strat_dir.mkdir()
    (strat_dir / "bad.yaml").write_text(
        "id: bad\nname: Bad\nenabled: true\npriority: 10\nsteps:\n"
        "  - action: cold_outreach\n    kind: external_draft\n    risk: 0.9\n",
        encoding="utf-8",
    )
    os_engine = AutonomousOS(
        runtime_root=tmp_path / "rt", strategies_dir=strat_dir, env={"OUTBOUND_MODE": "draft_only"}
    )
    summary = os_engine.run()
    assert summary["counters"]["blocked"] == 1
    assert summary["counters"]["approval"] == 0
    # Nothing forbidden reached the approval queue.
    assert os_engine.approvals.stats()["pending"] == 0


def test_runtime_outputs_are_json_serialisable(tmp_path: Path):
    os_engine = AutonomousOS(runtime_root=tmp_path, env={"OUTBOUND_MODE": "draft_only"})
    summary = os_engine.run()
    json.dumps(summary)  # must not raise
