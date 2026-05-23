"""
Approval router.

Holds pending approvals in memory. Production wires this to a database
table; the in-memory implementation is enough for tests and the daily
brief generator. Every transition writes through the audit hook so the
private repo's approval_log.csv remains the single source of truth.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Callable, Iterable


@dataclass(slots=True)
class PendingApproval:
    id: str
    label: str
    approval_class: str
    created_at: datetime
    status: str = "pending"  # pending | approved | rejected
    resolved_at: datetime | None = None
    reason: str | None = None


class ApprovalRouter:
    def __init__(
        self,
        *,
        audit_hook: Callable[[PendingApproval, str], None] | None = None,
    ) -> None:
        self._items: dict[str, PendingApproval] = {}
        self._audit = audit_hook or (lambda _a, _e: None)
        self._counter = 0

    def submit(self, label: str, approval_class: str) -> PendingApproval:
        self._counter += 1
        item = PendingApproval(
            id=f"appr-{self._counter:06d}",
            label=label,
            approval_class=approval_class,
            created_at=datetime.now(timezone.utc),
        )
        self._items[item.id] = item
        self._audit(item, "submitted")
        return item

    def pending(self) -> list[PendingApproval]:
        return [a for a in self._items.values() if a.status == "pending"]

    def resolve(self, approval_id: str, *, approved: bool, reason: str = "") -> PendingApproval:
        item = self._items[approval_id]
        if item.status != "pending":
            raise ValueError(f"approval {approval_id} already resolved to {item.status}")
        item.status = "approved" if approved else "rejected"
        item.resolved_at = datetime.now(timezone.utc)
        item.reason = reason or None
        self._audit(item, item.status)
        return item

    def stats(self) -> dict[str, int]:
        out = {"pending": 0, "approved": 0, "rejected": 0}
        for a in self._items.values():
            out[a.status] = out.get(a.status, 0) + 1
        return out

    def items(self) -> Iterable[PendingApproval]:
        return list(self._items.values())
