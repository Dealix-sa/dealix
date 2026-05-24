"""
MCP server review policy.

MCP is powerful but exposes Dealix to tool poisoning, shadowing, rug-pull
updates, and over-broad data access. Every server must pass this review
and be added to an allowlist before any agent can call it.
"""

from __future__ import annotations

from pydantic import BaseModel

DEFAULT_CONTROLS: tuple[str, ...] = (
    "allowlist server",
    "log all tool calls",
    "disable external execution by default",
    "require Sami approval for sensitive actions",
)


class MCPServerReview(BaseModel):
    server_name: str
    server_url: str | None = None
    owner: str
    requested_tools: list[str]
    data_access_scope: str  # "narrow" | "scoped" | "broad" | "all"
    external_execution: bool
    reviewed: bool = False


class MCPReviewResult(BaseModel):
    approved: bool
    risk_level: str  # low | medium | high | critical
    reasons: list[str]
    required_controls: list[str]


def review_mcp_server(review: MCPServerReview) -> MCPReviewResult:
    reasons: list[str] = []
    controls = list(DEFAULT_CONTROLS)
    risk = "medium"

    if review.external_execution:
        reasons.append("Server can perform external execution.")
        risk = "high"
        controls.append("require explicit per-call approval")

    if review.data_access_scope in {"broad", "all"}:
        reasons.append("Broad data access requested.")
        risk = "critical"
        controls.append("reduce data scope before approval")

    if not review.owner:
        reasons.append("No human owner assigned.")
        risk = "high" if risk != "critical" else risk
        controls.append("assign a single accountable human owner")

    approved = risk == "medium" and not reasons
    return MCPReviewResult(
        approved=approved,
        risk_level=risk,
        reasons=reasons,
        required_controls=controls,
    )
