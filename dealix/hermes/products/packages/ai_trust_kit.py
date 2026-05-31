"""AI Trust Kit — policy, registry, approvals, evidence templates."""

from __future__ import annotations

from dealix.hermes.control_plane.sovereignty_gate import SovereigntyLevel
from dealix.hermes.products.offer_market_fit import Package, register_package


AI_TRUST_KIT = Package(
    package_id="ai_trust_kit",
    name="AI Trust Kit",
    buyer="Companies using AI internally without permissions, approvals, or audit trail.",
    pain="No AI use policy, no agent registry, no approval workflow, no evidence pack.",
    deliverables=(
        "AI Use Policy",
        "Agent Registry Template",
        "Tool Permission Matrix",
        "Approval Workflow",
        "Evidence Pack Template",
        "Risk Register",
    ),
    price_range_sar=(5_000, 25_000),
    upsell="AI Governance OS monthly retainer",
    trust_risks=("overclaim", "privacy", "compliance wording"),
    required_approval=SovereigntyLevel.S2_SAMI_APPROVAL,
    delivery_playbook_id="ai_trust_kit_delivery",
    tags=("flagship", "governance"),
)

register_package(AI_TRUST_KIT)
