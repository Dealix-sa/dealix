"""Compose an intelligence report from signals + competitor moves."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class IntelligenceReport:
    id: str
    title: str
    body: str
    refs: list[str]
    created_at: datetime


@dataclass
class ReportBuilder:
    _by_id: dict[str, IntelligenceReport] = field(default_factory=dict)

    def build(self, *, title: str, sections: list[str], refs: list[str] | None = None) -> IntelligenceReport:
        if not sections:
            raise ValueError("Report needs at least one section.")
        body = "\n\n".join(f"## Section {i+1}\n{s}" for i, s in enumerate(sections))
        r = IntelligenceReport(
            id=f"rpt_{uuid.uuid4().hex[:10]}",
            title=title,
            body=body,
            refs=list(refs or []),
            created_at=datetime.now(timezone.utc),
        )
        self._by_id[r.id] = r
        return r

    def all(self) -> list[IntelligenceReport]:
        return list(self._by_id.values())


__all__ = ["IntelligenceReport", "ReportBuilder"]
