"""Intelligence reports — durable artefacts shippable to customers."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime

from pydantic import BaseModel, ConfigDict, Field


def _now() -> str:
    return datetime.now(UTC).isoformat()


def _rid() -> str:
    return f"rep_{uuid.uuid4().hex[:16]}"


class IntelligenceReport(BaseModel):
    model_config = ConfigDict(extra="forbid")

    report_id: str = Field(default_factory=_rid)
    title: str
    sector: str
    summary: str
    sources: list[str] = Field(default_factory=list)
    classification: str = "INTERNAL"
    published: bool = False
    created_at: str = Field(default_factory=_now)


@dataclass
class IntelligenceReportStore:
    _reports: dict[str, IntelligenceReport] = field(default_factory=dict)

    def save(self, report: IntelligenceReport) -> IntelligenceReport:
        self._reports[report.report_id] = report
        return report

    def list(self) -> list[IntelligenceReport]:
        return list(self._reports.values())
