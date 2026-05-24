"""Pipeline tests: Signal → Opportunity → Decision → Plan → Outcome → Asset → ScaleKill."""

from __future__ import annotations

from decimal import Decimal

from dealix.hermes.core.assets import AssetBuilder, AssetType
from dealix.hermes.core.decisions import (
    DecisionMemoBuilder,
    DecisionStatus,
)
from dealix.hermes.core.executions import (
    ExecutionPlanner,
    ExecutionResult,
    ExecutionStatus,
    StepResult,
    StepStatus,
)
from dealix.hermes.core.opportunities import (
    OpportunityMapper,
    OpportunityType,
    ScoredOpportunity,
)
from dealix.hermes.core.outcomes import OutcomeKind, OutcomeLogger
from dealix.hermes.core.scale import ScaleKillKind, ScaleKillRecommender
from dealix.hermes.core.schemas import Money, RiskLevel, WorkspaceScope
from dealix.hermes.core.scoring import (
    opportunity_score,
    partner_fit_score,
    risk_score,
)
from dealix.hermes.core.signals import (
    Signal,
    SignalClassifier,
    SignalSource,
)


def _signal(text: str, source: SignalSource = SignalSource.INBOUND_MESSAGE) -> Signal:
    return Signal(source=source, raw_text=text, channel="test")


def test_happy_path_signal_to_asset() -> None:
    signal = _signal("we'd like a recurring monthly retainer proposal")
    classifier = SignalClassifier()
    mapper = OpportunityMapper()

    classification = classifier.classify(signal)
    assert classification.monetizable is True
    assert classification.repeatable is True

    opp = mapper.map(signal, classification)
    assert opp.opp_type == OpportunityType.REVENUE
    assert opp.expected_value is not None

    score = opportunity_score(opp)
    assert 0 <= score <= 5

    scored = ScoredOpportunity(
        opportunity=opp,
        score=score,
        rationale="happy path",
        components={"revenue": 1.0, "urgency": 4.0, "fit": 5.0, "effort_inverse": 3.0},
    )
    decision = DecisionMemoBuilder().build(scored)
    assert len(decision.options) >= 2
    assert decision.chosen_option in decision.options

    plan = ExecutionPlanner().plan(decision, opp.opp_type)
    assert plan.steps

    # Simulate every step succeeding
    step_results = [
        StepResult(step_id=s.step_id, status=StepStatus.OK, detail="ok") for s in plan.steps
    ]
    execution = ExecutionResult.from_steps(plan_id=plan.plan_id, results=step_results)
    assert execution.status == ExecutionStatus.COMPLETED

    logger = OutcomeLogger()
    outcome = logger.log(
        execution=execution,
        kind=OutcomeKind.MONEY,
        summary="Retainer closed",
        value=Money.sar(Decimal("5000")),
        metrics={"repeatable": 1.0},
    )

    asset = AssetBuilder().consider(outcome, reusability_score=4, monetization_potential=4)
    assert asset is not None
    assert asset.asset_type == AssetType.OFFER

    rec = ScaleKillRecommender().recommend([outcome, outcome, outcome])
    # Repeated money outcome with metric → SCALE
    assert rec.kind in {ScaleKillKind.SCALE, ScaleKillKind.HOLD}


def test_opportunity_mapping_categories() -> None:
    classifier = SignalClassifier()
    mapper = OpportunityMapper()
    cases = {
        "white-label partnership please": OpportunityType.PARTNER,
        "we need a feature": OpportunityType.PRODUCT,
        "how do you handle this best practice": OpportunityType.KNOWLEDGE,
        "lawsuit notice from regulator": OpportunityType.RISK_AVOIDANCE,
        "send invoice for the contract": OpportunityType.REVENUE,
    }
    for text, expected in cases.items():
        sig = _signal(text)
        opp = mapper.map(sig, classifier.classify(sig))
        assert opp.opp_type == expected, (text, opp.opp_type)


def test_decision_state_machine_transitions() -> None:
    sig = _signal("send a proposal")
    classifier = SignalClassifier()
    mapper = OpportunityMapper()
    opp = mapper.map(sig, classifier.classify(sig))
    scored = ScoredOpportunity(
        opportunity=opp,
        score=4.0,
        rationale="r",
        components={"revenue": 1.0, "urgency": 5.0, "fit": 5.0, "effort_inverse": 3.0},
    )
    decision = DecisionMemoBuilder().build(scored)
    assert decision.status == DecisionStatus.DRAFT
    decision = decision.transition(DecisionStatus.PENDING_APPROVAL)
    assert decision.status == DecisionStatus.PENDING_APPROVAL
    decision = decision.transition(DecisionStatus.APPROVED, by="sami")
    assert decision.status == DecisionStatus.APPROVED
    assert decision.decided_by == "sami"
    decision = decision.transition(DecisionStatus.EXECUTED)
    assert decision.status == DecisionStatus.EXECUTED


def test_execution_result_from_steps_classifies_status() -> None:
    ok = [StepResult(step_id="a", status=StepStatus.OK)]
    partial = [
        StepResult(step_id="a", status=StepStatus.OK),
        StepResult(step_id="b", status=StepStatus.ERROR),
    ]
    failed = [StepResult(step_id="a", status=StepStatus.ERROR)]
    assert ExecutionResult.from_steps("p", ok).status == ExecutionStatus.COMPLETED
    assert ExecutionResult.from_steps("p", partial).status == ExecutionStatus.PARTIAL
    assert ExecutionResult.from_steps("p", failed).status == ExecutionStatus.FAILED


def test_outcome_logger_filters_and_totals() -> None:
    logger = OutcomeLogger()
    exec_ok = ExecutionResult.from_steps(
        "p1",
        [StepResult(step_id="x", status=StepStatus.OK)],
    )
    a = logger.log(exec_ok, OutcomeKind.MONEY, "x", value=Money.sar(100))
    b = logger.log(exec_ok, OutcomeKind.LEARNING, "y")
    assert len(logger.all()) == 2
    assert logger.by_kind(OutcomeKind.MONEY) == [a]
    assert logger.by_kind(OutcomeKind.LEARNING) == [b]
    assert logger.total_money().amount == Decimal("100")


def test_asset_builder_returns_none_for_low_value_partner() -> None:
    exec_ok = ExecutionResult.from_steps(
        "p1",
        [StepResult(step_id="x", status=StepStatus.OK)],
    )
    outcome = OutcomeLogger().log(exec_ok, OutcomeKind.PARTNER, "intro made")
    assert AssetBuilder().consider(outcome, reusability_score=1) is None


def test_partner_fit_and_risk_score_pure_functions() -> None:
    classifier = SignalClassifier()
    mapper = OpportunityMapper()
    sig = _signal("partnership inquiry")
    opp = mapper.map(sig, classifier.classify(sig))
    score = partner_fit_score(
        {"categories": ["partner"], "trust_score": 4.0, "value_overlap": 0.5},
        opp,
    )
    assert 0 <= score <= 5
    assert risk_score({"sensitive_data": True}) == RiskLevel.CRITICAL
    assert risk_score({"monetary_amount": 200_000}) == RiskLevel.CRITICAL
    assert risk_score({}) == RiskLevel.LOW


def test_scale_recommender_kills_money_drain() -> None:
    exec_ok = ExecutionResult.from_steps(
        "p1",
        [StepResult(step_id="x", status=StepStatus.OK)],
    )
    logger = OutcomeLogger()
    for _ in range(5):
        logger.log(
            exec_ok,
            OutcomeKind.LEARNING,
            "explain again",
            metrics={
                "explain_effort": 0.9,
                "channel_unknown": 1.0,
                "time_drain": 1.0,
            },
            risk_flag=True,
        )
    rec = ScaleKillRecommender().recommend(logger.all())
    assert rec.kind == ScaleKillKind.KILL
    assert rec.reasons


def test_signal_with_pii_marks_sensitive() -> None:
    classifier = SignalClassifier()
    sig = _signal("our customer id is 1234567890 and IBAN SA0380000000608010167519")
    cls = classifier.classify(sig)
    assert cls.sensitive is True


def test_opportunity_default_workspace_preserved() -> None:
    sig = Signal(
        source=SignalSource.INTERNAL_NOTE,
        raw_text="just a note",
        channel="slack",
        workspace=WorkspaceScope.CUSTOMER,
    )
    opp = OpportunityMapper().map(sig, SignalClassifier().classify(sig))
    assert opp.workspace == WorkspaceScope.CUSTOMER
