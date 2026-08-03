"""TestSprite-compatible acceptance entry for the governed Company Operator slice.

This module intentionally reuses the canonical Company Loops runner. It does not
introduce a second orchestrator, execute external effects, or create synthetic
financial or delivery truth.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNNER_PATH = ROOT / "scripts/commercial/run_company_loop_simulation.py"
REGISTRY_PATH = ROOT / "dealix/registers/company_loops_registry.json"


def _load_runner():
    spec = importlib.util.spec_from_file_location(
        "testsprite_company_operator_runner", RUNNER_PATH
    )
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_company_operator_vertical_slice_is_governed_and_evidence_safe() -> None:
    runner = _load_runner()
    result = runner.run_loop(
        "lead_to_cash", mode="synthetic", registry_path=REGISTRY_PATH
    )

    assert result["status"] == "completed_synthetic"
    assert result["external_actions_executed"] == 0
    assert result["daily_command"] is not None

    command = result["daily_command"]
    assert command["tenant_id"]
    assert command["recognized_revenue"] is False
    assert command["delivery_completed"] is False
    assert command["payment_proof_ids"] == []
    assert command["delivery_proof_ids"] == []

    withheld = {item["claim"] for item in result["withheld_claims"]}
    assert withheld == {"payment_received", "delivery_completed"}
    assert result["learning_events"]
    assert all(item["approval_required"] for item in result["learning_events"])
    assert all(item["applied"] is False for item in result["learning_events"])


def test_company_operator_realistic_mode_stops_before_external_effect() -> None:
    runner = _load_runner()
    result = runner.run_loop(
        "lead_to_cash", mode="draft_only", registry_path=REGISTRY_PATH
    )

    assert result["status"] == "blocked_pending_approval"
    assert result["blocked_stage"] == "discovery_contact_approved"
    assert result["external_actions_executed"] == 0
