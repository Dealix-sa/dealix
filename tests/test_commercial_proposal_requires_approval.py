"""Proposal Factory produces briefs (not binding offers) and requires approval."""

from __future__ import annotations

import pytest

from app.commercial import proposal_factory, safety


@pytest.fixture(autouse=True)
def _clear_flags(monkeypatch):
    for key in safety.SAFE_DEFAULT_FLAGS:
        monkeypatch.delenv(key, raising=False)
    yield


def test_brief_requires_approval_and_no_final_price():
    brief = proposal_factory.build_proposal_brief("c1", "sales_prospecting")
    assert brief.approval_required is True
    assert brief.final_price_allowed is False
    assert brief.status == "draft"


def test_brief_has_required_sections():
    brief = proposal_factory.build_proposal_brief("c1", "proposal_push")
    assert brief.scope
    assert brief.deliverables
    assert brief.pricing_range_sar
    assert brief.out_of_scope
    assert brief.acceptance_criteria
    assert brief.timeline


def test_out_of_scope_blocks_guarantees_and_cold_whatsapp():
    brief = proposal_factory.build_proposal_brief("c1")
    joined = " ".join(brief.out_of_scope).lower()
    assert "guaranteed" in joined
    assert "cold whatsapp" in joined


def test_finalize_proposal_denied_by_default():
    decision = safety.can_finalize_proposal({}, account={})
    assert decision.allowed is False
    assert "founder_pricing_approval" in decision.required_approvals


def test_finalize_proposal_needs_flag_and_approval(monkeypatch):
    monkeypatch.setenv("PROPOSAL_FINALIZATION_ENABLED", "true")
    decision = safety.can_finalize_proposal(
        {"founder_approved": True, "pricing_within_guardrails": True}, account={}
    )
    assert decision.allowed is True
