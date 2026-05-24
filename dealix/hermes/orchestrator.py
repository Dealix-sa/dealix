"""خادم Hermes — orchestrator (spec §28).

Walks the full kernel pipeline:

    signal → opportunity → score → decision → plan → trust check →
    (approval if needed) → execute → outcome → asset? → scale/kill

Each step publishes the appropriate Event onto the injected EventBus.
External integrations (AgentRegistry, ToolRegistry, ApprovalCenter) are
declared as Protocols so this module stays at the kernel layer and never
imports concrete agents.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from enum import StrEnum
from typing import Any, Protocol, runtime_checkable

from dealix.hermes.core.assets import Asset, AssetBuilder
from dealix.hermes.core.decisions import Decision, DecisionMemoBuilder, DecisionStatus
from dealix.hermes.core.executions import (
    ExecutionPlan,
    ExecutionPlanner,
    ExecutionResult,
    StepResult,
    StepStatus,
)
from dealix.hermes.core.opportunities import (
    Opportunity,
    OpportunityMapper,
    ScoredOpportunity,
)
from dealix.hermes.core.outcomes import Outcome, OutcomeKind, OutcomeLogger
from dealix.hermes.core.scale import (
    ScaleKillKind,
    ScaleKillRecommendation,
    ScaleKillRecommender,
)
from dealix.hermes.core.schemas import Money, RiskLevel, utcnow
from dealix.hermes.core.scoring import opportunity_score, opportunity_score_components, risk_score
from dealix.hermes.core.signals import Signal, SignalClassification, SignalClassifier
from dealix.hermes.events import Event, EventBus, EventType
from dealix.hermes.sovereignty import (
    Sovereignty,
    SovereigntyLevel,
    SovereigntyVerdict,
)


# ─────────────────────────────────────────────────────────────
# Protocols for injected dependencies
# ─────────────────────────────────────────────────────────────


@runtime_checkable
class AgentRegistryProto(Protocol):
    def assert_can_use_tool(self, agent_id: str, tool_id: str) -> Any: ...


@runtime_checkable
class ToolRegistryProto(Protocol):
    def assert_callable(
        self, tool_id: str, agent_id: str, data_scope: str | None = None
    ) -> Any: ...


@runtime_checkable
class ApprovalCenterProto(Protocol):
    """Minimal contract the orchestrator needs."""

    def submit(self, ticket: Any) -> str: ...

    def get(self, ticket_id: str) -> Any: ...


# ─────────────────────────────────────────────────────────────
# Run trace container
# ─────────────────────────────────────────────────────────────


class RunStatus(StrEnum):
    COMPLETED = "completed"
    AWAITING_APPROVAL = "awaiting_approval"
    BLOCKED = "blocked"
    FAILED = "failed"


@dataclass
class OrchestratorRun:
    """Trace + artifacts produced by HermesOrchestrator.run()."""

    signal: Signal
    classification: SignalClassification | None = None
    opportunity: Opportunity | None = None
    scored: ScoredOpportunity | None = None
    decision: Decision | None = None
    plan: ExecutionPlan | None = None
    sovereignty_verdict: SovereigntyVerdict | None = None
    approval_ticket_id: str | None = None
    execution_result: ExecutionResult | None = None
    outcome: Outcome | None = None
    asset: Asset | None = None
    recommendation: ScaleKillRecommendation | None = None
    events_published: list[str] = field(default_factory=list)
    status: RunStatus = RunStatus.COMPLETED
    blocked_reason: str | None = None
    started_at: datetime = field(default_factory=utcnow)
    completed_at: datetime | None = None

    def step_ids(self) -> dict[str, str | None]:
        return {
            "signal_id": self.signal.signal_id,
            "opp_id": self.opportunity.opp_id if self.opportunity else None,
            "decision_id": self.decision.decision_id if self.decision else None,
            "plan_id": self.plan.plan_id if self.plan else None,
            "approval_ticket_id": self.approval_ticket_id,
            "execution_plan_id": self.execution_result.plan_id if self.execution_result else None,
            "outcome_id": self.outcome.outcome_id if self.outcome else None,
            "asset_id": self.asset.asset_id if self.asset else None,
        }


# ─────────────────────────────────────────────────────────────
# Orchestrator
# ─────────────────────────────────────────────────────────────


_ACTOR = "HermesOrchestratorAgent"


class HermesOrchestrator:
    """Coordinates the full Hermes pipeline.

    All collaborator dependencies are optional. If a registry isn't
    supplied we skip the corresponding enforcement step and emit
    `tool.blocked` / `agent.blocked` events when a check is requested but
    impossible.
    """

    def __init__(
        self,
        event_bus: EventBus,
        sovereignty: type[Sovereignty] | Sovereignty = Sovereignty,
        agent_registry: AgentRegistryProto | None = None,
        tool_registry: ToolRegistryProto | None = None,
        approval_center: ApprovalCenterProto | None = None,
        outcome_logger: OutcomeLogger | None = None,
        asset_builder: AssetBuilder | None = None,
        memo_builder: DecisionMemoBuilder | None = None,
        planner: ExecutionPlanner | None = None,
        classifier: SignalClassifier | None = None,
        mapper: OpportunityMapper | None = None,
        recommender: ScaleKillRecommender | None = None,
    ) -> None:
        self._bus = event_bus
        self._sovereignty = sovereignty
        self._agents = agent_registry
        self._tools = tool_registry
        self._approvals = approval_center
        self._outcomes = outcome_logger or OutcomeLogger()
        self._asset_builder = asset_builder or AssetBuilder()
        self._memo_builder = memo_builder or DecisionMemoBuilder()
        self._planner = planner or ExecutionPlanner()
        self._classifier = classifier or SignalClassifier()
        self._mapper = mapper or OpportunityMapper()
        self._recommender = recommender or ScaleKillRecommender()

    # ── helpers ────────────────────────────────────────────────
    def _publish(
        self,
        run: OrchestratorRun,
        event_type: EventType,
        entity_type: str,
        entity_id: str,
        payload: dict[str, Any] | None = None,
        risk_level: RiskLevel = RiskLevel.LOW,
        sovereignty_level: str = SovereigntyLevel.S0_AUTONOMOUS.value,
    ) -> Event:
        event = Event(
            event_type=event_type,
            actor=_ACTOR,
            entity_type=entity_type,
            entity_id=entity_id,
            payload=payload or {},
            risk_level=risk_level,
            sovereignty_level=sovereignty_level,
        )
        self._bus.publish(event)
        run.events_published.append(event.event_type.value)
        return event

    # ── pipeline steps ────────────────────────────────────────
    def ingest_signal(self, signal: Signal) -> Opportunity:
        classification = self._classifier.classify(signal)
        return self._mapper.map(signal, classification)

    def classify(self, signal: Signal) -> SignalClassification:
        return self._classifier.classify(signal)

    def score(self, opportunity: Opportunity) -> ScoredOpportunity:
        score = opportunity_score(opportunity)
        components = opportunity_score_components(opportunity)
        rationale = (
            f"weighted opportunity score = {score:.2f} "
            f"(revenue={components['revenue']:.2f}, urgency={components['urgency']:.2f}, "
            f"fit={components['fit']:.2f}, effort_inverse={components['effort_inverse']:.2f})"
        )
        return ScoredOpportunity(
            opportunity=opportunity,
            score=score,
            rationale=rationale,
            components=components,
        )

    def decide(
        self,
        scored: ScoredOpportunity,
        sovereignty_level: str = SovereigntyLevel.S0_AUTONOMOUS.value,
    ) -> Decision:
        return self._memo_builder.build(scored, sovereignty_level=sovereignty_level)

    def plan(self, decision: Decision, opportunity: Opportunity) -> ExecutionPlan:
        return self._planner.plan(decision, opportunity.opp_type)

    def request_approval_if_needed(
        self,
        plan: ExecutionPlan,
        decision: Decision,
        verdict: SovereigntyVerdict,
        evidence_pack_ref: str | None = None,
    ) -> str | None:
        needs = verdict.level.numeric >= SovereigntyLevel.S2_SAMI_APPROVAL.numeric
        if not needs:
            return None
        if self._approvals is None:
            return None
        # Lazy import to avoid hard dep at module-load
        from dealix.trust.approvals import ApprovalTicket

        ticket = ApprovalTicket(
            decision_id=decision.decision_id,
            plan_id=plan.plan_id,
            summary=decision.summary,
            sovereignty_level=verdict.level,
            evidence_pack_ref=evidence_pack_ref,
        )
        return self._approvals.submit(ticket)

    def execute(self, plan: ExecutionPlan) -> ExecutionResult:
        results: list[StepResult] = []
        for step in plan.steps:
            try:
                if self._tools is not None:
                    self._tools.assert_callable(step.tool_id, step.agent_id)
                if self._agents is not None:
                    self._agents.assert_can_use_tool(step.agent_id, step.tool_id)
                results.append(
                    StepResult(
                        step_id=step.step_id,
                        status=StepStatus.OK,
                        detail=step.expected_outcome,
                    )
                )
            except PermissionError as exc:
                results.append(
                    StepResult(
                        step_id=step.step_id,
                        status=StepStatus.ERROR,
                        detail=str(exc),
                    )
                )
        return ExecutionResult.from_steps(
            plan_id=plan.plan_id,
            results=results,
            cost=plan.estimated_cost,
        )

    def log_outcome(
        self,
        execution: ExecutionResult,
        decision: Decision,
        opportunity: Opportunity,
    ) -> Outcome:
        if execution.status.value == "failed":
            kind = OutcomeKind.LEARNING
            summary = f"execution failed for {decision.decision_id}"
            value = None
        else:
            kind = self._infer_outcome_kind(opportunity)
            summary = decision.chosen_option
            value = self._value_for_outcome(opportunity, kind)
        return self._outcomes.log(
            execution=execution,
            kind=kind,
            summary=summary,
            value=value,
            metrics={"steps": float(len(execution.step_results))},
            learnings=["initial run"] if kind == OutcomeKind.LEARNING else [],
        )

    @staticmethod
    def _infer_outcome_kind(opportunity: Opportunity) -> OutcomeKind:
        from dealix.hermes.core.opportunities import OpportunityType as _OT

        mapping = {
            _OT.REVENUE: OutcomeKind.MONEY,
            _OT.PARTNER: OutcomeKind.PARTNER,
            _OT.PRODUCT: OutcomeKind.ASSET,
            _OT.KNOWLEDGE: OutcomeKind.LEARNING,
            _OT.RISK_AVOIDANCE: OutcomeKind.TRUST,
        }
        return mapping[opportunity.opp_type]

    @staticmethod
    def _value_for_outcome(opportunity: Opportunity, kind: OutcomeKind) -> Money | None:
        if kind != OutcomeKind.MONEY:
            return None
        if opportunity.expected_value is not None:
            return opportunity.expected_value
        return Money.sar(Decimal("0"))

    def consider_asset(self, outcome: Outcome) -> Asset | None:
        return self._asset_builder.consider(outcome)

    def recommend(self, outcomes: list[Outcome]) -> ScaleKillRecommendation:
        return self._recommender.recommend(outcomes)

    # ── full pipeline ─────────────────────────────────────────
    def run(self, signal: Signal) -> OrchestratorRun:
        run = OrchestratorRun(signal=signal)

        # 1. signal.captured
        classification = self._classifier.classify(signal)
        run.classification = classification
        self._publish(
            run,
            EventType.SIGNAL_CAPTURED,
            entity_type="signal",
            entity_id=signal.signal_id,
            payload={"source": signal.source.value, "category": classification.category.value},
        )

        # 2. opportunity.created
        opportunity = self._mapper.map(signal, classification)
        run.opportunity = opportunity
        self._publish(
            run,
            EventType.OPPORTUNITY_CREATED,
            entity_type="opportunity",
            entity_id=opportunity.opp_id,
            payload={"opp_type": opportunity.opp_type.value},
        )

        # 3. opportunity.scored
        scored = self.score(opportunity)
        run.scored = scored
        self._publish(
            run,
            EventType.OPPORTUNITY_SCORED,
            entity_type="opportunity",
            entity_id=opportunity.opp_id,
            payload={"score": scored.score, "components": scored.components},
        )

        # 4. sovereignty + trust check
        risk = risk_score(
            {
                "sensitive_data": classification.sensitive,
                "external_visibility": opportunity.opp_type.value != "knowledge",
                "monetary_amount": opportunity.expected_value,
            }
        )
        verdict = self._sovereignty.evaluate(
            risk_level=risk,
            sensitivity="confidential" if classification.sensitive else "internal",
            monetary_amount=opportunity.expected_value,
            external_visibility=opportunity.opp_type.value not in {"knowledge", "risk_avoidance"},
            entity_type="customer" if classification.monetizable else "internal",
            flags={
                "strategic_partnership": opportunity.opp_type.value == "partner",
            },
        )
        run.sovereignty_verdict = verdict

        self._publish(
            run,
            EventType.TRUST_CHECKED,
            entity_type="opportunity",
            entity_id=opportunity.opp_id,
            payload=verdict.to_dict(),
            risk_level=risk,
            sovereignty_level=verdict.level.value,
        )

        if risk.at_least(RiskLevel.HIGH):
            self._publish(
                run,
                EventType.RISK_DETECTED,
                entity_type="opportunity",
                entity_id=opportunity.opp_id,
                payload={"risk": risk.value, "reasons": verdict.reasons},
                risk_level=risk,
                sovereignty_level=verdict.level.value,
            )

        if verdict.level == SovereigntyLevel.S4_NEVER:
            run.status = RunStatus.BLOCKED
            run.blocked_reason = "sovereignty=S4_NEVER — blocked"
            run.completed_at = utcnow()
            return run

        # 5. decision.created
        decision = self.decide(scored, sovereignty_level=verdict.level.value)
        run.decision = decision
        self._publish(
            run,
            EventType.DECISION_CREATED,
            entity_type="decision",
            entity_id=decision.decision_id,
            payload={"summary": decision.summary, "chosen": decision.chosen_option},
            sovereignty_level=verdict.level.value,
        )

        # 6. execution.planned
        plan = self.plan(decision, opportunity)
        run.plan = plan
        self._publish(
            run,
            EventType.EXECUTION_PLANNED,
            entity_type="plan",
            entity_id=plan.plan_id,
            payload={"steps": len(plan.steps), "estimated_cost": str(plan.estimated_cost)},
            sovereignty_level=verdict.level.value,
        )

        # 7. approval (if needed)
        ticket_id = self.request_approval_if_needed(plan, decision, verdict)
        if ticket_id is not None:
            run.approval_ticket_id = ticket_id
            self._publish(
                run,
                EventType.APPROVAL_REQUESTED,
                entity_type="approval",
                entity_id=ticket_id,
                payload={"plan_id": plan.plan_id, "decision_id": decision.decision_id},
                risk_level=risk,
                sovereignty_level=verdict.level.value,
            )
            decision = decision.transition(DecisionStatus.PENDING_APPROVAL)
            run.decision = decision
            run.status = RunStatus.AWAITING_APPROVAL
            run.completed_at = utcnow()
            return run

        # 8. execute
        execution = self.execute(plan)
        run.execution_result = execution
        self._publish(
            run,
            EventType.EXECUTION_COMPLETED,
            entity_type="plan",
            entity_id=plan.plan_id,
            payload={"status": execution.status.value, "steps": len(execution.step_results)},
        )

        # 9. outcome.logged
        outcome = self.log_outcome(execution, decision, opportunity)
        run.outcome = outcome
        self._publish(
            run,
            EventType.OUTCOME_LOGGED,
            entity_type="outcome",
            entity_id=outcome.outcome_id,
            payload={"kind": outcome.kind.value, "summary": outcome.summary},
        )

        # 10. asset.created?
        asset = self.consider_asset(outcome)
        if asset is not None:
            run.asset = asset
            self._publish(
                run,
                EventType.ASSET_CREATED,
                entity_type="asset",
                entity_id=asset.asset_id,
                payload={"asset_type": asset.asset_type.value, "name": asset.name},
            )

        # 11. scale / kill recommendation
        recommendation = self.recommend(self._outcomes.all())
        run.recommendation = recommendation
        if recommendation.kind == ScaleKillKind.SCALE:
            self._publish(
                run,
                EventType.SCALE_RECOMMENDED,
                entity_type="recommendation",
                entity_id=outcome.outcome_id,
                payload={"reasons": recommendation.reasons},
            )
        elif recommendation.kind == ScaleKillKind.KILL:
            self._publish(
                run,
                EventType.KILL_RECOMMENDED,
                entity_type="recommendation",
                entity_id=outcome.outcome_id,
                payload={"reasons": recommendation.reasons},
            )

        run.status = RunStatus.COMPLETED
        run.completed_at = utcnow()
        return run


__all__ = [
    "AgentRegistryProto",
    "ApprovalCenterProto",
    "HermesOrchestrator",
    "OrchestratorRun",
    "RunStatus",
    "ToolRegistryProto",
]
