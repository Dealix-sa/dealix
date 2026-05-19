"""Tests for the Full Ops auto-execution gate — the safety spine."""

from __future__ import annotations

from auto_client_acquisition.full_ops_os.gate import (
    auto_exec_allowed,
    evaluate_gate,
)

# Internal-safe actions that MUST auto-execute (A0, R0/R1, S0-S2).
_AUTO_ACTIONS = [
    "lead_intake",
    "enrichment_query",
    "icp_match",
    "pain_extract",
    "qualification_questions",
    "pipeline_prioritize",
    "proposal_generate_draft",
    "delivery_step",
    "proof_pack_assemble",
    "expansion_assess",
    "learning_capture",
]

# External / high-stakes actions that MUST be gated.
_GATED_ACTIONS = [
    "outreach_send",
    "proposal_send",
    "followup_send",
    "booking_schedule",
    "content_publish",
]

# Actions that may never auto-execute under any classification.
_NEVER_AUTO = [
    "pricing_offer_commit",
    "contract_change",
    "nda_send",
    "payment_terms_change",
    "regulator_communication",
    "sensitive_data_export",
    "market_facing_statement",
]


def test_internal_safe_actions_auto_execute() -> None:
    for action in _AUTO_ACTIONS:
        assert auto_exec_allowed(action) is True, f"{action} should auto-execute"
        assert evaluate_gate(action).reason == "internal_safe"


def test_external_actions_are_gated() -> None:
    for action in _GATED_ACTIONS:
        assert auto_exec_allowed(action) is False, f"{action} must be gated"
        assert evaluate_gate(action).reason.startswith("approval_required")


def test_never_auto_actions_are_blocked() -> None:
    for action in _NEVER_AUTO:
        decision = evaluate_gate(action)
        assert decision.auto_exec_allowed is False
        assert decision.reason == "never_auto_execute"


def test_unknown_action_falls_back_to_gated() -> None:
    # classify() returns the safe default (A2, R2, S2) for unknown actions.
    decision = evaluate_gate("some_unclassified_action")
    assert decision.auto_exec_allowed is False
    assert decision.approval_class.value == "A2"


def test_gate_decision_to_dict_round_trips() -> None:
    payload = evaluate_gate("lead_intake").to_dict()
    assert payload["action_type"] == "lead_intake"
    assert payload["auto_exec_allowed"] is True
    assert payload["approval_class"] == "A0"
