"""Sovereign decision journal — every S3+ decision becomes durable history."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime

from pydantic import BaseModel, ConfigDict, Field

from dealix.hermes.sovereignty.levels import SovereigntyLevel


def _now() -> str:
    return datetime.now(UTC).isoformat()


def _jid() -> str:
    return f"sjr_{uuid.uuid4().hex[:16]}"


class JournalEntry(BaseModel):
    model_config = ConfigDict(extra="forbid")

    entry_id: str = Field(default_factory=_jid)
    decision_id: str
    title: str
    memo: str
    sovereignty_level: SovereigntyLevel
    outcome_expected: str
    outcome_observed: str = ""
    learnings: str = ""
    revisit_at: str | None = None
    created_at: str = Field(default_factory=_now)


@dataclass
class DecisionJournal:
    _entries: dict[str, JournalEntry] = field(default_factory=dict)

    def record(self, entry: JournalEntry) -> JournalEntry:
        self._entries[entry.entry_id] = entry
        return entry

    def annotate_outcome(self, entry_id: str, observed: str, learnings: str = "") -> JournalEntry:
        e = self._entries[entry_id]
        updated = e.model_copy(update={"outcome_observed": observed, "learnings": learnings})
        self._entries[entry_id] = updated
        return updated

    def get(self, entry_id: str) -> JournalEntry:
        return self._entries[entry_id]

    def list(self) -> list[JournalEntry]:
        return list(self._entries.values())
