"""Track potential acquisition targets (only catalogs; never negotiates)."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field


@dataclass
class AcquisitionTarget:
    id: str
    name: str
    sector: str
    rationale: str
    asking_price_sar: float | None = None


@dataclass
class AcquisitionScout:
    _by_id: dict[str, AcquisitionTarget] = field(default_factory=dict)

    def add(self, *, name: str, sector: str, rationale: str, asking_price_sar: float | None = None) -> AcquisitionTarget:
        t = AcquisitionTarget(
            id=f"acq_{uuid.uuid4().hex[:10]}",
            name=name,
            sector=sector,
            rationale=rationale,
            asking_price_sar=asking_price_sar,
        )
        self._by_id[t.id] = t
        return t

    def all(self) -> list[AcquisitionTarget]:
        return list(self._by_id.values())


__all__ = ["AcquisitionScout", "AcquisitionTarget"]
