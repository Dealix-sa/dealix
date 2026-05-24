"""End-to-end Hermes pipeline: signal → opportunity → memo → plan → outcome."""

from __future__ import annotations

from dealix.hermes import ValueOutput
from dealix.hermes.core.schemas import (
    ExecutionStatus,
    ExecutionStep,
    OpportunityKind,
    OutcomeKind,
    SignalSource,
)
from dealix.hermes.orchestrator import HermesOrchestrator
from dealix.hermes.sovereignty import SovereigntyLevel


def test_signal_to_outcome_pipeline():
    orch = HermesOrchestrator()

    sig = orch.intake.capture(
        source=SignalSource.INBOUND_LEAD,
        title="Agency wants AI ops",
        summary="Founder of a 12-person agency asked about Revenue Hunter.",
        captured_by="sami",
    )
    opp = orch.opportunities.register(
        source_signals=[sig],
        kind=OpportunityKind.DIRECT_DEAL,
        title="Revenue Hunter Pilot — Agency A",
        buyer_segment="agency",
        estimated_value_sar=4999,
        close_probability=0.6,
        fit_score=0.8,
        urgency_score=0.7,
        risk_score=0.2,
        proposed_value_outputs=[ValueOutput.MONEY, ValueOutput.ASSET],
    )
    assert opp.expected_value_sar > 0

    memo = orch.decisions.draft(
        opportunity=opp,
        recommendation="Ship pilot this week",
        rationale="Warm intro, fit score 0.8, risk 0.2.",
        sovereignty_level=SovereigntyLevel.S2_SAMI_APPROVAL,
        written_by="sami",
    )
    assert memo.approval_required is True
    assert memo.approved_at is None

    plan = orch.plans.draft_plan(
        opportunity=opp,
        memo=memo,
        steps=[
            ExecutionStep(description="Draft proposal", owner="proposal_agent"),
            ExecutionStep(description="Sami review", owner="sami"),
        ],
    )
    assert plan.status is ExecutionStatus.PENDING_APPROVAL

    orch.decisions.approve(memo.memo_id, approver="sami")
    orch.plans.mark(plan.plan_id, ExecutionStatus.APPROVED)

    paid = orch.outcomes.record(
        opportunity_id=opp.opportunity_id,
        plan_id=plan.plan_id,
        kind=OutcomeKind.PAID,
        realised_value_sar=4999,
        realised_outputs=[ValueOutput.MONEY],
        summary="Pilot invoice paid via Moyasar.",
        recorded_by="sami",
    )
    assert orch.outcomes.cash_collected_sar() == 4999

    asset = orch.assets.register(
        kind=__import__(
            "dealix.hermes.core.schemas", fromlist=["AssetKind"]
        ).AssetKind.CASE_STUDY,
        title="Agency A — Revenue Hunter Pilot",
        summary="14-day pilot, 5 cash actions, 2 closed.",
        body="# Case study\n…",
        created_by="evidence_agent",
        derived_from=[paid],
    )
    assert asset.version == 1
    orch.outcomes.mark_asset_reviewed(paid.outcome_id)
    assert paid.outcome_id not in [o.outcome_id for o in orch.outcomes.pending_asset_review()]


def test_paid_outcome_requires_positive_value():
    orch = HermesOrchestrator()
    import pytest

    with pytest.raises(ValueError):
        orch.outcomes.record(
            opportunity_id="x",
            kind=OutcomeKind.PAID,
            realised_value_sar=0,
            summary="invalid",
            recorded_by="sami",
        )
