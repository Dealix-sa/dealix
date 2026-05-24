"""End-to-end pipeline tests — Signal → Opportunity → Decision → Execution → Outcome → Asset."""

from __future__ import annotations

import pytest

from dealix.hermes.core.assets import AssetStore
from dealix.hermes.core.decisions import DecisionStore
from dealix.hermes.core.executions import ExecutionStore
from dealix.hermes.core.opportunities import OpportunityStore
from dealix.hermes.core.outcomes import OutcomeStore
from dealix.hermes.core.schemas import (
    AssetType,
    OutcomeStatus,
    PermissionLevel,
    SignalType,
    SovereigntyLevel,
)
from dealix.hermes.core.signals import SignalStore
from dealix.hermes.orchestrator import HermesOrchestrator
from dealix.hermes.sovereignty import SovereignLayer
from dealix.hermes.trust.approvals import ApprovalCenter
from dealix.hermes.trust.audit import AuditLog


@pytest.fixture(autouse=True)
def _isolate(monkeypatch):
    """Replace every default singleton with a fresh instance for each test."""
    import dealix.hermes.core.assets as a_mod
    import dealix.hermes.core.decisions as d_mod
    import dealix.hermes.core.executions as e_mod
    import dealix.hermes.core.opportunities as o_mod
    import dealix.hermes.core.outcomes as out_mod
    import dealix.hermes.core.signals as s_mod
    import dealix.hermes.orchestrator as orch_mod
    import dealix.hermes.sovereignty as sov_mod
    import dealix.hermes.trust.approvals as appr_mod
    import dealix.hermes.trust.audit as aud_mod

    s_mod._default_store = SignalStore()
    o_mod._default_store = OpportunityStore()
    d_mod._default_store = DecisionStore()
    e_mod._default_store = ExecutionStore()
    out_mod._default_store = OutcomeStore()
    a_mod._default_store = AssetStore()
    orch_mod._default_orchestrator = HermesOrchestrator()
    sov_mod._default_layer = SovereignLayer()
    appr_mod._default_center = ApprovalCenter()
    aud_mod._default_log = AuditLog()
    yield
    for m in (s_mod, o_mod, d_mod, e_mod, out_mod, a_mod):
        m._default_store = None
    orch_mod._default_orchestrator = None
    sov_mod._default_layer = None
    appr_mod._default_center = None
    aud_mod._default_log = None


def test_full_pipeline_produces_outcome_and_asset():
    orch = HermesOrchestrator()
    sig = orch.ingest_signal(
        source="sami",
        signal_type=SignalType.CUSTOMER,
        title="Agency wants AI service",
        content="An agency has 30 B2B clients and wants a white-label AI offer.",
    )
    opp = orch.evaluate_opportunity(sig, estimated_value_sar=12_000)
    assert opp.score > 0
    assert opp.sovereignty_level in {
        SovereigntyLevel.S1_INTERNAL.value,
        SovereigntyLevel.S2_SAMI_APPROVAL.value,
        SovereigntyLevel.S3_SAMI_REVIEW.value,
    }

    decision = orch.make_decision(opp)
    assert decision.opportunity_id == opp.id

    result = orch.plan_execution(
        decision,
        agent_id="revenue_hunter",
        tool_id="draft_message",
        action_type="draft_outreach",
        permission_level=PermissionLevel.L1_DRAFT,
        expected_result="Draft outreach for white-label pitch",
    )
    assert result.permission_decision is not None
    assert result.permission_decision.allowed is True

    exe = result.execution
    assert exe is not None
    orch.run(exe)

    outcome = orch.record_outcome(
        exe,
        status=OutcomeStatus.REPLIED,
        actual_result="Agency replied with interest",
        learning="Agencies prefer white-label framing",
    )
    asset = orch.register_asset(
        outcome,
        asset_type=AssetType.TEMPLATE,
        title="Agency white-label pitch v1",
        commercializable=True,
    )
    assert asset.outcome_id == outcome.id


def test_external_action_holds_execution_for_approval():
    orch = HermesOrchestrator()
    sig = orch.ingest_signal(
        source="customer",
        signal_type=SignalType.CUSTOMER,
        title="Hot lead",
    )
    opp = orch.evaluate_opportunity(sig, estimated_value_sar=30_000, risk=4)
    # estimated_value >= 25_000 OR risk_score >= 4 → S2 sovereignty
    assert opp.sovereignty_level == SovereigntyLevel.S2_SAMI_APPROVAL.value
    decision = orch.make_decision(opp)
    result = orch.plan_execution(
        decision,
        agent_id="revenue_hunter",
        tool_id="draft_message",
        action_type="send_external_email",
        permission_level=PermissionLevel.L3_EXTERNAL_SEND,
        external_action=True,
    )
    assert result.execution is not None
    assert result.execution.status in {"held", "blocked"}


def test_outcome_required_after_execution_flag():
    orch = HermesOrchestrator()
    sig = orch.ingest_signal(source="sami", signal_type=SignalType.PRODUCT, title="Idea")
    opp = orch.evaluate_opportunity(sig)
    decision = orch.make_decision(opp)
    result = orch.plan_execution(
        decision,
        agent_id="revenue_hunter",
        tool_id="draft_message",
        action_type="draft_outreach",
    )
    exe = result.execution
    assert exe is not None
    # Outcome is mandatory; it must be created with one of the OutcomeStatus values.
    outcome = orch.record_outcome(exe, status=OutcomeStatus.DRAFTED, actual_result="ok")
    assert outcome.execution_id == exe.id
    assert outcome.asset_review_required is True


def test_asset_review_satisfied_by_attaching_asset():
    orch = HermesOrchestrator()
    sig = orch.ingest_signal(source="sami", signal_type=SignalType.PRODUCT, title="Idea")
    opp = orch.evaluate_opportunity(sig)
    decision = orch.make_decision(opp)
    result = orch.plan_execution(
        decision,
        agent_id="revenue_hunter",
        tool_id="draft_message",
        action_type="draft_outreach",
    )
    exe = result.execution
    out = orch.record_outcome(exe, status=OutcomeStatus.WON, revenue_sar=4_999)
    asset = orch.register_asset(out, asset_type=AssetType.PLAYBOOK, title="Playbook")
    from dealix.hermes.core.outcomes import get_outcome_store

    refreshed = get_outcome_store().get(out.id)
    assert refreshed is not None
    assert refreshed.asset_id == asset.id
    assert refreshed.asset_review_required is False
