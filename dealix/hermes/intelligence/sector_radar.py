"""Per-sector watch."""

from __future__ import annotations

from dataclasses import dataclass, field

from pydantic import BaseModel, ConfigDict, Field


class SectorSnapshot(BaseModel):
    model_config = ConfigDict(extra="forbid")

    sector: str
    notable_events: list[str] = Field(default_factory=list)
    score: float = 0.0


@dataclass
class SectorRadar:
    _snapshots: dict[str, SectorSnapshot] = field(default_factory=dict)

    def update(self, snapshot: SectorSnapshot) -> SectorSnapshot:
        self._snapshots[snapshot.sector] = snapshot
        return snapshot

    def list(self) -> list[SectorSnapshot]:
        return list(self._snapshots.values())
