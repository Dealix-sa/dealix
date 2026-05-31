"""Growth OS — revenue marketing, attribution, and assurance endpoints.

Mounted under ``/api/v1/growth-os/`` as a read-only / pure-computation surface.
No external sends. No scraping. No automation.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict, Field

from dealix.growth_os.abm.pipeline import ABM_STAGES
from dealix.growth_os.attribution.analysis import group_revenue_by
from dealix.growth_os.attribution.types import ATTRIBUTION_TYPES
from dealix.growth_os.brand.positioning import BRAND_POSITIONING
from dealix.growth_os.content_engine.cta_matrix import CONTENT_TO_CASH
from dealix.growth_os.content_engine.operating_rules import (
    MARKETING_OPERATING_RULES,
    check_asset,
)
from dealix.growth_os.dashboard.metrics import build_snapshot
from dealix.growth_os.dashboard.red_flags import (
    RED_FLAG_CATALOG,
    detect_red_flags,
)
from dealix.growth_os.experiments.card import ExperimentCard, ExperimentResult
from dealix.growth_os.experiments.decision_engine import evaluate_experiment
from dealix.growth_os.funnels.registry import FUNNELS
from dealix.growth_os.geo.checker import validate_geo_page
from dealix.growth_os.geo.pages_registry import GEO_PAGES
from dealix.growth_os.icp.matrix import ICP_MATRIX
from dealix.growth_os.partners.motion import PARTNER_MOTION_STAGES
from dealix.growth_os.revenue_assurance.quality_score import revenue_quality_score
from dealix.growth_os.revenue_proof.proof_rules import (
    is_real_revenue,
    rejection_reasons,
)
from dealix.growth_os.revenue_proof.revenue_record import RevenueRecord
from dealix.growth_os.revenue_proof.statuses import REVENUE_STATUSES
from dealix.growth_os.streams.decisions import decide_stream_action
from dealix.growth_os.streams.portfolio import REVENUE_PORTFOLIO
from dealix.growth_os.streams.stream_card import RevenueStreamCard

router = APIRouter(prefix="/api/v1/growth-os", tags=["growth-os"])


_GATES: dict[str, bool] = {
    "no_external_send": True,
    "no_scraping": True,
    "no_vanity_metric_counted": True,
    "approval_required_for_external_actions": True,
}


def _ok(payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "payload": payload,
        "governance_decision": "ALLOW",
        "hard_gates": _GATES,
    }


# ── ICP ────────────────────────────────────────────────────────────


@router.get("/icp-matrix")
async def get_icp_matrix() -> dict[str, Any]:
    return _ok({"icps": [icp.model_dump() for icp in ICP_MATRIX.values()]})


# ── ABM ────────────────────────────────────────────────────────────


@router.get("/abm/pipeline-stages")
async def get_abm_stages() -> dict[str, Any]:
    return _ok({"stages": list(ABM_STAGES)})


# ── GEO ────────────────────────────────────────────────────────────


@router.get("/geo/pages")
async def get_geo_pages() -> dict[str, Any]:
    return _ok({"pages": [p.model_dump() for p in GEO_PAGES.values()]})


class _GEOValidateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    path: str = Field(..., min_length=1)
    sections: dict[str, str] = Field(default_factory=dict)


@router.post("/geo/validate-page")
async def post_geo_validate_page(req: _GEOValidateRequest) -> dict[str, Any]:
    report = validate_geo_page(req.model_dump())
    return _ok({"report": report.model_dump()})


# ── Content ────────────────────────────────────────────────────────


@router.get("/content/cta-matrix")
async def get_cta_matrix() -> dict[str, Any]:
    return _ok({"mappings": [m.model_dump() for m in CONTENT_TO_CASH.values()]})


# ── Revenue Proof + Assurance ──────────────────────────────────────


@router.post("/revenue/verify")
async def post_revenue_verify(record: RevenueRecord) -> dict[str, Any]:
    real = is_real_revenue(record)
    qs = revenue_quality_score(record)
    return _ok(
        {
            "is_real_revenue": real,
            "rejection_reasons": rejection_reasons(record),
            "quality_score": qs.model_dump(),
        }
    )


@router.post("/revenue/quality-score")
async def post_revenue_quality_score(record: RevenueRecord) -> dict[str, Any]:
    return _ok({"quality_score": revenue_quality_score(record).model_dump()})


@router.get("/revenue/statuses")
async def get_revenue_statuses() -> dict[str, Any]:
    return _ok({"statuses": list(REVENUE_STATUSES)})


# ── Attribution ────────────────────────────────────────────────────


@router.get("/attribution/types")
async def get_attribution_types() -> dict[str, Any]:
    return _ok({"types": list(ATTRIBUTION_TYPES)})


class _AttributionAnalyzeRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    records: list[RevenueRecord]
    dimensions: list[str] = Field(
        default_factory=lambda: ["channel", "offer", "campaign", "asset", "agent", "partner"]
    )
    only_real_revenue: bool = True


@router.post("/attribution/analyze")
async def post_attribution_analyze(req: _AttributionAnalyzeRequest) -> dict[str, Any]:
    out: dict[str, Any] = {}
    valid_dims = {"channel", "offer", "campaign", "asset", "agent", "partner"}
    for dim in req.dimensions:
        if dim not in valid_dims:
            raise HTTPException(status_code=400, detail=f"invalid dimension: {dim!r}")
        out[dim] = group_revenue_by(
            req.records,
            dim,  # type: ignore[arg-type]
            only_real_revenue=req.only_real_revenue,
        ).model_dump()
    return _ok({"breakdowns": out})


# ── Experiments ────────────────────────────────────────────────────


class _ExperimentEvaluateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    card: ExperimentCard
    result: ExperimentResult


@router.post("/experiments/evaluate")
async def post_experiment_evaluate(req: _ExperimentEvaluateRequest) -> dict[str, Any]:
    decision = evaluate_experiment(req.card, req.result)
    return _ok({"decision": decision.model_dump()})


# ── Dashboard ──────────────────────────────────────────────────────


@router.get("/dashboard/red-flags-catalog")
async def get_red_flag_catalog() -> dict[str, Any]:
    return _ok({"catalog": [f.model_dump() for f in RED_FLAG_CATALOG]})


class _DashboardSnapshotRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    metrics: dict[str, Any]


@router.post("/dashboard/snapshot")
async def post_dashboard_snapshot(req: _DashboardSnapshotRequest) -> dict[str, Any]:
    snapshot = build_snapshot(req.metrics)
    flags = detect_red_flags(snapshot)
    return _ok(
        {
            "snapshot": snapshot.model_dump(),
            "red_flags": [f.model_dump() for f in flags],
        }
    )


# ── Streams ────────────────────────────────────────────────────────


@router.get("/streams/portfolio")
async def get_streams_portfolio() -> dict[str, Any]:
    return _ok(
        {
            "buckets": list(REVENUE_PORTFOLIO.buckets),
            "streams": [s.model_dump() for s in REVENUE_PORTFOLIO.streams],
        }
    )


@router.post("/streams/decide")
async def post_streams_decide(card: RevenueStreamCard) -> dict[str, Any]:
    return _ok({"decision": decide_stream_action(card).model_dump()})


# ── Funnels ────────────────────────────────────────────────────────


@router.get("/funnels")
async def get_funnels() -> dict[str, Any]:
    return _ok({"funnels": [f.model_dump() for f in FUNNELS.values()]})


# ── Partners ───────────────────────────────────────────────────────


@router.get("/partners/motion")
async def get_partner_motion() -> dict[str, Any]:
    return _ok({"stages": [s.model_dump() for s in PARTNER_MOTION_STAGES]})


# ── Brand ──────────────────────────────────────────────────────────


@router.get("/brand/positioning")
async def get_brand_positioning() -> dict[str, Any]:
    return _ok({"positioning": BRAND_POSITIONING.model_dump()})


# ── Operating Rules ────────────────────────────────────────────────


@router.get("/operating-rules")
async def get_operating_rules() -> dict[str, Any]:
    return _ok({"rules": [r.model_dump() for r in MARKETING_OPERATING_RULES]})


class _OperatingRulesCheckRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    kind: str = Field(..., min_length=1)
    asset: dict[str, Any]


@router.post("/operating-rules/check")
async def post_operating_rules_check(
    req: _OperatingRulesCheckRequest,
) -> dict[str, Any]:
    try:
        violations = check_asset(req.kind, req.asset)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return _ok(
        {
            "kind": req.kind,
            "violations": [v.model_dump() for v in violations],
            "is_clean": not violations,
        }
    )


__all__ = ["router"]
