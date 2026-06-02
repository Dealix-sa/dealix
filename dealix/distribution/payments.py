"""Payment Handoff — a draft instruction for the founder to collect payment.

The OS **never** creates, sends, or charges a payment link. It produces a
``draft_pending_approval`` handoff (``approval_required = true``) that tells the
founder the amount + suggested provider; the founder issues the Moyasar link (or
manual invoice) manually. Handoffs are created only from **approved** proposals.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from dealix.distribution import offers as offers_mod
from dealix.distribution.doctrine import STATUS_PENDING, assert_distribution_safe, channel_allows
from dealix.distribution.ledger import append_record, new_id, now_iso, read_records, update_status
from dealix.distribution.paths import PAYMENTS_LEDGER, PROPOSALS_LEDGER


def _amount_from_offer(offer_ref: str) -> float:
    offer = offers_mod.get_offer(offer_ref) or {}
    block = offer.get("price_sar") or offer.get("price_sar_monthly") or {}
    val = block.get("typical") or block.get("min") or 0
    try:
        return float(val)
    except (TypeError, ValueError):
        return 0.0


def build_payment_handoff(proposal: dict[str, Any]) -> dict[str, Any]:
    """Build a payment-handoff draft from an approved proposal."""
    # Defense in depth: a payment link is never auto-sent.
    assert_distribution_safe(request_external_send_without_approval=False)
    assert channel_allows("proposal", "payment_handoff_draft")

    offer_ref = str(proposal.get("offer_ref") or "")
    amount = _amount_from_offer(offer_ref)
    return {
        "id": new_id("pay"),
        "proposal_id": str(proposal.get("id") or ""),
        "company": str(proposal.get("company") or "").strip(),
        "amount_sar": amount,
        "currency": "SAR",
        "payment_provider": "moyasar",
        "approval_required": True,
        "status": STATUS_PENDING,
        "notes": (
            "مسودة تسليم دفع — المؤسس ينشئ رابط Moyasar أو فاتورة يدوية بنفسه بعد الموافقة. "
            "لا إنشاء/إرسال رابط دفع تلقائيًا."
        ),
        "created_at": now_iso(),
    }


def run_generation(
    *,
    proposals: list[dict[str, Any]] | None = None,
    proposals_ledger: Path | None = None,
    ledger: Path | None = None,
) -> dict[str, Any]:
    """Create handoff drafts for approved proposals without one (dedupe per proposal)."""
    led = ledger or PAYMENTS_LEDGER
    props = (
        proposals if proposals is not None else read_records(proposals_ledger or PROPOSALS_LEDGER)
    )
    existing = read_records(led)
    have = {str(p.get("proposal_id")) for p in existing}
    new_items: list[dict[str, Any]] = []
    for prop in props:
        if str(prop.get("status") or "") != "approved":
            continue
        if str(prop.get("id") or "") in have:
            continue
        new_items.append(build_payment_handoff(prop))
    for h in new_items:
        append_record(led, h)
    return {
        "approved_proposals": sum(1 for p in props if str(p.get("status") or "") == "approved"),
        "new_handoffs": len(new_items),
        "ids": [h["id"] for h in new_items],
        "policy": "no_auto_send_payment_link",
    }


def approve_handoff(handoff_id: str, ledger: Path | None = None) -> dict[str, Any] | None:
    return update_status(ledger or PAYMENTS_LEDGER, handoff_id, "approved")


def all_handoffs(ledger: Path | None = None) -> list[dict[str, Any]]:
    return read_records(ledger or PAYMENTS_LEDGER)


__all__ = [
    "all_handoffs",
    "approve_handoff",
    "build_payment_handoff",
    "run_generation",
]
