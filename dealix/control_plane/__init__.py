"""
Dealix — Control Plane (Level Max System Spec).

This package is the *sovereign kernel* of Dealix. It implements sections
51–80 of `docs/level_max/DEALIX_LEVEL_MAX_SYSTEM_SPEC_AR.md`:

    51. Sovereignty (Control Plane, not just an App)
    52. Identity & Access
    53. Tenant & Workspace
    54. Data Classification
    55–56. Context Feed Engine + Context Packets
    57. Memory System
    58. Policy Engine
    59. Approval Center
    60. Audit & Evidence
    61. Agent Runtime
    62. Tool Runtime
    63. MCP Gateway
    64. Security Modes
    65. Incident Response
    66. Money Command
    67. Offer System
    68. Asset Library
    69. Intelligence Graph
    70. Scale/Kill Board
    71. Customer Loop
    72. Partner Loop
    73. Venture Loop
    74. Public API Readiness
    75. Marketplace Readiness
    76. UI Philosophy (data + contracts only — UI lives in frontend)
    77. Health Dashboard
    78. Commercial Packaging
    79–80. System Composition (ControlPlane facade)

Sovereignty rule:
    Sami > Internal > Customer > Partner > Agent > Tool

Doctrine:
    No external action without an Approval Card stamped by an authorised
    Sami identity. No raw unrestricted context — only scoped packets.
    Every meaningful event leaves an audit trail.
"""

from __future__ import annotations

from dealix.control_plane.agent_runtime import (
    AgentRun,
    AgentRunRegistry,
    AgentRunStatus,
)
from dealix.control_plane.approval_center import (
    ApprovalCard,
    ApprovalCenter,
    ApprovalDecision,
    SovereigntyLevel,
)
from dealix.control_plane.asset_library import (
    Asset,
    AssetLibrary,
    AssetType,
)
from dealix.control_plane.audit_evidence import (
    AuditEvent,
    AuditLog,
    EvidencePack as ControlPlaneEvidencePack,
    EvidenceTrigger,
)
from dealix.control_plane.commercial_packaging import (
    CommercialOfferTier,
    CommercialPackaging,
)
from dealix.control_plane.context_feed import (
    AllowedUse,
    ContextFeedEngine,
    ContextPacket,
)
from dealix.control_plane.customer_loop import (
    CustomerValueLoop,
    CustomerValueReport,
)
from dealix.control_plane.data_classification import (
    DataClass,
    DataClassificationPolicy,
    DataRecord,
)
from dealix.control_plane.health_dashboard import (
    HealthDashboard,
    HealthMetrics,
    RedFlag,
)
from dealix.control_plane.identity_access import (
    Identity,
    IdentityKind,
    IdentityRegistry,
    Permission,
)
from dealix.control_plane.incident_response import (
    Incident,
    IncidentLog,
    IncidentSeverity,
    IncidentType,
)
from dealix.control_plane.intelligence_graph import (
    Edge,
    EdgeKind,
    IntelligenceGraph,
    Node,
    NodeKind,
)
from dealix.control_plane.marketplace import (
    MarketplaceReadiness,
)
from dealix.control_plane.mcp_gateway import (
    MCPGateway,
    MCPServer,
    MCPServerStatus,
)
from dealix.control_plane.memory_system import (
    MemorySystem,
    MemoryKind,
)
from dealix.control_plane.money_command import (
    DealRoom,
    MoneyCommand,
    MoneySnapshot,
)
from dealix.control_plane.offer_system import (
    Offer,
    OfferMetrics,
    OfferState,
    OfferSystem,
)
from dealix.control_plane.partner_loop import (
    PartnerRiskKind,
    PartnerValueLoop,
)
from dealix.control_plane.policy_engine import (
    Policy,
    PolicyDecision as CPPolicyDecision,
    PolicyEngine,
    PolicyKind,
    PolicyResult as CPPolicyResult,
)
from dealix.control_plane.public_api import (
    PublicAPIReadiness,
)
from dealix.control_plane.scale_kill_board import (
    KillReason,
    ScaleKillBoard,
    ScaleScore,
)
from dealix.control_plane.security_modes import (
    SecurityMode,
    SecurityModeManager,
)
from dealix.control_plane.sovereignty import (
    SovereigntyTier,
    SOVEREIGNTY_ORDER,
)
from dealix.control_plane.system import ControlPlane, build_default_control_plane
from dealix.control_plane.tenants import (
    Tenant,
    TenantRegistry,
    Workspace,
    WorkspaceKind,
)
from dealix.control_plane.tool_runtime import (
    ToolCall,
    ToolCallStatus,
    ToolRegistry,
    ToolDescriptor,
    ToolRiskLevel,
)
from dealix.control_plane.venture_loop import (
    Venture,
    VentureStage,
    VentureValueLoop,
)

__all__ = [
    # 51
    "SOVEREIGNTY_ORDER",
    "SovereigntyTier",
    # 52
    "Identity",
    "IdentityKind",
    "IdentityRegistry",
    "Permission",
    # 53
    "Tenant",
    "TenantRegistry",
    "Workspace",
    "WorkspaceKind",
    # 54
    "DataClass",
    "DataClassificationPolicy",
    "DataRecord",
    # 55–56
    "AllowedUse",
    "ContextFeedEngine",
    "ContextPacket",
    # 57
    "MemoryKind",
    "MemorySystem",
    # 58
    "Policy",
    "PolicyEngine",
    "PolicyKind",
    "CPPolicyDecision",
    "CPPolicyResult",
    # 59
    "ApprovalCard",
    "ApprovalCenter",
    "ApprovalDecision",
    "SovereigntyLevel",
    # 60
    "AuditEvent",
    "AuditLog",
    "ControlPlaneEvidencePack",
    "EvidenceTrigger",
    # 61
    "AgentRun",
    "AgentRunRegistry",
    "AgentRunStatus",
    # 62
    "ToolCall",
    "ToolCallStatus",
    "ToolRegistry",
    "ToolDescriptor",
    "ToolRiskLevel",
    # 63
    "MCPGateway",
    "MCPServer",
    "MCPServerStatus",
    # 64
    "SecurityMode",
    "SecurityModeManager",
    # 65
    "Incident",
    "IncidentLog",
    "IncidentSeverity",
    "IncidentType",
    # 66
    "DealRoom",
    "MoneyCommand",
    "MoneySnapshot",
    # 67
    "Offer",
    "OfferMetrics",
    "OfferState",
    "OfferSystem",
    # 68
    "Asset",
    "AssetLibrary",
    "AssetType",
    # 69
    "Edge",
    "EdgeKind",
    "IntelligenceGraph",
    "Node",
    "NodeKind",
    # 70
    "KillReason",
    "ScaleKillBoard",
    "ScaleScore",
    # 71
    "CustomerValueLoop",
    "CustomerValueReport",
    # 72
    "PartnerRiskKind",
    "PartnerValueLoop",
    # 73
    "Venture",
    "VentureStage",
    "VentureValueLoop",
    # 74
    "PublicAPIReadiness",
    # 75
    "MarketplaceReadiness",
    # 77
    "HealthDashboard",
    "HealthMetrics",
    "RedFlag",
    # 78
    "CommercialOfferTier",
    "CommercialPackaging",
    # 79–80
    "ControlPlane",
    "build_default_control_plane",
]
