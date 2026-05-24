"""End-to-end kernel loop: Signal → Decision → Execution → Outcome → Asset."""

from __future__ import annotations

from dealix.hermes.core.schemas import (
    AssetKind,
    DecisionVerdict,
    ExecutionStatus,
    Outcome,
    OutcomeKind,
    Signal,
    SignalSource,
)
from dealix.hermes.orchestrator import Orchestrator
from dealix.hermes.trust.guardrails import TrustContext


def _orch() -> Orchestrator:
    return Orchestrator.fresh()


def test_capture_signal_creates_opportunity_and_money_action() -> None:
    orch = _orch()
    sig = Signal(
        source=SignalSource.INBOUND_LEAD,
        sector="agencies",
        payload={"title": "Agency X", "estimated_value_sar": 1500},
    )
    opp = orch.capture_signal(sig)
    assert opp.signal_id == sig.id
    assert opp.cash_speed_score > 0
    assert len(orch.opportunities) == 1
    assert len(orch.money_actions) == 1
    assert orch.money_actions[0].money_priority_score > 0


def test_internal_decision_does_not_require_approval() -> None:
    orch = _orch()
    sig = Signal(source=SignalSource.INBOUND_LEAD, sector="agencies", payload={})
    opp = orch.capture_signal(sig)
    decision = orch.decide(opp.id, DecisionVerdict.PURSUE, "good fit", "draft_message")
    assert decision.requires_approval is False
    assert decision.approval_status == "n/a"


def test_external_decision_requires_approval_and_blocks_execution() -> None:
    orch = _orch()
    sig = Signal(source=SignalSource.INBOUND_LEAD, sector="agencies", payload={})
    opp = orch.capture_signal(sig)
    decision = orch.decide(opp.id, DecisionVerdict.PURSUE, "ready", "send_external_message")
    assert decision.requires_approval is True

    blocked = orch.execute(decision.id, "revenue_hunter", tool_id=None)
    assert blocked.status == ExecutionStatus.BLOCKED

    orch.approve(decision.id)
    executed = orch.execute(decision.id, "revenue_hunter", tool_id=None)
    assert executed.status == ExecutionStatus.EXECUTED


def test_execute_blocks_unauthorised_tool() -> None:
    orch = _orch()
    sig = Signal(source=SignalSource.INBOUND_LEAD, sector="agencies", payload={})
    opp = orch.capture_signal(sig)
    decision = orch.decide(opp.id, DecisionVerdict.PURSUE, "draft only", "draft_message")
    result = orch.execute(decision.id, "revenue_hunter", tool_id="sign_contract")
    assert result.status == ExecutionStatus.FAILED
    assert "not authorised" in (result.error or "")


def test_log_outcome_mints_asset() -> None:
    orch = _orch()
    sig = Signal(source=SignalSource.INBOUND_LEAD, sector="agencies", payload={})
    opp = orch.capture_signal(sig)
    out = Outcome(
        opportunity_id=opp.id,
        kind=OutcomeKind.DEAL_WON,
        value_sar=999,
        sector="agencies",
        offer="Revenue Hunter Pilot",
        notes="closed on first call",
    )
    outcome, asset = orch.log_outcome(out)
    assert outcome.id == out.id
    assert asset.kind == AssetKind.CASE_STUDY
    assert asset.source_outcome_id == out.id
    assert len(orch.assets.all()) == 1


def test_trust_check_logged_to_orchestrator() -> None:
    orch = _orch()
    result = orch.run_trust_check(
        TrustContext(target_id="x", target_kind="message", text="guaranteed ROI 100%")
    )
    assert result.outcome.value == "deny"
    assert len(orch.trust_log) == 1


def test_sovereign_brief_surfaces_pending_and_blocked() -> None:
    orch = _orch()
    sig = Signal(source=SignalSource.INBOUND_LEAD, sector="agencies", payload={})
    opp = orch.capture_signal(sig)
    decision = orch.decide(opp.id, DecisionVerdict.PURSUE, "ready", "send_external_message")
    orch.execute(decision.id, "revenue_hunter", tool_id=None)

    brief = orch.sovereign_brief()
    assert any(d.id == decision.id for d in brief.pending_approvals)
    assert any(b["decision_id"] == decision.id for b in brief.blocked_risks)
    assert brief.fastest_cash_actions, "should rank money actions"
