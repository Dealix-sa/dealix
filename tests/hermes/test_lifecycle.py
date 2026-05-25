"""End-to-end lifecycle and events."""

from __future__ import annotations

from dealix.hermes.kernel.schemas import (
    AssetType,
    OpportunityType,
    OutcomeStatus,
    SignalSource,
    SignalType,
    SovereigntyLevel,
)
from dealix.hermes.kernel.signals import capture_signal


def test_full_lifecycle_emits_all_events(orch):
    """No 1: لا Signal يضيع — and the chain is complete."""
    sig = capture_signal(
        store=orch.kernel.signals,
        source=SignalSource.customer,
        signal_type=SignalType.customer,
        title="Lead",
        content="content",
    )
    opp = orch.kernel.opportunities.create_from_signal(
        sig,
        opportunity_type=OpportunityType.customer,
        title="Opp",
        sovereignty_level=SovereigntyLevel.S1_INTERNAL,
    )
    decision = orch.kernel.decisions.create_memo(opp, memo="proceed")
    ex = orch.kernel.executions.plan(decision, agent_id="proposal_factory", tools=["draft_proposal"])
    orch.kernel.executions.mark_trust_check(ex.execution_id, passed=True)
    orch.kernel.executions.dispatch(ex.execution_id)
    ex = orch.kernel.executions.complete(ex.execution_id)
    out = orch.kernel.outcomes.log(
        ex, status=OutcomeStatus.won, actual_result="signed",
        revenue_sar=10_000, asset_review_required=True,
    )
    asset = orch.kernel.assets.create_from_outcome(
        out, asset_type=AssetType.template, title="Template",
    )

    event_types = {e.event_type for e in orch.kernel.all_events()}
    expected = {
        "signal.captured",
        "opportunity.created",
        "opportunity.scored",
        "decision.created",
        "execution.planned",
        "execution.dispatched",
        "execution.completed",
        "outcome.logged",
        "asset.created",
    }
    assert expected.issubset(event_types), f"missing events: {expected - event_types}"


def test_no_score_no_opportunity(orch):
    """No 2: لا Opportunity بلا Score."""
    sig = capture_signal(
        store=orch.kernel.signals, source=SignalSource.market,
        signal_type=SignalType.market, title="x", content="y",
    )
    opp = orch.kernel.opportunities.create_from_signal(
        sig, opportunity_type=OpportunityType.report, title="o",
    )
    # composite_score is always set, even if zero
    assert opp.composite_score is not None
