"""Autonomous Distribution router — unified read-only status endpoints.

Exposes:
    GET  /api/v1/autonomous-distribution/health
    POST /api/v1/autonomous-distribution/lead/process
    POST /api/v1/autonomous-distribution/outreach/audit
    POST /api/v1/autonomous-distribution/payment/process
    POST /api/v1/autonomous-distribution/proof-pack/assemble
    POST /api/v1/autonomous-distribution/retainer/assess
    GET  /api/v1/autonomous-distribution/loops/morning
    GET  /api/v1/autonomous-distribution/loops/evening
    GET  /api/v1/autonomous-distribution/loops/weekly
    GET  /api/v1/autonomous-distribution/loops/monthly

All endpoints are read/compute-only — they do NOT send anything externally
and they do NOT mutate persistent state.
"""

from __future__ import annotations

from typing import Any, Literal

from fastapi import APIRouter
from pydantic import BaseModel, Field

from auto_client_acquisition.adoption_os import AdoptionDimensions
from auto_client_acquisition.autonomous_distribution import (
    assemble_proof_pack,
    assess_retainer,
    evening_loop,
    monthly_loop,
    morning_loop,
    process_lead,
    process_payment,
    weekly_loop,
)
from auto_client_acquisition.autonomous_distribution.engine import audit_outreach_draft
from auto_client_acquisition.data_os import SourcePassport
from auto_client_acquisition.sales_os import ICPDimensions

router = APIRouter(
    prefix="/api/v1/autonomous-distribution",
    tags=["autonomous-distribution"],
)


# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------

class _PassportBody(BaseModel):
    source_id: str
    source_type: str
    owner: str
    allowed_use: list[str] = Field(default_factory=lambda: ["internal_analysis"])
    contains_pii: bool = False
    sensitivity: str = "medium"
    retention_policy: str = "90_days"
    ai_access_allowed: bool = True
    external_use_allowed: bool = False


class _ICPBody(BaseModel):
    b2b_service_fit: int = 50
    data_maturity: int = 50
    governance_posture: int = 50
    budget_signal: int = 50
    decision_velocity: int = 50


class ProcessLeadBody(BaseModel):
    lead_row: dict[str, Any]
    passport: _PassportBody
    icp: _ICPBody
    discovery_answers: dict[str, Any] = Field(default_factory=dict)
    raw_request_text: str = ""


class AuditOutreachBody(BaseModel):
    text: str
    channel: Literal["email", "whatsapp", "linkedin"] = "email"


class ProcessPaymentBody(BaseModel):
    invoice_ref: str
    amount_sar: float
    moyasar_status: Literal["pending", "paid", "failed", "refunded"]
    moyasar_mode: Literal["test", "live"]
    customer_id: str
    rung: int
    proof_pack_score: int


class AssembleProofPackBody(BaseModel):
    sections: dict[str, str] = Field(default_factory=dict)
    governance_blocked: bool = False


class _AdoptionBody(BaseModel):
    executive_sponsor: int = 50
    workflow_owner: int = 50
    data_readiness: int = 50
    user_engagement: int = 50
    approval_completion: int = 50
    proof_visibility: int = 50
    monthly_cadence: int = 50
    expansion_pull: int = 50


class AssessRetainerBody(BaseModel):
    adoption: _AdoptionBody
    customer_id: str
    proof_score: int
    workflow_owner_exists: bool
    monthly_workflow_exists: bool
    governance_risk_controlled: bool


# ---------------------------------------------------------------------------
# Health
# ---------------------------------------------------------------------------

@router.get("/health")
def health() -> dict[str, Any]:
    return {
        "status": "ok",
        "engine": "auto_client_acquisition.autonomous_distribution",
        "layers": [
            "data_os",
            "governance_os",
            "sales_os",
            "proof_os",
            "value_os",
            "capital_os",
            "adoption_os",
            "client_os",
            "friction_log",
        ],
        "loops": ["morning", "evening", "weekly", "monthly"],
        "send_policy": "draft-only — no external send without founder approval",
    }


# ---------------------------------------------------------------------------
# Core endpoints
# ---------------------------------------------------------------------------

def _passport_from_body(body: _PassportBody) -> SourcePassport:
    return SourcePassport(
        source_id=body.source_id,
        source_type=body.source_type,
        owner=body.owner,
        allowed_use=frozenset(body.allowed_use),
        contains_pii=body.contains_pii,
        sensitivity=body.sensitivity,
        retention_policy=body.retention_policy,
        ai_access_allowed=body.ai_access_allowed,
        external_use_allowed=body.external_use_allowed,
    )


def _icp_from_body(body: _ICPBody) -> ICPDimensions:
    return ICPDimensions(
        b2b_service_fit=body.b2b_service_fit,
        data_maturity=body.data_maturity,
        governance_posture=body.governance_posture,
        budget_signal=body.budget_signal,
        decision_velocity=body.decision_velocity,
    )


@router.post("/lead/process")
def lead_process(body: ProcessLeadBody) -> dict[str, Any]:
    sp = _passport_from_body(body.passport)
    icp = _icp_from_body(body.icp)
    d = process_lead(
        lead_row=body.lead_row,
        source_passport=sp,
        icp_dims=icp,
        discovery_answers=body.discovery_answers,
        raw_request_text=body.raw_request_text,
    )
    return d.to_dict()


@router.post("/outreach/audit")
def outreach_audit(body: AuditOutreachBody) -> dict[str, Any]:
    d = audit_outreach_draft(body.text, channel=body.channel)
    return {
        "governance_decision": d.governance_decision.value,
        "safe_to_queue": d.safe_to_queue,
        "reasons": list(d.reasons),
        "rationale_ar": d.rationale_ar,
        "rationale_en": d.rationale_en,
        "timestamp": d.timestamp,
    }


@router.post("/payment/process")
def payment_process(body: ProcessPaymentBody) -> dict[str, Any]:
    d = process_payment(
        invoice_ref=body.invoice_ref,
        amount_sar=body.amount_sar,
        moyasar_status=body.moyasar_status,
        moyasar_mode=body.moyasar_mode,
        customer_id=body.customer_id,
        rung=body.rung,
        proof_pack_score=body.proof_pack_score,
    )
    return {
        "governance_decision": d.governance_decision.value,
        "capital_asset_eligible": d.capital_asset_eligible,
        "asset_type": d.asset_type,
        "invoice_ref": d.invoice_ref,
        "amount_sar": d.amount_sar,
        "rung": d.rung,
        "rationale_ar": d.rationale_ar,
        "rationale_en": d.rationale_en,
        "timestamp": d.timestamp,
    }


@router.post("/proof-pack/assemble")
def proof_pack_assemble(body: AssembleProofPackBody) -> dict[str, Any]:
    d = assemble_proof_pack(
        sections=body.sections,
        governance_blocked=body.governance_blocked,
    )
    return {
        "governance_decision": d.governance_decision.value,
        "score": d.score,
        "score_with_penalty": d.score_with_penalty,
        "sections_complete": d.sections_complete,
        "missing_sections": list(d.missing_sections),
        "publish_eligible": d.publish_eligible,
        "rationale_ar": d.rationale_ar,
        "rationale_en": d.rationale_en,
        "timestamp": d.timestamp,
    }


@router.post("/retainer/assess")
def retainer_assess(body: AssessRetainerBody) -> dict[str, Any]:
    ad = AdoptionDimensions(
        executive_sponsor=body.adoption.executive_sponsor,
        workflow_owner=body.adoption.workflow_owner,
        data_readiness=body.adoption.data_readiness,
        user_engagement=body.adoption.user_engagement,
        approval_completion=body.adoption.approval_completion,
        proof_visibility=body.adoption.proof_visibility,
        monthly_cadence=body.adoption.monthly_cadence,
        expansion_pull=body.adoption.expansion_pull,
    )
    d = assess_retainer(
        adoption_dims=ad,
        customer_id=body.customer_id,
        proof_score=body.proof_score,
        workflow_owner_exists=body.workflow_owner_exists,
        monthly_workflow_exists=body.monthly_workflow_exists,
        governance_risk_controlled=body.governance_risk_controlled,
    )
    return {
        "governance_decision": d.governance_decision.value,
        "eligible": d.eligible,
        "adoption_band": d.adoption_band,
        "adoption_score": d.adoption_score_value,
        "next_offer": d.next_offer,
        "blockers": list(d.blockers),
        "rationale_ar": d.rationale_ar,
        "rationale_en": d.rationale_en,
        "timestamp": d.timestamp,
    }


# ---------------------------------------------------------------------------
# Loops (read-only)
# ---------------------------------------------------------------------------

@router.get("/loops/morning")
def loop_morning(leads_inbound: int = 0, leads_scored: int = 0, drafts_pending: int = 0) -> dict[str, Any]:
    r = morning_loop(
        leads_inbound=leads_inbound,
        leads_scored=leads_scored,
        drafts_pending=drafts_pending,
    )
    return {
        "governance_decision": r.governance_decision.value,
        "leads_refreshed": r.leads_refreshed,
        "leads_scored": r.leads_scored,
        "drafts_queued": r.drafts_queued,
        "high_priority_actions": list(r.high_priority_actions),
        "founder_digest_ar": r.founder_digest_ar,
        "founder_digest_en": r.founder_digest_en,
        "timestamp": r.timestamp,
    }


@router.get("/loops/evening")
def loop_evening(revenue_today_sar: float = 0.0, leads_in_pipeline: int = 0) -> dict[str, Any]:
    r = evening_loop(
        revenue_today_sar=revenue_today_sar,
        leads_in_pipeline=leads_in_pipeline,
    )
    return {
        "governance_decision": r.governance_decision.value,
        "revenue_today_sar": r.revenue_today_sar,
        "leads_in_pipeline": r.leads_in_pipeline,
        "friction_events_today": r.friction_events_today,
        "high_severity_frictions": r.high_severity_frictions,
        "tomorrow_top_4": list(r.tomorrow_top_4),
        "founder_digest_ar": r.founder_digest_ar,
        "founder_digest_en": r.founder_digest_en,
        "timestamp": r.timestamp,
    }


@router.get("/loops/weekly")
def loop_weekly() -> dict[str, Any]:
    r = weekly_loop()
    return {
        "governance_decision": r.governance_decision.value,
        "retainers_eligible": r.retainers_eligible,
        "capital_assets_added": r.capital_assets_added,
        "proof_packs_completed": r.proof_packs_completed,
        "revenue_week_sar": r.revenue_week_sar,
        "mrr_sar": r.mrr_sar,
        "one_time_week_sar": r.one_time_week_sar,
        "week_over_week_pct": r.week_over_week_pct,
        "next_week_focus_ar": r.next_week_focus_ar,
        "next_week_focus_en": r.next_week_focus_en,
        "timestamp": r.timestamp,
    }


@router.get("/loops/monthly")
def loop_monthly(days_since_launch: int = 1) -> dict[str, Any]:
    r = monthly_loop(day_count_since_launch=days_since_launch)
    return {
        "governance_decision": r.governance_decision.value,
        "month_phase": r.month_phase,
        "cumulative_revenue_sar": r.cumulative_revenue_sar,
        "active_retainers": r.active_retainers,
        "capital_assets_total": r.capital_assets_total,
        "milestone_verdict": r.milestone_verdict,
        "decisions_for_founder": list(r.decisions_for_founder),
        "rationale_ar": r.rationale_ar,
        "rationale_en": r.rationale_en,
        "timestamp": r.timestamp,
    }


__all__ = ["router"]
