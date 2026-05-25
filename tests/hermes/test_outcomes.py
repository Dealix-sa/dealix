"""Outcome doctrine — every execution gets exactly one outcome."""

from __future__ import annotations

import pytest

from dealix.hermes.kernel.schemas import (
    OpportunityType,
    OutcomeStatus,
    SignalSource,
    SignalType,
    SovereigntyLevel,
)
from dealix.hermes.kernel.signals import capture_signal


def _execute_to_outcome(orch):
    sig = capture_signal(
        store=orch.kernel.signals,
        source=SignalSource.customer,
        signal_type=SignalType.customer,
        title="lead",
        content="lead content",
    )
    opp = orch.kernel.opportunities.create_from_signal(
        sig,
        opportunity_type=OpportunityType.customer,
        title="customer opp",
        sovereignty_level=SovereigntyLevel.S1_INTERNAL,
    )
    decision = orch.kernel.decisions.create_memo(opp, memo="proceed")
    ex = orch.kernel.executions.plan(decision, agent_id="proposal_factory", tools=["draft_proposal"])
    orch.kernel.executions.mark_trust_check(ex.execution_id, passed=True)
    orch.kernel.executions.dispatch(ex.execution_id)
    return orch.kernel.executions.complete(ex.execution_id)


def test_outcome_required_after_execution(orch):
    """No 8: لا Outcome بلا Asset Review."""
    ex = _execute_to_outcome(orch)
    out = orch.kernel.outcomes.log(
        ex,
        status=OutcomeStatus.won,
        actual_result="customer signed",
        revenue_sar=10_000,
    )
    assert orch.kernel.outcomes.for_execution(ex.execution_id) == out


def test_only_one_outcome_per_execution(orch):
    ex = _execute_to_outcome(orch)
    orch.kernel.outcomes.log(
        ex,
        status=OutcomeStatus.won,
        actual_result="ok",
    )
    with pytest.raises(ValueError):
        orch.kernel.outcomes.log(
            ex,
            status=OutcomeStatus.lost,
            actual_result="duplicate",
        )


def test_outcome_revenue_starts_unverified(orch):
    """No 9: لا Revenue بلا Verification."""
    ex = _execute_to_outcome(orch)
    out = orch.kernel.outcomes.log(
        ex,
        status=OutcomeStatus.won,
        actual_result="customer signed",
        revenue_sar=10_000,
    )
    assert out.revenue_verified is False
    verified = orch.kernel.outcomes.verify_revenue(out.outcome_id)
    assert verified.revenue_verified is True
