"""Evidence Pack store — every tier-A/B decision ships with one."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime

from pydantic import BaseModel, ConfigDict, Field


def _now() -> str:
    return datetime.now(UTC).isoformat()


def _pid() -> str:
    return f"epk_{uuid.uuid4().hex[:16]}"


class EvidenceItem(BaseModel):
    model_config = ConfigDict(extra="forbid")

    source: str
    uri: str | None = None
    excerpt: str
    content_hash: str | None = None
    retrieved_at: str = Field(default_factory=_now)


class EvidencePack(BaseModel):
    model_config = ConfigDict(extra="forbid")

    pack_id: str = Field(default_factory=_pid)
    subject_id: str
    subject_type: str
    items: list[EvidenceItem] = Field(default_factory=list)
    model_used: str = "unspecified"
    model_version: str = "unspecified"
    bilingual_memo_ar: str = ""
    bilingual_memo_en: str = ""
    created_at: str = Field(default_factory=_now)


@dataclass
class EvidencePackStore:
    _packs: dict[str, EvidencePack] = field(default_factory=dict)

    def save(self, pack: EvidencePack) -> EvidencePack:
        self._packs[pack.pack_id] = pack
        return pack

    def get(self, pack_id: str) -> EvidencePack:
        return self._packs[pack_id]

    def list(self) -> list[EvidencePack]:
        return list(self._packs.values())
