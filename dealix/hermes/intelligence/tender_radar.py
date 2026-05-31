"""Government tender radar — Saudi public-sector signals."""

from __future__ import annotations

from dataclasses import dataclass, field

from pydantic import BaseModel, ConfigDict


class Tender(BaseModel):
    model_config = ConfigDict(extra="forbid")

    tender_id: str
    entity: str
    title: str
    deadline: str
    estimated_value_sar: float = 0.0
    sector: str = ""


@dataclass
class TenderRadar:
    _tenders: dict[str, Tender] = field(default_factory=dict)

    def upsert(self, tender: Tender) -> Tender:
        self._tenders[tender.tender_id] = tender
        return tender

    def list(self) -> list[Tender]:
        return list(self._tenders.values())
