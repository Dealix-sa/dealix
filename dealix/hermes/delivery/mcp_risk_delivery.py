"""MCP Risk Review — delivery playbook."""

from __future__ import annotations

from dealix.hermes.delivery._playbook import Playbook, PlaybookStep


MCP_RISK_PLAYBOOK = Playbook(
    playbook_id="mcp_risk_delivery",
    package_id="mcp_risk_review",
    steps=(
        PlaybookStep(
            name="MCP server inventory",
            owner="sami",
            inputs=("customer environment",),
            outputs=("mcp_inventory",),
        ),
        PlaybookStep(
            name="Tool risk scoring",
            owner="agent:trust_checker",
            inputs=("mcp_inventory",),
            outputs=("tool_risk_scores",),
            quality_gates=("every tool has sensitivity + reversibility",),
        ),
        PlaybookStep(
            name="Approval-gated registry",
            owner="agent:trust_checker",
            inputs=("tool_risk_scores",),
            outputs=("approval_gated_registry",),
        ),
        PlaybookStep(
            name="Drift monitor wiring",
            owner="agent:trust_checker",
            inputs=("approval_gated_registry",),
            outputs=("drift_monitor",),
        ),
        PlaybookStep(
            name="Quarterly review",
            owner="agent:value_reporter",
            inputs=("drift_monitor", "incidents"),
            outputs=("mcp_risk_review_report",),
            approval_gates=("deliver_customer_report",),
        ),
    ),
    outcome_metrics=("high_risk_tools_gated", "drift_events_detected", "incidents_avoided"),
    upsell_path="MCP Governance retainer.",
)
