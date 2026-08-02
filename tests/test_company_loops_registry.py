from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOOPS_PATH = ROOT / "dealix/registers/company_loops_registry.json"
ENTITIES_PATH = ROOT / "dealix/registers/company_intelligence_entity_ownership.json"
RUNNER_PATH = ROOT / "scripts/commercial/run_company_loop_simulation.py"


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _load_runner():
    spec = importlib.util.spec_from_file_location("company_loop_runner", RUNNER_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_company_loop_registry_references_only_canonical_entities() -> None:
    loops = _load(LOOPS_PATH)
    entities = _load(ENTITIES_PATH)
    canonical = {entity["name"] for entity in entities["entities"]}

    for loop in loops["loops"]:
        for stage in loop.get("stages", []):
            assert set(stage["inputs"]) <= canonical
            assert set(stage["outputs"]) <= canonical


def test_loop_and_stage_identity_and_order_are_unique() -> None:
    registry = _load(LOOPS_PATH)
    loop_ids = [loop["id"] for loop in registry["loops"]]
    assert len(loop_ids) == len(set(loop_ids))

    for loop in registry["loops"]:
        if loop["status"].startswith("executable"):
            stage_ids = [stage["id"] for stage in loop["stages"]]
            stage_orders = [stage["order"] for stage in loop["stages"]]
            assert len(stage_ids) == len(set(stage_ids))
            assert len(stage_orders) == len(set(stage_orders))
            assert stage_orders == sorted(stage_orders)
        else:
            assert len(loop["stage_outline"]) >= 4


def test_external_effects_are_approval_gated() -> None:
    registry = _load(LOOPS_PATH)
    for loop in registry["loops"]:
        for stage in loop.get("stages", []):
            if stage["external_effect"]:
                assert stage["approval_required"] is True
                assert stage["autonomy_level"] <= 4
                assert "Approval" in stage["outputs"] or "Approval" in stage["inputs"]


def test_revenue_and_delivery_claims_require_proof() -> None:
    registry = _load(LOOPS_PATH)
    lead_to_cash = next(loop for loop in registry["loops"] if loop["id"] == "lead_to_cash")

    revenue_stage = next(
        stage for stage in lead_to_cash["stages"] if "revenue_recognized" in stage["recognition_effects"]
    )
    assert "payment_received" in revenue_stage["proof_requirements"]
    assert "ProofEvent" in revenue_stage["outputs"]

    delivery_stage = next(
        stage for stage in lead_to_cash["stages"] if "delivery_claim_allowed" in stage["recognition_effects"]
    )
    assert "delivery_completed" in delivery_stage["proof_requirements"]
    assert "ProofEvent" in delivery_stage["outputs"]


def test_every_loop_closes_with_outcome_learning_and_command() -> None:
    registry = _load(LOOPS_PATH)
    for loop in registry["loops"]:
        assert {"OutcomeEvent", "LearningEvent", "DailyCommand"} <= set(loop["closure_targets"])
        if loop["status"].startswith("executable"):
            outputs = {entity for stage in loop["stages"] for entity in stage["outputs"]}
            assert "OutcomeEvent" in outputs
            assert "LearningEvent" in outputs
            assert "DailyCommand" in outputs


def test_synthetic_lead_to_cash_completes_without_external_execution() -> None:
    runner = _load_runner()
    result = runner.run_loop("lead_to_cash", mode="synthetic", registry_path=LOOPS_PATH)

    assert result["status"] == "completed_synthetic"
    assert result["external_actions_executed"] == 0
    assert result["daily_command"] is not None
    assert any(proof["proof_type"] == "payment_received" for proof in result["proof_events"])
    assert any(proof["proof_type"] == "delivery_completed" for proof in result["proof_events"])
    assert result["learning_events"]
    assert all(approval["is_synthetic"] for approval in result["approvals"])


def test_draft_only_lead_to_cash_blocks_at_first_external_stage() -> None:
    runner = _load_runner()
    result = runner.run_loop("lead_to_cash", mode="draft_only", registry_path=LOOPS_PATH)

    assert result["status"] == "blocked_pending_approval"
    assert result["blocked_stage"] == "discovery_contact_approved"
    assert result["external_actions_executed"] == 0
