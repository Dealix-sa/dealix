"""Research OS API.

Multi-source deep research with safe fallback when no keys are configured.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from intelligence.bilingual import LanguageCode, get_lang
from intelligence.deep_research import DeepResearchEngine, ResearchSource
from intelligence.knowledge_storage import KnowledgeStorageUnavailable

router = APIRouter(prefix="/api/v1/ops/research", tags=["Research OS"])
_engine = DeepResearchEngine()


class ResearchQueryRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=1000)
    sources: list[str] | None = None
    sector: str | None = None
    lang: LanguageCode = "both"
    limit: int = Field(default=10, ge=1, le=50)


def _raise_storage_unavailable(exc: KnowledgeStorageUnavailable) -> None:
    raise HTTPException(
        status_code=503,
        detail={
            "code": "knowledge_storage_unavailable",
            "message": "Research OS durable knowledge storage is unavailable; persistence fails closed.",
        },
    ) from exc


@router.get("/readiness")
async def research_storage_readiness() -> dict[str, Any]:
    """Return the shared Knowledge OS storage readiness signal."""

    return _engine.storage_readiness()


@router.get("/sources")
async def research_sources(lang: LanguageCode = Depends(get_lang)) -> dict[str, Any]:
    return {"sources": _engine.available_sources(), "lang": lang}


@router.post("/query")
async def research_query(payload: ResearchQueryRequest) -> dict[str, Any]:
    sources = None
    if payload.sources:
        sources = [ResearchSource(s) for s in payload.sources]
    try:
        bundle = _engine.research(
            query=payload.query,
            sources=sources,
            sector=payload.sector,
            lang=payload.lang,
            limit=payload.limit,
        )
    except KnowledgeStorageUnavailable as exc:
        _raise_storage_unavailable(exc)
    return bundle.to_dict(payload.lang)


@router.get("/company/{company_name}")
async def company_dossier(
    company_name: str, lang: LanguageCode = Depends(get_lang)
) -> dict[str, Any]:
    try:
        return _engine.company_dossier(company_name, lang)
    except KnowledgeStorageUnavailable as exc:
        _raise_storage_unavailable(exc)


@router.get("/sector/{sector}")
async def sector_intelligence(
    sector: str, lang: LanguageCode = Depends(get_lang)
) -> dict[str, Any]:
    try:
        bundle = _engine.research(
            query=f"Saudi {sector} market intelligence",
            sector=sector,
            lang=lang,
            limit=10,
        )
    except KnowledgeStorageUnavailable as exc:
        _raise_storage_unavailable(exc)
    return bundle.to_dict(lang)
