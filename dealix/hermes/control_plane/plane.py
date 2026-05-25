"""
ControlPlane — high-level orchestration over the Hermes primitives.

The plane is *stateless* with respect to delivery side-effects: every
decision is a structured verdict that the caller (FastAPI surface,
worker, CLI) executes. The plane is *stateful* with respect to identity,
sessions, provenance, MCP allowlist, and the kill switch.
"""

from __future__ import annotations

from dataclasses import dataclass

from dealix.hermes.agent_comms.cross_agent_validator import (
    CrossAgentValidation,
    validate_cross_agent_message,
)
from dealix.hermes.agent_comms.message_sanitizer import sanitize_message
from dealix.hermes.agent_comms.provenance import AgentMessage
from dealix.hermes.identity.agent_identity import AgentIdentity
from dealix.hermes.identity.capability_scope import check_capability
from dealix.hermes.identity.revocation import RevocationLedger
from dealix.hermes.identity.session_policy import (
    SessionPolicy,
    SessionState,
    start_session,
    validate_session,
)
from dealix.hermes.mcp.gateway import MCPGateway, MCPRequest, MCPVerdict
from dealix.hermes.mcp.kill_switch import KillSwitch
from dealix.hermes.mcp.server_allowlist import ServerAllowlist
from dealix.hermes.provenance.ledger import ProvenanceLedger
from dealix.hermes.provenance.source_metadata import SourceMetadata


@dataclass
class ControlPlaneDecision:
    allowed: bool
    reason: str
    must_request_approval: bool = False


class ControlPlane:
    def __init__(
        self,
        *,
        allowlist: ServerAllowlist | None = None,
        kill_switch: KillSwitch | None = None,
        revocation: RevocationLedger | None = None,
        provenance: ProvenanceLedger | None = None,
    ):
        self.allowlist = allowlist or ServerAllowlist()
        self.kill_switch = kill_switch or KillSwitch()
        self.revocation = revocation or RevocationLedger()
        self.provenance = provenance or ProvenanceLedger()
        self.mcp = MCPGateway(self.allowlist, self.kill_switch)
        self._identities: dict[str, AgentIdentity] = {}
        self._sessions: dict[str, SessionState] = {}

    # --- identity ---
    def register_identity(self, identity: AgentIdentity) -> AgentIdentity:
        if identity.agent_id in self._identities:
            raise ValueError(f"identity {identity.agent_id} already registered")
        self._identities[identity.agent_id] = identity
        return identity

    def get_identity(self, agent_id: str) -> AgentIdentity:
        if agent_id not in self._identities:
            raise KeyError(f"unknown identity {agent_id}")
        return self._identities[agent_id]

    # --- sessions ---
    def open_session(self, agent_id: str, policy: SessionPolicy) -> SessionState:
        identity = self.get_identity(agent_id)
        if self.revocation.is_revoked(identity.agent_id):
            raise PermissionError(f"identity {identity.agent_id} is revoked")
        session = start_session(identity.agent_id, policy)
        self._sessions[session.session_id] = session
        return session

    # --- capability check ---
    def authorize_capability(
        self, session_id: str, capability: str
    ) -> ControlPlaneDecision:
        if session_id not in self._sessions:
            return ControlPlaneDecision(False, "unknown_session")
        session = self._sessions[session_id]
        if self.revocation.is_revoked(session.agent_id):
            return ControlPlaneDecision(False, "identity_revoked")
        ok, reason = validate_session(session)
        if not ok:
            return ControlPlaneDecision(False, f"session:{reason}")
        identity = self.get_identity(session.agent_id)
        check = check_capability(identity, capability)
        if not check.allowed:
            return ControlPlaneDecision(False, f"capability:{check.reason}")
        return ControlPlaneDecision(True, "ok")

    # --- cross-agent messages ---
    def authorize_cross_agent(
        self, message: AgentMessage
    ) -> CrossAgentValidation:
        sender = self.get_identity(message.sender_agent_id)
        receiver = self.get_identity(message.receiver_agent_id)
        return validate_cross_agent_message(message, sender, receiver)

    # --- MCP ---
    def authorize_mcp(self, request: MCPRequest) -> MCPVerdict:
        return self.mcp.evaluate(request)

    # --- provenance helpers ---
    def record_provenance(
        self,
        object_type: str,
        source_metadata: SourceMetadata,
        created_by: str,
        *,
        payload_preview: str = "",
    ):
        return self.provenance.append(
            object_type=object_type,
            source_metadata=source_metadata,
            created_by=created_by,
            payload_preview=payload_preview,
        )

    # --- prompt sanitization helper ---
    @staticmethod
    def sanitize(text: str):
        return sanitize_message(text)
