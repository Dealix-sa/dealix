"""Draft-only queue builder for warm and explicitly approved opportunities."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Iterable

from .models import ClientCard, QueueBundle, QueueItem

DRAFT_ONLY_MODE = "draft-only"
SAFEGUARDS = [
    "warm_inbound_referral_or_explicitly_approved_targets_only",
    "research_only_sources_never_receive_outreach_drafts",
    "founder_review_required",
    "external_execution_disabled",
    "review_before_price_scope_or_delivery_commitment",
    "confirmed_payment_before_revenue_status",
    "proof_required_for_claims",
]


def _angle_for(card: ClientCard) -> str:
    if card.segment == "foreign_market_access":
        return "اختبار دخول السوق السعودي بأقل مخاطرة قبل أي توسع كبير."
    if card.segment == "b2g_readiness":
        return "رفع الجاهزية والملفات والشراكات بدون ادعاء فوز أو وصول حكومي."
    if card.segment == "clinic_or_service":
        return "قياس فجوة الرد والمتابعة قبل اقتراح أي توسع أو أتمتة."
    return "ترتيب الفرص والمتابعة وربط كل خطوة بدليل قابل للمراجعة."


def _priority_reason(card: ClientCard) -> str:
    drivers = {
        "intent": card.intent_score,
        "urgency": card.urgency_score,
        "value": card.value_score,
        "trust": card.trust_score,
    }
    strongest = max(drivers, key=drivers.get)
    permission = "confirmed" if card.contact_permission_confirmed else "research_only"
    return (
        f"score={card.priority_score}; strongest_driver={strongest}; "
        f"risk={card.risk_score}; permission={permission}; "
        f"signal={card.signal or 'not_recorded'}"
    )


def _next_action_for(card: ClientCard) -> str:
    if not card.contact_permission_confirmed:
        return "Verify permission or obtain a warm introduction before drafting outreach."
    if card.priority_score >= 80:
        return "Prepare a one-page evidence-first offer for founder review."
    if card.priority_score >= 60:
        return "Prepare a short value note and verify the decision-maker."
    return "Keep in research hold until a stronger, source-backed signal appears."


def _copy_for(card: ClientCard) -> str:
    if not card.contact_permission_confirmed:
        return ""
    return (
        f"السلام عليكم، أعددت فرضية أولية حول {card.company} مرتبطة بـ"
        f" {card.likely_pain or 'مسار الفرص والمتابعة'}. "
        "إذا كان الموضوع أولوية حالية، أقدر أرسل لقطة من صفحة واحدة توضح الفجوة، "
        "الإجراء التالي، والدليل المطلوب قبل أي التزام."
    )


def _objection_for(card: ClientCard) -> str:
    if not card.contact_permission_confirmed:
        return "Permission or consent has not been established; do not contact yet."
    if card.risk_score >= 60:
        return "Privacy, proof quality, scope boundaries, or permission to use the data."
    if card.intent_score < 50:
        return "Low urgency; avoid a meeting ask and lead with a small evidence snapshot."
    return "Time, price, proof, and how Dealix differs from a CRM."


def _proof_for(card: ClientCard) -> str:
    offer = card.offer_fit.casefold()
    if "market" in offer or "snapshot" in offer:
        return "Source-backed opportunity snapshot with assumptions and confidence levels."
    if "b2g" in offer or "readiness" in offer:
        return "Readiness checklist, capability gaps, and evidence-backed partner map."
    return "Revenue Proof Sprint scope, evidence tracker, approval record, and proof-pack format."


def build_queue(cards: Iterable[ClientCard], mode: str = DRAFT_ONLY_MODE) -> QueueBundle:
    """Build a ranked internal queue; any non-draft mode is rejected."""

    if mode != DRAFT_ONLY_MODE:
        raise ValueError("client acquisition queue only supports draft-only mode")

    items = []
    for card in cards:
        contactable = card.contact_permission_confirmed
        status = "needs_founder_review" if contactable and card.priority_score >= 60 else "research_hold"
        channel = "manual_email_or_linkedin_after_approval" if contactable else "none_research_only"
        items.append(
            QueueItem(
                client=card,
                status=status,
                priority_reason=_priority_reason(card),
                recommended_channel=channel,
                local_angle=_angle_for(card),
                next_action=_next_action_for(card),
                suggested_copy=_copy_for(card),
                objection_to_expect=_objection_for(card),
                proof_to_show=_proof_for(card),
            )
        )

    items.sort(key=lambda item: item.client.priority_score, reverse=True)
    return QueueBundle(
        generated_at=datetime.now(UTC).isoformat(),
        mode=DRAFT_ONLY_MODE,
        items=items,
        safeguards=SAFEGUARDS,
    )


def write_queue_bundle(bundle: QueueBundle, output_path: Path) -> Path:
    """Write one internal JSON artifact without sending or publishing anything."""

    if bundle.mode != DRAFT_ONLY_MODE:
        raise ValueError("refusing to persist a non-draft acquisition bundle")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(bundle.to_dict(), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return output_path
