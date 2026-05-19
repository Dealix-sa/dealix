"""Tests for the FullOpsOrchestrator spine (Wave 18)."""

from __future__ import annotations

import pytest

from auto_client_acquisition.agent_os import clear_agent_registry_for_tests
from auto_client_acquisition.full_ops_os import audit_store
from auto_client_acquisition.full_ops_os.orchestrator import (
    WORKFLOW_ID,
    FullOpsOrchestrator,
)
from auto_client_acquisition.full_ops_os.stages import STAGES, Stage


@pytest.fixture(autouse=True)
def _isolated(tmp_path, monkeypatch):
    monkeypatch.setenv("DEALIX_FULL_OPS_AUDIT_PATH", str(tmp_path / "audit.jsonl"))
    monkeypatch.setenv("DEALIX_AGENT_REGISTRY_PATH", str(tmp_path / "agents.jsonl"))
    audit_store.clear_for_test()
    clear_agent_registry_for_tests()
    yield
    audit_store.clear_for_test()
    clear_agent_registry_for_tests()


def _orch() -> FullOpsOrchestrator:
    return FullOpsOrchestrator()


def test_start_run_registers_run_and_audits() -> None:
    orch = _orch()
    run = orch.start_run(customer_id="acme")
    assert run.workflow_id == WORKFLOW_ID
    assert run.customer_id == "acme"
    assert run.state == "registered"
    trail = orch.audit_trail(run.run_id)
    assert any(e.action.value == "workflow.started" for e in trail)


def test_run_stage_auto_executes_internal_stage() -> None:
    orch = _orch()
    run = orch.start_run(customer_id="acme")
    result = orch.run_stage(run.run_id, Stage.SIGNAL_INTAKE)
    assert result.auto_executed is True
    assert result.approval_ticket_id is None
    assert result.gate.reason == "internal_safe"
    assert result.worker_agent == "lead-intake-agent"


def test_run_stage_attributes_worker_in_audit() -> None:
    orch = _orch()
    run = orch.start_run(customer_id="acme")
    result = orch.run_stage(run.run_id, Stage.SCORING)
    trail = orch.audit_trail(run.run_id)
    entry = next(e for e in trail if e.audit_id == result.audit_id)
    assert entry.details["worker_agent"] == "scoring-agent"


def test_approval_gate_stage_creates_approval_ticket() -> None:
    orch = _orch()
    run = orch.start_run(customer_id="acme")
    result = orch.run_stage(run.run_id, Stage.APPROVAL_GATE)
    assert result.auto_executed is False
    assert result.approval_ticket_id is not None
    ticket = orch.repo.get_ticket(
        tenant_id="default", ticket_id=result.approval_ticket_id
    )
    assert ticket.state == "pending"
    assert ticket.action_type == "outreach_send"


def test_run_all_runs_twelve_stages_and_completes() -> None:
    orch = _orch()
    run = orch.start_run(customer_id="acme")
    results = orch.run_all(run.run_id)
    assert len(results) == 12
    assert [r.stage for r in results] == [s.stage for s in STAGES]
    completed = orch.repo.get_run(tenant_id="default", run_id=run.run_id)
    assert completed.state == "completed"
    assert completed.current_step == Stage.LEARNING.name


def test_advance_progresses_sequentially() -> None:
    orch = _orch()
    run = orch.start_run(customer_id="acme")
    first = orch.advance(run.run_id)
    second = orch.advance(run.run_id)
    assert first.stage == Stage.SIGNAL_INTAKE
    assert second.stage == Stage.ENRICHMENT


def test_advance_after_completion_raises() -> None:
    orch = _orch()
    run = orch.start_run(customer_id="acme")
    orch.run_all(run.run_id)
    with pytest.raises(ValueError, match="already completed"):
        orch.advance(run.run_id)


def test_every_stage_writes_an_audit_entry() -> None:
    orch = _orch()
    run = orch.start_run(customer_id="acme")
    orch.run_all(run.run_id)
    trail = orch.audit_trail(run.run_id)
    # 1 started + 12 stages + 1 completed.
    assert len(trail) == 14
    assert all(e.workflow_id == run.run_id for e in trail)


def test_trace_returns_control_events_for_run() -> None:
    orch = _orch()
    run = orch.start_run(customer_id="acme")
    orch.run_stage(run.run_id, Stage.SIGNAL_INTAKE)
    events = orch.trace(run.run_id)
    assert len(events) >= 2  # workflow.registered + stage event
    assert all(ev.run_id == run.run_id for ev in events)


def test_approval_gate_audit_marks_escalated() -> None:
    orch = _orch()
    run = orch.start_run(customer_id="acme")
    result = orch.run_stage(run.run_id, Stage.APPROVAL_GATE)
    trail = orch.audit_trail(run.run_id)
    gate_entry = next(e for e in trail if e.audit_id == result.audit_id)
    assert gate_entry.action.value == "approval.requested"
    assert gate_entry.outcome == "escalated"
