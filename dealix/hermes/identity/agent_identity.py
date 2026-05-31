"""
AgentIdentity — the formal identity attached to every Dealix agent.

No agent runs without an identity. Each identity carries explicit
capabilities, an explicit forbidden list, a workspace scope, a maximum
sovereignty level, and is revocable at runtime.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

from dealix.classifications import SensitivityClass
from dealix.hermes.control_plane.sovereignty_gate import SovereigntyLevel
from dealix.hermes.identity.capability_scope import CAPABILITY_REGISTRY


@dataclass
class AgentIdentity:
    agent_id: str
    agent_type: str
    owner: str
    workspace_scope: tuple[str, ...]
    capabilities: tuple[str, ...]
    forbidden_capabilities: tuple[str, ...]
    max_sovereignty_level: SovereigntyLevel
    max_data_sensitivity: SensitivityClass
    allowed_tools: tuple[str, ...] = field(default_factory=tuple)
    revocable: bool = True
    status: str = "active"  # "active" | "revoked" | "suspended"
    registered_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "agent_id": self.agent_id,
            "agent_type": self.agent_type,
            "owner": self.owner,
            "workspace_scope": list(self.workspace_scope),
            "capabilities": list(self.capabilities),
            "forbidden_capabilities": list(self.forbidden_capabilities),
            "max_sovereignty_level": self.max_sovereignty_level.value,
            "max_data_sensitivity": self.max_data_sensitivity.value,
            "allowed_tools": list(self.allowed_tools),
            "revocable": self.revocable,
            "status": self.status,
            "registered_at": self.registered_at.isoformat(),
            "metadata": self.metadata,
        }


AGENT_REGISTRY: dict[str, AgentIdentity] = {}


def register_agent(identity: AgentIdentity) -> AgentIdentity:
    for cap in identity.capabilities:
        if cap == "*":
            continue
        if cap not in CAPABILITY_REGISTRY:
            raise ValueError(
                f"Cannot register agent {identity.agent_id!r}: capability {cap!r} "
                "is not in CAPABILITY_REGISTRY."
            )
        spec = CAPABILITY_REGISTRY[cap]
        if spec.requires_approval and "agent" in spec.forbidden_for:
            raise ValueError(
                f"Agent {identity.agent_id!r} cannot hold sovereign-only capability {cap!r}."
            )
    AGENT_REGISTRY[identity.agent_id] = identity
    return identity


def _seed_default_agents() -> None:
    seeds = [
        AgentIdentity(
            agent_id="revenue_hunter",
            agent_type="money_agent",
            owner="Sami",
            workspace_scope=("dealix_internal",),
            capabilities=("read_icp", "score_leads", "draft_messages"),
            forbidden_capabilities=(
                "send_external_email",
                "approve_pricing",
                "sign_contract",
                "export_customer_data",
            ),
            max_sovereignty_level=SovereigntyLevel.S1_INTERNAL,
            max_data_sensitivity=SensitivityClass.S2,
            allowed_tools=("icp_db", "lead_scorer", "copy_drafter"),
        ),
        AgentIdentity(
            agent_id="proposal_factory",
            agent_type="money_agent",
            owner="Sami",
            workspace_scope=("dealix_internal",),
            capabilities=("read_icp", "draft_commercial_proposal", "record_outcome"),
            forbidden_capabilities=(
                "send_external_email",
                "approve_pricing",
                "sign_contract",
                "export_customer_data",
            ),
            max_sovereignty_level=SovereigntyLevel.S1_INTERNAL,
            max_data_sensitivity=SensitivityClass.S2,
            allowed_tools=("proposal_template", "pricing_engine_readonly"),
        ),
        AgentIdentity(
            agent_id="trust_checker",
            agent_type="governance_agent",
            owner="Sami",
            workspace_scope=("*",),
            capabilities=("read_icp", "record_outcome", "register_asset"),
            forbidden_capabilities=(
                "send_external_email",
                "approve_pricing",
                "sign_contract",
                "export_customer_data",
                "publish_brand_claim",
            ),
            max_sovereignty_level=SovereigntyLevel.S1_INTERNAL,
            max_data_sensitivity=SensitivityClass.S2,
            allowed_tools=("trust_rules",),
        ),
        AgentIdentity(
            agent_id="value_reporter",
            agent_type="customer_agent",
            owner="Sami",
            workspace_scope=("*",),
            capabilities=("read_icp", "register_asset", "record_outcome"),
            forbidden_capabilities=("send_external_email", "publish_brand_claim"),
            max_sovereignty_level=SovereigntyLevel.S3_CUSTOMER_SENSITIVE,
            max_data_sensitivity=SensitivityClass.S3,
            allowed_tools=("value_report_template",),
        ),
        AgentIdentity(
            agent_id="growth_engine",
            agent_type="growth_agent",
            owner="Sami",
            workspace_scope=("dealix_internal",),
            capabilities=("read_icp", "score_leads", "draft_messages", "register_asset", "record_outcome"),
            forbidden_capabilities=("launch_campaign", "approve_pricing", "send_external_email"),
            max_sovereignty_level=SovereigntyLevel.S1_INTERNAL,
            max_data_sensitivity=SensitivityClass.S2,
            allowed_tools=("attribution_engine", "channel_quality_scorer"),
        ),
    ]
    for s in seeds:
        register_agent(s)


_seed_default_agents()
