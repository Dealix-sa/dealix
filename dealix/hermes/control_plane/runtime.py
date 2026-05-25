"""
ControlPlaneRuntime — the only legitimate entry point for any
agent / tool / workflow call inside Dealix.

Lifecycle::

    runtime = ControlPlaneRuntime()
    decision = runtime.dispatch(
        context=RequestContext.new(...),
        actor=resolve(...),
        agent=registry.get("revenue_hunter"),
        execute=lambda ctx: my_handler(ctx),
    )

The runtime returns a ``ControlPlaneDecision`` describing what happened:
allowed and executed, queued for approval, or denied.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from dealix.hermes.control_plane import approval_gate, audit_gate, outcome_gate
from dealix.hermes.control_plane.actor_identity import ActorIdentity
from dealix.hermes.control_plane.policy_enforcement import PolicyVerdict, evaluate
from dealix.hermes.control_plane.request_context import RequestContext
from dealix.hermes.identity.agent_identity import AgentIdentity


class RuntimeOutcome(StrEnum):
    EXECUTED = "executed"
    QUEUED_FOR_APPROVAL = "queued_for_approval"
    DENIED = "denied"
    KILLED = "killed"


@dataclass
class ControlPlaneDecision:
    outcome: RuntimeOutcome
    verdict: PolicyVerdict
    approval_ticket_id: str | None = None
    audit_id: str | None = None
    result: Any | None = None
    reasons: tuple[str, ...] = field(default_factory=tuple)


ExecuteFn = Callable[[RequestContext], Any]


@dataclass
class ControlPlaneRuntime:
    def dispatch(
        self,
        *,
        context: RequestContext,
        actor: ActorIdentity,
        agent: AgentIdentity | None,
        execute: ExecuteFn,
        skip_outcome: bool = False,
    ) -> ControlPlaneDecision:
        verdict = evaluate(context, actor, agent)

        if verdict.kill is not None:
            audit = audit_gate.write(
                request_id=context.request_id,
                actor_id=actor.actor_id,
                capability=context.capability,
                sovereignty=verdict.sovereignty.level.value,
                approval_status="killed",
                trust_passed=verdict.trust.passed,
                data_allowed=verdict.data.allowed,
                tool_allowed=verdict.tool.allowed,
                executed=False,
                outcome_recorded=False,
                findings=verdict.reasons(),
            )
            return ControlPlaneDecision(
                outcome=RuntimeOutcome.KILLED,
                verdict=verdict,
                audit_id=audit.audit_id,
                reasons=verdict.reasons(),
            )

        if not verdict.allowed:
            audit = audit_gate.write(
                request_id=context.request_id,
                actor_id=actor.actor_id,
                capability=context.capability,
                sovereignty=verdict.sovereignty.level.value,
                approval_status="denied",
                trust_passed=verdict.trust.passed,
                data_allowed=verdict.data.allowed,
                tool_allowed=verdict.tool.allowed,
                executed=False,
                outcome_recorded=False,
                findings=verdict.reasons(),
            )
            return ControlPlaneDecision(
                outcome=RuntimeOutcome.DENIED,
                verdict=verdict,
                audit_id=audit.audit_id,
                reasons=verdict.reasons(),
            )

        if verdict.requires_approval:
            status, ticket = approval_gate.evaluate(context, verdict.sovereignty)
            audit = audit_gate.write(
                request_id=context.request_id,
                actor_id=actor.actor_id,
                capability=context.capability,
                sovereignty=verdict.sovereignty.level.value,
                approval_status=status.value,
                trust_passed=verdict.trust.passed,
                data_allowed=verdict.data.allowed,
                tool_allowed=verdict.tool.allowed,
                executed=False,
                outcome_recorded=False,
            )
            return ControlPlaneDecision(
                outcome=RuntimeOutcome.QUEUED_FOR_APPROVAL,
                verdict=verdict,
                approval_ticket_id=ticket.ticket_id if ticket else None,
                audit_id=audit.audit_id,
            )

        result = execute(context)

        outcome_recorded = False
        if not skip_outcome:
            try:
                outcome_gate.require(context.request_id)
                outcome_recorded = True
            except RuntimeError:
                outcome_recorded = False

        audit = audit_gate.write(
            request_id=context.request_id,
            actor_id=actor.actor_id,
            capability=context.capability,
            sovereignty=verdict.sovereignty.level.value,
            approval_status="not_required",
            trust_passed=verdict.trust.passed,
            data_allowed=verdict.data.allowed,
            tool_allowed=verdict.tool.allowed,
            executed=True,
            outcome_recorded=outcome_recorded,
        )

        if not skip_outcome and not outcome_recorded:
            return ControlPlaneDecision(
                outcome=RuntimeOutcome.DENIED,
                verdict=verdict,
                audit_id=audit.audit_id,
                reasons=("outcome_gate: executed without recorded Outcome",),
            )

        return ControlPlaneDecision(
            outcome=RuntimeOutcome.EXECUTED,
            verdict=verdict,
            audit_id=audit.audit_id,
            result=result,
        )
