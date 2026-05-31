"""AI Trust Kit — delivery playbook."""

from __future__ import annotations

from dealix.hermes.delivery._playbook import Playbook, PlaybookStep


AI_TRUST_KIT_PLAYBOOK = Playbook(
    playbook_id="ai_trust_kit_delivery",
    package_id="ai_trust_kit",
    steps=(
        PlaybookStep(
            name="Discovery and inventory",
            owner="sami",
            inputs=("customer use cases",),
            outputs=("agent_inventory", "tool_inventory"),
        ),
        PlaybookStep(
            name="Draft AI Use Policy",
            owner="agent:proposal_factory",
            inputs=("agent_inventory", "sector context"),
            outputs=("ai_use_policy_draft",),
            quality_gates=("PDPL-aligned wording",),
        ),
        PlaybookStep(
            name="Agent registry and tool matrix",
            owner="agent:trust_checker",
            inputs=("agent_inventory", "tool_inventory"),
            outputs=("agent_registry", "tool_permission_matrix"),
        ),
        PlaybookStep(
            name="Approval workflow and risk register",
            owner="agent:trust_checker",
            inputs=("agent_registry", "tool_permission_matrix"),
            outputs=("approval_workflow", "risk_register"),
        ),
        PlaybookStep(
            name="Evidence pack",
            owner="agent:value_reporter",
            inputs=("approval_workflow", "risk_register"),
            outputs=("evidence_pack",),
            approval_gates=("deliver_customer_report",),
        ),
    ),
    outcome_metrics=(
        "policies_deployed",
        "approval_pass_rate",
        "incidents_reduced",
        "retainer_conversion",
    ),
    upsell_path="AI Governance OS monthly retainer.",
)
