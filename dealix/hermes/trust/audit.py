"""Audit Log — append-only ledger of every consequential action."""

from __future__ import annotations

import hashlib
import json
from threading import RLock
from typing import Any

from dealix.hermes.core.schemas import AuditEvent, RiskLevel, SovereigntyLevel


def _hash_payload(payload: dict[str, Any]) -> str:
    blob = json.dumps(payload, sort_keys=True, default=str).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()[:32]


class AuditLog:
    def __init__(self) -> None:
        self._events: list[AuditEvent] = []
        self._lock = RLock()

    def record(
        self,
        *,
        action_type: str,
        agent_id: str = "",
        tool_id: str = "",
        payload: dict[str, Any] | None = None,
        risk_level: RiskLevel | str = RiskLevel.LOW,
        sovereignty_level: SovereigntyLevel | str = SovereigntyLevel.S0_AGENT_FREE,
        approval_id: str | None = None,
        result: str = "",
    ) -> AuditEvent:
        event = AuditEvent(
            agent_id=agent_id,
            tool_id=tool_id,
            action_type=action_type,
            payload_hash=_hash_payload(payload or {}),
            risk_level=RiskLevel(risk_level),
            sovereignty_level=SovereigntyLevel(sovereignty_level),
            approval_id=approval_id,
            result=result,
        )
        with self._lock:
            self._events.append(event)
        return event

    def list(self, *, limit: int = 200) -> list[AuditEvent]:
        with self._lock:
            return list(self._events[-limit:])

    def clear(self) -> None:
        with self._lock:
            self._events.clear()


_default_log: AuditLog | None = None


def get_audit_log() -> AuditLog:
    global _default_log
    if _default_log is None:
        _default_log = AuditLog()
    return _default_log
