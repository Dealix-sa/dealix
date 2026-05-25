"""
CapabilityScope — the registry of *what* an agent or actor is allowed to
do. Capabilities are coarser than tools: a single capability such as
``draft_commercial_proposal`` may use several tools, but the
authorization decision is made on the capability + tool pair.

High-risk capabilities are explicitly enumerated below so a static scan
can verify that no agent is granted one without approval routing.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum

from dealix.classifications import SensitivityClass


class RiskLevel(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass(frozen=True)
class Capability:
    capability: str
    description: str
    risk_level: RiskLevel
    allowed_roles: tuple[str, ...]
    requires_approval: bool
    max_data_sensitivity: SensitivityClass
    external_action: bool
    approval_role: str | None = None
    forbidden_for: tuple[str, ...] = field(default_factory=tuple)


CAPABILITY_REGISTRY: dict[str, Capability] = {}


def register_capability(capability: Capability) -> Capability:
    CAPABILITY_REGISTRY[capability.capability] = capability
    return capability


def _seed() -> None:
    seed = [
        Capability(
            capability="read_icp",
            description="Read ICP profile objects for the active workspace.",
            risk_level=RiskLevel.LOW,
            allowed_roles=("revenue_hunter", "proposal_factory", "growth_engine"),
            requires_approval=False,
            max_data_sensitivity=SensitivityClass.S2,
            external_action=False,
        ),
        Capability(
            capability="score_leads",
            description="Score and rank leads against an ICP.",
            risk_level=RiskLevel.LOW,
            allowed_roles=("revenue_hunter", "growth_engine"),
            requires_approval=False,
            max_data_sensitivity=SensitivityClass.S2,
            external_action=False,
        ),
        Capability(
            capability="draft_messages",
            description="Draft message variants for review.",
            risk_level=RiskLevel.LOW,
            allowed_roles=("revenue_hunter", "copywriter"),
            requires_approval=False,
            max_data_sensitivity=SensitivityClass.S2,
            external_action=False,
        ),
        Capability(
            capability="draft_commercial_proposal",
            description="Draft a commercial proposal for Sami review.",
            risk_level=RiskLevel.MEDIUM,
            allowed_roles=("proposal_factory",),
            requires_approval=False,
            max_data_sensitivity=SensitivityClass.S2,
            external_action=False,
        ),
        Capability(
            capability="send_external_email",
            description="Send an outbound email to a non-internal address.",
            risk_level=RiskLevel.HIGH,
            allowed_roles=(),
            requires_approval=True,
            approval_role="Sami",
            max_data_sensitivity=SensitivityClass.S1,
            external_action=True,
        ),
        Capability(
            capability="approve_pricing",
            description="Approve a pricing decision for a proposal.",
            risk_level=RiskLevel.HIGH,
            allowed_roles=(),
            requires_approval=True,
            approval_role="Sami",
            max_data_sensitivity=SensitivityClass.S2,
            external_action=False,
        ),
        Capability(
            capability="sign_contract",
            description="Sign a contract on behalf of Dealix.",
            risk_level=RiskLevel.HIGH,
            allowed_roles=(),
            requires_approval=True,
            approval_role="Sami",
            max_data_sensitivity=SensitivityClass.S3,
            external_action=True,
        ),
        Capability(
            capability="export_customer_data",
            description="Export a customer's data outside of Dealix.",
            risk_level=RiskLevel.HIGH,
            allowed_roles=(),
            requires_approval=True,
            approval_role="Sami",
            max_data_sensitivity=SensitivityClass.S3,
            external_action=True,
        ),
        Capability(
            capability="publish_brand_claim",
            description="Publish a claim attached to the Dealix brand.",
            risk_level=RiskLevel.HIGH,
            allowed_roles=(),
            requires_approval=True,
            approval_role="Sami",
            max_data_sensitivity=SensitivityClass.S0,
            external_action=True,
        ),
        Capability(
            capability="launch_campaign",
            description="Launch a growth campaign with attached spend.",
            risk_level=RiskLevel.HIGH,
            allowed_roles=(),
            requires_approval=True,
            approval_role="Sami",
            max_data_sensitivity=SensitivityClass.S1,
            external_action=True,
        ),
        Capability(
            capability="release_product",
            description="Release a productized package to customers.",
            risk_level=RiskLevel.HIGH,
            allowed_roles=(),
            requires_approval=True,
            approval_role="Sami",
            max_data_sensitivity=SensitivityClass.S2,
            external_action=True,
        ),
        Capability(
            capability="modify_revenue_share",
            description="Change partner revenue share rules.",
            risk_level=RiskLevel.HIGH,
            allowed_roles=(),
            requires_approval=True,
            approval_role="Sami",
            max_data_sensitivity=SensitivityClass.S2,
            external_action=False,
        ),
        Capability(
            capability="publish_public_api",
            description="Expose a new public API endpoint.",
            risk_level=RiskLevel.HIGH,
            allowed_roles=(),
            requires_approval=True,
            approval_role="Sami",
            max_data_sensitivity=SensitivityClass.S2,
            external_action=True,
        ),
        Capability(
            capability="publish_marketplace_item",
            description="List an asset, agent, or package on the marketplace.",
            risk_level=RiskLevel.HIGH,
            allowed_roles=(),
            requires_approval=True,
            approval_role="Sami",
            max_data_sensitivity=SensitivityClass.S2,
            external_action=True,
        ),
        Capability(
            capability="modify_partner_sla",
            description="Change a partner SLA in production.",
            risk_level=RiskLevel.HIGH,
            allowed_roles=(),
            requires_approval=True,
            approval_role="Sami",
            max_data_sensitivity=SensitivityClass.S2,
            external_action=False,
        ),
        Capability(
            capability="deliver_customer_report",
            description="Deliver a customer-facing value report.",
            risk_level=RiskLevel.MEDIUM,
            allowed_roles=("proposal_factory", "value_reporter"),
            requires_approval=True,
            approval_role="Sami",
            max_data_sensitivity=SensitivityClass.S3,
            external_action=True,
        ),
        Capability(
            capability="activate_retainer",
            description="Activate a recurring retainer on a customer.",
            risk_level=RiskLevel.HIGH,
            allowed_roles=(),
            requires_approval=True,
            approval_role="Sami",
            max_data_sensitivity=SensitivityClass.S3,
            external_action=True,
        ),
        Capability(
            capability="read_sovereign_memory",
            description="Read Sami's sovereign memory.",
            risk_level=RiskLevel.HIGH,
            allowed_roles=(),
            requires_approval=True,
            approval_role="Sami",
            max_data_sensitivity=SensitivityClass.S3,
            external_action=False,
            forbidden_for=("agent", "customer", "partner", "system"),
        ),
        Capability(
            capability="execute_sovereign_strategy",
            description="Execute a sovereign-only strategic action.",
            risk_level=RiskLevel.HIGH,
            allowed_roles=(),
            requires_approval=True,
            approval_role="Sami",
            max_data_sensitivity=SensitivityClass.S3,
            external_action=True,
            forbidden_for=("agent", "customer", "partner", "system"),
        ),
        Capability(
            capability="record_outcome",
            description="Record an Outcome against a previous request.",
            risk_level=RiskLevel.LOW,
            allowed_roles=("*",),
            requires_approval=False,
            max_data_sensitivity=SensitivityClass.S2,
            external_action=False,
        ),
        Capability(
            capability="register_asset",
            description="Register a new reusable asset in the asset store.",
            risk_level=RiskLevel.LOW,
            allowed_roles=("*",),
            requires_approval=False,
            max_data_sensitivity=SensitivityClass.S2,
            external_action=False,
        ),
        Capability(
            capability="run_workflow",
            description="Run a declared workflow.",
            risk_level=RiskLevel.MEDIUM,
            allowed_roles=("*",),
            requires_approval=False,
            max_data_sensitivity=SensitivityClass.S2,
            external_action=False,
        ),
    ]
    for cap in seed:
        register_capability(cap)


_seed()
