"""PAGRL: stack global -> workspace -> workflow -> agent -> situational rules."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from . import agent_rules, global_rules, situational_rules, workflow_rules
from .escalation import EscalationTicket, escalate


@dataclass(frozen=True)
class PAGRLDecision:
    decision: str
    reasons: list[str] = field(default_factory=list)
    risk_score: int = 0
    approval_id: str | None = None


def decide(
    *,
    action: str,
    actor: str,
    workflow_id: str,
    context: dict[str, Any],
) -> PAGRLDecision:
    """Run the layered governance reasoning loop; return one of execute|modify|escalate|block."""
    reasons: list[str] = []

    global_result = global_rules.evaluate(action, context)
    if not global_result.allowed:
        return PAGRLDecision(decision="block", reasons=[global_result.reason])

    workflow_result = workflow_rules.evaluate(workflow_id, action, context)
    if not workflow_result.allowed:
        return PAGRLDecision(decision="block", reasons=[workflow_result.reason])

    agent_result = agent_rules.evaluate(actor, action, int(context.get("required_autonomy", 1)))
    if not agent_result.allowed:
        reasons.append(agent_result.reason)
        ticket = _open_ticket(action, actor, agent_result.reason, context)
        return PAGRLDecision(decision="escalate", reasons=reasons, approval_id=ticket.approval_id)

    risk = situational_rules.score(context)
    if risk.escalate:
        reasons.append(f"situational risk={risk.risk_score} sensitivity={risk.sensitivity}")
        ticket = _open_ticket(action, actor, reasons[-1], context)
        return PAGRLDecision(
            decision="escalate",
            reasons=reasons,
            risk_score=risk.risk_score,
            approval_id=ticket.approval_id,
        )

    if risk.risk_score >= 5:
        return PAGRLDecision(decision="modify", reasons=["situational risk requires modified scope"], risk_score=risk.risk_score)

    return PAGRLDecision(decision="execute", risk_score=risk.risk_score)


def _open_ticket(action: str, actor: str, reason: str, context: dict[str, Any]) -> EscalationTicket:
    return escalate(action=action, actor=actor, reason=reason, context=context)
