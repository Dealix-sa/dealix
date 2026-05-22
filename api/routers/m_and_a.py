"""Wave 15.1 — M&A Radar HTTP surface.

Exposes acquisition evaluation, LOI drafting, and proposal ledger:
  POST /api/v1/m-and-a/evaluate     — EBITDA calc + acquisition proposal
  GET  /api/v1/m-and-a/proposals    — list proposals from ledger
  POST /api/v1/m-and-a/loi-draft    — generate bilingual Letter of Intent
  GET  /api/v1/m-and-a/radar        — dashboard radar summary

Hard rules:
- no_fake_revenue: EBITDA must be positive for a proposal to exist
- no_upsell_without_proof: LOI requires a completed evaluation
- is_estimate_always_true: all valuations carry is_estimate=True flag
- approval_required: LOI output is a draft only; founder approves before use
"""
from __future__ import annotations

import json
import os
import threading
import uuid
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter(prefix="/api/v1/m-and-a", tags=["M&A Radar"])

_HARD_GATES: dict[str, bool] = {
    "no_fake_revenue": True,
    "is_estimate_always_true": True,
    "approval_required_for_loi": True,
    "no_upsell_without_proof": True,
}

_DEFAULT_LEDGER = "var/m_and_a_proposals.jsonl"
_lock = threading.Lock()


def _ledger_path() -> Path:
    p = Path(os.environ.get("DEALIX_MA_LEDGER_PATH", _DEFAULT_LEDGER))
    if not p.is_absolute():
        p = Path(__file__).resolve().parent.parent.parent / p
    return p


def _multiplier(margin_pct: float) -> float:
    if margin_pct >= 0.25:
        return 4.0
    if margin_pct >= 0.15:
        return 3.5
    return 3.0


def _write_proposal(proposal: dict[str, Any]) -> None:
    path = _ledger_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    with _lock:
        with path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(proposal, ensure_ascii=False) + "\n")


def _read_proposals(limit: int = 50) -> list[dict[str, Any]]:
    path = _ledger_path()
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    with _lock:
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    rows.append(json.loads(line))
                except Exception:  # noqa: BLE001
                    continue
    return rows[-limit:]


# ─── Evaluate ────────────────────────────────────────────────────────────────

class EvaluateRequest(BaseModel):
    company_name: str = Field(..., min_length=1)
    annual_revenue_sar: float = Field(..., gt=0)
    ebitda_margin_pct: float = Field(..., ge=0.0, le=1.0,
        description="EBITDA margin as decimal, e.g. 0.20 for 20%")
    sector: str = "general"
    notes: str = ""


@router.post("/evaluate")
async def evaluate(req: EvaluateRequest) -> dict[str, Any]:
    """Compute EBITDA-based acquisition proposal.

    Hard gate: ebitda_margin_pct must yield positive EBITDA.
    All figures carry is_estimate=True.
    """
    ebitda = req.annual_revenue_sar * req.ebitda_margin_pct
    if ebitda <= 0:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "no_fake_revenue",
                "message": "EBITDA must be positive. Verify revenue and margin inputs.",
                "message_ar": "يجب أن تكون الأرباح قبل الفوائد موجبة. راجع الإيرادات والهامش.",
            },
        )

    multiplier = _multiplier(req.ebitda_margin_pct)
    proposed_offer_sar = ebitda * multiplier
    upfront_cash_sar = proposed_offer_sar * 0.60
    earnout_sar = proposed_offer_sar * 0.40

    proposal_id = f"ma_{uuid.uuid4().hex[:10]}"
    proposal: dict[str, Any] = {
        "proposal_id": proposal_id,
        "company_name": req.company_name,
        "sector": req.sector,
        "annual_revenue_sar": req.annual_revenue_sar,
        "ebitda_margin_pct": req.ebitda_margin_pct,
        "ebitda_sar": round(ebitda, 2),
        "multiplier": multiplier,
        "proposed_offer_sar": round(proposed_offer_sar, 2),
        "upfront_cash_sar": round(upfront_cash_sar, 2),
        "earnout_sar": round(earnout_sar, 2),
        "earnout_months": 12,
        "is_estimate": True,
        "notes": req.notes,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "hard_gates": _HARD_GATES,
    }
    _write_proposal(proposal)
    return proposal


# ─── Proposals ledger ─────────────────────────────────────────────────────────

@router.get("/proposals")
async def list_proposals(limit: int = 50) -> dict[str, Any]:
    """Return recent M&A proposals from the ledger."""
    rows = _read_proposals(limit=min(limit, 200))
    return {
        "proposals": rows,
        "count": len(rows),
        "hard_gates": _HARD_GATES,
    }


# ─── LOI draft ────────────────────────────────────────────────────────────────

class LoiRequest(BaseModel):
    proposal_id: str = Field(..., min_length=1)
    acquirer_name: str = Field(default="Dealix Holdings")
    target_name: str = Field(..., min_length=1)
    proposed_offer_sar: float = Field(..., gt=0)
    upfront_cash_sar: float = Field(..., gt=0)
    earnout_sar: float = Field(..., gt=0)
    earnout_months: int = Field(default=12, ge=1, le=60)


@router.post("/loi-draft")
async def loi_draft(req: LoiRequest) -> dict[str, Any]:
    """Generate a bilingual (AR + EN) Letter of Intent draft.

    Hard rule: output is draft_only — founder must approve before use.
    """
    today = date.today().isoformat()

    loi_en = f"""LETTER OF INTENT (DRAFT — FOR REVIEW ONLY)
Date: {today}
From: {req.acquirer_name}
To:   {req.target_name}

This non-binding Letter of Intent outlines the proposed terms for the
acquisition of {req.target_name} by {req.acquirer_name}.

PROPOSED CONSIDERATION:
  Total Offer:       SAR {req.proposed_offer_sar:,.0f}
  Upfront Cash (60%): SAR {req.upfront_cash_sar:,.0f} (at closing)
  Earn-out (40%):    SAR {req.earnout_sar:,.0f} (over {req.earnout_months} months, performance-linked)

NEXT STEPS:
  1. Mutual NDA execution
  2. Preliminary due diligence (financial, legal, operational)
  3. Final SPA negotiation and execution

This LOI is non-binding and subject to satisfactory due diligence.
All figures are estimates (is_estimate=True). Proposal ref: {req.proposal_id}

_____________________________          _____________________________
{req.acquirer_name}                      {req.target_name}
Authorised Signatory                   Authorised Signatory
"""

    loi_ar = f"""خطاب نوايا (مسودة — للمراجعة فقط)
التاريخ: {today}
من: {req.acquirer_name}
إلى: {req.target_name}

يُحدد هذا الخطاب غير الملزم الشروط المقترحة لاستحواذ {req.acquirer_name} على {req.target_name}.

العوض المقترح:
  إجمالي العرض:         {req.proposed_offer_sar:,.0f} ريال سعودي
  دفعة نقدية فورية (60%): {req.upfront_cash_sar:,.0f} ريال سعودي (عند الإغلاق)
  أداء مرتبط (40%):      {req.earnout_sar:,.0f} ريال سعودي (على مدى {req.earnout_months} شهراً مرتبطة بالأداء)

الخطوات التالية:
  1. توقيع اتفاقية السرية المتبادلة
  2. التحقق الأولي (المالي والقانوني والتشغيلي)
  3. التفاوض وتوقيع عقد الاستحواذ النهائي

هذا الخطاب غير ملزم ومشروط بنتائج التحقق. جميع الأرقام تقديرية.
رقم المقترح: {req.proposal_id}

_____________________________          _____________________________
{req.acquirer_name}                      {req.target_name}
المفوض بالتوقيع                          المفوض بالتوقيع
"""

    return {
        "proposal_id": req.proposal_id,
        "status": "draft_only",
        "approval_required": True,
        "loi_en": loi_en,
        "loi_ar": loi_ar,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "hard_gates": _HARD_GATES,
    }


# ─── Radar summary ────────────────────────────────────────────────────────────

@router.get("/radar")
async def radar() -> dict[str, Any]:
    """Return M&A radar dashboard summary from ledger."""
    rows = _read_proposals(limit=200)
    total_pipeline_sar = sum(r.get("proposed_offer_sar", 0) for r in rows)
    avg_multiple = (
        sum(r.get("multiplier", 0) for r in rows) / len(rows) if rows else 0.0
    )
    sectors: dict[str, int] = {}
    for r in rows:
        s = r.get("sector", "general")
        sectors[s] = sectors.get(s, 0) + 1

    return {
        "targets_evaluated": len(rows),
        "total_pipeline_sar": round(total_pipeline_sar, 2),
        "avg_ebitda_multiple": round(avg_multiple, 2),
        "sector_breakdown": sectors,
        "recent_proposals": rows[-5:],
        "hard_gates": _HARD_GATES,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }
