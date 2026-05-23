"""Tests for `dealix/trust/policy_engine.py` — composition of Trust modules."""

from __future__ import annotations

import pytest

from dealix.trust.evidence_pack import approve, new_pack
from dealix.trust.policy_engine import PolicyViolation, assert_send, evaluate_send
from dealix.trust.suppression import SuppressionList, set_default_list


@pytest.fixture(autouse=True)
def _reset_suppression() -> None:
    # Tests must not leak suppression state.
    set_default_list(SuppressionList())
    yield
    set_default_list(SuppressionList())


def test_a0_internal_action_passes_with_no_approvals() -> None:
    result = evaluate_send(
        action_class="message_draft_generation",
        text="Draft for founder review.",
    )
    assert result.passed


def test_a1_outreach_without_founder_fails() -> None:
    result = evaluate_send(
        action_class="sending_first_outreach",
        text="Hello — a specific reason for outreach.",
        recipient_type="email",
        recipient_value="prospect@example.com",
        approvals=[],
    )
    assert not result.passed
    assert any("founder approval" in b for b in result.blockers)


def test_a1_outreach_with_founder_passes() -> None:
    result = evaluate_send(
        action_class="sending_first_outreach",
        text="Hello — a specific reason for outreach.",
        recipient_type="email",
        recipient_value="prospect@example.com",
        approvals=["founder"],
    )
    assert result.passed, result.blockers


def test_suppression_blocks_send_even_with_approval() -> None:
    lst = SuppressionList()
    lst.add(
        "email",
        "prospect@example.com",
        reason="opt-out",
        source="reply",
        owner="founder",
    )
    set_default_list(lst)
    result = evaluate_send(
        action_class="sending_first_outreach",
        text="Hello — a specific reason for outreach.",
        recipient_type="email",
        recipient_value="prospect@example.com",
        approvals=["founder"],
    )
    assert not result.passed
    assert any("suppression" in b.lower() for b in result.blockers)


def test_a3_claim_blocked_without_evidence_pack() -> None:
    result = evaluate_send(
        action_class="public_claim_post",
        text="In our last 3 sprints, delivery time averaged 6 days.",
        approvals=["founder"],
        evidence_pack=None,
    )
    assert not result.passed
    assert any("evidence pack" in b.lower() for b in result.blockers)


def test_a3_claim_passes_with_complete_evidence_pack() -> None:
    pack = new_pack("EP-T", "In our last 3 sprints, delivery time averaged 6 days.")
    pack.sources.append("internal:sprint_log")
    pack.methodology = "Aggregated from n=3 sprints."
    approve(pack, "founder")

    result = evaluate_send(
        action_class="public_claim_post",
        text="In our last 3 sprints, delivery time averaged 6 days.",
        approvals=["founder"],
        evidence_pack=pack,
    )
    assert result.passed, result.blockers


def test_a4_action_always_fails() -> None:
    result = evaluate_send(
        action_class="cold_whatsapp",
        text="hi",
        approvals=["founder", "advisor"],
    )
    assert not result.passed
    assert any("prohibited" in b.lower() for b in result.blockers)


def test_claim_guard_blocks_overclaim_in_outreach() -> None:
    result = evaluate_send(
        action_class="sending_first_outreach",
        text="Our industry-leading 10x AI guarantees results.",
        recipient_type="email",
        recipient_value="prospect@example.com",
        approvals=["founder"],
    )
    assert not result.passed
    assert any("claim_guard" in b for b in result.blockers)


def test_assert_send_raises_on_failure() -> None:
    with pytest.raises(PolicyViolation):
        assert_send(
            action_class="cold_whatsapp",
            text="hi",
        )
