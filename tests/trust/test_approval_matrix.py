"""Tests for the Company OS approval matrix.

Covers the canonical mapping in `docs/trust/APPROVAL_MATRIX.md`.
"""

from __future__ import annotations

import pytest

from dealix.trust.approval_matrix import (
    ApprovalRequired,
    ApprovalTier,
    ProhibitedAction,
    all_actions,
    entry_for,
    require_approval,
    tier_for,
)


def test_known_actions_have_expected_tiers() -> None:
    assert tier_for("internal_lead_scoring") == ApprovalTier.A0
    assert tier_for("sending_first_outreach") == ApprovalTier.A1
    assert tier_for("sending_followup") == ApprovalTier.A2
    assert tier_for("public_claim_post") == ApprovalTier.A3
    assert tier_for("refund_or_credit") == ApprovalTier.A4
    assert tier_for("compliance_claim") == ApprovalTier.A4
    assert tier_for("cold_whatsapp") == ApprovalTier.A4


def test_unknown_action_defaults_to_a4() -> None:
    """Refusing the unknown is the safe default — `DEALIX_DECISION_RULES.md`."""
    assert tier_for("something_we_have_never_seen") == ApprovalTier.A4


def test_a0_actions_need_no_approval() -> None:
    # Should not raise even with no approvals supplied.
    require_approval("internal_lead_scoring")
    require_approval("lead_enrichment")
    require_approval("message_draft_generation")


def test_a1_requires_founder() -> None:
    with pytest.raises(ApprovalRequired):
        require_approval("sending_first_outreach", approvals=[])
    # With founder, should pass.
    require_approval("sending_first_outreach", approvals=["founder"])


def test_a3_requires_evidence_pack() -> None:
    with pytest.raises(ApprovalRequired):
        require_approval(
            "public_claim_post", approvals=["founder"], has_evidence_pack=False
        )
    require_approval(
        "public_claim_post", approvals=["founder"], has_evidence_pack=True
    )


def test_a4_always_raises_prohibited() -> None:
    with pytest.raises(ProhibitedAction):
        require_approval("refund_or_credit", approvals=["founder", "advisor"])
    with pytest.raises(ProhibitedAction):
        require_approval("contract_change", approvals=["founder", "advisor"])
    with pytest.raises(ProhibitedAction):
        require_approval("cold_whatsapp", approvals=["founder", "advisor"])


def test_entry_for_unknown_returns_a4_default() -> None:
    e = entry_for("unknown_action_xyz")
    assert e.tier == ApprovalTier.A4
    assert e.founder_required is True
    assert e.advisor_required is True
    assert "unknown" in e.note.lower()


def test_matrix_inventory_is_nonempty() -> None:
    actions = list(all_actions())
    assert len(actions) >= 10
    # Every known action class returns a non-default entry.
    for a in actions:
        e = entry_for(a)
        assert e.action_class == a
