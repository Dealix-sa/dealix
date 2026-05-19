"""Tests for the canonical lead lifecycle state machine (M8)."""
from __future__ import annotations

from auto_client_acquisition.sales_os.lead_lifecycle import (
    LeadLifecycleStage,
    advance,
    can_transition,
    from_intake_status,
    from_revenue_stage,
    is_terminal,
    next_stages,
)

S = LeadLifecycleStage


def test_forward_transition_allowed() -> None:
    ok, _ = can_transition(S.CAPTURED, S.QUALIFIED)
    assert ok
    ok, _ = can_transition(S.QUALIFIED, S.PAID)  # skipping forward is allowed
    assert ok


def test_backward_transition_blocked() -> None:
    ok, reason = can_transition(S.PROPOSAL, S.QUALIFIED)
    assert not ok
    assert "forward-only" in reason


def test_same_stage_is_noop() -> None:
    ok, reason = can_transition(S.ENGAGED, S.ENGAGED)
    assert not ok
    assert "no-op" in reason


def test_lost_reachable_from_anywhere() -> None:
    for stage in (S.CAPTURED, S.MEETING, S.DELIVERING, S.RETAINED):
        ok, _ = can_transition(stage, S.LOST)
        assert ok, f"{stage} should be able to go to lost"


def test_terminal_blocks_all_transitions() -> None:
    assert is_terminal(S.LOST)
    ok, reason = can_transition(S.LOST, S.CAPTURED)
    assert not ok
    assert "terminal" in reason


def test_next_stages_includes_lost_and_forward_only() -> None:
    nxt = next_stages(S.MEETING)
    assert S.LOST in nxt
    assert S.PROPOSAL in nxt
    assert S.CAPTURED not in nxt  # backward excluded
    assert next_stages(S.LOST) == []


def test_intake_status_mapping() -> None:
    assert from_intake_status("new") == S.CAPTURED
    assert from_intake_status("won") == S.RETAINED
    assert from_intake_status("disqualified") == S.LOST
    assert from_intake_status("garbage") == S.CAPTURED  # safe default


def test_revenue_stage_mapping() -> None:
    assert from_revenue_stage("invoice_paid") == S.PAID
    assert from_revenue_stage("proof_pack_sent") == S.PROOF_DELIVERED
    assert from_revenue_stage("retainer_candidate") == S.RETAINED
    assert from_revenue_stage("closed_lost") == S.LOST


def test_advance_returns_transition_result() -> None:
    ok_result = advance(
        lead_id="lead_1", current=S.CAPTURED, target=S.QUALIFIED, actor="founder"
    )
    assert ok_result.allowed
    assert ok_result.from_stage == "captured"
    assert ok_result.to_stage == "qualified"
    assert ok_result.actor == "founder"
    assert ok_result.occurred_at  # ISO timestamp present

    bad_result = advance(lead_id="lead_1", current=S.PAID, target=S.CAPTURED)
    assert not bad_result.allowed
