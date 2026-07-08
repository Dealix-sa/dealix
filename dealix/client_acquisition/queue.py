"""Queue builder for Dealix client acquisition work.

The builder converts manually supplied or warm signals into ranked review items.
It writes internal files only.
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Iterable

from .models import ClientCard, QueueBundle, QueueItem

SAFEGUARDS = [
    "founder_review_required",
    "review_before_external_action",
    "review_before_price_or_scope_commitment",
    "confirmed_payment_before_revenue_status",
    "proof_required_for_claims",
]


def _angle_for(card: ClientCard) -> str:
    if card.segment == "foreign_market_access":
        return "اختبار دخول السوق السعودي بأقل مخاطرة قبل التوسع الكبير."
    if card.segment == "b2g_readiness":
        return "جاهزية ملفات وفرص وشركاء بدون وعود فوز."
    if card.segment == "clinic_or_service":
        return "تقليل ضياع الاستفسارات والمتابعة اليومية مع تقرير واضح."
    return "ترتيب الفرص والمتابعة وتحويل الاهتمام إلى خطوة عملية قابلة للقياس."


def _next_action_for(card: ClientCard) -> str:
    if card.priority_score >= 80:
        return "Prepare one-page offer and review note."
    if card.priority_score >= 60:
        return "Prepare short value note and reminder."
    return "Keep in research queue until a stronger signal appears."


def _copy_for(card: ClientCard) -> str:
    company = card.company or "شركتكم"
    return (
        f"السلام عليكم، لاحظت أن {company} قد تستفيد من ترتيب الفرص والمتابعة بشكل أوضح. "
        "Dealix يساعد على بناء قائمة فرص، مسودات متابعة، وتقرير أسبوعي مختصر: ماذا حدث، ماذا نتابع، وما الأقرب للإغلاق. "
        "نبدأ بتجربة صغيرة بدون تغيير أنظمتكم الحالية."
    )


def _objection_for(card: ClientCard) -> str:
    if card.risk_score >= 60:
        return "Will likely ask for proof, privacy controls, or clearer scope."
    if card.intent_score < 50:
        return "May not see urgency yet; lead with a small snapshot."
    return "May ask about time, cost, and how this differs from a CRM."


def _proof_for(card: ClientCard) -> str:
    if "snapshot" in card.offer_fit.lower():
        return "Sample Saudi opportunity snapshot and source-backed lead map."
    if "diagnostic" in card.offer_fit.lower():
        return "Diagnostic scope, evidence tracker, and proof-pack checklist."
    return "Revenue Proof Sprint outline, review gate, and proof-pack format."


def build_queue(cards: Iterable[ClientCard], mode: str = "draft-only") -> QueueBundle:
    items = []
    for card in cards:
        items.append(
            QueueItem(
                client=card,
                status="needs_founder_review" if card.priority_score >= 60 else "research_hold",
                recommended_channel="email_or_linkedin_manual",
                local_angle=_angle_for(card),
                next_action=_next_action_for(card),
                suggested_copy=_copy_for(card),
                objection_to_expect=_objection_for(card),
                proof_to_show=_proof_for(card),
                approval_required=True,
            )
        )
    items.sort(key=lambda item: item.client.priority_score, reverse=True)
    return QueueBundle(
        generated_at=datetime.now(UTC).isoformat(),
        mode=mode,
        items=items,
        safeguards=SAFEGUARDS,
    )


def write_queue_bundle(bundle: QueueBundle, output_path: Path) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(bundle.to_dict(), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return output_path
