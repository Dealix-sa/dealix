"""Decision engine — the 'brain'. For each deal it decides the next-best action,
drafts the artifact that action needs, and marks whether a human must approve
before anything leaves the building."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Any

from . import pipeline
from .schemas import Deal, DealStage


@dataclass
class Recommendation:
    deal_id: str
    account_name: str
    stage: str
    score: float
    action: str
    action_type: str          # internal | approval
    requires_approval: bool
    draft: str = ""
    rationale: str = ""
    stalled: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "deal_id": self.deal_id,
            "account_name": self.account_name,
            "stage": self.stage,
            "score": self.score,
            "action": self.action,
            "action_type": self.action_type,
            "requires_approval": self.requires_approval,
            "draft": self.draft,
            "rationale": self.rationale,
            "stalled": self.stalled,
        }


def _outreach_draft(deal: Deal) -> str:
    return (
        f"مرحباً {deal.account_name}،\n"
        "لاحظنا أن كثير من شركات B2B في السوق السعودي تفقد إيرادات بسبب ضعف "
        "المتابعة لا بسبب نقص الطلب.\n"
        f"نقترح {deal.offer} بـ {deal.value_sar} ريال: نحلّل تسريب إيراد واحد "
        "ونعطيك خطة إغلاق قابلة للتطبيق خلال أيام.\n"
        "الهدف هو إثبات القيمة أولاً ثم نقيس النتيجة معاً.\n"
        "— مسودة للمراجعة قبل الإرسال —"
    )


def _followup_draft(deal: Deal, days: int) -> str:
    return (
        f"متابعة لطيفة مع {deal.account_name} (بدون إلحاح).\n"
        f"مضى {days} يوم منذ آخر تواصل. نذكّر بقيمة {deal.offer} ونسأل إن كان "
        "التوقيت مناسب لمكالمة 15 دقيقة.\n"
        "— مسودة للمراجعة قبل الإرسال —"
    )


def _proposal_draft(deal: Deal) -> str:
    return (
        f"مسودة عرض/فاتورة لـ {deal.account_name} — {deal.offer} ({deal.value_sar} ريال).\n"
        "النطاق: تشخيص تسريب إيراد واحد + خطة إغلاق + Proof Pack.\n"
        "الدفع يدوي بعد موافقة المؤسس. لا فوترة تلقائية ولا خصم تلقائي.\n"
        "— مسودة للمراجعة قبل الإصدار —"
    )


# stage -> (action label, action_type, requires_approval, draft builder, rationale)
def recommend(deal: Deal, today: date) -> Recommendation:
    stage = deal.stage
    days = deal.days_since_touch(today)
    stalled = pipeline.is_stalled(deal, today)

    action = "Review"
    action_type = "internal"
    requires_approval = False
    draft = ""
    rationale = ""

    if stage == DealStage.LOST:
        action, rationale = "Archive (lost)", "Terminal — no further action."
        action_type = "internal"
    elif stage == DealStage.NEW:
        if not deal.opted_in:
            action = "Confirm opt-in before any outreach"
            rationale = "Lead is not opted-in; do not contact until it is warm/opted-in."
            action_type = "internal"
        else:
            action = "Send first outreach (draft ready)"
            action_type = "approval"
            requires_approval = True
            draft = _outreach_draft(deal)
            rationale = "Warm lead awaiting first touch."
    elif stage == DealStage.CONTACTED:
        action = "Follow up / book a call (draft ready)"
        action_type = "approval"
        requires_approval = True
        draft = _followup_draft(deal, days)
        rationale = f"Contacted {days}d ago; nudge toward a call."
    elif stage == DealStage.ENGAGED:
        action = "Send proposal + manual invoice draft"
        action_type = "approval"
        requires_approval = True
        draft = _proposal_draft(deal)
        rationale = "Call booked — convert to a proposal."
    elif stage == DealStage.PROPOSED:
        action = "Follow up on invoice; take manual payment when confirmed"
        action_type = "approval"
        requires_approval = True
        draft = _followup_draft(deal, days)
        rationale = "Invoice sent — close the payment (manual, no auto-charge)."
    elif stage == DealStage.WON:
        action = "Deliver the work; record work_delivered"
        rationale = "Paid — deliver and log delivery."
        action_type = "internal"
    elif stage == DealStage.DELIVERED:
        action = "Assemble proof pack (real evidence only)"
        rationale = "Delivered — build an honest proof pack."
        action_type = "internal"
    elif stage == DealStage.PROOF:
        action = "Ask for a referral (draft ready)"
        action_type = "approval"
        requires_approval = True
        draft = (
            f"طلب توصية لطيف من {deal.account_name} بعد تسليم Proof Pack. اختياري "
            "وبموافقة العميل.\n— مسودة للمراجعة قبل الإرسال —"
        )
        rationale = "Proof delivered — now compound via referral."
    elif stage == DealStage.REFERRAL:
        action = "Nurture / consider retainer offer"
        rationale = "Relationship warm — consider Revenue Command Room retainer."
        action_type = "internal"

    if stalled and requires_approval:
        rationale = f"STALLED ({days}d) — {rationale}"

    return Recommendation(
        deal_id=deal.id,
        account_name=deal.account_name,
        stage=stage.value,
        score=deal.score,
        action=action,
        action_type=action_type,
        requires_approval=requires_approval,
        draft=draft,
        rationale=rationale,
        stalled=stalled,
    )


@dataclass
class DecisionResult:
    recommendations: list[Recommendation] = field(default_factory=list)
    approvals: list[Recommendation] = field(default_factory=list)
    stalled: list[Recommendation] = field(default_factory=list)


def decide(deals: list[Deal], today: date, top_n: int = 10) -> DecisionResult:
    """Score, prioritise, and produce recommendations for the active book."""

    for deal in deals:
        deal.stage = pipeline.derive_stage(deal)
        deal.stalled = pipeline.is_stalled(deal, today)
        deal.score = pipeline.score(deal, today)

    active = [d for d in deals if d.stage != DealStage.LOST]
    active.sort(key=lambda d: d.score, reverse=True)

    recs = [recommend(d, today) for d in active]
    result = DecisionResult(
        recommendations=recs[:top_n] if top_n > 0 else recs,
        approvals=[r for r in recs if r.requires_approval][: top_n if top_n > 0 else None],
        stalled=[r for r in recs if r.stalled],
    )
    return result
