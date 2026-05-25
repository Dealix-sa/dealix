"""Strategy OS HTTP surface — use-case ranking and AI readiness."""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict, Field

from auto_client_acquisition.strategy_os.ai_readiness import compute_ai_readiness
from auto_client_acquisition.strategy_os.use_case_scoring import (
    UseCaseScores,
    rank_use_cases,
    roadmap_buckets,
)

router = APIRouter(prefix="/api/v1/strategy-os", tags=["strategy-os"])


class _UseCaseIn(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=1, max_length=120)
    revenue_impact: float = Field(ge=0.0, le=1.0)
    time_save: float = Field(ge=0.0, le=1.0)
    data_readiness: float = Field(ge=0.0, le=1.0)
    ease: float = Field(ge=0.0, le=1.0)
    low_risk: float = Field(ge=0.0, le=1.0)


class _RankRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    use_cases: list[_UseCaseIn] = Field(min_length=1, max_length=20)


class _AiReadinessRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    data: float = Field(default=0.5, ge=0.0, le=1.0)
    process: float = Field(default=0.5, ge=0.0, le=1.0)
    governance: float = Field(default=0.5, ge=0.0, le=1.0)
    people: float = Field(default=0.5, ge=0.0, le=1.0)
    tech: float = Field(default=0.5, ge=0.0, le=1.0)


@router.get("/status")
async def status() -> dict[str, Any]:
    return {
        "service": "strategy_os",
        "version": "1.0.0",
        "endpoints": [
            "/rank-use-cases",
            "/ai-readiness",
        ],
        "read_only_scoring": True,
    }


@router.post("/rank-use-cases")
async def rank_use_cases_endpoint(body: _RankRequest) -> dict[str, Any]:
    try:
        cases = [
            UseCaseScores(
                name=u.name,
                revenue_impact=u.revenue_impact,
                time_save=u.time_save,
                data_readiness=u.data_readiness,
                ease=u.ease,
                low_risk=u.low_risk,
            )
            for u in body.use_cases
        ]
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    ranked = rank_use_cases(cases)
    top_names = [name for name, _ in ranked]
    return {
        "ranked": [{"name": name, "score": score} for name, score in ranked],
        "roadmap_buckets": roadmap_buckets(top_names),
        "weights": {
            "revenue_impact": 0.30,
            "time_save": 0.20,
            "data_readiness": 0.20,
            "ease": 0.15,
            "low_risk": 0.15,
        },
    }


@router.post("/ai-readiness")
async def ai_readiness_endpoint(body: _AiReadinessRequest) -> dict[str, Any]:
    return compute_ai_readiness(
        {
            "data": body.data,
            "process": body.process,
            "governance": body.governance,
            "people": body.people,
            "tech": body.tech,
        }
    )
