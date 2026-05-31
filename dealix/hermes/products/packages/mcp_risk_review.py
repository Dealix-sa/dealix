"""MCP Risk Review — descriptor audit + approval-gated tool registry."""

from __future__ import annotations

from dealix.hermes.control_plane.sovereignty_gate import SovereigntyLevel
from dealix.hermes.products.offer_market_fit import Package, register_package


MCP_RISK_REVIEW = register_package(
    Package(
        package_id="mcp_risk_review",
        name="MCP Risk Review",
        buyer="Teams running MCP servers exposed to LLMs without review or approval gates.",
        pain="MCP descriptors are unreviewed, unpinned, and tools fire without approval.",
        deliverables=(
            "MCP server inventory",
            "Tool risk scores",
            "Approval-gated tool registry",
            "Descriptor drift monitor",
            "Quarterly review cadence",
        ),
        price_range_sar=(10_000, 35_000),
        upsell="MCP Governance retainer",
        trust_risks=("missed descriptor changes", "scope creep into product audits"),
        required_approval=SovereigntyLevel.S2_SAMI_APPROVAL,
        delivery_playbook_id="mcp_risk_delivery",
        tags=("governance", "security"),
    )
)
