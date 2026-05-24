"""Agent Runtime + Tool Runtime + MCP Gateway (sections 61, 62, 63)."""

from __future__ import annotations

import pytest

from dealix.control_plane.agent_runtime import AgentRunRegistry, AgentRunStatus
from dealix.control_plane.data_classification import DataClass
from dealix.control_plane.mcp_gateway import MCPGateway, MCPServerStatus
from dealix.control_plane.tool_runtime import (
    ToolDescriptor,
    ToolRegistry,
    ToolRiskLevel,
    ToolCallStatus,
)


def test_agent_run_requires_outcome_to_complete() -> None:
    registry = AgentRunRegistry()
    run = registry.start(
        agent_id="proposal_factory",
        workspace_id="ws_internal_dealix",
        input_hash="h1",
    )
    with pytest.raises(ValueError):
        run.complete()
    run.outcome_id = "outc_1"
    run.complete()
    assert run.status is AgentRunStatus.COMPLETED


def test_agent_run_lifecycle_advances_forward_only() -> None:
    registry = AgentRunRegistry()
    run = registry.start(
        agent_id="revenue_hunter",
        workspace_id="ws_internal_dealix",
        input_hash="h2",
        outcome_required=False,
    )
    run.advance(AgentRunStatus.CONTEXT_LOADED)
    run.advance(AgentRunStatus.POLICY_CHECKED)
    with pytest.raises(ValueError):
        run.advance(AgentRunStatus.CONTEXT_LOADED)


def test_high_risk_tool_blocks_without_approval() -> None:
    registry = ToolRegistry()
    descriptor = ToolDescriptor(
        tool_id="gmail_send",
        name="Gmail Send",
        owner_identity_id="sami",
        risk_level=ToolRiskLevel.HIGH,
        data_scope=DataClass.CONFIDENTIAL,
        manifest_hash="abc",
        enabled=True,
        is_external=True,
    )
    registry.register(descriptor)
    call = registry.request(
        tool_id="gmail_send", agent_id="followup_agent", workspace_id="ws_internal_dealix"
    )
    assert call.approval_required is True
    blocked = registry.execute(call.tool_call_id)
    assert blocked.status is ToolCallStatus.BLOCKED


def test_mcp_gateway_quarantines_on_manifest_change() -> None:
    tools = ToolRegistry()
    gateway = MCPGateway(tool_registry=tools)
    descriptor = ToolDescriptor(
        tool_id="hubspot_lookup",
        name="HubSpot Lookup",
        owner_identity_id="sami",
        risk_level=ToolRiskLevel.LOW,
        data_scope=DataClass.INTERNAL,
        manifest_hash="initial",
        enabled=True,
    )
    server = gateway.register_server(
        server_id="srv_hubspot",
        display_name="HubSpot MCP",
        manifest_hash="initial",
        tools=[descriptor],
    )
    gateway.allow(server.server_id)
    assert gateway.report_manifest(server.server_id, manifest_hash="initial") is True
    assert gateway.report_manifest(server.server_id, manifest_hash="rugpull") is False
    assert gateway.get(server.server_id).status is MCPServerStatus.QUARANTINED


def test_mcp_kill_switch_disables_all_tools() -> None:
    tools = ToolRegistry()
    gateway = MCPGateway(tool_registry=tools)
    descriptor = ToolDescriptor(
        tool_id="slack_post",
        name="Slack Post",
        owner_identity_id="sami",
        risk_level=ToolRiskLevel.LOW,
        data_scope=DataClass.INTERNAL,
        manifest_hash="m",
        enabled=True,
    )
    gateway.register_server(
        server_id="srv_slack",
        display_name="Slack MCP",
        manifest_hash="m",
        tools=[descriptor],
    )
    gateway.allow("srv_slack")
    gateway.engage_kill_switch()
    assert tools.get("slack_post").enabled is False
    assert gateway.kill_switch_engaged is True
