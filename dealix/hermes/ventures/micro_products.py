"""Micro-products — single-SKU, sub-vertical experiments."""

from __future__ import annotations

from dataclasses import dataclass, field

from pydantic import BaseModel, ConfigDict, Field


class MicroProduct(BaseModel):
    model_config = ConfigDict(extra="forbid")

    micro_id: str
    name: str
    parent_vertical_id: str
    pain: str
    promise: str
    price_sar: float = Field(ge=0)


@dataclass
class MicroProductLibrary:
    _items: dict[str, MicroProduct] = field(default_factory=dict)

    def upsert(self, item: MicroProduct) -> MicroProduct:
        self._items[item.micro_id] = item
        return item

    def list(self) -> list[MicroProduct]:
        return list(self._items.values())
