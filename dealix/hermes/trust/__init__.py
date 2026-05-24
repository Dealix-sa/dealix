"""Trust Module — no execution without registry, scope, and audit.

* ``agent_registry``  — every Hermes agent has a card with KPIs.
* ``tool_registry``   — every callable tool has an owner + risk level.
* ``permissions``     — matrix joining agents × tools.
* ``approvals``       — approval workflow for S2/S3 actions.
* ``guardrails``      — input/output sanitization (prompt injection,
                        secret leakage, output validation).
* ``evidence``        — evidence packs attached to high-risk decisions.
* ``audit``           — append-only audit log of every gate decision.
* ``mcp_security``    — MCP gateway that vets every external server +
                        per-call data scope.
* ``incident_response`` — register + workflow for trust incidents.
* ``risk_scores``     — per-agent / per-tool risk score over time.
"""

from dealix.hermes.trust.agent_registry import AgentCard, AgentRegistry
from dealix.hermes.trust.audit import AuditLog, AuditEvent
from dealix.hermes.trust.evidence import EvidencePack, EvidenceStore
from dealix.hermes.trust.guardrails import (
    GuardrailReport,
    GuardrailViolation,
    Guardrails,
)
from dealix.hermes.trust.incident_response import (
    Incident,
    IncidentRegister,
    IncidentSeverity,
    IncidentStatus,
)
from dealix.hermes.trust.mcp_security import (
    MCPGateway,
    MCPServerCard,
    MCPViolation,
)
from dealix.hermes.trust.permissions import PermissionMatrix
from dealix.hermes.trust.risk_scores import RiskScoreboard
from dealix.hermes.trust.tool_registry import ToolCard, ToolRegistry
from dealix.hermes.trust.approvals import ApprovalCenter, ApprovalRequest, ApprovalState

__all__ = [
    "AgentCard",
    "AgentRegistry",
    "ApprovalCenter",
    "ApprovalRequest",
    "ApprovalState",
    "AuditLog",
    "AuditEvent",
    "EvidencePack",
    "EvidenceStore",
    "GuardrailReport",
    "GuardrailViolation",
    "Guardrails",
    "Incident",
    "IncidentRegister",
    "IncidentSeverity",
    "IncidentStatus",
    "MCPGateway",
    "MCPServerCard",
    "MCPViolation",
    "PermissionMatrix",
    "RiskScoreboard",
    "ToolCard",
    "ToolRegistry",
]
