"""Hermes orchestrator — the single in-process control loop.

Responsibilities:
  1. Capture signals into the kernel.
  2. Score and rank them into opportunities.
  3. Issue decisions, respecting the sovereignty gate.
  4. Queue executions for the right agent + tool, blocking any that
     would breach trust guardrails.
  5. Record outcomes.
  6. Mint assets from outcomes.
  7. Render the Sovereign Console brief on demand.

The orchestrator is intentionally stateful — it owns the ledgers so
the API router does not have to wire seven globals together. Use
`Orchestrator.fresh()` from tests to get a clean instance.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from threading import RLock
from typing import Any

from dealix.hermes.core.assets import AssetStore, build_from_outcome
from dealix.hermes.core.schemas import (
    Asset,
    Decision,
    DecisionVerdict,
    Execution,
    ExecutionStatus,
    MoneyAction,
    MoneyActionSource,
    Opportunity,
    Outcome,
    Signal,
    SovereignBrief,
    TrustCheckOutcome,
    TrustCheckResult,
)
from dealix.hermes.core.scoring import (
    money_priority_score,
    rank_money_actions,
    rank_opportunities,
)
from dealix.hermes.money.dashboard import MoneyDashboard, build_dashboard
from dealix.hermes.money.opportunity_cash_score import hydrate
from dealix.hermes.sovereignty import (
    SovereigntyLevel,
)
from dealix.hermes.sovereignty import (
    evaluate as evaluate_sovereignty,
)
from dealix.hermes.trust.guardrails import TrustContext, trust_check
from dealix.hermes.trust.registry import (
    AgentRegistry,
    ToolRegistry,
    build_default_registries,
)


@dataclass
class Orchestrator:
    """Single-process orchestrator. Thread-safe ledgers."""

    agents: AgentRegistry
    tools: ToolRegistry
    assets: AssetStore = field(default_factory=AssetStore)

    signals: list[Signal] = field(default_factory=list)
    opportunities: list[Opportunity] = field(default_factory=list)
    decisions: list[Decision] = field(default_factory=list)
    executions: list[Execution] = field(default_factory=list)
    outcomes: list[Outcome] = field(default_factory=list)
    money_actions: list[MoneyAction] = field(default_factory=list)
    trust_log: list[TrustCheckResult] = field(default_factory=list)

    _lock: RLock = field(default_factory=RLock, repr=False)

    @classmethod
    def fresh(cls) -> Orchestrator:
        agents, tools = build_default_registries()
        return cls(agents=agents, tools=tools)

    # ── Signal → Opportunity ──────────────────────────────────────────

    def capture_signal(self, signal: Signal) -> Opportunity:
        """Persist a signal and produce its first opportunity."""
        with self._lock:
            self.signals.append(signal)
            value_hint = signal.payload.get("estimated_value_sar")
            try:
                value = float(value_hint) if value_hint is not None else None
            except (TypeError, ValueError):
                value = None

            opp = Opportunity(
                signal_id=signal.id,
                title=signal.payload.get("title")
                or f"{signal.source.value} → {signal.sector or signal.region}",
                sector=signal.sector,
                buyer_persona=signal.payload.get("buyer_persona"),
                pain_hypothesis=signal.payload.get("pain_hypothesis"),
                recommended_offer=signal.payload.get("recommended_offer"),
                estimated_value_sar=value,
                sovereignty_level=SovereigntyLevel.L2_INTERNAL_TASK,
            )
            hydrate(opp, signal)
            self.opportunities.append(opp)
            self._mint_money_action_from(opp)
            return opp

    def _mint_money_action_from(self, opp: Opportunity) -> MoneyAction:
        action = MoneyAction(
            title=opp.title,
            source=MoneyActionSource.DIRECT_CLIENT,
            estimated_value_sar=opp.estimated_value_sar,
            cash_speed_score=opp.cash_speed_score,
            close_probability=opp.close_probability,
            strategic_value_score=opp.strategic_value_score,
            risk_score=opp.risk_score,
            next_action="founder review",
            sovereignty_level=opp.sovereignty_level,  # type: ignore[arg-type]
            opportunity_id=opp.id,
        )
        action.money_priority_score = money_priority_score(action)
        self.money_actions.append(action)
        return action

    # ── Decisions ─────────────────────────────────────────────────────

    def decide(
        self,
        opportunity_id: str,
        verdict: DecisionVerdict,
        rationale: str,
        next_action: str,
    ) -> Decision:
        with self._lock:
            opp = self._get_opportunity(opportunity_id)
            sov = evaluate_sovereignty(next_action)
            decision = Decision(
                opportunity_id=opp.id,
                verdict=verdict,
                rationale=rationale,
                next_action=next_action,
                sovereignty_level=sov.level,
                requires_approval=sov.requires_approval,
                approval_status="pending" if sov.requires_approval else "n/a",
            )
            self.decisions.append(decision)
            return decision

    # ── Trust check ───────────────────────────────────────────────────

    def run_trust_check(self, ctx: TrustContext) -> TrustCheckResult:
        with self._lock:
            result = trust_check(ctx)
            self.trust_log.append(result)
            return result

    # ── Execution ─────────────────────────────────────────────────────

    def execute(
        self,
        decision_id: str,
        agent_id: str,
        tool_id: str | None,
        artifact: dict[str, Any] | None = None,
    ) -> Execution:
        with self._lock:
            decision = self._get_decision(decision_id)
            agent = self.agents.get(agent_id)
            if agent is None:
                return self._fail(
                    decision_id, agent_id, tool_id, "agent not registered"
                )

            if tool_id:
                ok, why = self.tools.can_agent_call(agent, tool_id)
                if not ok:
                    return self._fail(decision_id, agent_id, tool_id, why)

            if decision.requires_approval and decision.approval_status != "approved":
                exe = Execution(
                    decision_id=decision_id,
                    agent_id=agent_id,
                    tool_id=tool_id,
                    status=ExecutionStatus.BLOCKED,
                    artifact=artifact or {},
                    error="awaiting sovereign approval",
                )
                self.executions.append(exe)
                return exe

            exe = Execution(
                decision_id=decision_id,
                agent_id=agent_id,
                tool_id=tool_id,
                status=ExecutionStatus.EXECUTED,
                artifact=artifact or {},
            )
            self.executions.append(exe)
            return exe

    def approve(self, decision_id: str) -> Decision:
        with self._lock:
            decision = self._get_decision(decision_id)
            if not decision.requires_approval:
                return decision
            decision.approval_status = "approved"
            return decision

    def reject(self, decision_id: str, reason: str) -> Decision:
        with self._lock:
            decision = self._get_decision(decision_id)
            decision.approval_status = "rejected"
            decision.rationale = f"{decision.rationale} | rejected: {reason}"
            return decision

    # ── Outcome + Asset ───────────────────────────────────────────────

    def log_outcome(self, outcome: Outcome) -> tuple[Outcome, Asset]:
        with self._lock:
            self.outcomes.append(outcome)
            asset = build_from_outcome(outcome)
            self.assets.add(asset)
            return outcome, asset

    # ── Sovereign Console ─────────────────────────────────────────────

    def sovereign_brief(self, top_n: int = 5) -> SovereignBrief:
        with self._lock:
            ranked_actions = rank_money_actions(list(self.money_actions))
            ranked_opps = rank_opportunities(list(self.opportunities))
            fastest = sorted(
                ranked_actions, key=lambda a: a.cash_speed_score, reverse=True
            )[:top_n]

            pending = [
                d
                for d in self.decisions
                if d.requires_approval and d.approval_status == "pending"
            ]
            blocked: list[dict[str, Any]] = [
                {
                    "execution_id": e.id,
                    "decision_id": e.decision_id,
                    "agent_id": e.agent_id,
                    "tool_id": e.tool_id,
                    "reason": e.error,
                }
                for e in self.executions
                if e.status == ExecutionStatus.BLOCKED
                or e.status == ExecutionStatus.FAILED
            ]

            dashboard = build_dashboard(ranked_actions, top_n=top_n)
            return SovereignBrief(
                fastest_cash_actions=fastest,
                highest_strategic_opportunities=ranked_opps[:top_n],
                pending_approvals=pending,
                blocked_risks=blocked,
                kill_recommendations=list(dashboard.kill_scale.pause_or_kill),
                scale_recommendations=list(dashboard.kill_scale.scale),
                notes=(
                    f"pipeline={dashboard.pipeline_value_sar:.0f} SAR | "
                    f"weighted={dashboard.weighted_pipeline_sar:.0f} SAR"
                ),
            )

    def money_dashboard(self, top_n: int = 5) -> MoneyDashboard:
        with self._lock:
            return build_dashboard(list(self.money_actions), top_n=top_n)

    # ── Internals ─────────────────────────────────────────────────────

    def _get_opportunity(self, opportunity_id: str) -> Opportunity:
        for o in self.opportunities:
            if o.id == opportunity_id:
                return o
        raise KeyError(f"opportunity {opportunity_id!r} not found")

    def _get_decision(self, decision_id: str) -> Decision:
        for d in self.decisions:
            if d.id == decision_id:
                return d
        raise KeyError(f"decision {decision_id!r} not found")

    def _fail(
        self, decision_id: str, agent_id: str, tool_id: str | None, error: str
    ) -> Execution:
        exe = Execution(
            decision_id=decision_id,
            agent_id=agent_id,
            tool_id=tool_id,
            status=ExecutionStatus.FAILED,
            error=error,
        )
        self.executions.append(exe)
        return exe


_default_orchestrator: Orchestrator | None = None


def default_orchestrator() -> Orchestrator:
    """Return the process-wide orchestrator, creating it on first use."""
    global _default_orchestrator
    if _default_orchestrator is None:
        _default_orchestrator = Orchestrator.fresh()
    return _default_orchestrator


def reset_default_orchestrator() -> Orchestrator:
    """Replace the process-wide orchestrator. For tests + cold starts."""
    global _default_orchestrator
    _default_orchestrator = Orchestrator.fresh()
    return _default_orchestrator
