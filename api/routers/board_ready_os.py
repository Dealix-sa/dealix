"""Wave 17.0 — Board Ready OS HTTP surface.

Endpoints surface investor-grade governance checks, board memo generation,
due diligence coverage, and unit economics gates.

Hard gates:
  - no_fake_revenue: unit economics gate enforced
  - is_estimate_always_true: coverage scores carry is_estimate=True
  - approval_required_for_external_actions: board memo is draft_only=True
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel

from auto_client_acquisition.board_ready_os import (
    BOARD_DASHBOARD_METRICS,
    BOARD_MEMO_SECTIONS,
    BOARD_ROADMAP_PHASES,
    DUE_DILIGENCE_ARTIFACTS,
    board_dashboard_coverage_score,
    board_memo_sections_complete,
    board_roadmap_milestone_count,
    board_roadmap_phase_name,
    build_board_memo_markdown_skeleton,
    due_diligence_pack_coverage_score,
    unit_economics_scale_ok,
)

try:
    from auto_client_acquisition.investment_os import OPERATING_COVENANTS, VALUATION_DRIVERS

    _OPERATING_COVENANTS: list[str] = list(OPERATING_COVENANTS)
    _VALUATION_DRIVERS: list[str] = list(VALUATION_DRIVERS)
except Exception:  # noqa: BLE001
    _OPERATING_COVENANTS = []
    _VALUATION_DRIVERS = []

router = APIRouter(prefix="/api/v1/board-ready", tags=["Wave 17 — Board Ready OS"])

_HARD_GATES: dict[str, bool] = {
    "no_fake_revenue": True,
    "is_estimate_always_true": True,
    "approval_required_for_external_actions": True,
}


# ── Request models ────────────────────────────────────────────────────────────


class DashboardCoverageRequest(BaseModel):
    metrics_reported: list[str] = []


class MemoCompletenessRequest(BaseModel):
    sections_done: list[str] = []


class DueDiligenceRequest(BaseModel):
    artifacts_ready: list[str] = []


class UnitEconomicsRequest(BaseModel):
    gross_margin_pct: float
    proof_strength_ok: bool = False
    scope_creep_high: bool = False


class RoadmapPhaseRequest(BaseModel):
    phases: list[str] = []  # use BOARD_ROADMAP_PHASES if empty


# ── Endpoints ─────────────────────────────────────────────────────────────────


@router.get("/dashboard-metrics")
async def dashboard_metrics() -> dict[str, Any]:
    """Return the 12 headline board dashboard metric names."""
    return {
        "metrics": list(BOARD_DASHBOARD_METRICS),
        "count": len(BOARD_DASHBOARD_METRICS),
        "is_estimate": False,
    }


@router.post("/dashboard-coverage")
async def dashboard_coverage(body: DashboardCoverageRequest) -> dict[str, Any]:
    """Compute what share of board metrics are being tracked (0–100)."""
    reported_set = frozenset(body.metrics_reported)
    score = board_dashboard_coverage_score(reported_set)
    missing = [m for m in BOARD_DASHBOARD_METRICS if m not in reported_set]
    return {
        "coverage_score": score,
        "metrics_reported": body.metrics_reported,
        "total_metrics": len(BOARD_DASHBOARD_METRICS),
        "missing": missing,
        "is_estimate": True,
    }


@router.get("/memo-skeleton")
async def memo_skeleton() -> dict[str, Any]:
    """Return the twelve-section board memo markdown skeleton."""
    return {
        "skeleton_markdown": build_board_memo_markdown_skeleton(),
        "sections": list(BOARD_MEMO_SECTIONS),
        "draft_only": True,
        "is_estimate": False,
    }


@router.post("/memo-completeness")
async def memo_completeness(body: MemoCompletenessRequest) -> dict[str, Any]:
    """Check whether all board memo sections have been filled in.

    Sections are treated as complete when present in sections_done; content
    value is set to a non-empty placeholder so the function recognises them.
    """
    # board_memo_sections_complete takes Mapping[str, str]; a section is
    # considered complete when it maps to a non-empty string.
    content_map: dict[str, str] = {s: "provided" for s in body.sections_done}
    complete, missing = board_memo_sections_complete(content_map)
    return {
        "complete": complete,
        "sections_done": body.sections_done,
        "total_sections": len(BOARD_MEMO_SECTIONS),
        "all_sections": list(BOARD_MEMO_SECTIONS),
        "is_estimate": False,
    }


@router.post("/due-diligence-coverage")
async def due_diligence_coverage(body: DueDiligenceRequest) -> dict[str, Any]:
    """Compute what share of due diligence artifacts are ready (0–100)."""
    artifacts_set = frozenset(body.artifacts_ready)
    score = due_diligence_pack_coverage_score(artifacts_set)
    missing = [a for a in DUE_DILIGENCE_ARTIFACTS if a not in artifacts_set]
    return {
        "coverage_score": score,
        "artifacts_ready": body.artifacts_ready,
        "all_artifacts": list(DUE_DILIGENCE_ARTIFACTS),
        "missing": missing,
        "is_estimate": True,
    }


@router.post("/unit-economics-gate")
async def unit_economics_gate(body: UnitEconomicsRequest) -> dict[str, Any]:
    """Gate whether unit economics support scaling an offer."""
    scale_ok, errors = unit_economics_scale_ok(
        gross_margin_pct=body.gross_margin_pct,
        proof_strength_ok=body.proof_strength_ok,
        scope_creep_high=body.scope_creep_high,
    )
    return {
        "scale_ok": scale_ok,
        "errors": list(errors),
        "gross_margin_pct": body.gross_margin_pct,
        "min_required_pct": 40.0,
        "is_estimate": False,
    }


@router.post("/roadmap-phases")
async def roadmap_phases(body: RoadmapPhaseRequest) -> dict[str, Any]:
    """Return milestone counts and display names for roadmap phases.

    When phases is empty the full BOARD_ROADMAP_PHASES list is used.
    Invalid phase names are silently skipped.
    """
    requested = body.phases if body.phases else list(BOARD_ROADMAP_PHASES)
    result: list[dict[str, Any]] = []
    for phase in requested:
        # BOARD_ROADMAP_PHASES is a tuple; phases are looked up by 1-based index
        if phase not in BOARD_ROADMAP_PHASES:
            continue
        idx = list(BOARD_ROADMAP_PHASES).index(phase) + 1  # 1-based
        try:
            name = board_roadmap_phase_name(idx)
            milestone_count = board_roadmap_milestone_count(idx)
        except (KeyError, ValueError):
            continue
        result.append(
            {
                "phase": phase,
                "name": name,
                "milestone_count": milestone_count,
            }
        )
    return {"phases": result, "is_estimate": False}


@router.get("/investor-brief-schema")
async def investor_brief_schema() -> dict[str, Any]:
    """Return the structure an investor brief should contain."""
    return {
        "brief_sections": [
            {
                "section": "company_overview",
                "fields": ["name", "founded", "sector", "team_size"],
            },
            {
                "section": "traction",
                "fields": [
                    "arr_sar",
                    "mrr_sar",
                    "customers",
                    "nrr_pct",
                    "proof_packs",
                ],
            },
            {
                "section": "product",
                "fields": ["stage", "live_features", "ai_modules"],
            },
            {
                "section": "financials",
                "fields": ["gross_margin_pct", "burn_rate_sar", "runway_months"],
            },
            {
                "section": "ask",
                "fields": ["amount_sar", "use_of_funds", "target_close_date"],
            },
            {
                "section": "governance",
                "fields": [
                    "pdpl_compliant",
                    "zatca_compliant",
                    "board_dashboard_pct",
                ],
            },
        ],
        "covenants": _OPERATING_COVENANTS,
        "valuation_drivers": _VALUATION_DRIVERS,
        "draft_only": True,
        "is_estimate": False,
    }
