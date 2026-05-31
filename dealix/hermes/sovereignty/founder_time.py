"""
FounderTimeLedger — append-only record of founder hours per activity.

The dashboard reads this to surface "where did Sami's hours go this week?"
and to flag any activity that consumes hours without producing an asset
or retainer.
"""

from __future__ import annotations

import time
from collections import defaultdict
from dataclasses import dataclass, field


@dataclass
class FounderTimeRecord:
    record_id: str
    activity: str
    hours: float
    customer_id: str = ""
    offer_id: str = ""
    produces_asset: bool = False
    produces_retainer: bool = False
    note: str = ""
    occurred_at: float = field(default_factory=time.time)


class FounderTimeLedger:
    def __init__(self) -> None:
        self._records: list[FounderTimeRecord] = []
        self._counter = 0

    def log(
        self,
        activity: str,
        hours: float,
        *,
        customer_id: str = "",
        offer_id: str = "",
        produces_asset: bool = False,
        produces_retainer: bool = False,
        note: str = "",
    ) -> FounderTimeRecord:
        if not activity:
            raise ValueError("activity required")
        if hours <= 0:
            raise ValueError("hours must be > 0")
        self._counter += 1
        record = FounderTimeRecord(
            record_id=f"ft_{self._counter}",
            activity=activity,
            hours=hours,
            customer_id=customer_id,
            offer_id=offer_id,
            produces_asset=produces_asset,
            produces_retainer=produces_retainer,
            note=note,
        )
        self._records.append(record)
        return record

    def total_hours(self, *, since: float | None = None) -> float:
        return round(
            sum(r.hours for r in self._records if since is None or r.occurred_at >= since),
            2,
        )

    def hours_by_offer(self) -> dict[str, float]:
        out: dict[str, float] = defaultdict(float)
        for r in self._records:
            key = r.offer_id or "unallocated"
            out[key] += r.hours
        return {k: round(v, 2) for k, v in out.items()}

    def unproductive_hours(self) -> float:
        """Hours that produced neither an asset nor a retainer."""
        return round(
            sum(
                r.hours
                for r in self._records
                if not (r.produces_asset or r.produces_retainer)
            ),
            2,
        )

    def __iter__(self):
        return iter(self._records)

    def __len__(self) -> int:
        return len(self._records)
