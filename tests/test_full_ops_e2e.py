"""End-to-end test: a full 12-stage Full Ops run (Wave 21)."""

from __future__ import annotations

import pytest

from auto_client_acquisition.agent_os import clear_agent_registry_for_tests
from auto_client_acquisition.full_ops_os import audit_store
from auto_client_acquisition.full_ops_os.orchestrator import FullOpsOrchestrator
from auto_client_acquisition.full_ops_os.stages import STAGES, Stage

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

WEAK_LEAD = {"company_name": "Tiny Co", "source": "cold_list"}


@pytest.fixture(autouse=True)
def _isolated(tmp_path, monkeypatch):
    monkeypatch.setenv("DEALIX_FULL_OPS_AUDIT_PATH", str(tmp_path / "audit.jsonl"))
    monkeypatch.setenv("DEALIX_AGENT_REGISTRY_PATH", str(tmp_path / "agents.jsonl"))
    audit_store.clear_for_test()
    clear_agent_registry_for_tests()
    yield
    audit_store.clear_for_test()
    clear_agent_registry_for_tests()


def test_strong_lead_runs_all_twelve_stages() -> None:
    orch = FullOpsOrchestrator()
    run = orch.start_run(customer_id="acme", lead=STRONG_LEAD)
    results = orch.run_all(run.run_id)
    assert [r.stage for r in results] == [s.stage for s in STAGES]
    completed = orch.repo.get_run(tenant_id="default", run_id=run.run_id)
    assert completed.state == "completed"


def test_strong_lead_produces_a_proof_pack() -> None:
    """Non-negotiable #10 — no project without a Proof Pack."""
    orch = FullOpsOrchestrator()
    run = orch.start_run(customer_id="acme", lead=STRONG_LEAD)
    orch.run_all(run.run_id)
    proof = orch.repo.get_run(
        tenant_id="default", run_id=run.run_id
    ).metadata["state"][Stage.PROOF.name]
    assert proof["proof_score"] >= 70
    assert proof["proof_band"] in ("sales_support", "case_candidate")


def test_strong_lead_registers_a_capital_asset() -> None:
    """Non-negotiable #11 — no project without a Capital Asset."""
    orch = FullOpsOrchestrator()
    run = orch.start_run(customer_id="acme", lead=STRONG_LEAD)
    orch.run_all(run.run_id)
    learning = orch.repo.get_run(
        tenant_id="default", run_id=run.run_id
    ).metadata["state"][Stage.LEARNING.name]
    assert learning["capital_asset_candidate"]


def test_strong_lead_is_retainer_ready() -> None:
    orch = FullOpsOrchestrator()
    run = orch.start_run(customer_id="acme", lead=STRONG_LEAD)
    orch.run_all(run.run_id)
    expansion = orch.repo.get_run(
        tenant_id="default", run_id=run.run_id
    ).metadata["state"][Stage.EXPANSION.name]
    assert expansion["retainer_ready"] is True


def test_e2e_audit_has_one_entry_per_transition() -> None:
    orch = FullOpsOrchestrator()
    run = orch.start_run(customer_id="acme", lead=STRONG_LEAD)
    orch.run_all(run.run_id)
    trail = orch.audit_trail(run.run_id)
    # 1 started + 12 stages + 1 completed.
    assert len(trail) == 14


def test_only_the_approval_gate_stage_is_gated() -> None:
    orch = FullOpsOrchestrator()
    run = orch.start_run(customer_id="acme", lead=STRONG_LEAD)
    results = orch.run_all(run.run_id)
    gated = [r for r in results if not r.auto_executed]
    assert len(gated) == 1
    assert gated[0].stage == Stage.APPROVAL_GATE


def test_weak_lead_still_completes_with_lower_proof() -> None:
    orch = FullOpsOrchestrator()
    run = orch.start_run(customer_id="tiny", lead=WEAK_LEAD)
    orch.run_all(run.run_id)
    completed = orch.repo.get_run(tenant_id="default", run_id=run.run_id)
    assert completed.state == "completed"
    proof = completed.metadata["state"][Stage.PROOF.name]
    weak_proof = completed.metadata["state"][Stage.EXPANSION.name]
    # A weak lead must not be retainer-ready.
    assert weak_proof["retainer_ready"] is False
    assert proof["proof_score"] < 70
