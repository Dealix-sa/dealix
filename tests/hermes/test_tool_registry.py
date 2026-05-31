"""Tool registry doctrine."""

from __future__ import annotations


def test_dangerous_tools_disabled_by_default(orch):
    """No 5: لا Tool بلا Registry."""
    for tool_id in ("send_external", "transfer_money", "sign_contract", "export_data"):
        t = orch.tool_registry.get(tool_id)
        assert t.enabled is False, f"{tool_id} should be disabled by default"
        assert t.requires_approval is True


def test_pdpl_tools_flagged(orch):
    for tool_id in ("send_external", "export_data"):
        t = orch.tool_registry.get(tool_id)
        assert t.pdpl_relevant is True


def test_tool_requires_registry(orch):
    """No 5: لا Tool بلا Registry — unknown tool cannot be invoked."""
    can = orch.permission_matrix.can_invoke(
        agent_id="proposal_factory",
        tool_id="unknown_phantom",
        workspace_id="dealix_internal",
    )
    assert can is False
