"""Tender / RFP tracker."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Tender:
    id: str
    title: str
    issuer: str
    sector: str
    closes_at: datetime
    estimated_value_sar: float


@dataclass
class TenderRadar:
    _by_id: dict[str, Tender] = field(default_factory=dict)

    def add(self, *, title: str, issuer: str, sector: str, closes_at: datetime, estimated_value_sar: float) -> Tender:
        t = Tender(
            id=f"tdr_{uuid.uuid4().hex[:10]}",
            title=title,
            issuer=issuer,
            sector=sector,
            closes_at=closes_at,
            estimated_value_sar=estimated_value_sar,
        )
        self._by_id[t.id] = t
        return t

    def open(self) -> list[Tender]:
        from datetime import datetime as _dt, timezone as _tz
        now = _dt.now(_tz.utc)
        return [t for t in self._by_id.values() if t.closes_at >= now]


__all__ = ["Tender", "TenderRadar"]
