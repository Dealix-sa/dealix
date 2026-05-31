"""Agent permission and tool-allow-list enforcement."""

from __future__ import annotations

from dealix.hermes.trust.agent_registry import AgentCard


def test_agent_cannot_use_forbidden_tool(orch):
    """No 4: لا Agent بلا Owner + KPI — and tool boundaries."""
    card = orch.agent_registry.get("proposal_factory")
    assert "send_external" in card.forbidden_tools
    assert orch.permission_matrix.can_invoke(
        agent_id="proposal_factory",
        tool_id="send_external",
        workspace_id="dealix_internal",
    ) is False


def test_agent_can_use_allowed_tool(orch):
    can = orch.permission_matrix.can_invoke(
        agent_id="proposal_factory",
        tool_id="draft_proposal",
        workspace_id="dealix_internal",
    )
    assert can is True


def test_unregistered_tool_blocked(orch):
    can = orch.permission_matrix.can_invoke(
        agent_id="proposal_factory",
        tool_id="some_phantom_tool",
        workspace_id="dealix_internal",
    )
    assert can is False


def test_inactive_agent_blocked(orch):
    orch.agent_registry.deactivate("proposal_factory")
    can = orch.permission_matrix.can_invoke(
        agent_id="proposal_factory",
        tool_id="draft_proposal",
        workspace_id="dealix_internal",
    )
    assert can is False


def test_every_agent_has_owner_and_kpis(orch):
    """No 4: لا Agent بلا Owner + KPI."""
    for card in orch.agent_registry.list():
        assert card.owner, f"agent {card.agent_id} missing owner"
        # Read-only agents may have empty kpis if they are purely guardrails;
        # but the core/money/growth agents must declare KPIs.
        if card.domain in {"money", "growth", "customer", "venture"}:
            assert card.kpis, f"agent {card.agent_id} missing kpis"
