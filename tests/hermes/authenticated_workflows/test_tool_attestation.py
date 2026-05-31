"""Verify tool attestation accepts only registered (tool, version) pairs."""

from __future__ import annotations

from dealix.hermes.authenticated_workflows.tool_attestation import attest_tool, clear_registry, register_tool


def test_tool_attestation_only_approved_versions() -> None:
    clear_registry()
    register_tool("crm.create_lead", "1.4.0")
    assert attest_tool("crm.create_lead", "1.4.0").approved is True
    assert attest_tool("crm.create_lead", "9.9.9").approved is False
    assert attest_tool("scraper", "1.0.0").approved is False
