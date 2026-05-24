"""End-to-end pipeline: Signal → Opportunity → Decision → Execution → Outcome → Asset."""

from __future__ import annotations

import pytest

from dealix.hermes.core.scoring import ScoreInputs
from dealix.hermes.core.schemas import (
    Asset,
    Decision,
    Opportunity,
    Outcome,
    OutcomeStatus,
    Signal,
)
from dealix.hermes.kernel import HermesKernel
from dealix.hermes.sovereignty.levels import SovereigntyLevel


def test_signal_to_asset_lineage_preserved():
    k = HermesKernel()
    sig = k.signals.receive(
        Signal.make(source="email", domain="money", summary="Lead from CTO")
    )
    opp = k.opportunities.add(
        Opportunity.make(signal_id=sig.id, domain="money", title="Pilot proposal")
    )
    k.scorer.score(
        opp,
        ScoreInputs(
            cash_speed=0.7,
            close_probability=0.5,
            deal_value_sar=80_000,
            strategic_value=0.6,
            risk=0.2,
        ),
    )
    k.opportunities.mark_scored(opp.id)
    k.opportunities.queue(opp.id)

    dec = Decision.make(
        opportunity_id=opp.id,
        action="draft_proposal",
        sovereignty_level=SovereigntyLevel.S1_INTERNAL,
        rationale="Draft internal pilot pack",
    )
    k.decisions.file(dec, domain="money")
    assert dec.is_executable, "S1 actions should auto-approve"

    exe = k.executions.plan(
        decision=dec, agent_id="proposal_factory", steps=[{"kind": "draft"}]
    )
    k.executions.start(exe.id)
    k.executions.complete(exe.id)

    outcome = k.outcomes.record(
        Outcome.make(execution_id=exe.id, status=OutcomeStatus.WIN, revenue_sar=15_000)
    )
    asset = k.assets.add(
        Asset.make(
            outcome_id=outcome.id,
            kind="template",
            title="Pilot Proposal v1",
            summary="Reusable fintech pilot pack",
        )
    )

    assert opp.signal_id == sig.id
    assert exe.decision_id == dec.id
    assert outcome.execution_id == exe.id
    assert asset.outcome_id == outcome.id


def test_unscored_opportunity_cannot_be_queued():
    k = HermesKernel()
    sig = k.signals.receive(Signal.make(source="x", domain="money", summary="x"))
    opp = k.opportunities.add(Opportunity.make(signal_id=sig.id, domain="money", title="x"))
    with pytest.raises(ValueError):
        k.opportunities.mark_scored(opp.id)


def test_outcome_cannot_be_duplicated_for_same_execution():
    k = HermesKernel()
    sig = k.signals.receive(Signal.make(source="x", domain="money", summary="x"))
    opp = k.opportunities.add(Opportunity.make(signal_id=sig.id, domain="money", title="x"))
    k.scorer.score(opp, ScoreInputs(cash_speed=0.5, close_probability=0.5, deal_value_sar=10_000, strategic_value=0.5, risk=0.1))
    k.opportunities.mark_scored(opp.id); k.opportunities.queue(opp.id)
    dec = Decision.make(opportunity_id=opp.id, action="draft_proposal",
                        sovereignty_level=SovereigntyLevel.S0_AUTO_SAFE, rationale="r")
    k.decisions.file(dec)
    exe = k.executions.plan(decision=dec, agent_id="a", steps=[])
    k.executions.start(exe.id); k.executions.complete(exe.id)
    k.outcomes.record(Outcome.make(execution_id=exe.id, status=OutcomeStatus.WIN))
    with pytest.raises(ValueError):
        k.outcomes.record(Outcome.make(execution_id=exe.id, status=OutcomeStatus.LOSS))
