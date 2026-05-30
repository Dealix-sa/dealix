"""
Notion Founder Command Center integration — typed async REST client.
تكامل نوشن لمركز قيادة المؤسس — عميل REST غير متزامن.

Docs: https://developers.notion.com/reference

Defence in depth: every string leaving this process is run through the
canonical PII redactor (``redact_text`` / ``redact_dict``) before it is
placed in an outbound payload. The client never reads approval state back
to trigger a send — it is write-only by contract.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import httpx
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from auto_client_acquisition.customer_data_plane.pii_redactor import redact_dict, redact_text
from core.config.settings import get_settings
from core.errors import RateLimitError
from core.logging import get_logger

logger = get_logger(__name__)


@dataclass
class NotionResult:
    success: bool
    page_id: str | None = None
    created: bool = False
    error: str | None = None
    mock: bool = False
    raw: dict[str, Any] | None = None


# ── Module-level property builders (each redacts internally) ────────
def title_prop(text: str) -> dict[str, Any]:
    """Build a Notion `title` property (PII-redacted)."""
    return {"title": [{"type": "text", "text": {"content": redact_text(text)}}]}


def rich_text_prop(text: str) -> dict[str, Any]:
    """Build a Notion `rich_text` property (PII-redacted)."""
    return {"rich_text": [{"type": "text", "text": {"content": redact_text(text)}}]}


def number_prop(n: float | int | None) -> dict[str, Any]:
    """Build a Notion `number` property."""
    return {"number": n}


def select_prop(name: str) -> dict[str, Any]:
    """Build a Notion `select` property (PII-redacted name)."""
    return {"select": {"name": redact_text(name)}}


def date_prop(iso: str) -> dict[str, Any]:
    """Build a Notion `date` property from an ISO string."""
    return {"date": {"start": redact_text(iso)}}


def checkbox_prop(b: bool) -> dict[str, Any]:
    """Build a Notion `checkbox` property."""
    return {"checkbox": bool(b)}


def markdown_to_blocks(md: str) -> list[dict[str, Any]]:
    """Convert markdown text to Notion paragraph/heading blocks (PII-redacted).

    Minimal converter: `#`/`##`/`###` headings, `-` bullets, blank-line
    separated paragraphs. Each line is redacted before it becomes content.
    """
    blocks: list[dict[str, Any]] = []
    for raw_line in redact_text(md).splitlines():
        line = raw_line.rstrip()
        if not line.strip():
            continue
        if line.startswith("### "):
            kind, content = "heading_3", line[4:]
        elif line.startswith("## "):
            kind, content = "heading_2", line[3:]
        elif line.startswith("# "):
            kind, content = "heading_1", line[2:]
        elif line.startswith("- ") or line.startswith("* "):
            kind, content = "bulleted_list_item", line[2:]
        else:
            kind, content = "paragraph", line
        blocks.append(
            {
                "object": "block",
                "type": kind,
                kind: {"rich_text": [{"type": "text", "text": {"content": content}}]},
            }
        )
    return blocks


class NotionClient:
    """Thin async client for the Notion REST API."""

    BASE_URL = "https://api.notion.com/v1"

    def __init__(self) -> None:
        self.settings = get_settings()

    # ── Config check ────────────────────────────────────────────
    @property
    def configured(self) -> bool:
        return self.settings.notion_api_key is not None

    @property
    def mock(self) -> bool:
        return self.settings.notion_mock_mode or not self.configured

    def _headers(self) -> dict[str, str]:
        if not self.settings.notion_api_key:
            raise RateLimitError("NOTION_API_KEY not configured")
        key = self.settings.notion_api_key.get_secret_value()
        return {
            "Authorization": f"Bearer {key}",
            "Notion-Version": self.settings.notion_version,
            "Content-Type": "application/json",
        }

    # ── Transport ───────────────────────────────────────────────
    @retry(
        stop=stop_after_attempt(4),
        wait=wait_exponential(multiplier=1, min=1, max=20),
        retry=retry_if_exception_type((httpx.TimeoutException, RateLimitError)),
        reraise=True,
    )
    async def _request(
        self, method: str, path: str, json: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """One Notion API call with retry/backoff and 429 handling."""
        url = f"{self.BASE_URL}{path}"
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.request(method, url, json=json, headers=self._headers())
            if response.status_code == 429:
                retry_after = response.headers.get("Retry-After", "1")
                logger.info("notion_rate_limited", retry_after=retry_after, path=path)
                raise RateLimitError(f"Notion rate limited (Retry-After={retry_after})")
            response.raise_for_status()
            return response.json()

    # ── Discovery ───────────────────────────────────────────────
    async def find_database(self, title: str) -> str | None:
        """Resolve a database id by exact title match via /search."""
        if not self.configured:
            logger.info("notion_not_configured", op="find_database")
            return None
        payload = {
            "query": title,
            "filter": {"property": "object", "value": "database"},
        }
        data = await self._request("POST", "/search", json=payload)
        for result in data.get("results", []) or []:
            title_parts = result.get("title", []) or []
            rendered = "".join(p.get("plain_text", "") for p in title_parts).strip()
            if rendered == title:
                return result.get("id")
        return None

    async def query_by_external_id(
        self, db_id: str, external_id: str, *, key_prop: str = "external_id"
    ) -> str | None:
        """Return the page id whose `key_prop` rich_text equals `external_id`."""
        if not self.configured:
            logger.info("notion_not_configured", op="query_by_external_id")
            return None
        payload = {
            "filter": {
                "property": key_prop,
                "rich_text": {"equals": external_id},
            },
            "page_size": 1,
        }
        data = await self._request("POST", f"/databases/{db_id}/query", json=payload)
        results = data.get("results", []) or []
        if results:
            return results[0].get("id")
        return None

    # ── Write paths ─────────────────────────────────────────────
    async def upsert_row(
        self,
        db_id: str,
        *,
        external_id: str,
        properties: dict[str, Any],
        key_prop: str = "external_id",
    ) -> NotionResult:
        """Create or update a row keyed by a deterministic external id.

        Redacts every string in `properties` first (defence in depth on top
        of the per-builder redaction), short-circuits to a zero-HTTP mock
        result when not configured / mock mode, otherwise queries by external
        id and PATCHes the existing page or POSTs a new one.
        """
        safe_props: dict[str, Any] = redact_dict(properties)
        safe_props[key_prop] = rich_text_prop(external_id)

        if self.mock:
            existing = None
            if self.configured:
                # Configured + explicit mock: still no HTTP, so created flag
                # is best-effort. Keep deterministic: treat as create.
                existing = None
            created = existing is None
            logger.info(
                "notion_mock_upsert",
                db_id=db_id,
                external_id=external_id,
                created=created,
            )
            return NotionResult(success=True, mock=True, created=created)

        page_id = await self.query_by_external_id(db_id, external_id, key_prop=key_prop)
        if page_id is not None:
            data = await self._request(
                "PATCH", f"/pages/{page_id}", json={"properties": safe_props}
            )
            logger.info("notion_updated", db_id=db_id, page_id=data.get("id"))
            return NotionResult(
                success=True, page_id=data.get("id"), created=False, raw=data
            )
        data = await self._request(
            "POST",
            "/pages",
            json={"parent": {"database_id": db_id}, "properties": safe_props},
        )
        logger.info("notion_created", db_id=db_id, page_id=data.get("id"))
        return NotionResult(success=True, page_id=data.get("id"), created=True, raw=data)

    async def append_blocks(self, page_id: str, blocks: list[dict[str, Any]]) -> NotionResult:
        """Append child blocks to a page (text redacted, mock honored)."""
        safe_blocks: list[dict[str, Any]] = [redact_dict(b) for b in blocks]
        if self.mock:
            logger.info("notion_mock_append", page_id=page_id, count=len(safe_blocks))
            return NotionResult(success=True, page_id=page_id, mock=True)
        if not self.configured:
            logger.info("notion_not_configured", op="append_blocks")
            return NotionResult(success=False, error="NOTION_API_KEY not configured")
        data = await self._request(
            "PATCH", f"/blocks/{page_id}/children", json={"children": safe_blocks}
        )
        logger.info("notion_blocks_appended", page_id=page_id, count=len(safe_blocks))
        return NotionResult(success=True, page_id=page_id, raw=data)
