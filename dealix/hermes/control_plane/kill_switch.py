"""
Kill Switch — يوقف agent/tool/workflow/MCP server/customer workspace فورًا.
الـ runtime يستشير الـ kill switch قبل أي tool call أو agent run، وأي tripped
target يردّ deny فوريًا بدون استدعاء النموذج.
"""

from __future__ import annotations

import threading
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import StrEnum


class KillTargetKind(StrEnum):
    AGENT = "agent"
    TOOL = "tool"
    WORKFLOW = "workflow"
    MCP_SERVER = "mcp_server"
    CUSTOMER_WORKSPACE = "customer_workspace"
    PARTNER_WORKSPACE = "partner_workspace"


class KillSwitchState(StrEnum):
    ACTIVE = "active"
    TRIPPED = "tripped"


@dataclass
class KillRecord:
    kind: KillTargetKind
    target_id: str
    state: KillSwitchState = KillSwitchState.ACTIVE
    tripped_by: str | None = None
    tripped_at: datetime | None = None
    reason: str | None = None
    history: list[dict[str, str]] = field(default_factory=list)


class KillSwitch:
    def __init__(self) -> None:
        self._records: dict[tuple[KillTargetKind, str], KillRecord] = {}
        self._lock = threading.Lock()

    def _key(self, kind: KillTargetKind, target_id: str) -> tuple[KillTargetKind, str]:
        return (kind, target_id)

    def is_active(self, kind: KillTargetKind, target_id: str) -> bool:
        with self._lock:
            rec = self._records.get(self._key(kind, target_id))
            return rec is None or rec.state == KillSwitchState.ACTIVE

    def trip(
        self,
        kind: KillTargetKind,
        target_id: str,
        *,
        tripped_by: str,
        reason: str,
    ) -> KillRecord:
        with self._lock:
            key = self._key(kind, target_id)
            rec = self._records.get(key) or KillRecord(kind=kind, target_id=target_id)
            rec.state = KillSwitchState.TRIPPED
            rec.tripped_by = tripped_by
            rec.tripped_at = datetime.now(timezone.utc)
            rec.reason = reason
            rec.history.append(
                {
                    "ts": rec.tripped_at.isoformat(),
                    "by": tripped_by,
                    "reason": reason,
                    "action": "tripped",
                }
            )
            self._records[key] = rec
            return rec

    def restore(
        self, kind: KillTargetKind, target_id: str, *, restored_by: str, reason: str
    ) -> KillRecord:
        with self._lock:
            key = self._key(kind, target_id)
            rec = self._records.get(key) or KillRecord(kind=kind, target_id=target_id)
            rec.state = KillSwitchState.ACTIVE
            rec.history.append(
                {
                    "ts": datetime.now(timezone.utc).isoformat(),
                    "by": restored_by,
                    "reason": reason,
                    "action": "restored",
                }
            )
            self._records[key] = rec
            return rec

    def status(self, kind: KillTargetKind, target_id: str) -> KillRecord | None:
        with self._lock:
            return self._records.get(self._key(kind, target_id))

    def all_tripped(self) -> list[KillRecord]:
        with self._lock:
            return [r for r in self._records.values() if r.state == KillSwitchState.TRIPPED]


__all__ = ["KillRecord", "KillSwitch", "KillSwitchState", "KillTargetKind"]
