"""Outreach Sequencing Engine — multi-channel campaign planning and execution.

Pure-logic engine that plans personalized outreach sequences, generates
draft messages for each touch point, manages timing and cadence, and
tracks sequence progress across email, WhatsApp, and SMS channels.

No database, network, or LLM calls. Every message is a draft that requires
human approval before sending. The engine NEVER triggers external sends.

Design principles:
- Deterministic content-addressable IDs (SHA-256).
- Frozen Pydantic v2 models — no silent mutation.
- Safety: ``auto_send=False`` always, ``approval_required=True``.
- All messages are drafts until founder approves.
- Arabic-first with English support.
"""
from __future__ import annotations

import json
from datetime import UTC, datetime
from enum import StrEnum
from hashlib import sha256
from typing import Annotated, Any

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    StringConstraints,
    model_validator,
)

NonEmptyString = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _stable_id(prefix: str, payload: dict[str, Any]) -> str:
    canonical = json.dumps(
        payload,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
        default=str,
    )
    return f"{prefix}_{sha256(canonical.encode('utf-8')).hexdigest()[:16]}"


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------


class OutreachChannel(StrEnum):
    """Channels available for outreach."""

    EMAIL = "email"
    WHATSAPP = "whatsapp"
    SMS = "sms"
    LINKEDIN = "linkedin"
    PHONE = "phone"


class TouchType(StrEnum):
    """Type of touch point in a sequence."""

    INTRO = "intro"
    VALUE_ADD = "value_add"
    FOLLOW_UP = "follow_up"
    BREAKUP = "breakup"
    RE_ENGAGE = "re_engage"
    REFERRAL_ASK = "referral_ask"
    DISCOVERY_INVITE = "discovery_invite"


class SequenceStatus(StrEnum):
    """Status of an outreach sequence."""

    PLANNED = "planned"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    STOPPED = "stopped"


class TouchStatus(StrEnum):
    """Status of an individual touch point."""

    DRAFT = "draft"
    APPROVED = "approved"
    SENT = "sent"
    DELIVERED = "delivered"
    OPENED = "opened"
    REPLIED = "replied"
    BOUNCED = "bounced"
    OPTED_OUT = "opted_out"
    SKIPPED = "skipped"


class ResponseType(StrEnum):
    """Classification of a prospect's response."""

    POSITIVE = "positive"
    INTERESTED = "interested"
    QUESTION = "question"
    OBJECTION = "objection"
    NOT_NOW = "not_now"
    REFERRAL = "referral"
    OPT_OUT = "opt_out"
    NO_RESPONSE = "no_response"
    NEGATIVE = "negative"


class CadenceSpeed(StrEnum):
    """Speed of outreach cadence."""

    AGGRESSIVE = "aggressive"  # 2-day gaps
    STANDARD = "standard"  # 3-4 day gaps
    GENTLE = "gentle"  # 5-7 day gaps
    SLOW = "slow"  # 7-14 day gaps


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class TouchPoint(BaseModel):
    """A single touch point in an outreach sequence."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    touch_id: str = ""
    sequence_id: str = ""
    touch_number: int = 1
    touch_type: TouchType = TouchType.INTRO
    channel: OutreachChannel = OutreachChannel.EMAIL
    day_offset: int = 0  # Days from sequence start
    subject: str = ""
    body_ar: str = ""
    body_en: str = ""
    status: TouchStatus = TouchStatus.DRAFT
    approval_required: bool = True
    auto_send: bool = False

    @model_validator(mode="after")
    def _never_auto_send(self) -> TouchPoint:
        if self.auto_send:
            raise ValueError(
                "TouchPoint.auto_send must be False — "
                "all sends require human approval"
            )
        return self


class OutreachSequence(BaseModel):
    """A complete outreach sequence for a prospect."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    tenant_id: NonEmptyString
    sequence_id: str = ""
    prospect_name: str = ""
    prospect_company: str = ""
    prospect_email: str = ""
    prospect_whatsapp: str = ""
    prospect_phone: str = ""
    touches: tuple[TouchPoint, ...] = ()
    cadence: CadenceSpeed = CadenceSpeed.STANDARD
    status: SequenceStatus = SequenceStatus.PLANNED
    total_touches: int = 0
    completed_touches: int = 0
    primary_channel: OutreachChannel = OutreachChannel.EMAIL
    context: str = ""
    sector: str = ""
    pain_points: tuple[str, ...] = ()
    approval_required: bool = True
    auto_send: bool = False
    source_id: NonEmptyString = ""
    created_at: str = Field(
        default_factory=lambda: datetime.now(UTC).isoformat(),
    )

    @model_validator(mode="after")
    def _safety_invariants(self) -> OutreachSequence:
        if self.auto_send:
            raise ValueError(
                "OutreachSequence.auto_send must be False — "
                "all outreach requires human approval"
            )
        if not self.approval_required:
            raise ValueError(
                "OutreachSequence.approval_required must be True"
            )
        return self

    def model_post_init(self, _context: Any) -> None:
        if not self.sequence_id:
            object.__setattr__(
                self,
                "sequence_id",
                _stable_id(
                    "sequence",
                    {
                        "tenant": self.tenant_id,
                        "prospect": self.prospect_name,
                        "company": self.prospect_company,
                        "source": self.source_id,
                    },
                ),
            )
        if not self.total_touches:
            object.__setattr__(self, "total_touches", len(self.touches))


class SequenceAnalysis(BaseModel):
    """Analysis of outreach sequence performance."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    tenant_id: NonEmptyString
    analysis_id: str = ""
    total_sequences: int = 0
    active_sequences: int = 0
    completed_sequences: int = 0
    total_touches_sent: int = 0
    total_replies: int = 0
    reply_rate: float = 0.0
    positive_reply_rate: float = 0.0
    opt_out_count: int = 0
    best_channel: OutreachChannel = OutreachChannel.EMAIL
    best_touch_type: TouchType = TouchType.INTRO
    recommendations: tuple[str, ...] = ()
    source_id: NonEmptyString = ""


# ---------------------------------------------------------------------------
# Cadence configuration
# ---------------------------------------------------------------------------

CADENCE_GAPS: dict[CadenceSpeed, tuple[int, ...]] = {
    CadenceSpeed.AGGRESSIVE: (0, 2, 4, 7, 10),
    CadenceSpeed.STANDARD: (0, 3, 7, 12, 18),
    CadenceSpeed.GENTLE: (0, 5, 12, 21, 30),
    CadenceSpeed.SLOW: (0, 7, 14, 28, 42),
}

DEFAULT_SEQUENCE_TEMPLATE: tuple[TouchType, ...] = (
    TouchType.INTRO,
    TouchType.VALUE_ADD,
    TouchType.FOLLOW_UP,
    TouchType.DISCOVERY_INVITE,
    TouchType.BREAKUP,
)


# ---------------------------------------------------------------------------
# Message templates (Arabic-first)
# ---------------------------------------------------------------------------


def _intro_message(name: str, company: str, pain: str) -> tuple[str, str]:
    """Generate intro message drafts in AR and EN."""
    ar = (
        f"السلام عليكم {name}،\n\n"
        f"أتواصل معك بخصوص {company}. "
        f"نعمل مع شركات مشابهة في السوق السعودي وعندنا تجربة في {pain}.\n\n"
        f"نقدم تشخيص مجاني مختصر نحدد فيه أكبر فرصة تحسين في عملياتكم — "
        f"بدون أي التزام.\n\n"
        f"هل يناسبك نتكلم 15 دقيقة هالأسبوع؟\n\n"
        f"لإيقاف الرسائل: رد بكلمة إيقاف"
    )
    en = (
        f"Hi {name},\n\n"
        f"I'm reaching out regarding {company}. "
        f"We work with similar companies in the Saudi market on {pain}.\n\n"
        f"We offer a free mini diagnostic that identifies your biggest "
        f"operational improvement opportunity — no commitment.\n\n"
        f"Would you have 15 minutes this week for a quick call?\n\n"
        f"To unsubscribe: reply STOP"
    )
    return ar, en


def _value_add_message(name: str, sector: str) -> tuple[str, str]:
    """Generate value-add follow-up."""
    ar = (
        f"مرحباً {name}،\n\n"
        f"أحببت أشارك معك ملاحظة لاحظناها في قطاع {sector} بالسعودية: "
        f"أغلب الشركات تخسر 15-30% من فرصها بسبب تأخر المتابعة.\n\n"
        f"بنينا نظام يحل هالمشكلة بدون ما تغير أي شيء في أنظمتك الحالية.\n\n"
        f"لإيقاف الرسائل: رد بكلمة إيقاف"
    )
    en = (
        f"Hi {name},\n\n"
        f"Wanted to share an insight we've seen in the {sector} sector in Saudi: "
        f"most companies lose 15-30% of opportunities due to follow-up delays.\n\n"
        f"We've built a system that solves this without changing your existing tools.\n\n"
        f"To unsubscribe: reply STOP"
    )
    return ar, en


def _follow_up_message(name: str, touch_num: int) -> tuple[str, str]:
    """Generate follow-up message."""
    ar = (
        f"مرحباً {name}،\n\n"
        f"أتابع رسالتي السابقة. أعرف إنك مشغول — "
        f"لو عندك أي سؤال أو تحب نحدد موعد قصير، أنا متاح.\n\n"
        f"لإيقاف الرسائل: رد بكلمة إيقاف"
    )
    en = (
        f"Hi {name},\n\n"
        f"Following up on my previous message. I know you're busy — "
        f"if you have any questions or would like to schedule a quick call, "
        f"I'm available.\n\n"
        f"To unsubscribe: reply STOP"
    )
    return ar, en


def _discovery_invite(name: str, company: str) -> tuple[str, str]:
    """Generate discovery call invitation."""
    ar = (
        f"مرحباً {name}،\n\n"
        f"أقدر أعطيك تشخيص مجاني لـ{company} في 24 ساعة — "
        f"يتضمن 3 فرص مرتبة وتوصية بأفضل قناة تواصل وخطة عمل.\n\n"
        f"كل اللي أحتاجه 15 دقيقة منك.\n\n"
        f"لإيقاف الرسائل: رد بكلمة إيقاف"
    )
    en = (
        f"Hi {name},\n\n"
        f"I can deliver a free diagnostic for {company} in 24 hours — "
        f"including 3 ranked opportunities, best channel recommendation, "
        f"and an action plan.\n\n"
        f"All I need is 15 minutes of your time.\n\n"
        f"To unsubscribe: reply STOP"
    )
    return ar, en


def _breakup_message(name: str) -> tuple[str, str]:
    """Generate breakup (final) message."""
    ar = (
        f"مرحباً {name}،\n\n"
        f"يبدو إن الوقت مو مناسب حالياً — ما عندي مشكلة أبداً. "
        f"لو احتجت أي شيء مستقبلاً، أنا موجود.\n\n"
        f"أتمنى لك التوفيق.\n\n"
        f"لإيقاف الرسائل: رد بكلمة إيقاف"
    )
    en = (
        f"Hi {name},\n\n"
        f"It seems like the timing isn't right — no worries at all. "
        f"If you ever need anything in the future, I'm here.\n\n"
        f"Wishing you the best.\n\n"
        f"To unsubscribe: reply STOP"
    )
    return ar, en


_TOUCH_GENERATORS: dict[TouchType, Any] = {
    TouchType.INTRO: lambda name, company, pain, sector, n: _intro_message(name, company, pain),
    TouchType.VALUE_ADD: lambda name, company, pain, sector, n: _value_add_message(name, sector),
    TouchType.FOLLOW_UP: lambda name, company, pain, sector, n: _follow_up_message(name, n),
    TouchType.DISCOVERY_INVITE: lambda name, company, pain, sector, n: _discovery_invite(name, company),
    TouchType.BREAKUP: lambda name, company, pain, sector, n: _breakup_message(name),
}


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def plan_sequence(
    *,
    tenant_id: str,
    prospect_name: str,
    prospect_company: str,
    prospect_email: str = "",
    prospect_whatsapp: str = "",
    prospect_phone: str = "",
    sector: str = "",
    pain_points: tuple[str, ...] = (),
    cadence: CadenceSpeed = CadenceSpeed.STANDARD,
    channel: OutreachChannel = OutreachChannel.EMAIL,
    touch_types: tuple[TouchType, ...] | None = None,
    source_id: str = "",
) -> OutreachSequence:
    """Plan a complete outreach sequence for a prospect."""
    types = touch_types or DEFAULT_SEQUENCE_TEMPLATE
    gaps = CADENCE_GAPS.get(cadence, CADENCE_GAPS[CadenceSpeed.STANDARD])

    pain_text = pain_points[0] if pain_points else "تحسين عمليات الإيرادات"

    seq_id = _stable_id(
        "sequence",
        {
            "tenant": tenant_id,
            "prospect": prospect_name,
            "company": prospect_company,
            "source": source_id,
        },
    )

    touches: list[TouchPoint] = []
    for i, ttype in enumerate(types):
        day = gaps[i] if i < len(gaps) else gaps[-1] + (i - len(gaps) + 1) * 7
        gen = _TOUCH_GENERATORS.get(ttype)
        if gen:
            ar, en = gen(prospect_name, prospect_company, pain_text, sector, i + 1)
        else:
            ar, en = f"متابعة {i + 1}", f"Follow-up {i + 1}"

        subject = f"فرصة تحسين عمليات {prospect_company}" if i == 0 else f"متابعة — {prospect_company}"

        touch = TouchPoint(
            touch_id=_stable_id(
                "touch",
                {"sequence": seq_id, "number": i + 1, "type": ttype.value},
            ),
            sequence_id=seq_id,
            touch_number=i + 1,
            touch_type=ttype,
            channel=channel,
            day_offset=day,
            subject=subject,
            body_ar=ar,
            body_en=en,
            status=TouchStatus.DRAFT,
            approval_required=True,
            auto_send=False,
        )
        touches.append(touch)

    return OutreachSequence(
        tenant_id=tenant_id,
        sequence_id=seq_id,
        prospect_name=prospect_name,
        prospect_company=prospect_company,
        prospect_email=prospect_email,
        prospect_whatsapp=prospect_whatsapp,
        prospect_phone=prospect_phone,
        touches=tuple(touches),
        cadence=cadence,
        status=SequenceStatus.PLANNED,
        total_touches=len(touches),
        completed_touches=0,
        primary_channel=channel,
        sector=sector,
        pain_points=pain_points,
        approval_required=True,
        auto_send=False,
        source_id=source_id,
    )


def classify_response(text: str) -> ResponseType:
    """Classify a prospect's response into a category."""
    t = text.lower().strip()

    # Opt-out signals (Arabic and English)
    opt_out_keywords = ("stop", "unsubscribe", "إيقاف", "إلغاء", "لا تراسلني", "opt out", "opt-out")
    if any(kw in t for kw in opt_out_keywords):
        return ResponseType.OPT_OUT

    # Positive signals
    positive_keywords = (
        "نعم", "أكيد", "يناسبني", "موافق", "تمام", "ممتاز", "حياك",
        "yes", "sure", "sounds good", "interested", "let's", "great",
    )
    if any(kw in t for kw in positive_keywords):
        return ResponseType.POSITIVE

    # Interest signals
    interest_keywords = (
        "أبي أعرف أكثر", "كم السعر", "وش تقدمون", "عندي سؤال",
        "tell me more", "pricing", "how much", "what do you offer",
    )
    if any(kw in t for kw in interest_keywords):
        return ResponseType.INTERESTED

    # Question signals
    question_indicators = ("?", "؟", "كيف", "ليش", "وين", "متى", "how", "what", "when", "why")
    if any(kw in t for kw in question_indicators):
        return ResponseType.QUESTION

    # Objection signals
    objection_keywords = (
        "غالي", "مو مهتم", "عندنا نظام", "لا شكراً", "مشغول",
        "expensive", "not interested", "we already have", "no thanks", "busy",
    )
    if any(kw in t for kw in objection_keywords):
        return ResponseType.OBJECTION

    # Not-now signals
    not_now_keywords = (
        "مو الحين", "لاحقاً", "بعدين", "الشهر الجاي",
        "not now", "later", "next month", "not the right time",
    )
    if any(kw in t for kw in not_now_keywords):
        return ResponseType.NOT_NOW

    # Referral signals
    referral_keywords = ("كلم", "تواصل مع", "جرب", "talk to", "contact", "try reaching")
    if any(kw in t for kw in referral_keywords):
        return ResponseType.REFERRAL

    # Negative
    negative_keywords = ("لا", "no", "not", "never", "أبداً")
    if any(kw in t for kw in negative_keywords):
        return ResponseType.NEGATIVE

    return ResponseType.NO_RESPONSE


def analyze_sequences(
    *,
    tenant_id: str,
    sequences: list[OutreachSequence],
    source_id: str,
) -> SequenceAnalysis:
    """Analyze outreach sequence performance."""
    total = len(sequences)
    active = sum(1 for s in sequences if s.status == SequenceStatus.ACTIVE)
    completed = sum(1 for s in sequences if s.status == SequenceStatus.COMPLETED)

    sent = 0
    replies = 0
    positive = 0
    opt_outs = 0
    channel_counts: dict[OutreachChannel, int] = {}
    type_replies: dict[TouchType, int] = {}

    for seq in sequences:
        for t in seq.touches:
            if t.status in (TouchStatus.SENT, TouchStatus.DELIVERED, TouchStatus.OPENED, TouchStatus.REPLIED):
                sent += 1
                ch = OutreachChannel(t.channel)
                channel_counts[ch] = channel_counts.get(ch, 0) + 1
            if t.status == TouchStatus.REPLIED:
                replies += 1
                tt = t.touch_type
                type_replies[tt] = type_replies.get(tt, 0) + 1
            if t.status == TouchStatus.OPTED_OUT:
                opt_outs += 1

    reply_rate = (replies / sent * 100) if sent > 0 else 0.0

    best_ch = max(channel_counts, key=channel_counts.get, default=OutreachChannel.EMAIL)  # type: ignore[arg-type]
    best_tt = max(type_replies, key=type_replies.get, default=TouchType.INTRO)  # type: ignore[arg-type]

    recs: list[str] = []
    if reply_rate < 5:
        recs.append("معدل الرد منخفض — جرب تغيير القناة أو تحسين الرسالة الأولى")
    if opt_outs > total * 0.1:
        recs.append("نسبة الإيقاف مرتفعة — راجع استهداف العملاء المحتملين")
    if reply_rate > 20:
        recs.append("معدل رد ممتاز — استمر بنفس الأسلوب وزد عدد التسلسلات")

    return SequenceAnalysis(
        tenant_id=tenant_id,
        analysis_id=_stable_id(
            "seqanalysis",
            {"tenant": tenant_id, "count": total, "source": source_id},
        ),
        total_sequences=total,
        active_sequences=active,
        completed_sequences=completed,
        total_touches_sent=sent,
        total_replies=replies,
        reply_rate=reply_rate,
        positive_reply_rate=(positive / sent * 100) if sent > 0 else 0.0,
        opt_out_count=opt_outs,
        best_channel=best_ch,
        best_touch_type=best_tt,
        recommendations=tuple(recs),
        source_id=source_id,
    )
