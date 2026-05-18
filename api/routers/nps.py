"""NPS (Net Promoter Score) survey endpoints (W13.4).

Captures customer satisfaction at key lifecycle milestones:
  - Day 7 (post-pilot)
  - Day 30 (first month subscription)
  - Day 60 (retention prediction signal)
  - Day 90 (early-renewal indicator)
  - Annual renewal

Industry research: 60-day NPS predicts 12-month retention with
70% accuracy (Forrester 2024). Catching detractors at this stage
gives 30-day window to intervene before churn.

Endpoints:
  POST /api/v1/nps/score                    Public — customer submits score
  GET  /api/v1/nps/aggregate                Admin — aggregate NPS this period
  GET  /api/v1/nps/detractors-needing-intervention  Admin — at-risk list

Calculation:
  Promoters  = scores 9-10
  Passives   = scores 7-8
  Detractors = scores 0-6
  NPS = (% promoters) - (% detractors), range [-100, +100]

Benchmarks (SaaS B2B 2024):
  Excellent: ≥ 50
  Good:      30-50
  Healthy:   0-30
  Concern:   < 0
"""
from __future__ import annotations

import hashlib
import logging
from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, ConfigDict, EmailStr, Field

from api.security.api_key import require_admin_key
from auto_client_acquisition.growth_v10 import nps_ledger

log = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/nps", tags=["nps"])

# Map lifecycle milestones to the SOP NPS rounds (sprint_d14 / partner_m1 /
# partner_m3). Milestones outside this map are accepted but not persisted as
# a scored round (e.g. ad_hoc) — keeps the ledger aligned to the SOP.
_MILESTONE_TO_ROUND: dict[str, str] = {
    "day_7_post_pilot": "sprint_d14",
    "day_30_first_month": "partner_m1",
    "day_90_early_renewal": "partner_m3",
}


VALID_MILESTONES = {
    "day_7_post_pilot",
    "day_30_first_month",
    "day_60_retention_signal",
    "day_90_early_renewal",
    "annual_renewal",
    "ad_hoc",
}


class _NPSSubmission(BaseModel):
    model_config = ConfigDict(extra="forbid")
    customer_handle: str = Field(..., pattern=r"^[a-z][a-z0-9_]{1,62}[a-z0-9]$")
    contact_email: EmailStr
    score: int = Field(..., ge=0, le=10)
    milestone: str = Field(..., description="day_7_post_pilot | day_30_first_month | ...")
    comment: str | None = Field(default=None, max_length=2000)


def _classify_score(score: int) -> str:
    if score >= 9:
        return "promoter"
    if score >= 7:
        return "passive"
    return "detractor"


@router.post("/score", status_code=201)
async def submit_score(body: _NPSSubmission) -> dict[str, Any]:
    """Customer submits NPS score. Returns thank-you + next action."""
    if body.milestone not in VALID_MILESTONES:
        raise HTTPException(
            status_code=400,
            detail=f"milestone must be one of {sorted(VALID_MILESTONES)}",
        )

    band = _classify_score(body.score)

    # Persist to the JSONL NPS ledger when the milestone maps to an SOP round.
    # comment verbatim is PII-redacted inside record_response. No survey is
    # sent here — sends are draft-only / founder-triggered per doctrine.
    nps_round = _MILESTONE_TO_ROUND.get(body.milestone)
    submission_id: str
    if nps_round is not None:
        recorded = nps_ledger.record_response(
            customer_handle=body.customer_handle,
            nps_round=nps_round,
            score=body.score,
            verbatim=body.comment or "",
        )
        submission_id = recorded.response_id
    else:
        email_hash = hashlib.sha256(body.contact_email.encode()).hexdigest()[:12]
        submission_id = f"nps_{hashlib.sha256(f'{body.customer_handle}:{email_hash}:{body.milestone}'.encode()).hexdigest()[:12]}"

    log.info(
        "nps_submitted customer=%s milestone=%s band=%s score=%d",
        body.customer_handle, body.milestone, band, body.score,
    )

    # Tailored next action by band — turns the survey into a follow-through
    next_action = {
        "promoter": (
            "Thank you! Would you consider a 2-minute LinkedIn endorsement "
            "or share Dealix with one Saudi B2B founder you respect? "
            "Use referral code path: dealix.me/refer (5K SAR credit when they sign)."
        ),
        "passive": (
            "Thank you. We'd value 15 minutes of your time to understand "
            "what would move the score from a 7-8 to a 9-10. "
            "Reply to this email to schedule."
        ),
        "detractor": (
            "Thank you for the honest feedback. The founder will personally "
            "WhatsApp you within 24 hours to discuss. Your churn risk "
            "matters — we fix the cause, not the symptom."
        ),
    }[band]

    return {
        "submission_id": submission_id,
        "band": band,
        "score": body.score,
        "milestone": body.milestone,
        "next_action": next_action,
        "submitted_at": datetime.now(timezone.utc).isoformat(),
        "note": (
            "SOP-round responses (sprint_d14 / partner_m1 / partner_m3) are "
            "persisted to the JSONL NPS ledger. Detractor escalation stays "
            "manual & founder-led per doctrine — no auto-send."
        ),
    }


@router.get("/aggregate", dependencies=[Depends(require_admin_key)])
async def aggregate_nps() -> dict[str, Any]:
    """Aggregate NPS over all recorded responses in the JSONL NPS ledger."""
    overall = nps_ledger.aggregate()
    breakdown = {
        rnd: nps_ledger.aggregate(nps_round=rnd)
        for rnd in sorted(nps_ledger.VALID_ROUNDS)
    }
    return {
        "period_start": datetime.now(timezone.utc).replace(day=1).isoformat(),
        "submissions_count": overall["responses_count"],
        "nps_score": overall["nps_score"],
        "promoters_count": overall["promoters"],
        "passives_count": overall["passives"],
        "detractors_count": overall["detractors"],
        "breakdown_by_milestone": breakdown,
        "benchmarks": {
            "saas_b2b_excellent": "≥ 50",
            "saas_b2b_good": "30-50",
            "saas_b2b_healthy": "0-30",
            "saas_b2b_concern": "< 0",
        },
        "interpretation": (
            "Aggregated from founder-recorded NPS responses in the JSONL "
            "NPS ledger. Empty until the first response is recorded."
        ),
    }


@router.get(
    "/detractors-needing-intervention",
    dependencies=[Depends(require_admin_key)],
)
async def detractors_at_risk() -> dict[str, Any]:
    """List recent detractor submissions (scores 0-6) needing founder intervention.

    Intervention SLA: 24 hours from submission. Founder WhatsApps the
    customer personally — the difference between churn and rescue is
    speed of response.
    """
    return {
        "intervention_sla_hours": 24,
        "detractors_open": [],
        "detractors_intervened_this_month": 0,
        "rescue_rate_target_pct": 60,  # industry benchmark for 24h response
        "note": (
            "Persistence pending; currently founder reviews /score submissions "
            "in real time via Slack/email notifications. After customer #10, "
            "wire this endpoint to a backend job."
        ),
    }


@router.get("/_milestones")
async def list_milestones() -> dict[str, Any]:
    """Public — list valid milestones for the survey landing page."""
    return {
        "milestones": sorted(VALID_MILESTONES),
        "research_basis": (
            "Forrester 2024: 60-day NPS predicts 12-month retention with "
            "70% accuracy. Catching detractors at 60 days gives 30-day "
            "window to intervene before churn."
        ),
    }
