"""
Tool Gateway — لا أداة تُستدعى مباشرة. كل tool call يمر هنا ليُسجَّل، يُحاسب،
ويخضع للـ kill switch. هذا مهم لأن أكثر مخاطر agentic AI تأتي من الأدوات
وسياقها (prompt injection غير مباشر، tool override، الخ).
"""

from __future__ import annotations

import threading
import uuid
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

from ..control_plane.kill_switch import KillSwitch, KillTargetKind


ToolFn = Callable[[dict[str, Any]], dict[str, Any]]


@dataclass(frozen=True)
class ToolDescriptor:
    tool_id: str
    description: str
    sensitivity: str  # "read" | "write" | "external"
    allowed_actor_kinds: tuple[str, ...] = ()
    requires_approval: bool = False
    owner: str = "unowned"


@dataclass
class ToolCallResult:
    call_id: str
    tool_id: str
    success: bool
    output: dict[str, Any] = field(default_factory=dict)
    error: str | None = None
    started_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    finished_at: datetime | None = None
    cost_units: float = 0.0


class ToolGateway:
    def __init__(self, kill_switch: KillSwitch | None = None) -> None:
        self._tools: dict[str, tuple[ToolDescriptor, ToolFn]] = {}
        self._calls: list[ToolCallResult] = []
        self._lock = threading.Lock()
        self._kill = kill_switch or KillSwitch()

    def register(self, descriptor: ToolDescriptor, fn: ToolFn) -> None:
        if not descriptor.owner or descriptor.owner == "unowned":
            raise ValueError(
                f"tool `{descriptor.tool_id}` must have an owner (CTRL-GOV-002)"
            )
        with self._lock:
            if descriptor.tool_id in self._tools:
                raise ValueError(f"tool `{descriptor.tool_id}` already registered")
            self._tools[descriptor.tool_id] = (descriptor, fn)

    def descriptors(self) -> list[ToolDescriptor]:
        with self._lock:
            return [d for d, _ in self._tools.values()]

    def call(
        self,
        tool_id: str,
        *,
        args: dict[str, Any],
        actor_kind: str,
        approval_ticket_id: str | None = None,
    ) -> ToolCallResult:
        call = ToolCallResult(
            call_id=f"tcl_{uuid.uuid4().hex[:14]}",
            tool_id=tool_id,
            success=False,
        )
        with self._lock:
            pair = self._tools.get(tool_id)
        if pair is None:
            call.error = f"tool `{tool_id}` not registered"
            return self._finish(call)

        desc, fn = pair
        if not self._kill.is_active(KillTargetKind.TOOL, tool_id):
            call.error = f"tool `{tool_id}` is killed"
            return self._finish(call)
        if (
            desc.allowed_actor_kinds
            and actor_kind not in desc.allowed_actor_kinds
        ):
            call.error = f"actor kind `{actor_kind}` not allowed for `{tool_id}`"
            return self._finish(call)
        if desc.requires_approval and not approval_ticket_id:
            call.error = f"tool `{tool_id}` requires an approval ticket"
            return self._finish(call)

        try:
            output = fn(args) or {}
            if not isinstance(output, dict):
                raise TypeError("tool output must be a dict")
            call.output = output
            call.success = True
        except Exception as exc:  # noqa: BLE001 — boundary
            call.error = f"{type(exc).__name__}: {exc}"
        return self._finish(call)

    def history(self, limit: int = 100) -> list[ToolCallResult]:
        with self._lock:
            return list(self._calls)[-limit:]

    def _finish(self, call: ToolCallResult) -> ToolCallResult:
        call.finished_at = datetime.now(timezone.utc)
        with self._lock:
            self._calls.append(call)
        return call


__all__ = ["ToolCallResult", "ToolDescriptor", "ToolFn", "ToolGateway"]
