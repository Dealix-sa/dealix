"""Launch OS API Router — GTM Revenue Intelligence endpoints.

Exposes ICP scoring, vertical selection, pipeline management, outreach drafts,
proposals, and the founder daily command as HTTP endpoints.

All endpoints are read-safe by default. Pipeline mutations (POST/PATCH) are
admin-key gated. No external sends. No production data mutations.
"""
from __future__ import annotations

import tempfile
import os
from pathlib import Path
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field

from api.security.api_key import require_admin_key
from dealix.launch_os.icp_scorer import batch_score, score_account, tier_label, ICPScore
from dealix.launch_os.vertical_scorer import rank_verticals, top_wedge, SAUDI_VERTICALS
from dealix.launch_os.trust_preflight import run_preflight
from dealix.launch_os.pipeline_tracker import PipelineTracker, PipelineStage
from dealix.launch_os.founder_daily_command import generate_daily_command, render_brief

router = APIRouter(prefix="/launch", tags=["launch"])

# In-memory pipeline backed by a temp file for this process (stateless by default)
_PIPELINE_PATH = Path(os.environ.get("DEALIX_PIPELINE_PATH", "var/launch_pipeline.jsonl"))


def _get_tracker() -> PipelineTracker:
    _PIPELINE_PATH.parent.mkdir(parents=True, exist_ok=True)
    return PipelineTracker(path=_PIPELINE_PATH)


# ---------------------------------------------------------------------------
# Request / Response models
# ---------------------------------------------------------------------------

class AccountScoreRequest(BaseModel):
    accounts: list[dict[str, Any]] = Field(..., min_length=1, max_length=50)


class ICPScoreOut(BaseModel):
    account_id: str
    account_name: str
    total_score: float
    tier: str
    company_size_score: float
    pain_intensity_score: float
    budget_signal_score: float
    decision_maker_access_score: float
    timing_score: float
    notes: str = ""


class VerticalOut(BaseModel):
    rank: int
    sector: str
    total_score: int
    revenue_potential: int
    pain_clarity: int
    regulatory_ease: int
    ai_readiness: int
    competition_gap: int
    notes_ar: str
    notes_en: str


class PipelineAccountIn(BaseModel):
    account_id: str
    company_name: str
    offer_id: str
    value_sar: int = 0
    icp_score: int = 0
    next_action: str = ""
    owner_notes: str = ""


class StageUpdateIn(BaseModel):
    new_stage: str
    next_action: str = ""
    owner_notes: str = ""


class OutreachPreflightRequest(BaseModel):
    channel: str
    body: str
    consent_confirmed: bool = False
    pricing_status: str = "approved"
    evidence_level: str = "L2"
    drafted_by: str = "founder"


class DraftedByRequest(BaseModel):
    account_id: str
    offer_id: str
    channel: str


# ---------------------------------------------------------------------------
# ICP Scoring endpoints
# ---------------------------------------------------------------------------

@router.get("/icp/schema", summary="Get ICP scoring rubric")
async def get_icp_schema() -> dict[str, Any]:
    """Return the ICP scoring rubric — dimension weights and tier thresholds."""
    return {
        "rubric": {
            "company_size_score": {"max": 20, "description": "Headcount + revenue signal"},
            "pain_intensity_score": {"max": 20, "description": "How acute and documented"},
            "budget_signal_score": {"max": 20, "description": "Ability and willingness to pay"},
            "decision_maker_access_score": {"max": 20, "description": "Reach the signer"},
            "timing_score": {"max": 20, "description": "Readiness to buy now"},
        },
        "tiers": {
            "A": {"min": 80, "action": "Pursue immediately"},
            "B": {"min": 60, "action": "Pursue this week"},
            "C": {"min": 40, "action": "Nurture"},
            "DQ": {"min": 0, "action": "Disqualify"},
        },
    }


@router.post("/icp/score", response_model=ICPScoreOut, summary="Score a single account")
async def score_single_account(account: dict[str, Any]) -> ICPScoreOut:
    """Score one account dict against the 100-point ICP rubric."""
    try:
        result = score_account(account)
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))
    return ICPScoreOut(
        account_id=result.account_id,
        account_name=result.account_name_ar,
        total_score=result.total_score,
        tier=result.tier,
        company_size_score=result.company_size_score,
        pain_intensity_score=result.pain_intensity_score,
        budget_signal_score=result.budget_signal_score,
        decision_maker_access_score=result.decision_maker_access_score,
        timing_score=result.timing_score,
        notes=result.notes,
    )


@router.post("/icp/batch", summary="Batch score up to 50 accounts")
async def batch_score_accounts(request: AccountScoreRequest) -> list[ICPScoreOut]:
    """Score a list of accounts and return them sorted by total_score descending."""
    results = batch_score(request.accounts)
    return [
        ICPScoreOut(
            account_id=r.account_id,
            account_name=r.account_name_ar,
            total_score=r.total_score,
            tier=r.tier,
            company_size_score=r.company_size_score,
            pain_intensity_score=r.pain_intensity_score,
            budget_signal_score=r.budget_signal_score,
            decision_maker_access_score=r.decision_maker_access_score,
            timing_score=r.timing_score,
            notes=r.notes,
        )
        for r in results
    ]


# ---------------------------------------------------------------------------
# Vertical Selection endpoints
# ---------------------------------------------------------------------------

@router.get("/verticals", response_model=list[VerticalOut], summary="All 15 Saudi verticals ranked")
async def list_verticals() -> list[VerticalOut]:
    """Return all 15 Saudi market verticals sorted by total_score descending."""
    ranked = rank_verticals()
    return [
        VerticalOut(
            rank=i + 1,
            sector=v.sector,
            total_score=v.total_score,
            revenue_potential=v.revenue_potential,
            pain_clarity=v.pain_clarity,
            regulatory_ease=v.regulatory_ease,
            ai_readiness=v.ai_readiness,
            competition_gap=v.competition_gap,
            notes_ar=v.notes_ar,
            notes_en=v.notes_en,
        )
        for i, v in enumerate(ranked)
    ]


@router.get("/verticals/top-wedge", response_model=VerticalOut, summary="Recommended first vertical")
async def get_top_wedge() -> VerticalOut:
    """Return the highest-scored vertical — the recommended entry wedge."""
    v = top_wedge()
    ranked = rank_verticals()
    return VerticalOut(
        rank=1,
        sector=v.sector,
        total_score=v.total_score,
        revenue_potential=v.revenue_potential,
        pain_clarity=v.pain_clarity,
        regulatory_ease=v.regulatory_ease,
        ai_readiness=v.ai_readiness,
        competition_gap=v.competition_gap,
        notes_ar=v.notes_ar,
        notes_en=v.notes_en,
    )


@router.get("/verticals/{sector}", response_model=VerticalOut, summary="Get one vertical")
async def get_vertical(sector: str) -> VerticalOut:
    """Return one vertical's full scorecard by sector name."""
    ranked = rank_verticals()
    for i, v in enumerate(ranked):
        if v.sector == sector:
            return VerticalOut(
                rank=i + 1,
                sector=v.sector,
                total_score=v.total_score,
                revenue_potential=v.revenue_potential,
                pain_clarity=v.pain_clarity,
                regulatory_ease=v.regulatory_ease,
                ai_readiness=v.ai_readiness,
                competition_gap=v.competition_gap,
                notes_ar=v.notes_ar,
                notes_en=v.notes_en,
            )
    raise HTTPException(status_code=404, detail=f"Sector '{sector}' not found")


# ---------------------------------------------------------------------------
# Pipeline endpoints
# ---------------------------------------------------------------------------

@router.get("/pipeline", summary="Pipeline summary")
async def get_pipeline_summary() -> dict[str, Any]:
    """Return pipeline summary: stage counts + total ARR."""
    tracker = _get_tracker()
    stage_counts = tracker.pipeline_summary()
    all_items = tracker.list_all()
    total_arr = sum(i.value_sar for i in all_items)
    arr_by_stage = {}
    for stage in PipelineStage.ALL:
        arr_by_stage[stage] = sum(i.value_sar for i in all_items if i.stage == stage)
    return {
        "total_deals": len(all_items),
        "total_arr_sar": total_arr,
        "by_stage": stage_counts,
        "arr_by_stage": arr_by_stage,
    }


@router.post("/pipeline/accounts", summary="Add account to pipeline", dependencies=[Depends(require_admin_key)])
async def add_to_pipeline(account: PipelineAccountIn) -> dict[str, Any]:
    """Add a new account to the sales pipeline."""
    tracker = _get_tracker()
    item = tracker.add(
        account_id=account.account_id,
        company_name=account.company_name,
        offer_id=account.offer_id,
        value_sar=account.value_sar,
        icp_score=account.icp_score,
        next_action=account.next_action,
        owner_notes=account.owner_notes,
    )
    return item.to_dict()


@router.patch("/pipeline/accounts/{account_id}/stage", summary="Move account stage", dependencies=[Depends(require_admin_key)])
async def update_account_stage(account_id: str, update: StageUpdateIn) -> dict[str, Any]:
    """Move a pipeline account to a new stage."""
    tracker = _get_tracker()
    try:
        item = tracker.update_stage(account_id, update.new_stage, update.next_action, update.owner_notes)
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Account '{account_id}' not found")
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    return item.to_dict()


@router.get("/pipeline/accounts/{account_id}", summary="Get pipeline account")
async def get_pipeline_account(account_id: str) -> dict[str, Any]:
    """Get details for a single pipeline account."""
    tracker = _get_tracker()
    item = tracker.get(account_id)
    if item is None:
        raise HTTPException(status_code=404, detail=f"Account '{account_id}' not found")
    return item.to_dict()


# ---------------------------------------------------------------------------
# Trust preflight endpoint
# ---------------------------------------------------------------------------

@router.post("/outreach/preflight", summary="Run trust preflight on a draft")
async def trust_preflight(request: OutreachPreflightRequest) -> dict[str, Any]:
    """Run the 10-rule trust gate on an outreach draft. Returns pass/fail + violations."""
    draft = {
        "channel": request.channel,
        "body": request.body,
        "consent_confirmed": request.consent_confirmed,
        "pricing_status": request.pricing_status,
        "evidence_level": request.evidence_level,
        "drafted_by": request.drafted_by,
    }
    passed, violations = run_preflight(draft)
    return {
        "passed": passed,
        "violations": [
            {
                "rule_id": v.rule_id,
                "severity": v.severity,
                "message_ar": v.message_ar,
                "message_en": v.message_en,
            }
            for v in violations
        ],
        "requires_founder_approval": any(v.severity == "warn" for v in violations),
    }


# ---------------------------------------------------------------------------
# Daily Command endpoint
# ---------------------------------------------------------------------------

@router.get("/daily-command", summary="Generate today's founder brief")
async def get_daily_command(format: str = Query(default="json", pattern="^(json|markdown)$")) -> Any:
    """Generate the founder daily command from the live pipeline."""
    tracker = _get_tracker()
    cmd = generate_daily_command(tracker, [])
    if format == "markdown":
        return {"markdown": render_brief(cmd)}
    return {
        "date": cmd.date,
        "priority_accounts": cmd.priority_accounts,
        "outreach_queue": cmd.outreach_queue,
        "approval_queue": cmd.approval_queue,
        "content_task": cmd.content_task,
        "pipeline_review_items": cmd.pipeline_review_items,
    }
