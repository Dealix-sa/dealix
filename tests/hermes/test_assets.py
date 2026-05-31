"""Asset doctrine — assets are reviewed, scored, and scale-killed."""

from __future__ import annotations

import pytest

from dealix.hermes.kernel.schemas import (
    AssetType,
    OpportunityType,
    OutcomeStatus,
    SignalSource,
    SignalType,
    SovereigntyLevel,
)
from dealix.hermes.kernel.scale_kill import ScaleKillVerdict, evaluate
from dealix.hermes.kernel.signals import capture_signal


def _outcome(orch, *, asset_review_required: bool = True):
    sig = capture_signal(
        store=orch.kernel.signals, source=SignalSource.customer,
        signal_type=SignalType.customer, title="t", content="c",
    )
    opp = orch.kernel.opportunities.create_from_signal(
        sig, opportunity_type=OpportunityType.customer, title="o",
        sovereignty_level=SovereigntyLevel.S1_INTERNAL,
    )
    decision = orch.kernel.decisions.create_memo(opp, memo="m")
    ex = orch.kernel.executions.plan(decision, agent_id="proposal_factory", tools=["draft_proposal"])
    orch.kernel.executions.mark_trust_check(ex.execution_id, passed=True)
    orch.kernel.executions.dispatch(ex.execution_id)
    ex = orch.kernel.executions.complete(ex.execution_id)
    return orch.kernel.outcomes.log(
        ex, status=OutcomeStatus.won,
        actual_result="ok", revenue_sar=15_000, cost_sar=5_000,
        asset_review_required=asset_review_required,
    )


def test_asset_review_required_after_outcome(orch):
    """No 8: لا Outcome بلا Asset Review."""
    out = _outcome(orch, asset_review_required=True)
    assert orch.kernel.assets.review_outcome(out)


def test_asset_creation_blocked_when_not_reviewed(orch):
    out = _outcome(orch, asset_review_required=False)
    # mark margin negative so auto-review also fails
    out = out.model_copy(update={"margin_sar": -1, "revenue_verified": False})
    with pytest.raises(ValueError):
        orch.kernel.assets.create_from_outcome(out, asset_type=AssetType.template, title="t")


def test_asset_scale_kill_thresholds(orch):
    out = _outcome(orch)
    a = orch.kernel.assets.create_from_outcome(out, asset_type=AssetType.template, title="t", moat_score=0.5)
    # zero reuse + zero quality should kill
    assert evaluate(a) == ScaleKillVerdict.kill
    # After many reuses + revenue, should scale
    for _ in range(6):
        a = orch.kernel.assets.record_reuse(a.asset_id, revenue_sar=20_000)
    assert evaluate(a) == ScaleKillVerdict.scale
