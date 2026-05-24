"""
Hermes Tool Gateway — §89.

The single entry point for all agent → tool calls. Enforces:

  1. Tool is registered.
  2. Agent is in the tool's allowlist.
  3. Context packet sensitivity is within tool data_scope.
  4. Policy engine outcomes (block / approval / audit / outcome).
  5. Approval is created when required.
  6. Kill switch is honored.
  7. Result is logged + emitted.
"""

from __future__ import annotations

import threading
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

from dealix.sovereign_control_plane.approvals import SovereignApprovalCenter
from dealix.sovereign_control_plane.context_feed import ContextPacket
from dealix.sovereign_control_plane.events import EventBus, make_event
from dealix.sovereign_control_plane.policy import PolicyEngine
from dealix.sovereign_control_plane.tool_runtime import ToolRuntimeLog
from dealix.sovereign_control_plane.types import (
    DataSensitivity,
    RiskLevel,
    SovereigntyLevel,
    ToolCallStatus,
    WorkspaceType,
)


_SENSITIVITY_ORDER: dict[DataSensitivity, int] = {
    DataSensitivity.PUBLIC: 0,
    DataSensitivity.INTERNAL: 1,
    DataSensitivity.CONFIDENTIAL: 2,
    DataSensitivity.RESTRICTED: 3,
    DataSensitivity.SOVEREIGN: 4,
}


@dataclass
class ToolDescriptor:
    tool_id: str
    name: str
    owner_id: str
    risk_level: RiskLevel
    allowed_agents: list[str]
    allowed_workspaces: list[WorkspaceType]
    data_scope: DataSensitivity
    requires_approval: bool = False
    kill_switch_enabled: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "tool_id": self.tool_id,
            "name": self.name,
            "owner_id": self.owner_id,
            "risk_level": self.risk_level.value,
            "allowed_agents": list(self.allowed_agents),
            "allowed_workspaces": [w.value for w in self.allowed_workspaces],
            "data_scope": self.data_scope.value,
            "requires_approval": self.requires_approval,
            "kill_switch_enabled": self.kill_switch_enabled,
        }


@dataclass
class ToolCallResult:
    status: ToolCallStatus
    tool_id: str
    agent_id: str
    reason: str
    approval_id: str | None = None
    result: dict[str, Any] = field(default_factory=dict)
    record_id: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status.value,
            "tool_id": self.tool_id,
            "agent_id": self.agent_id,
            "reason": self.reason,
            "approval_id": self.approval_id,
            "result": dict(self.result),
            "record_id": self.record_id,
        }


class ToolRegistry:
    def __init__(self) -> None:
        self._items: dict[str, ToolDescriptor] = {}
        self._lock = threading.Lock()

    def register(self, tool: ToolDescriptor) -> ToolDescriptor:
        with self._lock:
            self._items[tool.tool_id] = tool
            return tool

    def get(self, tool_id: str) -> ToolDescriptor | None:
        return self._items.get(tool_id)

    def list(self) -> list[ToolDescriptor]:
        return list(self._items.values())


class HermesToolGateway:
    def __init__(
        self,
        registry: ToolRegistry,
        policy_engine: PolicyEngine,
        approval_center: SovereignApprovalCenter,
        runtime_log: ToolRuntimeLog,
        event_bus: EventBus,
    ) -> None:
        self.registry = registry
        self.policy = policy_engine
        self.approvals = approval_center
        self.log = runtime_log
        self.bus = event_bus
        self._executor: dict[str, callable[..., dict[str, Any]]] = {}

    def register_executor(self, tool_id: str, fn) -> None:
        self._executor[tool_id] = fn

    def call(
        self,
        agent_id: str,
        tool_id: str,
        args: dict[str, Any],
        context_packet: ContextPacket | None = None,
    ) -> ToolCallResult:
        tool = self.registry.get(tool_id)
        if tool is None:
            return self._fail(tool_id, agent_id, "tool_not_registered", None, args)
        if agent_id not in tool.allowed_agents and "*" not in tool.allowed_agents:
            return self._fail(tool_id, agent_id, "agent_not_allowed",
                              context_packet, args, tool=tool)
        if context_packet is not None and self._exceeds_scope(
            context_packet.sensitivity, tool.data_scope
        ):
            return self._fail(tool_id, agent_id, "sensitivity_exceeds_scope",
                              context_packet, args, tool=tool)
        if tool.kill_switch_enabled:
            return self._kill(tool, agent_id, context_packet, args)

        event = {
            "action_type": "tool_call",
            "tool_risk": tool.risk_level.value,
            "channel": "tool",
            "workspace_kind": (
                tool.allowed_workspaces[0].value if tool.allowed_workspaces else None
            ),
        }
        outcomes = self.policy.evaluate(event)
        if any(o.block for o in outcomes):
            return self._fail(tool_id, agent_id, "policy_block",
                              context_packet, args, tool=tool)

        needs_approval = tool.requires_approval or any(o.requires_approval for o in outcomes)
        if needs_approval:
            req = self.approvals.submit(
                requested_by=agent_id,
                workspace_id=context_packet.workspace_id if context_packet else "system",
                action_type="tool_activation",
                sovereignty_level=SovereigntyLevel.S2_SAMI_APPROVAL,
                risk_level=tool.risk_level,
                summary=f"tool {tool.name} called by {agent_id}",
                payload_preview={"args": args},
            )
            rec = self.log.record(
                tool_id=tool_id,
                agent_id=agent_id,
                workspace_id=context_packet.workspace_id if context_packet else "system",
                context_id=context_packet.context_id if context_packet else None,
                args_preview=args,
                risk_level=tool.risk_level,
                status=ToolCallStatus.APPROVAL_REQUIRED,
                reason="approval_required",
                approval_id=req.approval_id,
            )
            return ToolCallResult(
                status=ToolCallStatus.APPROVAL_REQUIRED,
                tool_id=tool_id, agent_id=agent_id,
                reason="approval_required",
                approval_id=req.approval_id, record_id=rec.call_id,
            )

        # Execute (or stub) and record success.
        executor = self._executor.get(tool_id)
        result = executor(args) if executor else {"ok": True, "stub": True}
        rec = self.log.record(
            tool_id=tool_id, agent_id=agent_id,
            workspace_id=context_packet.workspace_id if context_packet else "system",
            context_id=context_packet.context_id if context_packet else None,
            args_preview=args, risk_level=tool.risk_level,
            status=ToolCallStatus.EXECUTED, reason="ok",
            result_preview=result,
        )
        self.bus.publish(make_event(
            event_type="tool.executed", source="hermes_tool_gateway",
            payload={"tool_id": tool_id, "agent_id": agent_id, "result_keys": list(result)},
        ))
        return ToolCallResult(
            status=ToolCallStatus.EXECUTED, tool_id=tool_id, agent_id=agent_id,
            reason="ok", result=result, record_id=rec.call_id,
        )

    def _fail(
        self,
        tool_id: str,
        agent_id: str,
        reason: str,
        context: ContextPacket | None,
        args: dict[str, Any],
        tool: ToolDescriptor | None = None,
    ) -> ToolCallResult:
        risk = tool.risk_level if tool else RiskLevel.NONE
        rec = self.log.record(
            tool_id=tool_id, agent_id=agent_id,
            workspace_id=context.workspace_id if context else "system",
            context_id=context.context_id if context else None,
            args_preview=args, risk_level=risk,
            status=ToolCallStatus.BLOCKED, reason=reason,
        )
        return ToolCallResult(
            status=ToolCallStatus.BLOCKED, tool_id=tool_id, agent_id=agent_id,
            reason=reason, record_id=rec.call_id,
        )

    def _kill(
        self,
        tool: ToolDescriptor,
        agent_id: str,
        context: ContextPacket | None,
        args: dict[str, Any],
    ) -> ToolCallResult:
        rec = self.log.record(
            tool_id=tool.tool_id, agent_id=agent_id,
            workspace_id=context.workspace_id if context else "system",
            context_id=context.context_id if context else None,
            args_preview=args, risk_level=tool.risk_level,
            status=ToolCallStatus.KILLED, reason="kill_switch_enabled",
        )
        return ToolCallResult(
            status=ToolCallStatus.KILLED, tool_id=tool.tool_id, agent_id=agent_id,
            reason="kill_switch_enabled", record_id=rec.call_id,
        )

    @staticmethod
    def _exceeds_scope(packet: DataSensitivity, scope: DataSensitivity) -> bool:
        return _SENSITIVITY_ORDER[packet] > _SENSITIVITY_ORDER[scope]
