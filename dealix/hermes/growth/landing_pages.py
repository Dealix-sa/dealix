"""Landing pages — drafted by agents, published only by Sami."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum

from pydantic import BaseModel, ConfigDict


class LandingState(StrEnum):
    draft = "draft"
    approved = "approved"
    live = "live"
    archived = "archived"


class LandingPage(BaseModel):
    model_config = ConfigDict(extra="forbid")

    page_id: str
    slug: str
    offer_id: str
    title: str
    hero_copy: str
    geo_optimised: bool = False
    state: LandingState = LandingState.draft
    approval_id: str | None = None


@dataclass
class LandingPageStore:
    _pages: dict[str, LandingPage] = field(default_factory=dict)

    def upsert(self, page: LandingPage) -> LandingPage:
        self._pages[page.page_id] = page
        return page

    def approve(self, page_id: str, approval_id: str) -> LandingPage:
        p = self._pages[page_id]
        updated = p.model_copy(update={"state": LandingState.approved, "approval_id": approval_id})
        self._pages[page_id] = updated
        return updated

    def publish(self, page_id: str) -> LandingPage:
        p = self._pages[page_id]
        if p.state != LandingState.approved:
            raise PermissionError("landing page must be approved before publish")
        updated = p.model_copy(update={"state": LandingState.live})
        self._pages[page_id] = updated
        return updated

    def list(self) -> list[LandingPage]:
        return list(self._pages.values())
