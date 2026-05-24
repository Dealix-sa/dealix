"""
MCP Security — review gate for any MCP server / tool before it is allowed online.

Hard rules:
  - MCP server without a review = blocked
  - Broad data scope (e.g. "*", "all_tenants") without S4 approval = blocked
  - JSON-RPC tools must be registered + ownerless = blocked
"""

from __future__ import annotations

from dataclasses import dataclass


_DISALLOWED_SCOPES = {"*", "all", "all_tenants", "global"}


@dataclass
class MCPReviewResult:
    approved: bool
    reasons: list[str]


class MCPReviewer:
    def review(
        self,
        *,
        server_name: str,
        owner: str,
        data_scope: str,
        tools: list[str],
        s4_approved: bool = False,
    ) -> MCPReviewResult:
        reasons: list[str] = []
        if not owner:
            reasons.append("mcp_owner_required")
        if data_scope in _DISALLOWED_SCOPES and not s4_approved:
            reasons.append(f"mcp_broad_scope_requires_s4:{data_scope}")
        if not tools:
            reasons.append("mcp_no_tools_declared")
        if not server_name:
            reasons.append("mcp_server_name_required")
        return MCPReviewResult(approved=not reasons, reasons=reasons)
