"""Hermes agent registry models.

The registry is a local configuration layer for Dealix agents. It does not run
external tools by itself; it defines agent roles, risk levels, review needs,
and operating cadence so real automations can be connected safely.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class AgentRiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass(frozen=True)
class AgentDefinition:
    agent_id: str
    name: str
    mission: str
    owner: str
    risk_level: AgentRiskLevel
    cadence: str
    inputs: tuple[str, ...]
    outputs: tuple[str, ...]
    allowed_actions: tuple[str, ...]
    blocked_actions: tuple[str, ...]
    review_required: bool
    escalation_path: str
    success_metrics: tuple[str, ...] = field(default_factory=tuple)


def load_default_registry() -> list[AgentDefinition]:
    """Return the default Hermes agent registry."""

    return [
        AgentDefinition(
            agent_id="hermes-founder-chief-of-staff",
            name="Founder Chief of Staff Agent",
            mission="Summarize executive priorities, blockers, decisions, and weekly outcomes.",
            owner="Founder",
            risk_level=AgentRiskLevel.MEDIUM,
            cadence="daily and weekly",
            inputs=("company scorecard", "issue updates", "decision log", "risk register"),
            outputs=("daily founder brief", "weekly executive memo", "decision queue"),
            allowed_actions=("summarize", "prioritize", "draft internal notes", "create review checklist"),
            blocked_actions=("make final decisions", "send external messages", "change production systems"),
            review_required=True,
            escalation_path="Founder review",
            success_metrics=("blocked decisions reduced", "weekly outcomes completed"),
        ),
        AgentDefinition(
            agent_id="hermes-gtm-intelligence",
            name="GTM Intelligence Agent",
            mission="Research ICP accounts, prepare sales context, and identify proof gaps.",
            owner="GTM Lead",
            risk_level=AgentRiskLevel.MEDIUM,
            cadence="daily",
            inputs=("ICP card", "target accounts", "CRM notes", "public research"),
            outputs=("account brief", "deal risk note", "message angle", "proof gap"),
            allowed_actions=("research", "summarize", "score fit", "draft internal sales prep"),
            blocked_actions=("send outreach without approval", "scrape restricted data", "commit pricing"),
            review_required=True,
            escalation_path="GTM Lead and Founder",
            success_metrics=("qualified meetings", "research time saved", "higher reply quality"),
        ),
        AgentDefinition(
            agent_id="hermes-customer-success",
            name="Customer Success Agent",
            mission="Track onboarding, health, risk, support signals, and customer proof.",
            owner="CS Lead",
            risk_level=AgentRiskLevel.MEDIUM,
            cadence="daily",
            inputs=("customer health", "usage notes", "support notes", "onboarding checklist"),
            outputs=("health summary", "risk flag", "save plan", "proof candidate"),
            allowed_actions=("summarize", "flag risks", "draft internal playbooks", "prepare QBR notes"),
            blocked_actions=("promise outcomes", "change customer contract", "send customer notice without review"),
            review_required=True,
            escalation_path="CS Lead and Founder",
            success_metrics=("time to value", "red accounts reduced", "proof assets created"),
        ),
        AgentDefinition(
            agent_id="hermes-ai-governance",
            name="AI Governance Agent",
            mission="Review AI workflows for data use, risk, evaluation, and human approval requirements.",
            owner="AI/Product Lead",
            risk_level=AgentRiskLevel.HIGH,
            cadence="per release and weekly",
            inputs=("AI registry", "evaluation results", "incident log", "prompt library"),
            outputs=("AI risk review", "eval gap", "release hold recommendation", "control checklist"),
            allowed_actions=("review", "score risk", "recommend hold", "create checklist"),
            blocked_actions=("approve high-risk release alone", "disable review controls", "ignore incident triggers"),
            review_required=True,
            escalation_path="Founder plus Security plus Product",
            success_metrics=("evaluation pass rate", "AI incidents", "unsupported claims reduced"),
        ),
        AgentDefinition(
            agent_id="hermes-security-reliability",
            name="Security and Reliability Agent",
            mission="Watch operational readiness, incidents, dependency posture, and reliability risks.",
            owner="Engineering Lead",
            risk_level=AgentRiskLevel.HIGH,
            cadence="daily and per release",
            inputs=("CI status", "security notes", "incident register", "release checklist"),
            outputs=("release risk note", "incident summary", "follow-up issue list"),
            allowed_actions=("summarize", "flag risks", "prepare incident record", "create checklist"),
            blocked_actions=("rotate secrets", "change infrastructure", "close incidents without owner"),
            review_required=True,
            escalation_path="Engineering Lead and Founder",
            success_metrics=("P1 risk age", "incident response time", "release readiness"),
        ),
        AgentDefinition(
            agent_id="hermes-finance-board",
            name="Finance and Board Agent",
            mission="Prepare founder-level cash, runway, board memo, and decision narratives.",
            owner="Founder",
            risk_level=AgentRiskLevel.MEDIUM,
            cadence="weekly and monthly",
            inputs=("KPI dashboard", "pipeline", "cash notes", "hiring plan"),
            outputs=("runway note", "board memo draft", "capital allocation question"),
            allowed_actions=("summarize", "draft internal memo", "flag finance questions"),
            blocked_actions=("give legal or investment advice", "commit spending", "change payroll or banking"),
            review_required=True,
            escalation_path="Founder review",
            success_metrics=("runway visibility", "decision clarity", "board memo readiness"),
        ),
    ]
