"""
MCP Gateway — the single ingress for every agent → MCP tool call.

No agent is allowed to import an MCP client directly. Every call goes:
  agent → MCPGateway.invoke() → server registry check → tool permission
  check → guardrails → anomaly detection → audit.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from dealix.hermes.mcp.anomaly_detection import AnomalyDetector
from dealix.hermes.mcp.runtime_guardrails import RuntimeGuardrails
from dealix.hermes.mcp.server_registry import MCPServerRegistry
from dealix.hermes.trust.agent_registry import AgentRegistry
from dealix.hermes.trust.audit import AuditEntry, AuditLog


class MCPCall(BaseModel):
    model_config = ConfigDict(extra="forbid")

    agent_id: str
    server_id: str
    tool_name: str
    arguments: dict[str, Any] = Field(default_factory=dict)
    approval_id: str | None = None


class MCPCallResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    allowed: bool
    blocked_reasons: list[str] = Field(default_factory=list)
    output: dict[str, Any] | None = None


@dataclass
class MCPGateway:
    server_registry: MCPServerRegistry
    agent_registry: AgentRegistry
    audit_log: AuditLog
    guardrails: RuntimeGuardrails = field(default_factory=RuntimeGuardrails)
    anomalies: AnomalyDetector = field(default_factory=AnomalyDetector)
    executor: Any = None  # set in production; tests pass a stub

    def invoke(self, call: MCPCall) -> MCPCallResult:
        reasons: list[str] = []

        if not self.agent_registry.exists(call.agent_id):
            reasons.append(f"agent {call.agent_id} is not registered")

        if not self.server_registry.is_approved(call.server_id):
            reasons.append(f"MCP server {call.server_id} is not approved")

        # Tool must be on the agent's allow-list.
        if self.agent_registry.exists(call.agent_id):
            card = self.agent_registry.get(call.agent_id)
            tool_id = f"{call.server_id}::{call.tool_name}"
            if tool_id in card.forbidden_tools:
                reasons.append(f"tool {tool_id} is on agent forbidden list")
            if (
                tool_id not in card.allowed_tools
                and call.tool_name not in card.allowed_tools
            ):
                reasons.append(f"tool {call.tool_name} not in agent allow list")

        # Guardrails: assume registered + audit-will-write at the gateway boundary.
        guard_violations = self.guardrails.enforce({
            "external": False,
            "tool_registered": True,
            "audit_written": True,
            "approval_id": call.approval_id,
        })
        reasons.extend(guard_violations)

        # Anomaly detection runs even on allowed calls so we record patterns.
        anomaly = self.anomalies.observe(
            server_id=call.server_id,
            tool_name=call.tool_name,
            payload=call.arguments,
        )
        if anomaly:
            reasons.append(f"anomaly detected: {anomaly.anomaly_type} ({anomaly.detail})")

        allowed = not reasons
        outcome = "ok" if allowed else "blocked"

        output: dict[str, Any] | None = None
        if allowed and self.executor is not None:
            output = self.executor(call.server_id, call.tool_name, call.arguments)

        self.audit_log.write(AuditEntry(
            actor=call.agent_id,
            action=f"mcp.invoke:{call.server_id}::{call.tool_name}",
            subject_id=call.server_id,
            subject_type="mcp_server",
            outcome=outcome,
            details={
                "tool_name": call.tool_name,
                "blocked_reasons": reasons,
                "occurred_at": datetime.now(UTC).isoformat(),
            },
        ))

        return MCPCallResult(allowed=allowed, blocked_reasons=reasons, output=output)
