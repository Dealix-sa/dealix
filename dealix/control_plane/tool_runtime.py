"""
Section 62 — Tool Runtime Lifecycle.

Every `ToolCall` traverses the lifecycle below and *cannot* execute
without crossing every gate:

    Requested → Tool Registry Check → Permission Check → Data Scope Check
    → Approval if needed → Execute / Block → Audit → Outcome

This module owns the lifecycle. The MCP-specific gateway extends it.
"""

from __future__ import annotations

import uuid
from collections.abc import Callable, Iterable
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any

from dealix.control_plane.data_classification import DataClass


class ToolRiskLevel(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

    @property
    def requires_approval(self) -> bool:
        return self in (ToolRiskLevel.HIGH, ToolRiskLevel.CRITICAL)


class ToolCallStatus(StrEnum):
    REQUESTED = "requested"
    REGISTRY_CHECKED = "registry_checked"
    PERMISSION_CHECKED = "permission_checked"
    SCOPE_CHECKED = "scope_checked"
    BLOCKED_PENDING_APPROVAL = "blocked_pending_approval"
    EXECUTING = "executing"
    COMPLETED = "completed"
    BLOCKED = "blocked"
    OUTCOME_LOGGED = "outcome_logged"


@dataclass(frozen=True)
class ToolDescriptor:
    tool_id: str
    name: str
    owner_identity_id: str
    risk_level: ToolRiskLevel
    data_scope: DataClass
    manifest_hash: str
    enabled: bool = False
    is_external: bool = False
    description: str = ""
    registered_at: datetime = field(default_factory=lambda: datetime.now(UTC))


@dataclass
class ToolCall:
    tool_call_id: str
    tool_id: str
    agent_id: str
    risk_level: ToolRiskLevel
    data_scope: DataClass
    workspace_id: str
    approval_required: bool
    status: ToolCallStatus = ToolCallStatus.REQUESTED
    approval_id: str | None = None
    arguments: dict[str, Any] = field(default_factory=dict)
    result: Any = None
    blocked_reason: str | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    completed_at: datetime | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "tool_call_id": self.tool_call_id,
            "tool_id": self.tool_id,
            "agent_id": self.agent_id,
            "risk_level": self.risk_level.value,
            "data_scope": self.data_scope.label,
            "workspace_id": self.workspace_id,
            "approval_required": self.approval_required,
            "approval_id": self.approval_id,
            "status": self.status.value,
            "arguments": dict(self.arguments),
            "blocked_reason": self.blocked_reason,
            "created_at": self.created_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
        }


ToolExecutor = Callable[[ToolCall], Any]


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, ToolDescriptor] = {}
        self._executors: dict[str, ToolExecutor] = {}
        self._calls: dict[str, ToolCall] = {}

    def register(self, descriptor: ToolDescriptor, executor: ToolExecutor | None = None) -> ToolDescriptor:
        if descriptor.tool_id in self._tools:
            raise ValueError(f"tool already registered: {descriptor.tool_id}")
        self._tools[descriptor.tool_id] = descriptor
        if executor is not None:
            self._executors[descriptor.tool_id] = executor
        return descriptor

    def enable(self, tool_id: str) -> ToolDescriptor:
        descriptor = self.get(tool_id)
        replaced = ToolDescriptor(
            tool_id=descriptor.tool_id,
            name=descriptor.name,
            owner_identity_id=descriptor.owner_identity_id,
            risk_level=descriptor.risk_level,
            data_scope=descriptor.data_scope,
            manifest_hash=descriptor.manifest_hash,
            enabled=True,
            is_external=descriptor.is_external,
            description=descriptor.description,
            registered_at=descriptor.registered_at,
        )
        self._tools[tool_id] = replaced
        return replaced

    def disable(self, tool_id: str) -> ToolDescriptor:
        descriptor = self.get(tool_id)
        replaced = ToolDescriptor(
            tool_id=descriptor.tool_id,
            name=descriptor.name,
            owner_identity_id=descriptor.owner_identity_id,
            risk_level=descriptor.risk_level,
            data_scope=descriptor.data_scope,
            manifest_hash=descriptor.manifest_hash,
            enabled=False,
            is_external=descriptor.is_external,
            description=descriptor.description,
            registered_at=descriptor.registered_at,
        )
        self._tools[tool_id] = replaced
        return replaced

    def get(self, tool_id: str) -> ToolDescriptor:
        try:
            return self._tools[tool_id]
        except KeyError as exc:
            raise KeyError(f"unknown tool: {tool_id}") from exc

    def all(self) -> list[ToolDescriptor]:
        return list(self._tools.values())

    def request(
        self,
        *,
        tool_id: str,
        agent_id: str,
        workspace_id: str,
        arguments: dict[str, Any] | None = None,
    ) -> ToolCall:
        descriptor = self.get(tool_id)
        call = ToolCall(
            tool_call_id=f"tc_{uuid.uuid4().hex[:12]}",
            tool_id=tool_id,
            agent_id=agent_id,
            risk_level=descriptor.risk_level,
            data_scope=descriptor.data_scope,
            workspace_id=workspace_id,
            approval_required=descriptor.risk_level.requires_approval or descriptor.is_external,
            arguments=dict(arguments or {}),
        )
        self._calls[call.tool_call_id] = call
        return call

    def mark_status(self, tool_call_id: str, status: ToolCallStatus) -> ToolCall:
        call = self.get_call(tool_call_id)
        call.status = status
        return call

    def attach_approval(self, tool_call_id: str, approval_id: str) -> ToolCall:
        call = self.get_call(tool_call_id)
        call.approval_id = approval_id
        call.status = ToolCallStatus.BLOCKED_PENDING_APPROVAL
        return call

    def block(self, tool_call_id: str, reason: str) -> ToolCall:
        call = self.get_call(tool_call_id)
        call.status = ToolCallStatus.BLOCKED
        call.blocked_reason = reason
        call.completed_at = datetime.now(UTC)
        return call

    def execute(self, tool_call_id: str) -> ToolCall:
        call = self.get_call(tool_call_id)
        descriptor = self.get(call.tool_id)
        if not descriptor.enabled:
            return self.block(tool_call_id, "tool not enabled")
        if call.approval_required and not call.approval_id:
            return self.block(tool_call_id, "approval required but missing")
        executor = self._executors.get(call.tool_id)
        call.status = ToolCallStatus.EXECUTING
        if executor is None:
            call.result = {"status": "noop", "tool_id": call.tool_id}
        else:
            call.result = executor(call)
        call.status = ToolCallStatus.COMPLETED
        call.completed_at = datetime.now(UTC)
        return call

    def get_call(self, tool_call_id: str) -> ToolCall:
        try:
            return self._calls[tool_call_id]
        except KeyError as exc:
            raise KeyError(f"unknown tool call: {tool_call_id}") from exc

    def calls(self, *, agent_id: str | None = None) -> list[ToolCall]:
        calls: Iterable[ToolCall] = self._calls.values()
        if agent_id is not None:
            calls = (c for c in calls if c.agent_id == agent_id)
        return list(calls)
