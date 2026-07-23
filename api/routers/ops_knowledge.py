"""Knowledge OS API.

Accumulate, search, and retrieve intelligence over time.
"""

from __future__ import annotations

from datetime import UTC
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from intelligence.bilingual import BilingualRenderer, LanguageCode, get_lang
from intelligence.knowledge_accumulator import KnowledgeAccumulator, KnowledgeEntry
from intelligence.knowledge_storage import KnowledgeStorageUnavailable

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


def _raise_storage_unavailable(exc: KnowledgeStorageUnavailable) -> None:
    raise HTTPException(
        status_code=503,
        detail={
            "code": "knowledge_storage_unavailable",
            "message": "Knowledge OS durable storage is unavailable; operations fail closed.",
        },
    ) from exc


@router.get("/readiness")
async def knowledge_storage_readiness() -> dict[str, Any]:
    """Return a non-secret readiness signal without dropping the router."""

    return _accumulator.storage_readiness()


@router.post("/ingest")
async def ingest(
    payload: KnowledgeIngestRequest, lang: LanguageCode = Depends(get_lang)
) -> dict[str, Any]:
    from datetime import datetime

    from core.utils import generate_id

    entry = KnowledgeEntry(
        entry_id=generate_id("knl"),
        category=payload.category,
        title=BilingualRenderer.bt(payload.title_en, payload.title_ar),
        content=BilingualRenderer.bt(payload.content_en, payload.content_ar),
        source=payload.source,
        sector=payload.sector,
        company=payload.company,
        tags=payload.tags,
        confidence=payload.confidence,
        created_at=datetime.now(UTC).isoformat(),
        expires_at=payload.expires_at,
    )
    try:
        _accumulator.ingest(entry)
    except KnowledgeStorageUnavailable as exc:
        _raise_storage_unavailable(exc)
    return {"entry_id": entry.entry_id, "status": "ingested", "lang": lang}


@router.post("/ingest-batch")
async def ingest_batch(payload: KnowledgeBatchRequest) -> dict[str, Any]:
    from datetime import datetime

    from core.utils import generate_id

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
    try:
        count = _accumulator.ingest_batch(entries)
    except KnowledgeStorageUnavailable as exc:
        _raise_storage_unavailable(exc)
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
    try:
        results = _accumulator.search(
            q,
            category=category,
            sector=sector,
            company=company,
            limit=limit,
        )
    except KnowledgeStorageUnavailable as exc:
        _raise_storage_unavailable(exc)
    return {
        "query": q,
        "count": len(results),
        "entries": [r.to_dict(lang) for r in results],
        "lang": lang,
    }


@router.get("/entry/{entry_id}")
async def get_entry(entry_id: str, lang: LanguageCode = Depends(get_lang)) -> dict[str, Any]:
    try:
        entry = _accumulator.get(entry_id)
    except KnowledgeStorageUnavailable as exc:
        _raise_storage_unavailable(exc)
    if not entry:
        return {"error": "entry not found"}
    return {"entry": entry.to_dict(lang), "lang": lang}


@router.get("/recent")
async def recent(
    days: int = 7,
    limit: int = 50,
    lang: LanguageCode = Depends(get_lang),
) -> dict[str, Any]:
    try:
        entries = _accumulator.list_recent(days=days, limit=limit)
    except KnowledgeStorageUnavailable as exc:
        _raise_storage_unavailable(exc)
    return {"count": len(entries), "entries": [e.to_dict(lang) for e in entries], "lang": lang}


@router.get("/digest")
async def digest(lang: LanguageCode = Depends(get_lang)) -> dict[str, Any]:
    try:
        return _accumulator.daily_digest(lang)
    except KnowledgeStorageUnavailable as exc:
        _raise_storage_unavailable(exc)


@router.delete("/purge-expired")
async def purge_expired() -> dict[str, Any]:
    try:
        removed = _accumulator.purge_expired()
    except KnowledgeStorageUnavailable as exc:
        _raise_storage_unavailable(exc)
    return {"removed": removed}


@router.get("/stats")
async def stats() -> dict[str, Any]:
    try:
        return _accumulator.stats()
    except KnowledgeStorageUnavailable as exc:
        _raise_storage_unavailable(exc)


@router.post("/redact/{entry_id}")
async def redact(entry_id: str, fields: list[str]) -> dict[str, Any]:
    try:
        ok = _accumulator.redact(entry_id, fields)
    except KnowledgeStorageUnavailable as exc:
        _raise_storage_unavailable(exc)
    return {"entry_id": entry_id, "redacted": ok}
