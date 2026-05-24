"""Revenue Share Ledger — append-only."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass(frozen=True)
class RevenueShareEntry:
    id: str
    partner_id: str
    deal_ref: str
    gross_sar: float
    share_pct: float
    share_sar: float
    recorded_at: datetime


@dataclass
class RevenueShareLedger:
    _entries: list[RevenueShareEntry] = field(default_factory=list)

    def record(self, *, partner_id: str, deal_ref: str, gross_sar: float, share_pct: float) -> RevenueShareEntry:
        if gross_sar <= 0:
            raise ValueError("Gross must be > 0.")
        if not 0.0 <= share_pct <= 100.0:
            raise ValueError("Share pct must be in [0,100].")
        e = RevenueShareEntry(
            id=f"rsh_{uuid.uuid4().hex[:10]}",
            partner_id=partner_id,
            deal_ref=deal_ref,
            gross_sar=float(gross_sar),
            share_pct=float(share_pct),
            share_sar=float(gross_sar) * (float(share_pct) / 100.0),
            recorded_at=datetime.now(timezone.utc),
        )
        self._entries.append(e)
        return e

    def total_for(self, partner_id: str) -> float:
        return sum(e.share_sar for e in self._entries if e.partner_id == partner_id)

    def all(self) -> list[RevenueShareEntry]:
        return list(self._entries)


__all__ = ["RevenueShareEntry", "RevenueShareLedger"]
