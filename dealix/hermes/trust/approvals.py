"""Approval Center — the single queue for every action that needs Sami's nod."""

from __future__ import annotations

from datetime import datetime, timezone
from threading import RLock
from typing import Any

from dealix.hermes.core.schemas import ApprovalRequest, RiskLevel, SovereigntyLevel


class ApprovalCenter:
    def __init__(self) -> None:
        self._items: dict[str, ApprovalRequest] = {}
        self._lock = RLock()

    def request(
        self,
        *,
        requested_by_agent: str,
        action_type: str,
        payload: dict[str, Any] | None = None,
        sovereignty_level: SovereigntyLevel | str,
        risk_level: RiskLevel | str = RiskLevel.MEDIUM,
    ) -> ApprovalRequest:
        sov = SovereigntyLevel(sovereignty_level)
        if sov == SovereigntyLevel.S5_NEVER_AUTONOMOUS:
            blocked = ApprovalRequest(
                requested_by_agent=requested_by_agent,
                action_type=action_type,
                payload=payload or {},
                sovereignty_level=sov,
                risk_level=RiskLevel(risk_level),
                status="blocked",
                rejection_reason="s5_never_autonomous",
            )
            with self._lock:
                self._items[blocked.id] = blocked
            return blocked
        req = ApprovalRequest(
            requested_by_agent=requested_by_agent,
            action_type=action_type,
            payload=payload or {},
            sovereignty_level=sov,
            risk_level=RiskLevel(risk_level),
            status="pending",
        )
        with self._lock:
            self._items[req.id] = req
        return req

    def approve(self, approval_id: str, approver: str = "Sami") -> ApprovalRequest | None:
        with self._lock:
            req = self._items.get(approval_id)
            if req is None or req.status == "blocked":
                return None
            updated = req.model_copy(
                update={
                    "status": "approved",
                    "approved_by": approver,
                    "approved_at": datetime.now(timezone.utc),
                }
            )
            self._items[approval_id] = updated
            return updated

    def reject(self, approval_id: str, reason: str) -> ApprovalRequest | None:
        with self._lock:
            req = self._items.get(approval_id)
            if req is None:
                return None
            updated = req.model_copy(
                update={"status": "rejected", "rejection_reason": reason}
            )
            self._items[approval_id] = updated
            return updated

    def get(self, approval_id: str) -> ApprovalRequest | None:
        with self._lock:
            return self._items.get(approval_id)

    def pending(self) -> list[ApprovalRequest]:
        with self._lock:
            return [r for r in self._items.values() if r.status == "pending"]

    def history(self) -> list[ApprovalRequest]:
        with self._lock:
            return sorted(self._items.values(), key=lambda r: r.created_at, reverse=True)

    def clear(self) -> None:
        with self._lock:
            self._items.clear()


_default_center: ApprovalCenter | None = None


def get_approval_center() -> ApprovalCenter:
    global _default_center
    if _default_center is None:
        _default_center = ApprovalCenter()
    return _default_center
