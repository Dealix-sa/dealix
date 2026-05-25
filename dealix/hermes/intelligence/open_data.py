"""Open data sources — registry of upstream feeds we ingest."""

from __future__ import annotations

from dataclasses import dataclass, field

from pydantic import BaseModel, ConfigDict


class OpenDataSource(BaseModel):
    model_config = ConfigDict(extra="forbid")

    source_id: str
    name: str
    url: str
    license: str = "unspecified"
    refresh_interval_hours: int = 24


@dataclass
class OpenDataRegistry:
    _sources: dict[str, OpenDataSource] = field(default_factory=dict)

    def register(self, source: OpenDataSource) -> OpenDataSource:
        self._sources[source.source_id] = source
        return source

    def list(self) -> list[OpenDataSource]:
        return list(self._sources.values())
