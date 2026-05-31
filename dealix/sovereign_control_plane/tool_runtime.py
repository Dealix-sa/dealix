"""
Tool runtime log — §96.

Every tool call (allowed, blocked, killed, executed) is appended here
for observability. Read-only after write.
"""

from __future__ import annotations

import threading
import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

from dealix.sovereign_control_plane.types import RiskLevel, ToolCallStatus


@dataclass
class ToolCallRecord:
    call_id: str
    tool_id: str
    agent_id: str
    workspace_id: str
    context_id: str | None
    args_preview: dict[str, Any]
    risk_level: RiskLevel
    status: ToolCallStatus
    reason: str
    approval_id: str | None
    result_preview: dict[str, Any]
    started_at: str
    finished_at: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "call_id": self.call_id,
            "tool_id": self.tool_id,
            "agent_id": self.agent_id,
            "workspace_id": self.workspace_id,
            "context_id": self.context_id,
            "args_preview": dict(self.args_preview),
            "risk_level": self.risk_level.value,
            "status": self.status.value,
            "reason": self.reason,
            "approval_id": self.approval_id,
            "result_preview": dict(self.result_preview),
            "started_at": self.started_at,
            "finished_at": self.finished_at,
        }


class ToolRuntimeLog:
    def __init__(self) -> None:
        self._records: list[ToolCallRecord] = []
        self._lock = threading.Lock()

    def record(
        self,
        *,
        tool_id: str,
        agent_id: str,
        workspace_id: str,
        context_id: str | None,
        args_preview: dict[str, Any],
        risk_level: RiskLevel,
        status: ToolCallStatus,
        reason: str = "",
        approval_id: str | None = None,
        result_preview: dict[str, Any] | None = None,
    ) -> ToolCallRecord:
        rec = ToolCallRecord(
            call_id=f"tcl_{uuid.uuid4().hex[:12]}",
            tool_id=tool_id,
            agent_id=agent_id,
            workspace_id=workspace_id,
            context_id=context_id,
            args_preview=dict(args_preview),
            risk_level=risk_level,
            status=status,
            reason=reason,
            approval_id=approval_id,
            result_preview=dict(result_preview or {}),
            started_at=datetime.now(UTC).isoformat(),
            finished_at=datetime.now(UTC).isoformat(),
        )
        with self._lock:
            self._records.append(rec)
        return rec

    def list_by_agent(self, agent_id: str) -> list[ToolCallRecord]:
        return [r for r in self._records if r.agent_id == agent_id]

    def list_blocked(self) -> list[ToolCallRecord]:
        blocked = {ToolCallStatus.BLOCKED, ToolCallStatus.KILLED}
        return [r for r in self._records if r.status in blocked]

    def all_records(self) -> list[ToolCallRecord]:
        return list(self._records)
