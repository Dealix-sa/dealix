"""Knowledge Accumulator — durable, searchable commercial intelligence."""

from __future__ import annotations

import logging
from dataclasses import asdict, dataclass
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any, Literal

from intelligence.bilingual import BilingualRenderer, BilingualText, LanguageCode
from intelligence.knowledge_storage import (
    KnowledgeStorage,
    get_knowledge_storage,
)


@dataclass
class KnowledgeEntry:
    entry_id: str
    category: Literal[
        "market_signal", "competitor_intel", "deal_insight", "research_finding", "user_note"
    ]
    title: BilingualText
    content: BilingualText
    source: str
    sector: str | None
    company: str | None
    tags: list[str]
    confidence: float
    created_at: str
    expires_at: str | None

    def to_dict(self, lang: LanguageCode = "both") -> dict[str, Any]:
        return {
            "entry_id": self.entry_id,
            "category": self.category,
            "title": BilingualRenderer.filter_text(self.title, lang),
            "content": BilingualRenderer.filter_text(self.content, lang),
            "source": self.source,
            "sector": self.sector,
            "company": self.company,
            "tags": self.tags,
            "confidence": self.confidence,
            "created_at": self.created_at,
            "expires_at": self.expires_at,
        }


class KnowledgeAccumulator:
    """Accumulates, searches, and retrieves intelligence entries."""

    STORE_PATH = Path("data/knowledge/accumulated_intel.json")

    def __init__(
        self,
        store_path: Path | None = None,
        storage: KnowledgeStorage | None = None,
    ) -> None:
        if store_path is not None and storage is not None:
            raise ValueError("Pass either store_path or storage, not both")
        self._storage = storage or get_knowledge_storage(
            backend="file" if store_path is not None else None,
            file_store_path=store_path or self.STORE_PATH,
        )

    def _read(self) -> list[dict[str, Any]]:
        return self._storage.read()

    def _entry_from_dict(self, raw: dict[str, Any]) -> KnowledgeEntry:
        return KnowledgeEntry(
            entry_id=raw["entry_id"],
            category=raw["category"],
            title=BilingualText(**raw["title"]),
            content=BilingualText(**raw["content"]),
            source=raw["source"],
            sector=raw.get("sector"),
            company=raw.get("company"),
            tags=raw.get("tags", []),
            confidence=raw.get("confidence", 0.5),
            created_at=raw["created_at"],
            expires_at=raw.get("expires_at"),
        )

    def _entry_to_dict(self, entry: KnowledgeEntry) -> dict[str, Any]:
        data = asdict(entry)
        data["title"] = {
            "en": entry.title.en,
            "ar": entry.title.ar,
            "ar_available": entry.title.ar_available,
        }
        data["content"] = {
            "en": entry.content.en,
            "ar": entry.content.ar,
            "ar_available": entry.content.ar_available,
        }
        return data

    def ingest(self, entry: KnowledgeEntry) -> str:
        def _append(data: list[dict[str, Any]]) -> None:
            data.append(self._entry_to_dict(entry))

        self._storage.mutate(_append)
        logging.getLogger(__name__).info(
            "knowledge_ingested entry_id=%s category=%s",
            entry.entry_id,
            entry.category,
        )
        return entry.entry_id

    def ingest_batch(self, entries: list[KnowledgeEntry]) -> int:
        serialized = [self._entry_to_dict(entry) for entry in entries]

        def _append_all(data: list[dict[str, Any]]) -> None:
            data.extend(serialized)

        self._storage.mutate(_append_all)
        return len(entries)

    def search(
        self,
        query: str,
        category: str | None = None,
        sector: str | None = None,
        company: str | None = None,
        limit: int = 20,
    ) -> list[KnowledgeEntry]:
        query_lower = query.lower()
        results: list[KnowledgeEntry] = []
        for raw in self._read():
            entry = self._entry_from_dict(raw)
            text = " ".join(
                filter(
                    None,
                    [
                        entry.title.en,
                        entry.title.ar,
                        entry.content.en,
                        entry.content.ar,
                        " ".join(entry.tags),
                        entry.sector,
                        entry.company,
                    ],
                )
            ).lower()
            if query_lower not in text:
                continue
            if category and entry.category != category:
                continue
            if sector and entry.sector != sector:
                continue
            if company and entry.company != company:
                continue
            results.append(entry)
        return results[:limit]

    def get(self, entry_id: str) -> KnowledgeEntry | None:
        for raw in self._read():
            if raw.get("entry_id") == entry_id:
                return self._entry_from_dict(raw)
        return None

    def list_recent(self, days: int = 7, limit: int = 50) -> list[KnowledgeEntry]:
        cutoff = datetime.now(UTC) - timedelta(days=days)
        entries: list[KnowledgeEntry] = []
        for raw in self._read():
            entry = self._entry_from_dict(raw)
            try:
                created = datetime.fromisoformat(entry.created_at)
                if created >= cutoff:
                    entries.append(entry)
            except Exception:
                continue
        return sorted(entries, key=lambda e: e.created_at, reverse=True)[:limit]

    def daily_digest(self, lang: LanguageCode = "both") -> dict[str, Any]:
        recent = self.list_recent(days=1, limit=50)
        return BilingualRenderer.wrap(
            {
                "date": datetime.now(UTC).strftime("%Y-%m-%d"),
                "total_entries": len(self._read()),
                "recent_24h_count": len(recent),
                "entries": [e.to_dict(lang) for e in recent],
            },
            lang,
        )

    def purge_expired(self) -> int:
        now = datetime.now(UTC)

        def _purge(data: list[dict[str, Any]]) -> int:
            kept: list[dict[str, Any]] = []
            removed = 0
            for raw in data:
                expires = raw.get("expires_at")
                if expires:
                    try:
                        if datetime.fromisoformat(expires) < now:
                            removed += 1
                            continue
                    except Exception:
                        # Retain malformed legacy expiry values; purge must fail safe.
                        pass
                kept.append(raw)
            data[:] = kept
            return removed

        return self._storage.mutate(_purge)

    def stats(self) -> dict[str, Any]:
        data = self._read()
        categories: dict[str, int] = {}
        for raw in data:
            categories[raw.get("category", "unknown")] = (
                categories.get(raw.get("category", "unknown"), 0) + 1
            )
        return {
            "total_entries": len(data),
            "categories": categories,
            "backend": self._storage.backend_name,
            "durable": self._storage.durable,
        }

    def redact(self, entry_id: str, fields: list[str]) -> bool:
        def _redact(data: list[dict[str, Any]]) -> bool:
            for raw in data:
                if raw.get("entry_id") == entry_id:
                    for field in fields:
                        if field in ("title", "content"):
                            raw[field] = {
                                "en": "[redacted]",
                                "ar": "[محذوف]",
                                "ar_available": True,
                            }
                        elif field in raw:
                            raw[field] = "[redacted]"
                    return True
            return False

        return self._storage.mutate(_redact)

    def storage_readiness(self) -> dict[str, Any]:
        """Expose a non-secret readiness signal for Knowledge and Research OS."""

        return self._storage.readiness()
