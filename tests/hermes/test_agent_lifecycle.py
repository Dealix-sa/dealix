"""Lifecycle + registry + promotion + restriction tests."""

from __future__ import annotations

import pytest

from dealix.hermes.agent_lifecycle import (
    AgentLifecycleStage,
    AgentRecord,
    AgentRegistry,
    PromotionError,
    RestrictionReason,
    evaluate_promotion_readiness,
    promote,
    restrict_agent,
    retire_agent,
    score_agent_risk,
)


def _seed_agent(registry: AgentRegistry, agent_id: str = "proposal_factory") -> AgentRecord:
    record = AgentRecord(
        agent_id=agent_id,
        owner="Sami",
        tool_scope=("read_approved_opportunity", "draft_proposal"),
        workspace_scope=("dealix_internal",),
        forbidden_capabilities=("send_external", "sign_contract"),
    )
    registry.register(record)
    return record


def test_lifecycle_starts_at_registered():
    reg = AgentRegistry()
    rec = _seed_agent(reg)
    assert rec.stage == AgentLifecycleStage.REGISTERED


def test_double_register_rejected():
    reg = AgentRegistry()
    _seed_agent(reg)
    with pytest.raises(ValueError):
        _seed_agent(reg)


def test_evaluate_promotion_blocks_underpowered_runs():
    reg = AgentRegistry()
    rec = _seed_agent(reg)
    rec.stage = AgentLifecycleStage.DRAFT_ONLY
    rec.runs = 10
    rec.trust_pass_count = 10
    rec.outcomes_logged = 5
    ev = evaluate_promotion_readiness(rec, AgentLifecycleStage.APPROVAL_GATED)
    assert ev.ready is False
    assert any(c.name == "min_runs" for c in ev.failing)


def test_promote_happy_path():
    reg = AgentRegistry()
    rec = _seed_agent(reg)
    rec.stage = AgentLifecycleStage.DRAFT_ONLY
    rec.runs = 60
    rec.successful_runs = 58
    rec.trust_pass_count = 58
    rec.outcomes_logged = 31
    result = promote(reg, rec.agent_id, AgentLifecycleStage.APPROVAL_GATED, approved_by="sami")
    assert result.to_stage == AgentLifecycleStage.APPROVAL_GATED
    assert reg.get(rec.agent_id).stage == AgentLifecycleStage.APPROVAL_GATED


def test_promote_blocks_when_critical_incidents():
    reg = AgentRegistry()
    rec = _seed_agent(reg)
    rec.stage = AgentLifecycleStage.DRAFT_ONLY
    rec.runs = 60
    rec.successful_runs = 60
    rec.trust_pass_count = 60
    rec.outcomes_logged = 31
    rec.critical_incidents = 1
    with pytest.raises(PromotionError):
        promote(reg, rec.agent_id, AgentLifecycleStage.APPROVAL_GATED, approved_by="sami")


def test_promote_requires_approver():
    reg = AgentRegistry()
    rec = _seed_agent(reg)
    rec.stage = AgentLifecycleStage.TESTED
    with pytest.raises(PromotionError):
        promote(reg, rec.agent_id, AgentLifecycleStage.DRAFT_ONLY, approved_by="")


def test_promote_rejects_non_adjacent_stages():
    reg = AgentRegistry()
    rec = _seed_agent(reg)
    # Registered → APPROVAL_GATED is non-adjacent
    with pytest.raises(PromotionError):
        promote(
            reg,
            rec.agent_id,
            AgentLifecycleStage.APPROVAL_GATED,
            approved_by="sami",
        )


def test_restriction_downgrades_stage():
    reg = AgentRegistry()
    rec = _seed_agent(reg)
    rec.stage = AgentLifecycleStage.APPROVAL_GATED
    action = restrict_agent(
        reg,
        rec.agent_id,
        RestrictionReason.SUSPECTED_INJECTION,
        requested_by="sami",
    )
    assert action.to_stage == AgentLifecycleStage.RESTRICTED
    assert reg.get(rec.agent_id).stage == AgentLifecycleStage.RESTRICTED


def test_retire_is_terminal():
    reg = AgentRegistry()
    rec = _seed_agent(reg)
    r = retire_agent(reg, rec.agent_id, approved_by="sami", reason="rotated out")
    assert r.from_stage == AgentLifecycleStage.REGISTERED
    assert reg.get(rec.agent_id).stage == AgentLifecycleStage.RETIRED


def test_risk_scoring_flags_external_send():
    score = score_agent_risk(
        ["read_approved_opportunity", "draft_proposal", "send_external"],
        forbidden_capabilities=(),
        can_initiate_external_send=True,
    )
    assert score.band.value in ("high", "critical")
    assert score.requires_human_approval() is True


def test_risk_scoring_low_for_read_only():
    score = score_agent_risk(
        ["read_approved_opportunity", "read_public_data"],
        workspace_scope=("dealix_internal",),
    )
    assert score.band.value == "low"
