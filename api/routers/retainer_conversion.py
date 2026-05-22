"""Wave 17.0 — Retainer Conversion Engine HTTP surface.

Detects Sprint -> Retainer upgrade signals and queues founder approval tasks.

Hard gates:
  - no_upsell_without_proof: NEVER recommend upgrade without proof_events_completed >= 1
  - no_auto_execute_offer: ALL conversion actions are draft_only, queued for founder approval
  - is_estimate_always_true: all scores carry is_estimate=True
"""
from __future__ import annotations

import json
import os
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(
    prefix="/api/v1/retainer-conversion",
    tags=["Wave 17 — Retainer Conversion Engine"],
)

_HARD_GATES: dict[str, bool] = {
    "no_upsell_without_proof": True,
    "no_auto_execute_offer": True,
    "is_estimate_always_true": True,
    "approval_required_for_external_actions": True,
}

_DEFAULT_LEDGER_PATH = "var/retainer_conversions.jsonl"
_lock = threading.Lock()


def _ledger_path() -> Path:
    p = Path(os.environ.get("DEALIX_RETAINER_CONVERSIONS_PATH", _DEFAULT_LEDGER_PATH))
    if not p.is_absolute():
        p = Path(__file__).resolve().parent.parent.parent / p
    return p


def _ensure_dir(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


# ─────────────────────────────────────────────────────────────────────
# Pydantic models
# ─────────────────────────────────────────────────────────────────────


class RetainerEligibilityRequest(BaseModel):
    customer_id: str
    current_tier: str = "sprint_499"  # sprint_499, data_pack_1500
    months_as_customer: int = 0
    proof_events_completed: int = 0
    monthly_engagement_drop_pct: float = 0.0  # 0..1
    nps: int | None = None
    pipeline_added_drop_pct: float = 0.0  # 0..1
    churn_band: str = "safe"  # safe, watch, at_risk, critical
    arr_so_far_sar: float = 0.0


class BatchEligibilityRequest(BaseModel):
    customers: list[RetainerEligibilityRequest]


class ConversionOutreachRequest(RetainerEligibilityRequest):
    founder_name: str = "المؤسس"
    retainer_tier_sar: int = 2999  # 2999, 3999, or 4999


class ConversionLogRequest(BaseModel):
    customer_id: str
    from_tier: str
    to_tier: str
    retainer_sar_per_month: int
    proof_events_count: int
    founder_approved: bool = False
    notes: str = ""


# ─────────────────────────────────────────────────────────────────────
# Pure-function business logic
# ─────────────────────────────────────────────────────────────────────


def _signal_rank(signal: str) -> int:
    """Return sort key: strong_signal=0, potential=1, anything else=2."""
    return {"strong_signal": 0, "potential": 1}.get(signal, 2)


def _check_eligibility(body: RetainerEligibilityRequest) -> dict[str, Any]:
    """Core eligibility logic — pure function, no I/O.

    Hard gate (no_upsell_without_proof): returns signal='blocked' when
    proof_events_completed < 1. This check runs before every other gate.
    """
    if body.proof_events_completed < 1:
        return {
            "customer_id": body.customer_id,
            "eligible": False,
            "signal": "blocked",
            "reason": "no_proof_events — no_upsell_without_proof gate",
            "recommended_retainer_sar": None,
            "proof_gate_passed": False,
            "months_as_customer": body.months_as_customer,
            "churn_band": body.churn_band,
            "is_estimate": True,
        }

    eligible = (
        body.months_as_customer >= 2
        and body.churn_band != "critical"
        and body.monthly_engagement_drop_pct < 0.3
        and body.current_tier in ("sprint_499", "data_pack_1500")
    )

    signal = "no_signal"
    if eligible:
        nps_ok = body.nps is not None and body.nps >= 7
        pipeline_ok = body.pipeline_added_drop_pct < 0.2
        strong = (nps_ok or pipeline_ok) and body.months_as_customer >= 3
        signal = "strong_signal" if strong else "potential"

    recommended_retainer_sar: int | None = None
    if eligible:
        recommended_retainer_sar = 2999
        if body.arr_so_far_sar >= 3000:
            recommended_retainer_sar = 3999
        if body.arr_so_far_sar >= 5000:
            recommended_retainer_sar = 4999

    return {
        "customer_id": body.customer_id,
        "eligible": eligible,
        "signal": signal,
        "recommended_retainer_sar": recommended_retainer_sar,
        "proof_gate_passed": body.proof_events_completed >= 1,
        "months_as_customer": body.months_as_customer,
        "churn_band": body.churn_band,
        "is_estimate": True,
    }


# ─────────────────────────────────────────────────────────────────────
# Endpoints
# ─────────────────────────────────────────────────────────────────────


@router.post("/check-eligibility")
async def check_eligibility(body: RetainerEligibilityRequest) -> dict[str, Any]:
    """Evaluate whether a customer is ready for a Sprint -> Retainer conversion.

    Hard gate: no_upsell_without_proof — if proof_events_completed < 1, the
    response is blocked regardless of all other signals.
    """
    return _check_eligibility(body)


@router.post("/batch-check")
async def batch_check(body: BatchEligibilityRequest) -> dict[str, Any]:
    """Run eligibility check on up to 100 customers, sorted by signal strength.

    Returns aggregate counts and a sorted result list (strong_signal first).
    """
    if len(body.customers) > 100:
        raise HTTPException(
            status_code=422,
            detail="batch_check: maximum 100 customers per request",
        )

    results = [_check_eligibility(c) for c in body.customers]
    results.sort(key=lambda r: _signal_rank(r["signal"]))

    strong = sum(1 for r in results if r["signal"] == "strong_signal")
    potential = sum(1 for r in results if r["signal"] == "potential")
    blocked = sum(1 for r in results if r["signal"] == "blocked")

    return {
        "total": len(results),
        "strong_signals": strong,
        "potential": potential,
        "blocked_no_proof": blocked,
        "results": results,
        "is_estimate": True,
    }


@router.post("/draft-outreach")
async def draft_outreach(body: ConversionOutreachRequest) -> dict[str, Any]:
    """Generate a bilingual retainer upgrade outreach draft — NEVER auto-sent.

    Hard gate (no_upsell_without_proof): blocked if proof_events_completed < 1.
    Hard gate (no_auto_execute_offer): draft_only=True always; approval_required=True.
    """
    eligibility = _check_eligibility(body)

    if not eligibility["eligible"]:
        return {
            "customer_id": body.customer_id,
            "eligible": False,
            "draft_ar": None,
            "draft_en": None,
            "retainer_sar": None,
            "draft_only": True,
            "approval_required": True,
            "reason": eligibility.get("reason", "not_eligible"),
            "signal": eligibility["signal"],
            "is_estimate": True,
        }

    retainer_sar = body.retainer_tier_sar
    months = body.months_as_customer
    proof_events = body.proof_events_completed
    benefits_ar = "بناء pipeline مستمر، حزم إثبات شهرية، دعم عمليات مخصص"
    benefits_en = "continuous pipeline building, monthly proof packs, dedicated ops support"

    draft_ar = (
        f"مرحباً،\n\n"
        f"لقد كنت تستخدم خدماتنا لـ {months} أشهر وحققنا معاً نتائج ملموسة.\n"
        f"بناءً على نتائجكم، نقترح الانتقال إلى خطة الرعاية الشهرية بـ {retainer_sar} ريال/شهر.\n"
        f"هذا يمنحكم: {benefits_ar}\n\n"
        f"للمناقشة، نرجو التواصل مع فريقنا.\n\n"
        f"(draft_only=True — مراجعة المؤسس مطلوبة قبل الإرسال)"
    )

    draft_en = (
        f"Based on {months} months of work together and {proof_events} completed deliverables,\n"
        f"we'd like to propose upgrading to our {retainer_sar} SAR/mo Managed Growth Ops retainer.\n"
        f"This unlocks: {benefits_en}.\n\n"
        f"(draft_only=True — founder review required before sending)"
    )

    return {
        "customer_id": body.customer_id,
        "eligible": True,
        "draft_ar": draft_ar,
        "draft_en": draft_en,
        "retainer_sar": retainer_sar,
        "draft_only": True,
        "approval_required": True,
        "is_estimate": True,
    }


@router.get("/conversion-playbook")
async def conversion_playbook() -> dict[str, Any]:
    """Return the static retainer conversion playbook and governance rules."""
    return {
        "playbook": {
            "trigger_conditions": [
                "proof_events_completed >= 1 (hard gate — no_upsell_without_proof)",
                "months_as_customer >= 2",
                "churn_band != 'critical'",
                "current_tier in ('sprint_499', 'data_pack_1500')",
                "monthly_engagement_drop_pct < 0.3",
            ],
            "signal_levels": {
                "strong_signal": "NPS>=7 + >=3 months + proof completed -> immediate proposal",
                "potential": "2+ months + proof + healthy engagement -> proposal next touchpoint",
                "blocked_no_proof": "Deliver proof event first — no_upsell_without_proof gate",
            },
            "retainer_tiers": [
                {
                    "tier": "Managed Growth Ops Base",
                    "sar_per_month": 2999,
                    "threshold_arr": 0,
                },
                {
                    "tier": "Managed Growth Ops Pro",
                    "sar_per_month": 3999,
                    "threshold_arr": 3000,
                },
                {
                    "tier": "Managed Growth Ops Elite",
                    "sar_per_month": 4999,
                    "threshold_arr": 5000,
                },
            ],
            "governance": {
                "no_upsell_without_proof": (
                    "All conversion actions blocked if proof_events_completed < 1"
                ),
                "no_auto_execute_offer": (
                    "Outreach drafts require founder approval — never auto-sent"
                ),
            },
        },
        "is_estimate": False,
    }


@router.post("/log-conversion")
async def log_conversion(body: ConversionLogRequest) -> dict[str, Any]:
    """Append a confirmed retainer conversion to the ledger.

    Hard gate (no_auto_execute_offer): founder_approved must be True.
    """
    if not body.founder_approved:
        raise HTTPException(
            status_code=422,
            detail=(
                "no_auto_execute_offer: founder_approved must be True "
                "before logging conversion"
            ),
        )

    timestamp = datetime.now(timezone.utc).isoformat()
    record = {
        "customer_id": body.customer_id,
        "from_tier": body.from_tier,
        "to_tier": body.to_tier,
        "retainer_sar_per_month": body.retainer_sar_per_month,
        "proof_events_count": body.proof_events_count,
        "founder_approved": body.founder_approved,
        "notes": body.notes,
        "timestamp": timestamp,
    }

    path = _ledger_path()
    _ensure_dir(path)
    with _lock:
        with path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    return {
        "logged": True,
        "customer_id": body.customer_id,
        "from_tier": body.from_tier,
        "to_tier": body.to_tier,
        "retainer_sar_per_month": body.retainer_sar_per_month,
        "timestamp": timestamp,
        "is_estimate": False,
    }
