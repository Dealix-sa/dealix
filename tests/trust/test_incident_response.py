"""Incident response tests."""

from __future__ import annotations

import pytest

from dealix.trust.agent_registry import AgentStatus, seed_default_registry
from dealix.trust.incident_response import (
    IncidentResponse,
    IncidentSeverity,
    IncidentStatus,
)
from dealix.trust.tool_registry import seed_default_tool_registry


def test_declare_sev1_auto_pauses_implicated_agents() -> None:
    agents = seed_default_registry()
    tools = seed_default_tool_registry()
    ir = IncidentResponse(agent_registry=agents, tool_registry=tools)
    incident = ir.declare(
        severity=IncidentSeverity.SEV1,
        summary="customer data leak in email_send",
        implicated_agents=["ProposalFactoryAgent"],
        implicated_tools=["email_send"],
        evidence_refs=["epk_42"],
    )
    assert incident.severity == IncidentSeverity.SEV1
    assert "ProposalFactoryAgent" in incident.agents_paused
    assert agents.get("ProposalFactoryAgent").status == AgentStatus.PAUSED
    assert "email_send" in incident.tools_blocked
    assert tools.get("email_send").allowlisted is False


def test_declare_sev2_pauses_agents_but_not_tools() -> None:
    agents = seed_default_registry()
    tools = seed_default_tool_registry()
    ir = IncidentResponse(agent_registry=agents, tool_registry=tools)
    incident = ir.declare(
        severity=IncidentSeverity.SEV2,
        summary="degraded performance",
        implicated_agents=["ProposalFactoryAgent"],
        implicated_tools=["email_send"],
    )
    assert agents.get("ProposalFactoryAgent").status == AgentStatus.PAUSED
    assert tools.get("email_send").allowlisted is True
    assert "email_send" not in incident.tools_blocked


def test_declare_sev3_does_not_auto_pause() -> None:
    agents = seed_default_registry()
    ir = IncidentResponse(agent_registry=agents)
    ir.declare(
        severity=IncidentSeverity.SEV3,
        summary="warning",
        implicated_agents=["ProposalFactoryAgent"],
    )
    assert agents.get("ProposalFactoryAgent").status == AgentStatus.ACTIVE


def test_state_machine_open_to_mitigating_to_resolved() -> None:
    ir = IncidentResponse()
    incident = ir.declare(IncidentSeverity.SEV3, summary="x")
    incident = ir.mitigate(incident.incident_id, action="rolled back deploy")
    assert incident.status == IncidentStatus.MITIGATING
    incident = ir.resolve(incident.incident_id)
    assert incident.status == IncidentStatus.RESOLVED
    assert incident.resolved_at is not None


def test_resolve_with_postmortem_transitions_to_postmortem() -> None:
    ir = IncidentResponse()
    incident = ir.declare(IncidentSeverity.SEV3, summary="x")
    ir.resolve(incident.incident_id)
    incident = ir.close_with_postmortem(incident.incident_id, postmortem_ref="pm_1")
    assert incident.status == IncidentStatus.POSTMORTEM
    assert incident.postmortem_ref == "pm_1"


def test_illegal_state_transition_raises() -> None:
    ir = IncidentResponse()
    incident = ir.declare(IncidentSeverity.SEV3, summary="x")
    with pytest.raises(ValueError):
        ir.close_with_postmortem(incident.incident_id, postmortem_ref="pm")


def test_unknown_implicated_agent_recorded_in_notes() -> None:
    agents = seed_default_registry()
    ir = IncidentResponse(agent_registry=agents)
    incident = ir.declare(
        IncidentSeverity.SEV1,
        summary="x",
        implicated_agents=["DoesNotExist"],
    )
    assert any("DoesNotExist" in n for n in incident.notes)


def test_open_filter_excludes_postmortem_incidents() -> None:
    ir = IncidentResponse()
    a = ir.declare(IncidentSeverity.SEV3, summary="a")
    ir.resolve(a.incident_id)
    ir.close_with_postmortem(a.incident_id, postmortem_ref="pm_a")
    ir.declare(IncidentSeverity.SEV3, summary="b")
    open_incidents = ir.open()
    assert len(open_incidents) == 1
    assert open_incidents[0].summary == "b"
