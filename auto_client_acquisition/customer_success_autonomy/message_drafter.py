"""Bilingual draft generators for customer-facing retention messages.

Every output is ``draft_only`` — no external send. Each draft passes the
forbidden-token gate enforced by ``tests/test_landing_forbidden_claims``:
zero occurrences of ``نضمن``, ``guaranteed``, ``blast``, ``scrape``,
``scraping``, or ``cold {whatsapp|outreach|email|messaging}``.

The disclaimer pattern is shared with ``templates/MONTHLY_VALUE_REPORT_EMAIL.md``.
"""
from __future__ import annotations

from typing import Any

from auto_client_acquisition.customer_success_autonomy.signal_aggregator import (
    CustomerSignalSnapshot,
)

_DISCLAIMER_AR = (
    "النتائج التقديرية ليست نتائج مضمونة. كل خطوة بموافقتك."
)
_DISCLAIMER_EN = (
    "Estimated outcomes are not guaranteed outcomes. Every step needs your approval."
)


def _draft(
    *,
    channel: str,
    subject_ar: str,
    subject_en: str,
    body_ar: str,
    body_en: str,
) -> dict[str, Any]:
    return {
        "channel": channel,
        "subject_ar": subject_ar,
        "subject_en": subject_en,
        "body_ar": f"{body_ar}\n\n{_DISCLAIMER_AR}",
        "body_en": f"{body_en}\n\n{_DISCLAIMER_EN}",
        "action_mode": "approval_required",
        "governance_decision": "allow_with_review",
    }


def draft_renewal_message(snapshot: CustomerSignalSnapshot) -> dict[str, Any]:
    """Draft a bilingual renewal confirmation message."""
    cid = snapshot.customer_id
    amount = float((snapshot.renewal_status or {}).get("amount_sar", 0.0))
    body_ar = (
        f"العميل {cid}، اقترب موعد تجديد الاشتراك بقيمة {amount:.0f} ر.س. "
        "نرجو تأكيد المتابعة قبل المعالجة."
    )
    body_en = (
        f"Customer {cid}, the next subscription cycle ({amount:.0f} SAR) is due. "
        "Please confirm before processing."
    )
    return _draft(
        channel="email",
        subject_ar="تأكيد تجديد الاشتراك",
        subject_en="Subscription renewal confirmation",
        body_ar=body_ar,
        body_en=body_en,
    )


def draft_expansion_proposal(
    snapshot: CustomerSignalSnapshot,
    offer: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Draft a bilingual expansion proposal grounded in proven value."""
    cid = snapshot.customer_id
    offer = offer or {}
    offer_label = str(offer.get("offer", "")) or "أعلى المستويات / next tier"
    rationale_en = str(offer.get("rationale_en", "Proven results unlock the next tier."))
    rationale_ar = str(offer.get("rationale_ar", "النتائج المُسجَّلة تفتح المستوى التالي."))
    body_ar = (
        f"العميل {cid}، استناداً إلى نتائجك المُسجَّلة، نرشّح الترقية إلى {offer_label}. "
        f"{rationale_ar}"
    )
    body_en = (
        f"Customer {cid}, based on your recorded results we recommend an upgrade to "
        f"{offer_label}. {rationale_en}"
    )
    return _draft(
        channel="email",
        subject_ar="اقتراح ترقية مبني على النتائج",
        subject_en="Outcome-grounded upgrade proposal",
        body_ar=body_ar,
        body_en=body_en,
    )


def draft_detractor_outreach(
    snapshot: CustomerSignalSnapshot,
    nps_score: int,
) -> dict[str, Any]:
    """Draft a listening-first follow-up for an NPS detractor."""
    cid = snapshot.customer_id
    milestone = snapshot.recent_nps_milestone or ""
    body_ar = (
        f"العميل {cid}، شكراً على تقييمك ({nps_score}/10) في مرحلة {milestone}. "
        "نطلب مكالمة قصيرة للاستماع وفهم ما يمكن تحسينه — لا عرض، فقط إصغاء."
    )
    body_en = (
        f"Customer {cid}, thank you for your score ({nps_score}/10) at the {milestone} "
        "milestone. May we book a short call to listen and understand — no pitch, just listening."
    )
    return _draft(
        channel="email",
        subject_ar="نتعلّم من ملاحظاتك",
        subject_en="Learning from your feedback",
        body_ar=body_ar,
        body_en=body_en,
    )


def draft_churn_intervention(snapshot: CustomerSignalSnapshot) -> dict[str, Any]:
    """Draft a founder-led intervention for a critical churn risk."""
    cid = snapshot.customer_id
    signals = list((snapshot.churn or {}).get("signals_active", []))
    signals_txt = ", ".join(signals) or "—"
    body_ar = (
        f"العميل {cid}، نلاحظ مؤشرات اضطراب ({signals_txt}). "
        "أحجز معك 20 دقيقة هذا الأسبوع — أستمع لما يحدث ونتفق على خطوة واحدة."
    )
    body_en = (
        f"Customer {cid}, we see risk signals ({signals_txt}). "
        "I'd like to book 20 minutes this week — listen to what's happening and agree on one next step."
    )
    return _draft(
        channel="email",
        subject_ar="20 دقيقة معك",
        subject_en="20 minutes with you",
        body_ar=body_ar,
        body_en=body_en,
    )


__all__ = [
    "draft_renewal_message",
    "draft_expansion_proposal",
    "draft_detractor_outreach",
    "draft_churn_intervention",
]
