from __future__ import annotations

from scripts.commercial.run_company_loop_simulation import load_registry, run_loop


def _customer_loop() -> dict:
    registry = load_registry()
    return next(loop for loop in registry["loops"] if loop["id"] == "customer_to_value")


def test_customer_to_value_is_executable_and_closed() -> None:
    loop = _customer_loop()

    assert loop["status"] == "executable_synthetic"
    assert loop["closure_targets"] == [
        "OutcomeEvent",
        "ProofEvent",
        "LearningEvent",
        "DailyCommand",
    ]
    assert loop["departments"] == [
        "operations",
        "customer_success",
        "support",
        "finance",
        "security",
        "executive",
    ]


def test_customer_to_value_has_complete_ordered_operating_path() -> None:
    loop = _customer_loop()
    stages = sorted(loop["stages"], key=lambda stage: stage["order"])

    assert [stage["order"] for stage in stages] == list(range(10, 151, 10))
    assert [stage["id"] for stage in stages] == [
        "customer_commitment_ready",
        "baseline_defined",
        "onboarding_plan_prepared",
        "onboarding_kickoff_approved",
        "access_readiness_validated",
        "activation_checkpoint",
        "adoption_health_measured",
        "risk_exception_triaged",
        "delivery_acceptance_prepared",
        "customer_acceptance_approved",
        "delivery_completion_proven",
        "customer_value_proven",
        "renewal_extension_prepared",
        "renewal_extension_approved",
        "customer_learning_closed",
    ]


def test_external_customer_actions_are_approval_gated() -> None:
    loop = _customer_loop()
    external_stages = [stage for stage in loop["stages"] if stage["external_effect"]]

    assert [stage["id"] for stage in external_stages] == [
        "onboarding_kickoff_approved",
        "customer_acceptance_approved",
        "renewal_extension_approved",
    ]
    assert all(stage["approval_required"] for stage in external_stages)
    assert all(stage["autonomy_level"] == 4 for stage in external_stages)


def test_synthetic_customer_run_withholds_real_value_truth() -> None:
    result = run_loop("customer_to_value", mode="synthetic")

    assert result["status"] == "completed_synthetic"
    assert result["external_actions_executed"] == 0
    assert len(result["stages"]) == 15
    assert len(result["approvals"]) == 3

    withheld = {(item["stage_id"], item["claim"]) for item in result["withheld_claims"]}
    assert ("delivery_completion_proven", "delivery_completed") in withheld
    assert ("customer_value_proven", "customer_value_proven") in withheld
    assert ("customer_value_proven", "customer_acceptance") in withheld
    assert ("customer_value_proven", "customer_value_evidence") in withheld

    command = result["daily_command"]
    assert command is not None
    assert command["recognized_revenue"] is False
    assert command["delivery_completed"] is False
    assert command["payment_proof_ids"] == []
    assert command["delivery_proof_ids"] == []


def test_synthetic_customer_learning_cannot_change_policy() -> None:
    result = run_loop("customer_to_value", mode="synthetic")

    assert len(result["learning_events"]) == 1
    learning = result["learning_events"][0]
    assert learning["approval_required"] is True
    assert learning["applied"] is False
    assert learning["official_policy_change_allowed"] is False
    assert learning["event_type"] == "delivery"


def test_draft_only_stops_before_first_customer_contact() -> None:
    result = run_loop("customer_to_value", mode="draft_only")

    assert result["status"] == "blocked_pending_approval"
    assert result["blocked_stage"] == "onboarding_kickoff_approved"
    assert result["external_actions_executed"] == 0
    assert [stage["stage_id"] for stage in result["stages"]] == [
        "customer_commitment_ready",
        "baseline_defined",
        "onboarding_plan_prepared",
        "onboarding_kickoff_approved",
    ]
    assert result["daily_command"] is None
