"""Tests for the strategic-decision loop closure.

Covers update_decision_status (status-transition rows + latest-row
collapse) and the run_strategic_cycle reconciliation step that advances
a founder-approved decision out of pending_approval.
"""
from __future__ import annotations

import pytest

from auto_client_acquisition.strategy_autonomy import decision_ledger as dl


@pytest.fixture(autouse=True)
def _isolated_ledger(tmp_path, monkeypatch):
    monkeypatch.setenv(
        "DEALIX_STRATEGIC_DECISION_LEDGER_PATH",
        str(tmp_path / "strategic-decision-ledger.jsonl"),
    )
    dl.clear_for_test()
    yield
    dl.clear_for_test()


def _record_pending() -> dl.StrategicDecision:
    return dl.record_decision(
        cycle_id="sac_test",
        decision_type="hire",
        target="founder_hours_per_sprint",
        rationale_ar="ضغط على وقت المؤسس",
        rationale_en="founder time pressure",
        score=88.0,
        decision_band="SCALE",
        gate_ref="founder_overload",
        evidence=["founder_hours=9"],
        customer_id="loop_test",
        status="pending_approval",
        approval_id="appr_xyz",
    )


def test_update_decision_status_advances_to_approved() -> None:
    decision = _record_pending()
    updated = dl.update_decision_status(decision.decision_id, status="approved")
    assert updated is not None
    assert updated.status == "approved"
    assert dl.get_decision(decision.decision_id).status == "approved"


def test_query_collapses_to_latest_row() -> None:
    decision = _record_pending()
    dl.update_decision_status(decision.decision_id, status="approved")
    assert dl.query_decisions(status="pending_approval", customer_id="loop_test") == []
    approved = dl.query_decisions(status="approved", customer_id="loop_test")
    assert len(approved) == 1
    assert approved[0].decision_id == decision.decision_id


def test_update_unknown_decision_returns_none() -> None:
    assert dl.update_decision_status("sd_does_not_exist", status="approved") is None


def test_update_rejects_invalid_status() -> None:
    decision = _record_pending()
    with pytest.raises(ValueError):
        dl.update_decision_status(decision.decision_id, status="not_a_status")


def test_reconciliation_promotes_founder_approved_decision() -> None:
    """An irreversible decision approved in the store is reconciled to approved."""
    from auto_client_acquisition.approval_center import (
        ApprovalRequest,
        get_default_approval_store,
    )
    from auto_client_acquisition.strategy_autonomy.strategic_cycle import (
        _reconcile_pending_approvals,
    )

    store = get_default_approval_store()
    req = store.create(
        ApprovalRequest(
            object_type="strategic_decision",
            object_id="sd_x",
            action_type="strategic_decision",
            action_mode="approval_required",
            summary_ar="قرار",
            summary_en="decision",
            risk_level="high",
            proof_impact="strategic_cycle:test",
            customer_id="loop_test",
        )
    )
    decision = dl.record_decision(
        cycle_id="sac_test",
        decision_type="hire",
        target="founder_hours_per_sprint",
        rationale_ar="x",
        rationale_en="x",
        score=88.0,
        decision_band="SCALE",
        gate_ref="founder_overload",
        evidence=["founder_hours=9"],
        customer_id="loop_test",
        status="pending_approval",
        approval_id=req.approval_id,
    )
    store.approve(req.approval_id, "founder")

    class _Report:
        reconciled_decisions: dict = {}

    report = _Report()
    _reconcile_pending_approvals("loop_test", report, lambda *_: None)

    assert decision.decision_id in report.reconciled_decisions["approved"]
    assert dl.get_decision(decision.decision_id).status == "approved"
