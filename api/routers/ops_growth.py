"""Growth OS API.

Campaigns, experiments, content briefs, social proof, PLG diagnostic.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from intelligence.bilingual import LanguageCode, get_lang
from intelligence.growth_ops import ContentType, GrowthOperatingSystem

router = APIRouter(prefix="/api/v1/ops/growth", tags=["Growth OS"])
_os = GrowthOperatingSystem()


class CampaignRequest(BaseModel):
    name: str = Field(..., min_length=1)
    sector: str = Field(..., min_length=1)
    city: str = Field(..., min_length=1)
    objective: str = Field(..., min_length=1)
    template: str = "diagnostic_outreach"
    lang: LanguageCode = "both"


class ExperimentRequest(BaseModel):
    hypothesis_en: str = Field(..., min_length=1)
    hypothesis_ar: str = Field(..., min_length=1)
    channel: str = Field(..., min_length=1)
    metric: str = Field(..., min_length=1)
    target: float = Field(..., gt=0)
    baseline: float | None = None


class ContentBriefRequest(BaseModel):
    topic_en: str = Field(..., min_length=1)
    topic_ar: str = Field(..., min_length=1)
    target_sector: str = Field(..., min_length=1)
    content_type: ContentType
    lang: LanguageCode = "both"


class SocialProofRequest(BaseModel):
    asset_type: str = Field(..., min_length=1)
    content_en: str = Field(..., min_length=1)
    content_ar: str = Field(..., min_length=1)
    company_name: str = Field(..., min_length=1)
    sector: str = Field(..., min_length=1)
    verified: bool = False
    lang: LanguageCode = "both"


class PLGRequest(BaseModel):
    company_name: str = Field(..., min_length=1)
    sector: str = Field(..., min_length=1)
    city: str = Field(..., min_length=1)
    employees: int = Field(..., ge=1)
    lang: LanguageCode = "both"


@router.post("/campaign")
async def plan_campaign(payload: CampaignRequest) -> dict[str, Any]:
    return _os.plan_campaign(
        name=payload.name,
        sector=payload.sector,
        city=payload.city,
        objective=payload.objective,
        template=payload.template,
        lang=payload.lang,
    )


@router.post("/campaign/{campaign_id}/approve")
async def approve_campaign(campaign_id: str) -> dict[str, Any]:
    return _os.approve_campaign(campaign_id)


@router.post("/experiment")
async def create_experiment(payload: ExperimentRequest) -> dict[str, Any]:
    return _os.create_experiment(
        hypothesis_en=payload.hypothesis_en,
        hypothesis_ar=payload.hypothesis_ar,
        channel=payload.channel,
        metric=payload.metric,
        target=payload.target,
        baseline=payload.baseline,
    )


@router.get("/experiments")
async def list_experiments() -> dict[str, Any]:
    return _os.list_experiments()


@router.post("/content-brief")
async def content_brief(payload: ContentBriefRequest) -> dict[str, Any]:
    return _os.generate_content_brief(
        topic_en=payload.topic_en,
        topic_ar=payload.topic_ar,
        target_sector=payload.target_sector,
        content_type=payload.content_type,
        lang=payload.lang,
    )


@router.post("/social-proof")
async def collect_social_proof(payload: SocialProofRequest) -> dict[str, Any]:
    return _os.collect_social_proof(
        asset_type=payload.asset_type,  # type: ignore[arg-type]
        content_en=payload.content_en,
        content_ar=payload.content_ar,
        company_name=payload.company_name,
        sector=payload.sector,
        verified=payload.verified,
        lang=payload.lang,
    )


@router.get("/dashboard")
async def growth_dashboard(lang: LanguageCode = Depends(get_lang)) -> dict[str, Any]:
    return _os.growth_dashboard(lang)


@router.post("/plg-diagnostic")
async def plg_diagnostic(payload: PLGRequest) -> dict[str, Any]:
    return _os.run_plg_diagnostic(
        company_name=payload.company_name,
        sector=payload.sector,
        city=payload.city,
        employees=payload.employees,
        lang=payload.lang,
    )
