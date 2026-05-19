"""Tests for Full Ops stage business logic + lead-driven runs (Wave 20)."""

from __future__ import annotations

import json

import pytest

from auto_client_acquisition.agent_os import clear_agent_registry_for_tests
from auto_client_acquisition.full_ops_os import audit_store
from auto_client_acquisition.full_ops_os.orchestrator import FullOpsOrchestrator
from auto_client_acquisition.full_ops_os.stage_logic import run_stage_logic
from auto_client_acquisition.full_ops_os.stages import Stage

STRONG_LEAD = {
    "company_name": "Acme Trading Co",
    "source": "warm_referral",
    "sector": "technology",
    "city": "riyadh",
    "employee_count": 60,
    "notes": "Long-standing relationship with substantive context noted here.",
    "relationship_status": "warm_intro",
    "request_text": "our leads go cold, there is no follow-up owner, we can't prove outcomes",
    "owner_present": True,
    "data_available": True,
    "accepts_governance": True,
    "has_budget": True,
    "retainer_interest": True,
}


@pytest.fixture(autouse=True)
def _isolated(tmp_path, monkeypatch):
    monkeypatch.setenv("DEALIX_FULL_OPS_AUDIT_PATH", str(tmp_path / "audit.jsonl"))
    monkeypatch.setenv("DEALIX_AGENT_REGISTRY_PATH", str(tmp_path / "agents.jsonl"))
    audit_store.clear_for_test()
    clear_agent_registry_for_tests()
    yield
    audit_store.clear_for_test()
    clear_agent_registry_for_tests()


def test_signal_intake_accepts_complete_lead() -> None:
    out = run_stage_logic(Stage.SIGNAL_INTAKE, STRONG_LEAD, {})
    assert out.metrics["accepted"] is True


def test_signal_intake_rejects_empty_lead() -> None:
    out = run_stage_logic(Stage.SIGNAL_INTAKE, {}, {})
    assert out.metrics["accepted"] is False
    assert "company_name" in out.metrics["missing_fields"]


def test_scoring_produces_a_score() -> None:
    out = run_stage_logic(Stage.SCORING, STRONG_LEAD, {})
    assert isinstance(out.metrics["score"], int)
    assert out.metrics["score"] >= 70


def test_pain_extraction_finds_signals() -> None:
    out = run_stage_logic(Stage.PAIN_EXTRACTION, STRONG_LEAD, {})
    assert out.metrics["pain_clear"] is True
    assert out.metrics["signal_count"] >= 2


def test_qualification_accepts_strong_lead() -> None:
    state = {
        Stage.SCORING.name: {"score": 100},
        Stage.PAIN_EXTRACTION.name: {"pain_clear": True},
    }
    out = run_stage_logic(Stage.QUALIFICATION, STRONG_LEAD, state)
    assert out.metrics["decision"] == "accept"


def test_prioritization_tiers_a_strong_lead_p1() -> None:
    state = {
        Stage.SCORING.name: {"score": 100},
        Stage.QUALIFICATION.name: {"decision": "accept"},
    }
    out = run_stage_logic(Stage.PRIORITIZATION, STRONG_LEAD, state)
    assert out.metrics["priority"] == "P1"


def test_draft_generation_produces_bilingual_draft() -> None:
    out = run_stage_logic(Stage.DRAFT_GENERATION, STRONG_LEAD, {})
    draft = out.state["draft"]
    assert draft["body_ar"] and draft["body_en"]
    assert out.metrics["draft_generated"] is True


def test_full_run_with_lead_accumulates_state() -> None:
    orch = FullOpsOrchestrator()
    run = orch.start_run(customer_id="acme", lead=STRONG_LEAD)
    orch.run_all(run.run_id)
    completed = orch.repo.get_run(tenant_id="default", run_id=run.run_id)
    state = completed.metadata["state"]
    assert state[Stage.SCORING.name]["score"] >= 70
    assert state[Stage.QUALIFICATION.name]["decision"] == "accept"
    assert state[Stage.PRIORITIZATION.name]["priority"] == "P1"


def test_approval_gate_queues_founder_approval() -> None:
    orch = FullOpsOrchestrator()
    run = orch.start_run(customer_id="acme", lead=STRONG_LEAD)
    result = orch.run_stage(run.run_id, Stage.APPROVAL_GATE)
    assert result.auto_executed is False
    assert result.approval_ticket_id is not None
    assert result.approval_request_id is not None


def test_audit_trail_carries_no_raw_pii() -> None:
    orch = FullOpsOrchestrator()
    run = orch.start_run(customer_id="acme", lead=STRONG_LEAD)
    orch.run_all(run.run_id)
    trail = orch.audit_trail(run.run_id)
    blob = json.dumps([e.model_dump(mode="json") for e in trail], ensure_ascii=False)
    # Raw request text and company name must never reach the audit log.
    assert "leads go cold" not in blob
    assert "Acme Trading Co" not in blob
