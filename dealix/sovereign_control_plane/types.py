"""
Shared enums for the Sovereign Value Control Plane.

These types encode the sovereign ordering, sensitivity, and lifecycle
vocabulary used throughout the control plane. They are intentionally
free of imports beyond the standard library so any sub-module can use
them without creating cycles.
"""

from __future__ import annotations

from enum import StrEnum


class SovereigntyLevel(StrEnum):
    """How sovereign an action is — drives auto/approve/lockdown gating."""

    S0_AUTONOMOUS = "S0_AUTONOMOUS"
    S1_TEAM_NOTIFY = "S1_TEAM_NOTIFY"
    S2_SAMI_APPROVAL = "S2_SAMI_APPROVAL"
    S3_SAMI_DECISION = "S3_SAMI_DECISION"
    S4_SOVEREIGN_LOCKDOWN = "S4_SOVEREIGN_LOCKDOWN"


class RiskLevel(StrEnum):
    NONE = "none"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class DataSensitivity(StrEnum):
    PUBLIC = "PUBLIC"
    INTERNAL = "INTERNAL"
    CONFIDENTIAL = "CONFIDENTIAL"
    RESTRICTED = "RESTRICTED"
    SOVEREIGN = "SOVEREIGN"


class WorkspaceType(StrEnum):
    SOVEREIGN = "SOVEREIGN"
    DEALIX_INTERNAL = "DEALIX_INTERNAL"
    CUSTOMER = "CUSTOMER"
    PARTNER = "PARTNER"
    TRUST = "TRUST"
    VENTURE = "VENTURE"
    MARKETPLACE = "MARKETPLACE"
    API = "API"


class SecurityMode(StrEnum):
    DRAFT_ONLY = "DRAFT_ONLY"
    APPROVAL_GATED = "APPROVAL_GATED"
    LOW_RISK_AUTONOMY = "LOW_RISK_AUTONOMY"
    ENTERPRISE_CONTROLLED = "ENTERPRISE_CONTROLLED"
    SOVEREIGN_LOCKDOWN = "SOVEREIGN_LOCKDOWN"


class IdentityKind(StrEnum):
    SAMI = "SAMI"
    INTERNAL_OPERATOR = "INTERNAL_OPERATOR"
    CUSTOMER_ADMIN = "CUSTOMER_ADMIN"
    CUSTOMER_USER = "CUSTOMER_USER"
    PARTNER_ADMIN = "PARTNER_ADMIN"
    AGENT = "AGENT"
    TOOL = "TOOL"
    API_CLIENT = "API_CLIENT"
    MARKETPLACE_PUBLISHER = "MARKETPLACE_PUBLISHER"

    def rank(self) -> int:
        """Sovereign ordering — Sami highest, automation lowest."""
        order = {
            IdentityKind.SAMI: 100,
            IdentityKind.INTERNAL_OPERATOR: 80,
            IdentityKind.CUSTOMER_ADMIN: 60,
            IdentityKind.CUSTOMER_USER: 50,
            IdentityKind.PARTNER_ADMIN: 40,
            IdentityKind.API_CLIENT: 30,
            IdentityKind.MARKETPLACE_PUBLISHER: 30,
            IdentityKind.AGENT: 20,
            IdentityKind.TOOL: 10,
        }
        return order[self]


class IncidentSeverity(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class IncidentType(StrEnum):
    AGENT_BEHAVIOR_ANOMALY = "agent_behavior_anomaly"
    TOOL_ABUSE = "tool_abuse"
    MCP_SERVER_COMPROMISE = "mcp_server_compromise"
    DATA_EXFILTRATION_ATTEMPT = "data_exfiltration_attempt"
    POLICY_VIOLATION = "policy_violation"
    APPROVAL_BYPASS_ATTEMPT = "approval_bypass_attempt"
    PARTNER_TRUST_BREACH = "partner_trust_breach"
    CUSTOMER_DATA_INCIDENT = "customer_data_incident"


class ApprovalDecision(StrEnum):
    PENDING = "pending"
    APPROVED = "approved"
    DENIED = "denied"
    CHANGES_REQUESTED = "changes_requested"
    ESCALATED = "escalated"
    KILLED = "killed"


class OfferState(StrEnum):
    DRAFT = "draft"
    INTERNAL_REVIEW = "internal_review"
    PILOT_READY = "pilot_ready"
    ACTIVE = "active"
    PRODUCTIZED = "productized"
    SCALED = "scaled"
    PAUSED = "paused"
    RETIRED = "retired"


OFFER_STATE_ORDER: tuple[OfferState, ...] = (
    OfferState.DRAFT,
    OfferState.INTERNAL_REVIEW,
    OfferState.PILOT_READY,
    OfferState.ACTIVE,
    OfferState.PRODUCTIZED,
    OfferState.SCALED,
)


class RunStatus(StrEnum):
    PENDING = "pending"
    RUNNING = "running"
    BLOCKED = "blocked"
    AWAITING_APPROVAL = "awaiting_approval"
    COMPLETED = "completed"
    FAILED = "failed"
    KILLED = "killed"


class ToolCallStatus(StrEnum):
    ALLOWED = "allowed"
    BLOCKED = "blocked"
    APPROVAL_REQUIRED = "approval_required"
    KILLED = "killed"
    EXECUTED = "executed"
    FAILED = "failed"
