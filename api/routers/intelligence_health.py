"""
Monitoring & Health Checks for Dealix Intelligence Services.

Provides a lightweight endpoint and CLI for monitoring the intelligence layer.
"""

from __future__ import annotations

import time
from datetime import datetime
from pathlib import Path
from typing import Any

from fastapi import APIRouter

from intelligence import (
    Deal,
    EvidenceItem,
    EvidenceSynthesizer,
    EvidenceType,
    IntelligenceRouter,
    RevenueIntelligenceEngine,
    SaudiCompanyProfile,
    SaudiMarketIntelligence,
    TaskType,
)

router = APIRouter(prefix="/api/v1/intelligence-health", tags=["Monitoring"])

BRIEF_DIR = Path("reports/daily_intelligence")


@router.get("/status")
async def health_status() -> dict[str, Any]:
    """Return health status of all intelligence subsystems."""
    start = time.perf_counter()

    checks = {
        "market_intelligence": _check_market_intel(),
        "revenue_intelligence": _check_revenue_intel(),
        "evidence_synthesizer": _check_evidence(),
        "router": _check_router(),
        "daily_brief_pipeline": _check_daily_brief(),
    }

    elapsed_ms = (time.perf_counter() - start) * 1000
    healthy = all(c["status"] == "ok" for c in checks.values())

    return {
        "service": "dealix-intelligence",
        "timestamp": datetime.utcnow().isoformat(),
        "overall": "healthy" if healthy else "degraded",
        "latency_ms": round(elapsed_ms, 2),
        "checks": checks,
    }


def _check_market_intel() -> dict[str, Any]:
    try:
        intel = SaudiMarketIntelligence()
        profile = SaudiCompanyProfile(
            company_name="Test Co",
            sector="software",
            city="Riyadh",
            employees_estimate=50,
            website="https://test.sa",
        )
        score = intel.score_icp(profile)
        return {"status": "ok", "sample_score": score.score}
    except Exception as exc:
        return {"status": "error", "message": str(exc)}


def _check_revenue_intel() -> dict[str, Any]:
    try:
        engine = RevenueIntelligenceEngine()
        engine.load_deals([
            Deal(
                deal_id="h1",
                company_name="Health Check Co",
                stage="qualified",
                value_sar=5000,
                created_at=datetime.utcnow(),
                last_activity_at=datetime.utcnow(),
            ),
        ])
        result = engine.analyze()
        return {"status": "ok", "pipeline_health": result.pipeline_health}
    except Exception as exc:
        return {"status": "error", "message": str(exc)}


def _check_evidence() -> dict[str, Any]:
    try:
        synth = EvidenceSynthesizer()
        synth.add(EvidenceItem(
            evidence_id="hc1",
            evidence_type=EvidenceType.METRIC,
            title="Test metric",
            description="10% uplift",
            source="test",
            created_at=datetime.utcnow(),
            verified=True,
        ))
        pack = synth.synthesize("Should we proceed?")
        return {"status": "ok", "confidence": pack.confidence}
    except Exception as exc:
        return {"status": "error", "message": str(exc)}


def _check_router() -> dict[str, Any]:
    try:
        router = IntelligenceRouter()
        decision = router.route(TaskType.REASONING)
        return {"status": "ok", "selected_model": decision.model}
    except Exception as exc:
        return {"status": "error", "message": str(exc)}


def _check_daily_brief() -> dict[str, Any]:
    try:
        if not BRIEF_DIR.exists():
            return {"status": "ok", "note": "No briefs generated yet"}
        files = sorted(BRIEF_DIR.glob("daily_brief_*.json"), reverse=True)
        if not files:
            return {"status": "ok", "note": "No briefs generated yet"}
        latest = files[0]
        return {"status": "ok", "latest_brief": latest.name}
    except Exception as exc:
        return {"status": "error", "message": str(exc)}
