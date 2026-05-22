"""Tests for the multi-step approver chain (M14, additive).

Critical invariant: ``approver_chain == []`` (the default) MUST behave
identically to before — all existing approval tests must stay green.
"""
from __future__ import annotations

import pytest

from auto_client_acquisition.approval_center.approval_store import ApprovalStore
from auto_client_acquisition.approval_center.schemas import (
    ApprovalRequest,
    ApprovalStatus,
)


def _req(**overrides: object) -> ApprovalRequest:
    base = dict(
        object_type="test",
        object_id="o1",
        action_type="draft_email",
        action_mode="approval_required",
        channel="email",
        risk_level="low",
    )
    base.update(overrides)
    return ApprovalRequest(**base)  # type: ignore[arg-type]


# ─── 1. empty chain → single-step (regression-safe) ─────────────


def test_empty_chain_single_step_flips_to_approved() -> None:
    store = ApprovalStore()
    req = store.create(_req())
    out = store.approve(req.approval_id, who="founder")
    assert out.status == ApprovalStatus.APPROVED
    assert out.chain_position == 0  # untouched when no chain
    # One audit entry, action "approve" (not "approve_chain_step")
    assert any(e.get("action") == "approve" for e in out.edit_history)
    assert not any(e.get("action") == "approve_chain_step" for e in out.edit_history)


# ─── 2. multi-step chain ────────────────────────────────────────


def test_two_step_chain_requires_two_approvals() -> None:
    store = ApprovalStore()
    req = store.create(_req(approver_chain=["legal", "founder"]))

    # First approval — chain advances but status stays PENDING
    mid = store.approve(req.approval_id, who="legal_reviewer")
    assert mid.status == ApprovalStatus.PENDING
    assert mid.chain_position == 1
    assert any(e.get("action") == "approve_chain_step" for e in mid.edit_history)

    # Second (final) approval — flips to APPROVED
    final = store.approve(req.approval_id, who="founder")
    assert final.status == ApprovalStatus.APPROVED
    assert final.chain_position == 2
    # Two chain-step entries recorded
    chain_steps = [e for e in final.edit_history if e.get("action") == "approve_chain_step"]
    assert len(chain_steps) == 2


def test_three_step_chain_stays_pending_until_third_approval() -> None:
    store = ApprovalStore()
    req = store.create(_req(approver_chain=["legal", "finance", "ceo"]))
    for i, who in enumerate(["lawyer", "cfo"], start=1):
        out = store.approve(req.approval_id, who=who)
        assert out.status == ApprovalStatus.PENDING, f"step {i} should keep PENDING"
        assert out.chain_position == i
    final = store.approve(req.approval_id, who="ceo")
    assert final.status == ApprovalStatus.APPROVED
    assert final.chain_position == 3


# ─── 3. rejection terminates the chain at any step ─────────────


def test_reject_at_first_step_terminates_chain() -> None:
    store = ApprovalStore()
    req = store.create(_req(approver_chain=["legal", "founder"]))
    out = store.reject(req.approval_id, who="legal_reviewer", reason="non-compliant")
    assert out.status == ApprovalStatus.REJECTED
    assert out.reject_reason == "non-compliant"
    # Cannot approve a rejected request — chain is terminated
    with pytest.raises(ValueError):
        store.approve(req.approval_id, who="founder")


def test_reject_mid_chain_terminates() -> None:
    store = ApprovalStore()
    req = store.create(_req(approver_chain=["legal", "finance", "ceo"]))
    store.approve(req.approval_id, who="lawyer")  # step 1 ok
    rejected = store.reject(req.approval_id, who="cfo", reason="over budget")
    assert rejected.status == ApprovalStatus.REJECTED


# ─── 4. defaults preserve back-compat ───────────────────────────


def test_defaults_back_compat() -> None:
    """A request constructed without chain fields gets safe defaults."""
    req = _req()
    assert req.approver_chain == []
    assert req.chain_position == 0
