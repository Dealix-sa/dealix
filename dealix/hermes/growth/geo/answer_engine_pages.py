"""Register pages designed to be cited by AI answer engines."""

from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field

_PAGES: dict[str, "AnswerEnginePage"] = {}


@dataclass(frozen=True)
class AnswerEnginePage:
    page_id: str
    title: str
    url: str
    target_queries: tuple[str, ...]
    citation_assets: tuple[str, ...] = field(default_factory=tuple)
    created_at: float = 0.0


def register(title: str, url: str, target_queries: list[str], citation_assets: list[str] | None = None) -> AnswerEnginePage:
    """Register an answer-engine-targeted page with its query targets and citation assets."""
    page = AnswerEnginePage(
        page_id=f"aep_{uuid.uuid4().hex[:8]}",
        title=title,
        url=url,
        target_queries=tuple(target_queries),
        citation_assets=tuple(citation_assets or ()),
        created_at=time.time(),
    )
    _PAGES[page.page_id] = page
    return page


def list_pages() -> list[AnswerEnginePage]:
    """Return all registered answer-engine pages."""
    return list(_PAGES.values())


def reset() -> None:
    """Clear answer-engine page registry (test helper)."""
    _PAGES.clear()
