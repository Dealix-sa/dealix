"""Published case-study registry."""

from __future__ import annotations

from dataclasses import dataclass, field

from pydantic import BaseModel, ConfigDict, Field


class CaseStudy(BaseModel):
    model_config = ConfigDict(extra="forbid")

    case_study_id: str
    customer_id: str
    title: str
    industry: str
    summary: str
    metrics: list[str] = Field(default_factory=list)
    approved_for_public_use: bool = False


@dataclass
class CaseStudyLibrary:
    _items: dict[str, CaseStudy] = field(default_factory=dict)

    def upsert(self, item: CaseStudy) -> CaseStudy:
        self._items[item.case_study_id] = item
        return item

    def published(self) -> list[CaseStudy]:
        return [c for c in self._items.values() if c.approved_for_public_use]

    def list(self) -> list[CaseStudy]:
        return list(self._items.values())
