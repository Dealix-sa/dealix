"""Market Intelligence API Router.

Saudi B2B market signals, sector rankings, opportunity intelligence,
and deterministic AI scoring for prospects, pipelines, and decisions.

Public endpoints for growth — no auth required for read-only sector data.

Prefix: /api/v1/market-intelligence
"""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Any

from fastapi import APIRouter, Query
from pydantic import BaseModel, Field

from dealix.commercial.market_intelligence import MarketIntelligenceEngine
from intelligence import (
    Deal,
    EvidenceItem,
    EvidenceSynthesizer,
    EvidenceType,
    RevenueIntelligenceEngine,
    SaudiCompanyProfile,
    SaudiMarketIntelligence,
)

log = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/market-intelligence", tags=["Analytics"])

_engine = MarketIntelligenceEngine()


# ── Deterministic AI scoring models ──────────────────────────────────

class ProspectRequest(BaseModel):
    company_name: str = Field(min_length=1, max_length=255)
    sector: str = Field(min_length=1, max_length=128)
    city: str = Field(min_length=1, max_length=128)
    employees_estimate: int | None = Field(default=None, ge=1)
    website: str | None = Field(default=None, max_length=512)


class ICPScoreResponse(BaseModel):
    company_name: str
    score: float
    reasons: list[str]
    risk_flags: list[str]
    momentum: str
    recommended_package: str
    next_action: str


class DealRequest(BaseModel):
    deal_id: str = Field(min_length=1, max_length=64)
    company_name: str = Field(min_length=1, max_length=255)
    stage: str = Field(min_length=1, max_length=64)
    value_sar: float = Field(gt=0)
    created_at: datetime
    last_activity_at: datetime
    activities_count: int = Field(default=0, ge=0)
    days_in_stage: int = Field(default=0, ge=0)


class PipelineAnalysisRequest(BaseModel):
    deals: list[DealRequest] = Field(min_length=1, max_length=1000)


class StageBreakdownItem(BaseModel):
    stage: str
    count: int
    total_value: float
    avg_days: float
    win_probability: float


class RevenueIntelligenceResponse(BaseModel):
    pipeline_health: float
    total_pipeline_sar: float
    weighted_pipeline_sar: float
    revenue_at_risk_sar: float
    recommended_actions: list[str]
    stage_breakdown: list[StageBreakdownItem]


class EvidenceRequest(BaseModel):
    evidence_id: str = Field(min_length=1, max_length=64)
    evidence_type: EvidenceType
    title: str = Field(min_length=1, max_length=255)
    description: str = Field(min_length=1, max_length=5000)
    source: str = Field(min_length=1, max_length=255)
    created_at: datetime
    verified: bool = False


class DecisionRequest(BaseModel):
    question: str = Field(min_length=1, max_length=1000)
    evidence: list[EvidenceRequest] = Field(min_length=1, max_length=50)


class DecisionResponse(BaseModel):
    pack_id: str
    decision_type: str
    decision: str
    confidence: float
    gaps: list[str]
    risks: list[str]


# ── Existing endpoints ───────────────────────────────────────────────

@router.get("/signals")
async def get_market_signals(
    urgency: str | None = Query(default=None, description="Filter: HIGH | MEDIUM | LOW"),
    sector: str | None = Query(default=None, description="Filter by sector key"),
) -> dict[str, Any]:
    """Get Saudi market signals by urgency and/or sector.

    Returns curated signals from public Saudi market research (2025-2026).
    Signals are NOT scraped — sourced from public research and regulatory announcements.
    """
    signals = _engine.get_all_signals(urgency_filter=urgency, sector_filter=sector)
    return {
        "count": len(signals),
        "signals": [s.model_dump() for s in signals],
        "source_note_ar": "من بحث عام مُعتمد — ليس scraping",
        "source_note_en": "From approved public research — not scraping",
    }


@router.get("/sector-ranking")
async def get_sector_ranking() -> dict[str, Any]:
    """Returns Saudi B2B sectors ranked by AI operations opportunity.

    Scoring: pain intensity × AI adoption gap × avg deal value.
    """
    ranking = _engine.get_sector_ranking()
    return {
        "ranking": ranking,
        "methodology_ar": "الترتيب بناءً على: شدة الألم × فجوة تبني AI × متوسط قيمة الصفقة",
        "methodology_en": "Ranked by: pain intensity × AI adoption gap × average deal value",
        "note_ar": "هذه تقديرات قطاعية — ليست ضمانات نتائج",
        "note_en": "These are sector estimates — not guaranteed outcomes",
    }


@router.get("/sector/{sector}")
async def get_sector_intelligence(sector: str) -> dict[str, Any]:
    """Get detailed intelligence for a specific Saudi B2B sector."""
    intel = _engine.get_sector_intelligence(sector)
    if not intel:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=404,
            detail=f"Sector '{sector}' not found. Available: b2b_saas, agency, healthcare_clinic, real_estate, logistics, fintech, engineering",
        )
    return intel.model_dump()


@router.get("/why-now/{sector}")
async def get_why_now(sector: str) -> dict[str, Any]:
    """Get a concise 'Why Act Now' brief for a sector — for use in proposals."""
    brief = _engine.get_why_now_brief(sector)
    return {
        "sector": sector,
        "why_now_ar": brief["ar"],
        "why_now_en": brief["en"],
        "governance_note": "تُستخدم في العروض التجارية — تتطلب مراجعة المؤسس قبل الإرسال",
    }


@router.get("/opportunities/top")
async def get_top_opportunities() -> dict[str, Any]:
    """Returns top 3 highest-opportunity sectors with entry recommendations."""
    ranking = _engine.get_sector_ranking()
    top3 = ranking[:3]
    return {
        "top_opportunities": top3,
        "action_ar": "هذه القطاعات تمثل أعلى ROI للوقت المستثمر في التنقيب",
        "action_en": "These sectors represent the highest ROI on prospecting time invested",
    }


# ── Deterministic AI scoring endpoints ───────────────────────────────

@router.post("/score-prospect", response_model=ICPScoreResponse)
async def score_prospect(payload: ProspectRequest) -> ICPScoreResponse:
    """Score a Saudi B2B prospect against the Dealix ICP."""
    profile = SaudiCompanyProfile(
        company_name=payload.company_name,
        sector=payload.sector,
        city=payload.city,
        employees_estimate=payload.employees_estimate,
        website=payload.website,
    )
    intel = SaudiMarketIntelligence()
    score = intel.score_icp(profile)
    entry = intel.recommend_entry(payload.sector, payload.city)

    return ICPScoreResponse(
        company_name=score.company_name,
        score=score.score,
        reasons=score.reasons,
        risk_flags=score.risk_flags,
        momentum=entry["momentum"],
        recommended_package=entry["recommended_package"],
        next_action=entry["next_action"],
    )


@router.post("/analyze-pipeline", response_model=RevenueIntelligenceResponse)
async def analyze_pipeline(payload: PipelineAnalysisRequest) -> RevenueIntelligenceResponse:
    """Analyze a sales pipeline and return intelligence + recommendations."""
    engine = RevenueIntelligenceEngine()
    deals = [
        Deal(
            deal_id=d.deal_id,
            company_name=d.company_name,
            stage=d.stage,
            value_sar=d.value_sar,
            created_at=d.created_at,
            last_activity_at=d.last_activity_at,
            activities_count=d.activities_count,
            days_in_stage=d.days_in_stage,
        )
        for d in payload.deals
    ]
    engine.load_deals(deals)
    result = engine.analyze()

    return RevenueIntelligenceResponse(
        pipeline_health=result.pipeline_health,
        total_pipeline_sar=result.total_pipeline_sar,
        weighted_pipeline_sar=result.weighted_pipeline_sar,
        revenue_at_risk_sar=result.revenue_at_risk_sar,
        recommended_actions=result.recommended_actions,
        stage_breakdown=[
            StageBreakdownItem(
                stage=s.stage,
                count=s.count,
                total_value=s.total_value,
                avg_days=s.avg_days,
                win_probability=s.win_probability,
            )
            for s in result.stage_breakdown
        ],
    )


@router.post("/synthesize-decision", response_model=DecisionResponse)
async def synthesize_decision(payload: DecisionRequest) -> DecisionResponse:
    """Build an evidence-based decision pack for a commercial question."""
    synth = EvidenceSynthesizer()
    for e in payload.evidence:
        synth.add(EvidenceItem(
            evidence_id=e.evidence_id,
            evidence_type=e.evidence_type,
            title=e.title,
            description=e.description,
            source=e.source,
            created_at=e.created_at,
            verified=e.verified,
        ))
    pack = synth.synthesize(payload.question)

    return DecisionResponse(
        pack_id=pack.pack_id,
        decision_type=pack.decision_type.value,
        decision=pack.decision,
        confidence=pack.confidence,
        gaps=pack.gaps,
        risks=pack.risks,
    )
