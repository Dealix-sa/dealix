"""Knowledge Accumulator — Daily Intelligence Container.

Persistent, searchable store for accumulated commercial intelligence.
v1 uses a JSON file with simple locking; production can migrate to SQLModel.
"""

from __future__ import annotations

import json
import logging
import threading
from dataclasses import asdict, dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Literal

from intelligence.bilingual import BilingualRenderer, BilingualText, LanguageCode


@dataclass
class KnowledgeEntry:
    entry_id: str
    category: Literal["market_signal", "competitor_intel", "deal_insight", "research_finding", "user_note"]
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
    _lock = threading.Lock()

    def __init__(self, store_path: Path | None = None) -> None:
        self.store_path = store_path or self.STORE_PATH
        self.store_path.parent.mkdir(parents=True, exist_ok=True)
        self._ensure_store()

    def _ensure_store(self) -> None:
        if not self.store_path.exists():
            self._write([])

    def _read(self) -> list[dict[str, Any]]:
        try:
            return json.loads(self.store_path.read_text(encoding="utf-8"))
        except Exception:
            return []

    def _write(self, data: list[dict[str, Any]]) -> None:
        with self._lock:
            self.store_path.write_text(
                json.dumps(data, indent=2, ensure_ascii=False),
                encoding="utf-8",
            )

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
        data["title"] = {"en": entry.title.en, "ar": entry.title.ar, "ar_available": entry.title.ar_available}
        data["content"] = {"en": entry.content.en, "ar": entry.content.ar, "ar_available": entry.content.ar_available}
        return data

    def ingest(self, entry: KnowledgeEntry) -> str:
        data = self._read()
        data.append(self._entry_to_dict(entry))
        self._write(data)
        logging.getLogger(__name__).info("knowledge_ingested", entry_id=entry.entry_id, category=entry.category)
        return entry.entry_id

    def ingest_batch(self, entries: list[KnowledgeEntry]) -> int:
        data = self._read()
        for entry in entries:
            data.append(self._entry_to_dict(entry))
        self._write(data)
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
        cutoff = datetime.now(timezone.utc) - timedelta(days=days)
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
                "date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
                "total_entries": len(self._read()),
                "recent_24h_count": len(recent),
                "entries": [e.to_dict(lang) for e in recent],
            },
            lang,
        )

    def purge_expired(self) -> int:
        now = datetime.now(timezone.utc)
        data = self._read()
        kept = []
        removed = 0
        for raw in data:
            expires = raw.get("expires_at")
            if expires:
                try:
                    if datetime.fromisoformat(expires) < now:
                        removed += 1
                        continue
                except Exception:
                    pass
            kept.append(raw)
        self._write(kept)
        return removed

    def stats(self) -> dict[str, Any]:
        data = self._read()
        categories: dict[str, int] = {}
        for raw in data:
            categories[raw.get("category", "unknown")] = categories.get(raw.get("category", "unknown"), 0) + 1
        return {
            "total_entries": len(data),
            "categories": categories,
            "store_path": str(self.store_path),
        }

    def redact(self, entry_id: str, fields: list[str]) -> bool:
        data = self._read()
        for raw in data:
            if raw.get("entry_id") == entry_id:
                for field in fields:
                    if field in ("title", "content"):
                        raw[field] = {"en": "[redacted]", "ar": "[محذوف]", "ar_available": True}
                    elif field in raw:
                        raw[field] = "[redacted]"
                self._write(data)
                return True
        return False
