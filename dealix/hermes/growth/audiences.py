"""Audience segmentation."""

from __future__ import annotations

from dataclasses import dataclass, field

from pydantic import BaseModel, ConfigDict, Field


class Audience(BaseModel):
    model_config = ConfigDict(extra="forbid")

    audience_id: str
    name: str
    icp_ids: list[str] = Field(default_factory=list)
    size: int = 0
    filters: dict[str, str] = Field(default_factory=dict)


@dataclass
class AudienceLibrary:
    _audiences: dict[str, Audience] = field(default_factory=dict)

    def upsert(self, audience: Audience) -> Audience:
        self._audiences[audience.audience_id] = audience
        return audience

    def list(self) -> list[Audience]:
        return list(self._audiences.values())
