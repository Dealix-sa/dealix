"""Tests for AgentRegistry + ToolRegistry."""

from __future__ import annotations

import pytest

from dealix.hermes.core.schemas import RiskLevel, WorkspaceScope
from dealix.trust.agent_registry import (
    AgentEntry,
    AgentFamily,
    AgentRegistry,
    AgentStatus,
    seed_default_registry,
)
from dealix.trust.permissions import PermissionLevel
from dealix.trust.tool_registry import (
    MCPRiskHints,
    ToolEntry,
    ToolRegistry,
    seed_default_tool_registry,
)


def test_seed_registry_covers_all_families() -> None:
    registry = seed_default_registry()
    families = {e.family for e in registry.all()}
    expected = {
        AgentFamily.SOVEREIGN,
        AgentFamily.CORE,
        AgentFamily.MONEY,
        AgentFamily.TRUST,
        AgentFamily.PRODUCT,
        AgentFamily.MARKET,
        AgentFamily.PARTNER,
        AgentFamily.CUSTOMER,
        AgentFamily.VENTURE,
    }
    assert expected.issubset(families)


def test_agent_register_and_get_round_trip() -> None:
    registry = AgentRegistry()
    entry = AgentEntry(
        agent_id="test_agent",
        name="Test Agent",
        family=AgentFamily.CORE,
        permission_level=PermissionLevel.L1_DRAFT,
        allowed_tools={"crm_sync"},
        workspace_scopes={WorkspaceScope.INTERNAL},
    )
    registry.register(entry)
    assert registry.get("test_agent") is entry
    assert registry.list_by_family(AgentFamily.CORE) == [entry]


def test_agent_register_rejects_duplicate() -> None:
    registry = AgentRegistry()
    entry = AgentEntry(
        agent_id="dup",
        name="Dup",
        family=AgentFamily.CORE,
        permission_level=PermissionLevel.L0_OBSERVE,
    )
    registry.register(entry)
    with pytest.raises(ValueError):
        registry.register(entry)


def test_assert_can_use_tool_raises_when_not_allowed() -> None:
    registry = seed_default_registry()
    with pytest.raises(PermissionError):
        registry.assert_can_use_tool("ProposalFactoryAgent", "payment_charge")


def test_assert_can_use_tool_succeeds_when_allowed() -> None:
    registry = seed_default_registry()
    entry = registry.assert_can_use_tool("ProposalFactoryAgent", "proposal_render")
    assert entry.agent_id == "ProposalFactoryAgent"


def test_pause_blocks_further_tool_use() -> None:
    registry = seed_default_registry()
    registry.pause("ProposalFactoryAgent", reason="under review")
    assert registry.get("ProposalFactoryAgent").status == AgentStatus.PAUSED
    with pytest.raises(PermissionError):
        registry.assert_can_use_tool("ProposalFactoryAgent", "proposal_render")


def test_resume_restores_active_status() -> None:
    registry = seed_default_registry()
    registry.pause("ProposalFactoryAgent", reason="x")
    registry.resume("ProposalFactoryAgent")
    assert registry.get("ProposalFactoryAgent").status == AgentStatus.ACTIVE


def test_tool_register_and_block() -> None:
    registry = ToolRegistry()
    entry = ToolEntry(
        tool_id="custom_tool",
        name="Custom",
        vendor="vendor_x",
        risk_level=RiskLevel.LOW,
    )
    registry.register(entry)
    assert registry.get("custom_tool") is entry
    registry.block("custom_tool", "found drift")
    with pytest.raises(PermissionError):
        registry.assert_callable("custom_tool", agent_id="ProposalFactoryAgent")


def test_default_tool_registry_blocks_payment_charge() -> None:
    registry = seed_default_tool_registry()
    with pytest.raises(PermissionError):
        registry.assert_callable("payment_charge", agent_id="ProposalFactoryAgent")


def test_allowlist_re_enables_tool() -> None:
    registry = seed_default_tool_registry()
    registry.allowlist("payment_charge", evidence_ref="epk_review")
    entry = registry.assert_callable("payment_charge", agent_id="ProposalFactoryAgent")
    assert entry.allowlisted is True
    assert entry.review_evidence_ref == "epk_review"


def test_data_scope_enforcement() -> None:
    registry = seed_default_tool_registry()
    with pytest.raises(PermissionError):
        registry.assert_callable(
            "email_send", agent_id="ProposalFactoryAgent", data_scope="venture"
        )
    entry = registry.assert_callable(
        "email_send", agent_id="ProposalFactoryAgent", data_scope="customer"
    )
    assert entry.tool_id == "email_send"


def test_mark_risk_adds_mcp_risk_hint() -> None:
    registry = seed_default_tool_registry()
    entry = registry.mark_risk("email_send", MCPRiskHints.EXCESSIVE_SCOPE)
    assert MCPRiskHints.EXCESSIVE_SCOPE in entry.mcp_risks


def test_unknown_agent_or_tool_raises_key_error() -> None:
    registry = AgentRegistry()
    tools = ToolRegistry()
    with pytest.raises(KeyError):
        registry.get("nope")
    with pytest.raises(KeyError):
        tools.get("nope")
