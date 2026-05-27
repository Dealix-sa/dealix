"""WorkshopBuilder — every workshop must declare an upsell hook."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field


@dataclass
class Workshop:
    id: str
    name: str
    audience: str
    duration_hours: int
    modules: list[str]
    upsell_offer_id: str
    price_sar: float


@dataclass
class WorkshopBuilder:
    _by_id: dict[str, Workshop] = field(default_factory=dict)

    def build(
        self,
        *,
        name: str,
        audience: str,
        duration_hours: int,
        modules: list[str],
        upsell_offer_id: str,
        price_sar: float,
    ) -> Workshop:
        if not modules:
            raise ValueError("Workshop must have at least one module.")
        if not upsell_offer_id:
            # Section 120: every training opens a path to an upsell.
            raise ValueError("Workshop must declare an upsell_offer_id.")
        w = Workshop(
            id=f"wks_{uuid.uuid4().hex[:10]}",
            name=name,
            audience=audience,
            duration_hours=duration_hours,
            modules=list(modules),
            upsell_offer_id=upsell_offer_id,
            price_sar=float(price_sar),
        )
        self._by_id[w.id] = w
        return w

    def all(self) -> list[Workshop]:
        return list(self._by_id.values())


__all__ = ["Workshop", "WorkshopBuilder"]
