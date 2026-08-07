"""Sales OS API.

Pipeline playbook, deal reviews, coaching, forecasting, and battlecards.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from intelligence.bilingual import LanguageCode, get_lang
from intelligence.sales_ops import SalesOperatingSystem

router = APIRouter(prefix="/api/v1/ops/sales", tags=["Sales OS"])
_os = SalesOperatingSystem()


class DealReviewRequest(BaseModel):
    deal: dict[str, Any]
    competitor: str | None = None
    lang: LanguageCode = "both"


class BatchReviewRequest(BaseModel):
    deals: list[dict[str, Any]] = Field(..., min_length=1)
    lang: LanguageCode = "both"


@router.get("/playbook")
async def get_playbook(lang: LanguageCode = Depends(get_lang)) -> dict[str, Any]:
    return _os.get_pipeline_playbook(lang)


@router.post("/review-deal")
async def review_deal(payload: DealReviewRequest) -> dict[str, Any]:
    return _os.review_deal(payload.deal, competitor=payload.competitor, lang=payload.lang)


@router.post("/batch-review")
async def batch_review(payload: BatchReviewRequest) -> dict[str, Any]:
    return _os.batch_review(payload.deals, lang=payload.lang)


@router.post("/coaching-brief")
async def coaching_brief(payload: BatchReviewRequest) -> dict[str, Any]:
    return _os.coaching_brief(payload.deals, lang=payload.lang)


@router.post("/weekly-brief")
async def weekly_brief(payload: BatchReviewRequest) -> dict[str, Any]:
    return _os.weekly_sales_brief(payload.deals, lang=payload.lang)


@router.get("/battlecard/{competitor}")
async def battlecard(competitor: str, lang: LanguageCode = Depends(get_lang)) -> dict[str, Any]:
    return _os.battlecard_for(competitor, lang)
