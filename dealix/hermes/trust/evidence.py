"""
Evidence pack — every decision or action can attach a small bundle of
facts (inputs, sources, checks passed) that explains why it was allowed.

This is the audit-friendly twin of an Outcome.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, Field


def _utcnow() -> datetime:
    return datetime.now(UTC)


class EvidenceItem(BaseModel):
    kind: str  # "source" | "check" | "input" | "approval"
    label: str
    value: Any
    captured_at: datetime = Field(default_factory=_utcnow)


class EvidencePack(BaseModel):
    subject: str
    items: list[EvidenceItem] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=_utcnow)

    def attach(self, kind: str, label: str, value: Any) -> None:
        self.items.append(EvidenceItem(kind=kind, label=label, value=value))
