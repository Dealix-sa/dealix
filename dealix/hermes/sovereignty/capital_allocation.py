"""Capital Allocation — every SAR move is logged and only Sami can disburse.

The ledger is intentionally additive. Agents may *plan* an allocation
(``propose``) but only Sami can ``approve`` and only an approved
allocation can be ``disburse``-d.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Iterable


class AllocationStatus(str, Enum):
    PROPOSED = "proposed"
    APPROVED = "approved"
    REJECTED = "rejected"
    DISBURSED = "disbursed"
    CANCELLED = "cancelled"


@dataclass
class CapitalAllocation:
    id: str
    bucket: str             # "product" | "marketing" | "partner_share" | ...
    amount_sar: float
    proposed_by: str
    rationale: str
    status: AllocationStatus = AllocationStatus.PROPOSED
    proposed_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    approved_by: str | None = None
    approved_at: datetime | None = None
    disbursed_at: datetime | None = None


@dataclass
class CapitalLedger:
    sovereign_author: str = "sami"
    _by_id: dict[str, CapitalAllocation] = field(default_factory=dict)

    def propose(self, *, bucket: str, amount_sar: float, proposed_by: str, rationale: str) -> CapitalAllocation:
        if amount_sar <= 0:
            raise ValueError("Allocation amount must be > 0.")
        alloc = CapitalAllocation(
            id=f"alc_{uuid.uuid4().hex[:10]}",
            bucket=bucket,
            amount_sar=amount_sar,
            proposed_by=proposed_by,
            rationale=rationale,
        )
        self._by_id[alloc.id] = alloc
        return alloc

    def approve(self, allocation_id: str, *, by: str) -> CapitalAllocation:
        if by != self.sovereign_author:
            raise PermissionError(
                f"Only '{self.sovereign_author}' can approve capital allocations; got '{by}'."
            )
        alloc = self._require(allocation_id)
        if alloc.status != AllocationStatus.PROPOSED:
            raise ValueError(f"Allocation {allocation_id} is not in PROPOSED state.")
        alloc.status = AllocationStatus.APPROVED
        alloc.approved_by = by
        alloc.approved_at = datetime.now(timezone.utc)
        return alloc

    def reject(self, allocation_id: str, *, by: str, reason: str) -> CapitalAllocation:
        if by != self.sovereign_author:
            raise PermissionError("Only sovereign may reject.")
        alloc = self._require(allocation_id)
        alloc.status = AllocationStatus.REJECTED
        alloc.approved_by = by
        alloc.approved_at = datetime.now(timezone.utc)
        alloc.rationale = f"{alloc.rationale} | rejected: {reason}"
        return alloc

    def disburse(self, allocation_id: str, *, by: str) -> CapitalAllocation:
        if by != self.sovereign_author:
            raise PermissionError("Only sovereign may disburse.")
        alloc = self._require(allocation_id)
        if alloc.status != AllocationStatus.APPROVED:
            raise ValueError(f"Allocation {allocation_id} must be APPROVED before disbursement.")
        alloc.status = AllocationStatus.DISBURSED
        alloc.disbursed_at = datetime.now(timezone.utc)
        return alloc

    def all(self) -> list[CapitalAllocation]:
        return list(self._by_id.values())

    def by_status(self, status: AllocationStatus) -> list[CapitalAllocation]:
        return [a for a in self._by_id.values() if a.status == status]

    def total(self, status: AllocationStatus | None = None) -> float:
        items: Iterable[CapitalAllocation]
        items = self._by_id.values() if status is None else self.by_status(status)
        return sum(a.amount_sar for a in items)

    def _require(self, allocation_id: str) -> CapitalAllocation:
        if allocation_id not in self._by_id:
            raise KeyError(f"Unknown allocation id: {allocation_id}")
        return self._by_id[allocation_id]


__all__ = ["AllocationStatus", "CapitalAllocation", "CapitalLedger"]
