"""Capital allocation guardrails — Sami owns the cap table."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum


class AllocationBucket(StrEnum):
    delivery = "delivery"
    growth = "growth"
    rnd = "rnd"
    partner = "partner"
    reserve = "reserve"


@dataclass
class AllocationLine:
    bucket: AllocationBucket
    budget_sar: float
    spent_sar: float = 0.0

    @property
    def remaining_sar(self) -> float:
        return max(0.0, self.budget_sar - self.spent_sar)


@dataclass
class CapitalAllocator:
    """Single-tenant capital ledger. Production stores in hermes_capital_lines."""

    _lines: dict[AllocationBucket, AllocationLine] = field(default_factory=dict)

    def set_budget(self, bucket: AllocationBucket, budget_sar: float) -> AllocationLine:
        line = self._lines.get(bucket)
        if line is None:
            self._lines[bucket] = AllocationLine(bucket=bucket, budget_sar=budget_sar)
        else:
            self._lines[bucket] = AllocationLine(
                bucket=bucket,
                budget_sar=budget_sar,
                spent_sar=line.spent_sar,
            )
        return self._lines[bucket]

    def spend(self, bucket: AllocationBucket, amount_sar: float) -> AllocationLine:
        line = self._lines.get(bucket)
        if line is None:
            raise ValueError(f"no budget set for bucket {bucket}")
        if amount_sar > line.remaining_sar:
            raise PermissionError(
                f"bucket {bucket} only has {line.remaining_sar} SAR remaining; tried to spend {amount_sar}"
            )
        new_line = AllocationLine(
            bucket=bucket,
            budget_sar=line.budget_sar,
            spent_sar=line.spent_sar + amount_sar,
        )
        self._lines[bucket] = new_line
        return new_line

    def summary(self) -> list[AllocationLine]:
        return list(self._lines.values())
