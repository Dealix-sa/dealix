"""خادم الذكاء — TenderRadar.

Filter a pool of tenders by sector + minimum size. Returns ranked
`TenderOpportunity` records.
"""

from __future__ import annotations

from datetime import date
from decimal import Decimal
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from dealix.hermes.core.schemas import Money


class TenderOpportunity(BaseModel):
    """A tender we want to consider chasing."""

    model_config = ConfigDict(extra="forbid")

    tender_id: str = Field(..., min_length=1, max_length=128)
    title: str = Field(..., min_length=1, max_length=400)
    sector: str = Field(..., min_length=1, max_length=64)
    issuer: str = Field(..., min_length=1, max_length=200)
    size: Money
    deadline: date | None = None
    why_relevant: str = Field(..., min_length=1, max_length=600)


class TenderRadar:
    """Filter + rank a pool of tenders for downstream review."""

    def scan(
        self,
        tender_pool: list[dict[str, Any]],
        sector: str | None = None,
        min_size_sar: int | float | Decimal = 0,
    ) -> list[TenderOpportunity]:
        floor = Decimal(str(min_size_sar))
        sector_key = sector.lower().strip() if sector else None
        out: list[TenderOpportunity] = []
        for entry in tender_pool:
            tender = self._coerce(entry)
            if tender is None:
                continue
            if sector_key and tender.sector.lower() != sector_key:
                continue
            if tender.size.amount < floor:
                continue
            out.append(tender)
        out.sort(key=lambda t: (-float(t.size.amount), t.title))
        return out

    @staticmethod
    def _coerce(entry: dict[str, Any]) -> TenderOpportunity | None:
        try:
            size_amount = Decimal(str(entry.get("size_sar") or entry.get("size") or 0))
        except Exception:
            return None
        deadline_raw = entry.get("deadline")
        deadline: date | None = None
        if isinstance(deadline_raw, date):
            deadline = deadline_raw
        elif isinstance(deadline_raw, str) and deadline_raw:
            try:
                deadline = date.fromisoformat(deadline_raw)
            except ValueError:
                deadline = None
        try:
            return TenderOpportunity(
                tender_id=str(entry.get("tender_id") or entry.get("id") or "tender"),
                title=str(entry.get("title") or "Unnamed tender"),
                sector=str(entry.get("sector") or "general"),
                issuer=str(entry.get("issuer") or "Unknown issuer"),
                size=Money.sar(size_amount),
                deadline=deadline,
                why_relevant=str(entry.get("why_relevant") or "matches sector filter"),
            )
        except ValueError:
            return None


__all__ = ["TenderOpportunity", "TenderRadar"]
