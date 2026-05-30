"""
Commercial Engine API Router — Revenue delivery endpoints.
راوتر ماكينة التجارة — نقاط نهاية تسليم الإيراد.

Endpoints:
  POST /api/v1/commercial/diagnostic/generate
  GET  /api/v1/commercial/diagnostic/{report_id}
  POST /api/v1/commercial/warm-intro/draft
  POST /api/v1/commercial/pilot/start
  GET  /api/v1/commercial/pilot/{pilot_id}/brief
  GET  /api/v1/commercial/pilot/{pilot_id}/plan
  POST /api/v1/commercial/proof/build
  POST /api/v1/commercial/upsell/evaluate
  GET  /api/v1/commercial/daily-brief

All write operations are approval-only (NO_LIVE_SEND / NO_LIVE_CHARGE enforced).
"""

from __future__ import annotations

import logging
import uuid
from typing import Any

import json
import os
import re

from fastapi import APIRouter, Body, HTTPException

log = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/commercial", tags=["commercial"])

_ID_RE = re.compile(r"^[a-zA-Z0-9_-]{1,128}$")
# Absolute path to pilots data dir — resolved once at import so realpath checks are reliable
_PILOTS_DIR = os.path.realpath(
    os.path.join(os.path.dirname(__file__), "..", "..", "data", "pilots")
)


def _safe_id(value: str) -> str:
    """Validate and sanitize a user-provided ID for use in file paths."""
    sanitized = re.sub(r"[^a-zA-Z0-9_-]", "_", value)[:128]
    # os.path.basename is a CodeQL-recognized path-traversal sanitizer
    return os.path.basename(sanitized)


_CONSTITUTIONAL_GATES = {
    "no_live_send": True,
    "no_live_charge": True,
    "no_fake_proof": True,
    "approval_required_for_all_drafts": True,
}


# ── Diagnostic ────────────────────────────────────────────────────

@router.post("/diagnostic/generate")
async def generate_diagnostic(payload: dict[str, Any] = Body(default_factory=dict)) -> dict[str, Any]:
    """
    Generate a bilingual diagnostic report for a Saudi B2B company.
    Returns a DRAFT — founder reviews before delivery to prospect.
    """
    company_name = payload.get("company_name", "").strip()
    if not company_name:
        raise HTTPException(status_code=422, detail="company_name required")

    sector = payload.get("sector", "other")
    pain_points = payload.get("pain_points", "")
    locale = payload.get("locale", "ar")

    try:
        from dealix.commercial.diagnostic_engine import DiagnosticRequest, generate_diagnostic as _gen

        req = DiagnosticRequest(
            company_name=company_name,
            sector=sector,
            pain_points=pain_points,
            website_url=payload.get("website_url", ""),
            employee_count=int(payload.get("employee_count", 0)),
            monthly_leads=int(payload.get("monthly_leads", 0)),
            current_tools=payload.get("current_tools", ""),
            contact_name=payload.get("contact_name", ""),
            contact_role=payload.get("contact_role", ""),
            locale=locale,
        )
        report = await _gen(req)
        return {
            "status": "draft",
            "constitutional_note": "هذا التقرير مسودة — الفاوندر يراجع قبل التسليم",
            "report": report.to_dict(),
            "markdown_ar": report.to_markdown_ar(),
        }
    except Exception as exc:
        log.error("Diagnostic generation failed: %s", exc, exc_info=True)
        raise HTTPException(status_code=500, detail=f"Diagnostic generation failed: {exc}") from exc


@router.get("/diagnostic/list")
async def list_diagnostics() -> dict[str, Any]:
    """List generated diagnostics from local JSONL ledger."""
    ledger_path = "data/proofs/diagnostics.jsonl"
    if not os.path.exists(ledger_path):
        return {"diagnostics": [], "count": 0}

    records = []
    try:
        with open(ledger_path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    records.append(json.loads(line))
    except Exception as exc:
        log.warning("Could not read diagnostics ledger: %s", exc)

    return {"diagnostics": records, "count": len(records)}


# ── Warm Intro ────────────────────────────────────────────────────

@router.post("/warm-intro/draft")
async def draft_warm_intro(payload: dict[str, Any] = Body(default_factory=dict)) -> dict[str, Any]:
    """
    Generate warm intro message drafts for human approval.
    Constitutional: NO_LIVE_SEND — all drafts require founder approval.
    """
    company_name = payload.get("company_name", "").strip()
    if not company_name:
        raise HTTPException(status_code=422, detail="company_name required")

    try:
        from dealix.commercial.warm_intro_generator import ProspectContext, generate_warm_intros

        ctx = ProspectContext(
            company_name=company_name,
            contact_name=payload.get("contact_name", ""),
            sector=payload.get("sector", "other"),
            pain_point=payload.get("pain_point", ""),
            signal=payload.get("signal", ""),
            channel=payload.get("channel", "whatsapp"),
            locale=payload.get("locale", "ar"),
        )
        bundle = await generate_warm_intros(ctx, num_variants=payload.get("num_variants", 5))
        return {
            "status": "pending_approval",
            "constitutional_note": _CONSTITUTIONAL_GATES,
            "bundle": bundle.to_dict(),
        }
    except Exception as exc:
        log.error("Warm intro generation failed: %s", exc, exc_info=True)
        raise HTTPException(status_code=500, detail=str(exc)) from exc


# ── Pilot ─────────────────────────────────────────────────────────

@router.post("/pilot/start")
async def start_pilot(payload: dict[str, Any] = Body(default_factory=dict)) -> dict[str, Any]:
    """
    Start a 499 SAR 7-day proof pilot for a company.
    Constitutional: payment_confirmed must be True (NO_LIVE_CHARGE).
    """
    company_name = payload.get("company_name", "").strip()
    if not company_name:
        raise HTTPException(status_code=422, detail="company_name required")

    payment_confirmed = payload.get("payment_confirmed", False)
    payment_ref = payload.get("payment_ref", "")

    if not payment_confirmed or not payment_ref:
        raise HTTPException(
            status_code=422,
            detail="payment_confirmed=true and payment_ref required (NO_LIVE_CHARGE gate)",
        )

    try:
        from dealix.commercial.pilot_delivery import PilotContext, build_pilot_plan, save_pilot

        ctx = PilotContext(
            pilot_id=str(uuid.uuid4()),
            account_id=payload.get("account_id", str(uuid.uuid4())),
            company_name=company_name,
            contact_name=payload.get("contact_name", ""),
            sector=payload.get("sector", "other"),
            pain_points=payload.get("pain_points", ""),
            amount_sar=float(payload.get("amount_sar", 499.0)),
            payment_ref=payment_ref,
            payment_confirmed=payment_confirmed,
        )
        plan = build_pilot_plan(ctx)
        save_pilot(plan)

        return {
            "status": "started",
            "pilot_id": plan.pilot_id,
            "company": plan.company_name,
            "days_total": 7,
            "plan_markdown_ar": plan.to_markdown_ar(),
            "day_1_brief": {
                "title_ar": plan.days[0].title_ar,
                "tasks_ar": plan.days[0].tasks_ar,
                "deliverable_ar": plan.days[0].deliverable_ar,
            },
        }
    except HTTPException:
        raise
    except Exception as exc:
        log.error("Pilot start failed: %s", exc, exc_info=True)
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.get("/pilot/{pilot_id}/brief")
async def pilot_day_brief(pilot_id: str, day: int = 1) -> dict[str, Any]:
    """Get today's task brief for a running pilot."""
    if not _ID_RE.match(pilot_id):
        raise HTTPException(status_code=422, detail="Invalid pilot_id format")
    pilot_id = os.path.basename(pilot_id)
    # Canonicalise and verify the resolved path stays inside _PILOTS_DIR
    resolved = os.path.realpath(os.path.join(_PILOTS_DIR, pilot_id + ".json"))
    if not resolved.startswith(_PILOTS_DIR + os.sep):
        raise HTTPException(status_code=422, detail="Invalid pilot_id")
    try:
        with open(resolved, encoding="utf-8") as f:
            plan_data = json.load(f)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Pilot not found")

    if day < 1 or day > 7:
        raise HTTPException(status_code=422, detail="day must be 1-7")

    day_data = plan_data["days"][day - 1]
    return {
        "pilot_id": os.path.basename(pilot_id),
        "company": plan_data["company_name"],
        "day": day,
        **day_data,
    }


@router.get("/pilot/{pilot_id}/plan")
async def get_pilot_plan(pilot_id: str) -> dict[str, Any]:
    """Get the full 7-day plan for a pilot."""
    if not _ID_RE.match(pilot_id):
        raise HTTPException(status_code=422, detail="Invalid pilot_id format")
    pilot_id = os.path.basename(pilot_id)
    resolved = os.path.realpath(os.path.join(_PILOTS_DIR, pilot_id + ".json"))
    if not resolved.startswith(_PILOTS_DIR + os.sep):
        raise HTTPException(status_code=422, detail="Invalid pilot_id")
    try:
        with open(resolved, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Pilot not found")


# ── Proof Pack ────────────────────────────────────────────────────

@router.post("/proof/build")
async def build_proof(payload: dict[str, Any] = Body(default_factory=dict)) -> dict[str, Any]:
    """
    Build a proof pack from pilot evidence.
    Constitutional: all metrics must be real (NO_FAKE_PROOF).
    """
    required = ["pilot_id", "account_id", "company_name"]
    missing = [f for f in required if not payload.get(f)]
    if missing:
        raise HTTPException(status_code=422, detail=f"Missing: {missing}")

    try:
        from dealix.commercial.proof_builder import ProofEvidence, build_proof_pack

        evidence = ProofEvidence(
            messages_drafted=int(payload.get("messages_drafted", 0)),
            messages_approved=int(payload.get("messages_approved", 0)),
            messages_sent=int(payload.get("messages_sent", 0)),
            replies_received=int(payload.get("replies_received", 0)),
            meetings_booked=int(payload.get("meetings_booked", 0)),
            deals_created=int(payload.get("deals_created", 0)),
            response_time_before_hours=float(payload.get("response_time_before_hours", 0)),
            response_time_after_hours=float(payload.get("response_time_after_hours", 0)),
            proof_events=payload.get("proof_events", []),
            testimonial_text=payload.get("testimonial_text", ""),
            testimonial_consented=bool(payload.get("testimonial_consented", False)),
        )

        pack = build_proof_pack(
            pilot_id=payload["pilot_id"],
            account_id=payload["account_id"],
            company_name=payload["company_name"],
            contact_name=payload.get("contact_name", ""),
            sector=payload.get("sector", "other"),
            pain_point=payload.get("pain_point", ""),
            evidence=evidence,
        )

        return {
            "status": "built",
            "pack_id": pack.pack_id,
            "evidence_level": pack.evidence_level,
            "evidence_level_name": pack.evidence_level_name,
            "is_complete": pack.is_complete,
            "can_use_as_case_study": pack.can_use_as_case_study,
            "pack": pack.to_dict(),
            "markdown_ar": pack.to_markdown_ar(),
        }
    except Exception as exc:
        log.error("Proof pack build failed: %s", exc, exc_info=True)
        raise HTTPException(status_code=500, detail=str(exc)) from exc


# ── Upsell ────────────────────────────────────────────────────────

@router.post("/upsell/evaluate")
async def evaluate_upsell(payload: dict[str, Any] = Body(default_factory=dict)) -> dict[str, Any]:
    """
    Evaluate upsell opportunities for an account.
    Returns list of eligible and gated offers.
    Constitutional: all results pending_approval.
    """
    account_id = payload.get("account_id", str(uuid.uuid4()))
    company_name = payload.get("company_name", "").strip()
    if not company_name:
        raise HTTPException(status_code=422, detail="company_name required")

    try:
        from dealix.commercial.upsell_engine import evaluate_upsell as _eval

        opportunities = _eval(
            account_id=account_id,
            company_name=company_name,
            sector=payload.get("sector", "other"),
            pain_point=payload.get("pain_point", ""),
            pilot_count=int(payload.get("pilot_count", 0)),
            proof_event_count=int(payload.get("proof_event_count", 0)),
            evidence_level=int(payload.get("evidence_level", 0)),
        )

        eligible = [o.to_dict() for o in opportunities if not o.is_gated]
        gated = [o.to_dict() for o in opportunities if o.is_gated]

        return {
            "account_id": account_id,
            "company_name": company_name,
            "eligible_offers": eligible,
            "gated_offers": gated,
            "constitutional_note": "NO_LIVE_SEND: جميع العروض تتطلب موافقة الفاوندر",
        }
    except Exception as exc:
        log.error("Upsell evaluation failed: %s", exc, exc_info=True)
        raise HTTPException(status_code=500, detail=str(exc)) from exc


# ── Daily Brief ───────────────────────────────────────────────────

@router.get("/daily-brief")
async def daily_brief() -> dict[str, Any]:
    """
    Founder daily brief — pipeline snapshot + top opportunities.
    Called by GitHub Actions at 6 AM Riyadh time daily.
    """
    from datetime import UTC, datetime

    brief: dict[str, Any] = {
        "date": datetime.now(UTC).strftime("%Y-%m-%d"),
        "generated_at": datetime.now(UTC).isoformat(),
        "diagnostics_total": 0,
        "pilots_active": 0,
        "warm_intros_pending": 0,
        "proof_packs_built": 0,
        "top_actions": [],
    }

    # Count diagnostics
    if os.path.exists("data/proofs/diagnostics.jsonl"):
        with open("data/proofs/diagnostics.jsonl") as f:
            brief["diagnostics_total"] = sum(1 for line in f if line.strip())

    # Count pilots
    pilots_dir = "data/pilots"
    if os.path.exists(pilots_dir):
        brief["pilots_active"] = len([f for f in os.listdir(pilots_dir) if f.endswith(".json")])

    # Count warm intros pending
    if os.path.exists("data/outbox/warm_intros.jsonl"):
        with open("data/outbox/warm_intros.jsonl") as f:
            bundles = [json.loads(line) for line in f if line.strip()]
        pending = sum(b.get("pending_approval_count", 0) for b in bundles)
        brief["warm_intros_pending"] = pending

    # Count proof packs
    packs_dir = "data/proof-packs"
    if os.path.exists(packs_dir):
        brief["proof_packs_built"] = len([f for f in os.listdir(packs_dir) if f.endswith(".json")])

    # Generate action recommendations
    actions = []
    if brief["diagnostics_total"] == 0:
        actions.append({"priority": 1, "action_ar": "أرسل أول warm intro وأجرِ أول تشخيص مجاني اليوم", "action_en": "Send first warm intro and run first free diagnostic today"})
    if brief["warm_intros_pending"] > 0:
        actions.append({"priority": 2, "action_ar": f"راجع وأرسل {brief['warm_intros_pending']} رسالة ترحيبية معلّقة", "action_en": f"Review and send {brief['warm_intros_pending']} pending warm intros"})
    if brief["pilots_active"] == 0 and brief["diagnostics_total"] > 0:
        actions.append({"priority": 3, "action_ar": "حوّل أحد التشخيصات إلى برنامج تجريبي مدفوع (499 ريال)", "action_en": "Convert one diagnostic to a paid pilot (499 SAR)"})
    if brief["pilots_active"] > 0 and brief["proof_packs_built"] == 0:
        actions.append({"priority": 4, "action_ar": "أكمل توثيق حدث الإثبات وأنشئ أول طقم إثبات", "action_en": "Complete proof event documentation and build first proof pack"})

    actions.sort(key=lambda a: a["priority"])
    brief["top_actions"] = actions

    return brief
