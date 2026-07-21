"""Knowledge OS API.

Accumulate, search, and retrieve intelligence over time.
"""

from __future__ import annotations

from datetime import UTC
from typing import Any

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from intelligence.bilingual import LanguageCode, get_lang
from intelligence.knowledge_accumulator import KnowledgeAccumulator, KnowledgeEntry

router = APIRouter(prefix="/api/v1/ops/knowledge", tags=["Knowledge OS"])
_accumulator = KnowledgeAccumulator()


class KnowledgeIngestRequest(BaseModel):
    category: str = Field(..., min_length=1)
    title_en: str = Field(..., min_length=1)
    title_ar: str = Field(..., min_length=1)
    content_en: str = Field(..., min_length=1)
    content_ar: str = Field(..., min_length=1)
    source: str = Field(..., min_length=1)
    sector: str | None = None
    company: str | None = None
    tags: list[str] = Field(default_factory=list)
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)
    expires_at: str | None = None


class KnowledgeBatchRequest(BaseModel):
    entries: list[KnowledgeIngestRequest]


@router.post("/ingest")
async def ingest(payload: KnowledgeIngestRequest, lang: LanguageCode = Depends(get_lang)) -> dict[str, Any]:
    from datetime import datetime, timezone

    from core.utils import generate_id

    entry = KnowledgeEntry(
        entry_id=generate_id("knl"),
        category=payload.category,
        title=__import__("intelligence.bilingual", fromlist=["BilingualRenderer"]).BilingualRenderer.bt(payload.title_en, payload.title_ar),
        content=__import__("intelligence.bilingual", fromlist=["BilingualRenderer"]).BilingualRenderer.bt(payload.content_en, payload.content_ar),
        source=payload.source,
        sector=payload.sector,
        company=payload.company,
        tags=payload.tags,
        confidence=payload.confidence,
        created_at=datetime.now(UTC).isoformat(),
        expires_at=payload.expires_at,
    )
    _accumulator.ingest(entry)
    return {"entry_id": entry.entry_id, "status": "ingested", "lang": lang}


@router.post("/ingest-batch")
async def ingest_batch(payload: KnowledgeBatchRequest) -> dict[str, Any]:
    from datetime import datetime, timezone

    from core.utils import generate_id
    from intelligence.bilingual import BilingualRenderer

    entries = [
        KnowledgeEntry(
            entry_id=generate_id("knl"),
            category=e.category,
            title=BilingualRenderer.bt(e.title_en, e.title_ar),
            content=BilingualRenderer.bt(e.content_en, e.content_ar),
            source=e.source,
            sector=e.sector,
            company=e.company,
            tags=e.tags,
            confidence=e.confidence,
            created_at=datetime.now(UTC).isoformat(),
            expires_at=e.expires_at,
        )
        for e in payload.entries
    ]
    count = _accumulator.ingest_batch(entries)
    return {"ingested": count}


@router.get("/search")
async def search(
    q: str,
    category: str | None = None,
    sector: str | None = None,
    company: str | None = None,
    limit: int = 20,
    lang: LanguageCode = Depends(get_lang),
) -> dict[str, Any]:
    results = _accumulator.search(q, category=category, sector=sector, company=company, limit=limit)
    return {
        "query": q,
        "count": len(results),
        "entries": [r.to_dict(lang) for r in results],
        "lang": lang,
    }


@router.get("/entry/{entry_id}")
async def get_entry(entry_id: str, lang: LanguageCode = Depends(get_lang)) -> dict[str, Any]:
    entry = _accumulator.get(entry_id)
    if not entry:
        return {"error": "entry not found"}
    return {"entry": entry.to_dict(lang), "lang": lang}


@router.get("/recent")
async def recent(
    days: int = 7,
    limit: int = 50,
    lang: LanguageCode = Depends(get_lang),
) -> dict[str, Any]:
    entries = _accumulator.list_recent(days=days, limit=limit)
    return {"count": len(entries), "entries": [e.to_dict(lang) for e in entries], "lang": lang}


@router.get("/digest")
async def digest(lang: LanguageCode = Depends(get_lang)) -> dict[str, Any]:
    return _accumulator.daily_digest(lang)


@router.delete("/purge-expired")
async def purge_expired() -> dict[str, Any]:
    removed = _accumulator.purge_expired()
    return {"removed": removed}


@router.get("/stats")
async def stats() -> dict[str, Any]:
    return _accumulator.stats()


@router.post("/redact/{entry_id}")
async def redact(entry_id: str, fields: list[str]) -> dict[str, Any]:
    ok = _accumulator.redact(entry_id, fields)
    return {"entry_id": entry_id, "redacted": ok}
