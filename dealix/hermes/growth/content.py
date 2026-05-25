"""Editorial content calendar."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class ContentStatus(StrEnum):
    backlog = "backlog"
    drafting = "drafting"
    review = "review"
    approved = "approved"
    published = "published"
    archived = "archived"


class ContentItem(BaseModel):
    model_config = ConfigDict(extra="forbid")

    item_id: str
    title: str
    format: str
    audience_id: str | None = None
    status: ContentStatus = ContentStatus.backlog
    approval_id: str | None = None
    tags: list[str] = Field(default_factory=list)


@dataclass
class ContentCalendar:
    _items: dict[str, ContentItem] = field(default_factory=dict)

    def upsert(self, item: ContentItem) -> ContentItem:
        self._items[item.item_id] = item
        return item

    def list(self) -> list[ContentItem]:
        return list(self._items.values())
