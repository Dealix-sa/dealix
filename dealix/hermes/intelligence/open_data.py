"""Open-data source registry (Saudi open data portals etc.)."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class OpenDataSource:
    name: str
    url: str
    license: str
    sector: str | None = None
    refreshed_at: str | None = None


@dataclass
class OpenDataRegistry:
    _by_name: dict[str, OpenDataSource] = field(default_factory=dict)

    def register(self, src: OpenDataSource) -> None:
        self._by_name[src.name] = src

    def all(self) -> list[OpenDataSource]:
        return list(self._by_name.values())


__all__ = ["OpenDataSource", "OpenDataRegistry"]
