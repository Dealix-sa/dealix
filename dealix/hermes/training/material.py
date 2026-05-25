"""Training material registry."""

from __future__ import annotations

from dataclasses import dataclass, field

from pydantic import BaseModel, ConfigDict


class TrainingMaterial(BaseModel):
    model_config = ConfigDict(extra="forbid")

    material_id: str
    title: str
    format: str  # slides | doc | video | notebook
    locale: str = "en"
    uri: str | None = None


@dataclass
class MaterialLibrary:
    _items: dict[str, TrainingMaterial] = field(default_factory=dict)

    def upsert(self, item: TrainingMaterial) -> TrainingMaterial:
        self._items[item.material_id] = item
        return item

    def list(self) -> list[TrainingMaterial]:
        return list(self._items.values())
