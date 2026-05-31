"""Hermes agent governance checks."""

from __future__ import annotations

from dataclasses import dataclass

from hermes_agents.registry import AgentDefinition, AgentRiskLevel


@dataclass(frozen=True)
class PolicyFinding:
    agent_id: str
    severity: str
    message: str


def validate_agent(agent: AgentDefinition) -> list[PolicyFinding]:
    findings: list[PolicyFinding] = []

    if not agent.owner:
        findings.append(PolicyFinding(agent.agent_id, "critical", "Missing owner."))

    if agent.risk_level in {AgentRiskLevel.HIGH, AgentRiskLevel.CRITICAL} and not agent.review_required:
        findings.append(PolicyFinding(agent.agent_id, "critical", "High risk requires review."))

    if not agent.escalation_path:
        findings.append(PolicyFinding(agent.agent_id, "high", "Missing escalation path."))

    if not agent.blocked_actions:
        findings.append(PolicyFinding(agent.agent_id, "medium", "Missing blocked action list."))

    if not agent.success_metrics:
        findings.append(PolicyFinding(agent.agent_id, "medium", "Missing success metrics."))

    return findings


def validate_registry(agents: list[AgentDefinition]) -> list[PolicyFinding]:
    findings: list[PolicyFinding] = []
    seen: set[str] = set()

    for agent in agents:
        if agent.agent_id in seen:
            findings.append(PolicyFinding(agent.agent_id, "critical", "Duplicate agent ID."))
        seen.add(agent.agent_id)
        findings.extend(validate_agent(agent))

    return findings
