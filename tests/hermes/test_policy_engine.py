"""Policy engine tests."""

from __future__ import annotations

from dealix.hermes.policy.engine import PolicyEngine, PolicyVerdict
from dealix.hermes.policy.external_action_policy import ExternalActionRule
from dealix.hermes.policy.mcp_policy import MCPGatewayRule
from dealix.hermes.policy.partner_policy import PartnerPolicyRule


def test_external_action_blocked_without_approval():
    engine = PolicyEngine()
    engine.register(ExternalActionRule())
    result = engine.evaluate({"external": True})
    assert result.verdict == PolicyVerdict.deny


def test_external_action_passes_with_approval():
    engine = PolicyEngine()
    engine.register(ExternalActionRule())
    result = engine.evaluate({"external": True, "approval_id": "appr_123"})
    assert result.verdict == PolicyVerdict.allow


def test_mcp_call_must_use_gateway():
    """No 7: لا MCP بلا Gateway + Review."""
    engine = PolicyEngine()
    engine.register(MCPGatewayRule())
    result = engine.evaluate({"is_mcp_call": True, "via_gateway": False, "server_approved": True})
    assert result.verdict == PolicyVerdict.deny


def test_mcp_call_passes_via_gateway_with_approved_server():
    engine = PolicyEngine()
    engine.register(MCPGatewayRule())
    result = engine.evaluate({"is_mcp_call": True, "via_gateway": True, "server_approved": True})
    assert result.verdict == PolicyVerdict.allow


def test_partner_action_requires_review():
    """No 11: لا Partner بلا Performance Review."""
    engine = PolicyEngine()
    engine.register(PartnerPolicyRule())
    result = engine.evaluate({"affects_partner": True})
    assert result.verdict == PolicyVerdict.deny

    result = engine.evaluate({"affects_partner": True, "partner_review_id": "prv_1"})
    assert result.verdict == PolicyVerdict.allow
