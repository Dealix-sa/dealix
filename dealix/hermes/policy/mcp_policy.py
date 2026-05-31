"""MCP-policy rule — every MCP call must go through the gateway."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from dealix.hermes.policy.rules import RuleResult


@dataclass(frozen=True)
class MCPGatewayRule:
    name: str = "mcp_calls_must_use_gateway"

    def evaluate(self, context: dict[str, Any]) -> RuleResult:
        if not context.get("is_mcp_call"):
            return RuleResult(rule_name=self.name, passed=True, reason="", severity="info")
        if not context.get("via_gateway"):
            return RuleResult(
                rule_name=self.name,
                passed=False,
                reason="MCP call did not pass through the gateway",
                severity="block",
            )
        if not context.get("server_approved"):
            return RuleResult(
                rule_name=self.name,
                passed=False,
                reason="MCP server is not on the approved registry",
                severity="block",
            )
        return RuleResult(rule_name=self.name, passed=True, reason="", severity="info")
