"""Proposal Factory — turns a qualified prospect into a proposal draft.

Pricing, scope, and duration come from the canonical offers catalog
(os/03_OFFERS.yml) via :mod:`dealix.distribution.offers` — never invented here.
Proposals start ``draft_pending_approval``; there is no contract commitment and
no payment link without an explicit human approval.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from dealix.distribution import offers as offers_mod
from dealix.distribution import sectors as sectors_mod
from dealix.distribution.doctrine import STATUS_PENDING, assert_distribution_safe
from dealix.distribution.ledger import append_record, new_id, now_iso, read_records, update_status
from dealix.distribution.paths import PROPOSALS_LEDGER
from dealix.distribution.prospects import load_prospects

# Prospect statuses eligible for a proposal (must be at least qualified).
ELIGIBLE_STATUSES = {"qualified", "proposal"}


def build_proposal(prospect: dict[str, Any]) -> dict[str, Any]:
    """Build a proposal draft for a prospect (does not persist it)."""
    assert_distribution_safe()
    sector_key = str(prospect.get("sector") or "")
    sector = sectors_mod.get_sector(sector_key) or {}
    offer_ref = str(sector.get("offer_ref") or "ai_workflow_audit")
    offer = offers_mod.get_offer(offer_ref) or {}

    deliverables = offer.get("deliverables") or []
    scope: list[str] = []
    for d in deliverables[:5]:
        if isinstance(d, dict):
            scope.append(str(d.get("name") or d.get("description") or "").strip())
        else:
            scope.append(str(d).strip())
    if not scope:
        scope = [
            "خريطة الـ workflow الحالي ونقاط التسرب",
            "أول workflow متابعة محكوم (موافقة قبل الإرسال)",
            "خطة قياس وProof Pack",
        ]

    company = str(prospect.get("company") or "").strip()
    pain = str(prospect.get("pain_hypothesis") or sector.get("pain") or "").strip()

    return {
        "id": new_id("proposal"),
        "prospect_id": str(prospect.get("id") or ""),
        "company": company,
        "sector": sector_key,
        "offer_ref": offer_ref,
        "problem": pain,
        "scope": [s for s in scope if s],
        "timeline_days": offers_mod.duration_days(offer),
        "price_range_sar": offers_mod.price_range_sar(offer),
        "evidence_level": int(prospect.get("evidence_level") or 1),
        "assumptions": [
            "وصول لأمثلة workflow الحالية وبيانات عينة عند الحاجة",
            "نقطة تواصل واحدة من جانبكم",
        ],
        "risks": [
            "النتائج تعتمد على جودة البيانات والوصول",
            "لا أرقام أو وعود مضمونة — القيمة تُثبت بالـ Proof",
        ],
        "status": STATUS_PENDING,
        "created_at": now_iso(),
    }


def run_generation(
    prospects_path: Path | None = None,
    *,
    ledger: Path | None = None,
) -> dict[str, Any]:
    """Generate proposal drafts for newly-qualified prospects (dedupe per prospect)."""
    led = ledger or PROPOSALS_LEDGER
    prospects = load_prospects(prospects_path)
    existing = read_records(led)
    have = {str(p.get("prospect_id")) for p in existing}
    new_props: list[dict[str, Any]] = []
    for pr in prospects:
        if str(pr.get("status") or "") not in ELIGIBLE_STATUSES:
            continue
        if str(pr.get("id") or "") in have:
            continue
        new_props.append(build_proposal(pr))
    for p in new_props:
        append_record(led, p)
    return {
        "prospects": len(prospects),
        "eligible": sum(1 for p in prospects if str(p.get("status") or "") in ELIGIBLE_STATUSES),
        "new_proposals": len(new_props),
        "ids": [p["id"] for p in new_props],
    }


def approve_proposal(proposal_id: str, ledger: Path | None = None) -> dict[str, Any] | None:
    return update_status(ledger or PROPOSALS_LEDGER, proposal_id, "approved")


def all_proposals(ledger: Path | None = None) -> list[dict[str, Any]]:
    return read_records(ledger or PROPOSALS_LEDGER)


__all__ = [
    "ELIGIBLE_STATUSES",
    "all_proposals",
    "approve_proposal",
    "build_proposal",
    "run_generation",
]
