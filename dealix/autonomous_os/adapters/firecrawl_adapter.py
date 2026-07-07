"""
Firecrawl adapter — compliant PUBLIC market/web research only.

Fetches public web content to support market and sector research (e.g. the
`saudi_market_access` strategy). It is read-only and offline-safe.

Hard compliance guard: this adapter refuses anything that looks like personal
contact harvesting or social-network scraping (LinkedIn etc.), consistent with
the Dealix safety doctrine (no scraping contacts, no LinkedIn automation). A
refused request returns a blocked result — it never silently proceeds.
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from typing import Any
from urllib.parse import urlparse

from .base import Adapter, AdapterResult, AdapterStatus

REQUEST_TIMEOUT_SECONDS = 25

# Domains/patterns that would imply contact scraping or social automation.
BLOCKED_HOST_FRAGMENTS = (
    "linkedin.",
    "facebook.",
    "instagram.",
    "x.com",
    "twitter.",
    "tiktok.",
    "wa.me",
    "whatsapp.",
)
BLOCKED_QUERY_TERMS = (
    "email",
    "phone",
    "mobile",
    "contact list",
    "personal",
    "whatsapp number",
    "linkedin",
)


class FirecrawlAdapter(Adapter):
    name = "firecrawl"

    def __init__(self, env: dict[str, str] | None = None) -> None:
        self._env = env if env is not None else dict(os.environ)

    def _get(self, key: str) -> str:
        return (self._env.get(key) or "").strip()

    def is_available(self) -> bool:
        return bool(self._get("FIRECRAWL_API_KEY"))

    def status(self) -> AdapterStatus:
        available = self.is_available()
        return AdapterStatus(
            name=self.name,
            available=available,
            mode="live" if available else "offline_fallback",
            detail="public research only; contact/social scraping refused",
        )

    @staticmethod
    def _is_blocked_url(url: str) -> tuple[bool, str]:
        host = (urlparse(url).hostname or "").lower()
        if not host:
            return True, "invalid or non-public URL"
        for frag in BLOCKED_HOST_FRAGMENTS:
            if frag in host:
                return True, f"host '{host}' is a social/contact source — refused by doctrine"
        return False, ""

    @staticmethod
    def _is_blocked_query(query: str) -> tuple[bool, str]:
        low = query.lower()
        for term in BLOCKED_QUERY_TERMS:
            if term in low:
                return True, f"query implies personal-contact harvesting ('{term}') — refused"
        return False, ""

    def scrape(self, url: str) -> AdapterResult:
        blocked, reason = self._is_blocked_url(url)
        if blocked:
            return AdapterResult(ok=False, mode="blocked", error=reason, meta={"url": url})

        if not self.is_available():
            return AdapterResult(
                ok=True,
                mode="offline_fallback",
                data={"url": url, "content": None},
                meta={"reason": "firecrawl not configured — research skipped"},
            )

        body = json.dumps({"url": url, "formats": ["markdown"]}).encode("utf-8")
        req = urllib.request.Request(
            "https://api.firecrawl.dev/v1/scrape",
            data=body,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self._get('FIRECRAWL_API_KEY')}",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT_SECONDS) as resp:
                parsed = json.loads(resp.read().decode("utf-8"))
            data = (parsed or {}).get("data", {}) or {}
            return AdapterResult(
                ok=True,
                mode="live",
                data={"url": url, "content": data.get("markdown")},
            )
        except (urllib.error.URLError, ValueError, json.JSONDecodeError, OSError) as exc:
            return AdapterResult(
                ok=True,
                mode="offline_fallback",
                data={"url": url, "content": None},
                error=f"{type(exc).__name__}: {exc}",
                meta={"reason": "firecrawl request failed"},
            )

    def guard_query(self, query: str) -> AdapterResult:
        """Validate a research query against the compliance guard without any
        network call. Useful for planners deciding whether research is allowed."""
        blocked, reason = self._is_blocked_query(query)
        if blocked:
            return AdapterResult(ok=False, mode="blocked", error=reason, meta={"query": query})
        return AdapterResult(ok=True, mode="allowed", data={"query": query})
