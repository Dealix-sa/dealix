from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ExaSearchResult:
    title: str
    url: str
    highlights: list[str]
    score: float | None = None
    provider: str = "exa"

    def to_dict(self) -> dict[str, Any]:
        return {
            "title": self.title,
            "url": self.url,
            "highlights": self.highlights,
            "score": self.score,
            "provider": self.provider,
        }


class ExaConnector:
    """Small stdlib-only Exa connector for Dealix research loops.

    Defaults are conservative. The connector only gathers research evidence for
    founder review and never performs message delivery, CRM mutation, or billing.
    """

    def __init__(self, api_key: str | None = None) -> None:
        self.api_key = api_key or os.getenv("EXA_API_KEY")
        self.base_url = os.getenv("EXA_BASE_URL", "https://api.exa.ai")
        self.default_type = os.getenv("EXA_DEFAULT_SEARCH_TYPE", "auto")
        self.deep_type = os.getenv("EXA_DEEP_SEARCH_TYPE", "deep")
        self.num_results = int(os.getenv("EXA_NUM_RESULTS", "10"))
        self.allow_live_search = os.getenv("EXA_ALLOW_LIVE_SEARCH", "true").lower() in {"1", "true", "yes", "on"}
        self.store_raw_text = os.getenv("EXA_STORE_RAW_TEXT", "false").lower() in {"1", "true", "yes", "on"}

    def configured(self) -> bool:
        return bool(self.api_key)

    def can_search_live(self) -> bool:
        return self.configured() and self.allow_live_search

    def dry_run_search(self, query: str, *, city: str = "Riyadh", sector: str = "Saudi B2B") -> dict[str, Any]:
        return {
            "mode": "dry_run",
            "provider": "exa",
            "query": query,
            "city": city,
            "sector": sector,
            "search_type": self.default_type,
            "num_results": self.num_results,
            "configured": self.configured(),
            "live_search_allowed": self.allow_live_search,
            "human_review_required": True,
            "source_url_required": True,
            "delivery_enabled": False,
        }

    def search(self, query: str, *, search_type: str | None = None, num_results: int | None = None) -> list[ExaSearchResult]:
        if not self.can_search_live():
            return []

        body = {
            "query": query,
            "type": search_type or self.default_type,
            "numResults": num_results or self.num_results,
            "contents": {"highlights": True},
        }
        if self.store_raw_text:
            body["contents"]["text"] = True

        request = urllib.request.Request(
            f"{self.base_url.rstrip('/')}/search",
            data=json.dumps(body).encode("utf-8"),
            headers={
                "content-type": "application/json",
                "x-api-key": self.api_key or "",
            },
            method="POST",
        )

        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                payload = json.loads(response.read().decode("utf-8"))
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            raise RuntimeError(f"Exa search failed safely: {exc}") from exc

        return [self.normalize_result(item) for item in payload.get("results", [])]

    def normalize_result(self, raw: dict[str, Any]) -> ExaSearchResult:
        highlights = raw.get("highlights") or []
        return ExaSearchResult(
            title=str(raw.get("title") or "").strip(),
            url=str(raw.get("url") or "").strip(),
            highlights=[str(item).strip() for item in highlights if str(item).strip()],
            score=raw.get("score"),
        )
