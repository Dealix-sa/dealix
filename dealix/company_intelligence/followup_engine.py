"""Follow-up & Closing Engine — response management and deal progression.

Pure-logic engine that manages prospect responses, schedules follow-ups,
handles objections, tracks deal progression, and drives opportunities
toward close with appropriate tactics.

No database, network, or LLM calls. All follow-up actions are drafts
that require human approval.

Design principles:
- Deterministic content-addressable IDs (SHA-256).
- Frozen Pydantic v2 models — no silent mutation.
- Safety: ``auto_send=False``, ``auto_close=False`` always.
- Objection responses are suggestions, never auto-sent.
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


class FollowUpUrgency(StrEnum):
    """How urgently a follow-up is needed."""

    IMMEDIATE = "immediate"  # Within hours
    SAME_DAY = "same_day"  # Today
    NEXT_DAY = "next_day"  # Tomorrow
    THIS_WEEK = "this_week"  # Within 7 days
    NEXT_WEEK = "next_week"  # 7-14 days
    MONITOR = "monitor"  # No active follow-up


class DealStage(StrEnum):
    """Stage of a deal in the closing pipeline."""

    PROSPECT = "prospect"
    CONTACTED = "contacted"
    INTERESTED = "interested"
    DISCOVERY = "discovery"
    DIAGNOSTIC = "diagnostic"
    PROPOSAL = "proposal"
    NEGOTIATION = "negotiation"
    VERBAL_YES = "verbal_yes"
    CONTRACT = "contract"
    WON = "won"
    LOST = "lost"
    DEFERRED = "deferred"


class ObjectionCategory(StrEnum):
    """Common objection categories."""

    PRICE = "price"
    TIMING = "timing"
    AUTHORITY = "authority"
    NEED = "need"
    TRUST = "trust"
    COMPETITOR = "competitor"
    COMPLEXITY = "complexity"
    CUSTOM = "custom"


class ClosingSignal(StrEnum):
    """Signals that indicate readiness to close."""

    ASKED_PRICING = "asked_pricing"
    REQUESTED_PROPOSAL = "requested_proposal"
    INTRODUCED_TEAM = "introduced_team"
    SHARED_DATA = "shared_data"
    ASKED_TIMELINE = "asked_timeline"
    VERBAL_AGREEMENT = "verbal_agreement"
    ASKED_NEXT_STEPS = "asked_next_steps"
    COMPARED_OPTIONS = "compared_options"


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class FollowUpAction(BaseModel):
    """A follow-up action to take with a prospect."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    action_id: str = ""
    tenant_id: NonEmptyString
    prospect_name: str = ""
    prospect_company: str = ""
    urgency: FollowUpUrgency = FollowUpUrgency.THIS_WEEK
    action_type: str = ""  # "reply", "call", "send_proposal", etc.
    reason: str = ""
    draft_ar: str = ""
    draft_en: str = ""
    context: str = ""
    deal_stage: DealStage = DealStage.PROSPECT
    auto_send: bool = False
    approval_required: bool = True
    source_id: NonEmptyString = ""
    created_at: str = Field(
        default_factory=lambda: datetime.now(UTC).isoformat(),
    )

    @model_validator(mode="after")
    def _safety_invariants(self) -> FollowUpAction:
        if self.auto_send:
            raise ValueError(
                "FollowUpAction.auto_send must be False — "
                "all follow-ups require human approval"
            )
        if not self.approval_required:
            raise ValueError(
                "FollowUpAction.approval_required must be True"
            )
        return self

    def model_post_init(self, _context: Any) -> None:
        if not self.action_id:
            object.__setattr__(
                self,
                "action_id",
                _stable_id(
                    "followup",
                    {
                        "tenant": self.tenant_id,
                        "prospect": self.prospect_name,
                        "type": self.action_type,
                        "source": self.source_id,
                    },
                ),
            )


class ObjectionResponse(BaseModel):
    """A prepared response to a prospect's objection."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    response_id: str = ""
    category: ObjectionCategory = ObjectionCategory.CUSTOM
    objection_text: str = ""
    response_ar: str = ""
    response_en: str = ""
    reframe_ar: str = ""
    reframe_en: str = ""
    proof_points: tuple[str, ...] = ()
    next_action: str = ""
    auto_send: bool = False

    @model_validator(mode="after")
    def _never_auto_send(self) -> ObjectionResponse:
        if self.auto_send:
            raise ValueError(
                "ObjectionResponse.auto_send must be False — "
                "objection responses require human approval"
            )
        return self


class DealProgression(BaseModel):
    """Tracking of a deal through the closing pipeline."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    tenant_id: NonEmptyString
    deal_id: str = ""
    prospect_name: str = ""
    prospect_company: str = ""
    current_stage: DealStage = DealStage.PROSPECT
    previous_stage: DealStage = DealStage.PROSPECT
    closing_signals: tuple[ClosingSignal, ...] = ()
    objections_raised: tuple[ObjectionCategory, ...] = ()
    objections_resolved: tuple[ObjectionCategory, ...] = ()
    days_in_stage: int = 0
    total_touches: int = 0
    total_replies: int = 0
    closing_probability: float = 0.0  # 0-100
    estimated_value: float = 0.0
    next_action: str = ""
    next_action_ar: str = ""
    auto_close: bool = False
    source_id: NonEmptyString = ""
    created_at: str = Field(
        default_factory=lambda: datetime.now(UTC).isoformat(),
    )

    @model_validator(mode="after")
    def _never_auto_close(self) -> DealProgression:
        if self.auto_close:
            raise ValueError(
                "DealProgression.auto_close must be False — "
                "closing requires explicit human approval"
            )
        return self

    def model_post_init(self, _context: Any) -> None:
        if not self.deal_id:
            object.__setattr__(
                self,
                "deal_id",
                _stable_id(
                    "deal",
                    {
                        "tenant": self.tenant_id,
                        "prospect": self.prospect_name,
                        "company": self.prospect_company,
                        "source": self.source_id,
                    },
                ),
            )


class ClosingPlan(BaseModel):
    """A plan to close a specific deal."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    tenant_id: NonEmptyString
    plan_id: str = ""
    deal_id: str = ""
    prospect_name: str = ""
    prospect_company: str = ""
    current_stage: DealStage = DealStage.PROSPECT
    target_stage: DealStage = DealStage.WON
    steps: tuple[str, ...] = ()
    steps_ar: tuple[str, ...] = ()
    estimated_days: int = 0
    blocking_issues: tuple[str, ...] = ()
    required_approvals: tuple[str, ...] = ()
    closing_probability: float = 0.0
    auto_close: bool = False
    approval_required: bool = True
    source_id: NonEmptyString = ""

    @model_validator(mode="after")
    def _safety_invariants(self) -> ClosingPlan:
        if self.auto_close:
            raise ValueError(
                "ClosingPlan.auto_close must be False — "
                "all closing requires human approval"
            )
        if not self.approval_required:
            raise ValueError(
                "ClosingPlan.approval_required must be True"
            )
        return self


# ---------------------------------------------------------------------------
# Objection handling library (Arabic-first)
# ---------------------------------------------------------------------------

OBJECTION_RESPONSES: dict[ObjectionCategory, tuple[str, str, str, str]] = {
    # (response_ar, response_en, reframe_ar, reframe_en)
    ObjectionCategory.PRICE: (
        "أفهم تماماً. التكلفة مهمة. خلنا نحسبها بطريقة ثانية — كم تخسر شهرياً بسبب الفرص الضائعة؟ لو النظام وفر لك حتى فرصة وحدة، يكون دفع نفسه.",
        "I completely understand. Cost matters. Let's look at it differently — how much do you lose monthly from missed opportunities? If the system saves even one deal, it pays for itself.",
        "السؤال مو كم يكلف — السؤال كم يكلفك إنك ما تستخدمه",
        "The question isn't what it costs — it's what it costs you NOT to use it",
    ),
    ObjectionCategory.TIMING: (
        "أفهم إن الوقت مو مناسب. بس الفرص ما تنتظر — كل يوم تأخير يعني فرص ضائعة. التشخيص المجاني ما ياخذ وقت وبيوضح لك الصورة.",
        "I understand the timing concern. But opportunities don't wait — every day of delay means lost deals. The free diagnostic takes minimal time and clarifies the picture.",
        "أفضل وقت كان أمس. ثاني أفضل وقت هو اليوم",
        "The best time was yesterday. The second best time is today",
    ),
    ObjectionCategory.AUTHORITY: (
        "تمام — مين الشخص المناسب أتواصل معه؟ أقدر أجهز ملخص قصير يسهّل عليك تشاركه مع صانع القرار.",
        "Got it — who would be the right person to speak with? I can prepare a brief summary that makes it easy for you to share with the decision maker.",
        "خلنا نجهز لك ملخص يقنع صانع القرار في دقيقتين",
        "Let me prepare a summary that convinces the decision maker in 2 minutes",
    ),
    ObjectionCategory.NEED: (
        "أفهم — ممكن عملياتكم ماشية كويس. بس التشخيص المجاني ممكن يكشف فرص ما كنتوا تشوفونها. أغلب عملائنا فوجئوا بحجم التحسين الممكن.",
        "I understand — your operations might be running well. But the free diagnostic often reveals opportunities you didn't see. Most of our clients were surprised by the improvement potential.",
        "اللي ما يقيس ما يتحسن — خلنا نقيس ونشوف",
        "What you don't measure, you can't improve — let's measure and see",
    ),
    ObjectionCategory.TRUST: (
        "سؤال مهم. نحن شركة سعودية ونلتزم بالشفافية الكاملة. نبدأ بتشخيص مجاني بدون أي التزام — تقدر تقيّم بنفسك قبل أي قرار.",
        "Important question. We're a Saudi company committed to full transparency. We start with a free diagnostic with zero commitment — you can evaluate for yourself before any decision.",
        "الثقة تُبنى بالإثبات — خلنا نثبت لك بالتشخيص المجاني",
        "Trust is built on proof — let us prove it with the free diagnostic",
    ),
    ObjectionCategory.COMPETITOR: (
        "ممتاز إنك تقارن — هذا ذكاء. الفرق إن ديلكس مبني للسوق السعودي بالعربي مع حوكمة كاملة وموافقة بشرية على كل إجراء خارجي.",
        "Great that you're comparing — that's smart. The difference is Dealix is built for the Saudi market in Arabic with full governance and human approval on every external action.",
        "مو كل نظام يفهم السوق السعودي — جرب واحكم بنفسك",
        "Not every system understands the Saudi market — try and judge for yourself",
    ),
    ObjectionCategory.COMPLEXITY: (
        "بالعكس — ديلكس يعمل فوق أنظمتك الحالية بدون ما تغير شيء. لا تحتاج migration ولا تدريب طويل. نربطه ويشتغل.",
        "Quite the opposite — Dealix works on top of your existing systems without changing anything. No migration needed, no lengthy training. We connect it and it works.",
        "مو المطلوب تعقيد — المطلوب تبسيط اللي عندك",
        "The goal isn't to add complexity — it's to simplify what you have",
    ),
}


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def handle_response(
    *,
    tenant_id: str,
    prospect_name: str,
    prospect_company: str,
    response_text: str,
    current_stage: DealStage = DealStage.CONTACTED,
    source_id: str,
) -> FollowUpAction:
    """Generate a follow-up action based on a prospect's response."""
    from dealix.company_intelligence.outreach_engine import ResponseType, classify_response

    response_type = classify_response(response_text)

    if response_type == ResponseType.OPT_OUT:
        return FollowUpAction(
            tenant_id=tenant_id,
            prospect_name=prospect_name,
            prospect_company=prospect_company,
            urgency=FollowUpUrgency.IMMEDIATE,
            action_type="opt_out",
            reason="العميل المحتمل طلب الإيقاف — يجب احترام الطلب فوراً",
            draft_ar="تم. شكراً لوقتك ولن نتواصل معك مجدداً. أتمنى لك التوفيق.",
            draft_en="Done. Thank you for your time, we won't contact you again. Wishing you the best.",
            context=response_text,
            deal_stage=DealStage.LOST,
            auto_send=False,
            approval_required=True,
            source_id=source_id,
        )

    if response_type == ResponseType.POSITIVE:
        return FollowUpAction(
            tenant_id=tenant_id,
            prospect_name=prospect_name,
            prospect_company=prospect_company,
            urgency=FollowUpUrgency.IMMEDIATE,
            action_type="schedule_discovery",
            reason="رد إيجابي — جدولة جلسة اكتشاف فوراً",
            draft_ar=f"ممتاز {prospect_name}! أقترح نحدد موعد 15 دقيقة هالأسبوع. وش الأوقات المناسبة لك؟",
            draft_en=f"Excellent {prospect_name}! I suggest we schedule a 15-minute call this week. What times work for you?",
            context=response_text,
            deal_stage=DealStage.INTERESTED,
            auto_send=False,
            approval_required=True,
            source_id=source_id,
        )

    if response_type == ResponseType.INTERESTED:
        return FollowUpAction(
            tenant_id=tenant_id,
            prospect_name=prospect_name,
            prospect_company=prospect_company,
            urgency=FollowUpUrgency.SAME_DAY,
            action_type="provide_info",
            reason="مهتم — أرسل معلومات إضافية",
            draft_ar=f"حياك {prospect_name}! نقدم تشخيص مجاني يتضمن تحليل لأكبر 3 فرص تحسين في عملياتكم. أقدر أسلمك النتائج خلال 24 ساعة.",
            draft_en=f"Welcome {prospect_name}! We offer a free diagnostic including analysis of your top 3 improvement opportunities. I can deliver results within 24 hours.",
            context=response_text,
            deal_stage=DealStage.INTERESTED,
            auto_send=False,
            approval_required=True,
            source_id=source_id,
        )

    if response_type == ResponseType.QUESTION:
        return FollowUpAction(
            tenant_id=tenant_id,
            prospect_name=prospect_name,
            prospect_company=prospect_company,
            urgency=FollowUpUrgency.SAME_DAY,
            action_type="answer_question",
            reason="سؤال من العميل المحتمل — يحتاج إجابة مخصصة",
            draft_ar="شكراً على سؤالك! خلني أجاوبك بالتفصيل...",
            draft_en="Thank you for your question! Let me answer in detail...",
            context=response_text,
            deal_stage=current_stage,
            auto_send=False,
            approval_required=True,
            source_id=source_id,
        )

    if response_type == ResponseType.OBJECTION:
        obj_cat = _classify_objection(response_text)
        obj_response = get_objection_response(obj_cat, response_text)
        return FollowUpAction(
            tenant_id=tenant_id,
            prospect_name=prospect_name,
            prospect_company=prospect_company,
            urgency=FollowUpUrgency.SAME_DAY,
            action_type="handle_objection",
            reason=f"اعتراض ({obj_cat.value}) — يحتاج معالجة",
            draft_ar=obj_response.response_ar,
            draft_en=obj_response.response_en,
            context=response_text,
            deal_stage=current_stage,
            auto_send=False,
            approval_required=True,
            source_id=source_id,
        )

    if response_type == ResponseType.NOT_NOW:
        return FollowUpAction(
            tenant_id=tenant_id,
            prospect_name=prospect_name,
            prospect_company=prospect_company,
            urgency=FollowUpUrgency.NEXT_WEEK,
            action_type="schedule_later",
            reason="مو الحين — جدولة متابعة لاحقة",
            draft_ar=f"تمام {prospect_name} — متى يكون الوقت أنسب؟ أقدر أتواصل معك الشهر الجاي لو يناسبك.",
            draft_en=f"No problem {prospect_name} — when would be a better time? I can reach out next month if that works.",
            context=response_text,
            deal_stage=DealStage.DEFERRED,
            auto_send=False,
            approval_required=True,
            source_id=source_id,
        )

    if response_type == ResponseType.REFERRAL:
        return FollowUpAction(
            tenant_id=tenant_id,
            prospect_name=prospect_name,
            prospect_company=prospect_company,
            urgency=FollowUpUrgency.SAME_DAY,
            action_type="follow_referral",
            reason="إحالة — تواصل مع الشخص المُحال إليه",
            draft_ar=f"شكراً جزيلاً {prospect_name}! أقدر التوصية. بتواصل معهم وأذكر إنك أحلتني.",
            draft_en=f"Thank you so much {prospect_name}! I appreciate the referral. I'll reach out and mention you recommended me.",
            context=response_text,
            deal_stage=current_stage,
            auto_send=False,
            approval_required=True,
            source_id=source_id,
        )

    # NEGATIVE or NO_RESPONSE
    return FollowUpAction(
        tenant_id=tenant_id,
        prospect_name=prospect_name,
        prospect_company=prospect_company,
        urgency=FollowUpUrgency.MONITOR,
        action_type="monitor",
        reason="رد سلبي أو بدون رد — راقب فقط",
        draft_ar="",
        draft_en="",
        context=response_text,
        deal_stage=current_stage,
        auto_send=False,
        approval_required=True,
        source_id=source_id,
    )


def get_objection_response(
    category: ObjectionCategory,
    objection_text: str = "",
) -> ObjectionResponse:
    """Get a prepared response for an objection category."""
    responses = OBJECTION_RESPONSES.get(category)
    if responses:
        ar, en, reframe_ar, reframe_en = responses
    else:
        ar = "أفهم وجهة نظرك. خلنا نناقشها بالتفصيل — التشخيص المجاني بيوضح الصورة."
        en = "I understand your perspective. Let's discuss in detail — the free diagnostic will clarify things."
        reframe_ar = "كل اعتراض هو فرصة لنفهم احتياجك أكثر"
        reframe_en = "Every objection is an opportunity to better understand your needs"

    return ObjectionResponse(
        response_id=_stable_id(
            "objection",
            {"category": category.value, "text": objection_text[:50]},
        ),
        category=category,
        objection_text=objection_text,
        response_ar=ar,
        response_en=en,
        reframe_ar=reframe_ar,
        reframe_en=reframe_en,
        proof_points=(),
        next_action="schedule_discovery",
        auto_send=False,
    )


def assess_deal_progression(
    *,
    tenant_id: str,
    prospect_name: str,
    prospect_company: str,
    current_stage: DealStage,
    closing_signals: tuple[ClosingSignal, ...] = (),
    objections_raised: tuple[ObjectionCategory, ...] = (),
    objections_resolved: tuple[ObjectionCategory, ...] = (),
    days_in_stage: int = 0,
    total_touches: int = 0,
    total_replies: int = 0,
    estimated_value: float = 0.0,
    source_id: str,
) -> DealProgression:
    """Assess where a deal stands and what to do next."""
    # Calculate closing probability
    prob = _closing_probability(
        current_stage, closing_signals, objections_raised,
        objections_resolved, days_in_stage, total_replies,
    )

    # Determine next action
    action, action_ar = _next_action(
        current_stage, closing_signals, objections_raised,
        objections_resolved, days_in_stage, prob,
    )

    return DealProgression(
        tenant_id=tenant_id,
        prospect_name=prospect_name,
        prospect_company=prospect_company,
        current_stage=current_stage,
        previous_stage=current_stage,
        closing_signals=closing_signals,
        objections_raised=objections_raised,
        objections_resolved=objections_resolved,
        days_in_stage=days_in_stage,
        total_touches=total_touches,
        total_replies=total_replies,
        closing_probability=prob,
        estimated_value=estimated_value,
        next_action=action,
        next_action_ar=action_ar,
        auto_close=False,
        source_id=source_id,
    )


def generate_closing_plan(
    *,
    tenant_id: str,
    deal: DealProgression,
    source_id: str,
) -> ClosingPlan:
    """Generate a plan to close a specific deal."""
    steps, steps_ar = _closing_steps(deal)
    blockers = _identify_blockers(deal)
    approvals = _required_approvals(deal)
    days = _estimate_days(deal)

    return ClosingPlan(
        tenant_id=tenant_id,
        plan_id=_stable_id(
            "closingplan",
            {"tenant": tenant_id, "deal": deal.deal_id, "source": source_id},
        ),
        deal_id=deal.deal_id,
        prospect_name=deal.prospect_name,
        prospect_company=deal.prospect_company,
        current_stage=deal.current_stage,
        target_stage=DealStage.WON,
        steps=tuple(steps),
        steps_ar=tuple(steps_ar),
        estimated_days=days,
        blocking_issues=tuple(blockers),
        required_approvals=tuple(approvals),
        closing_probability=deal.closing_probability,
        auto_close=False,
        approval_required=True,
        source_id=source_id,
    )


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _classify_objection(text: str) -> ObjectionCategory:
    """Classify an objection from text."""
    t = text.lower()
    price_kw = ("غالي", "سعر", "تكلفة", "expensive", "price", "cost", "budget")
    if any(k in t for k in price_kw):
        return ObjectionCategory.PRICE
    timing_kw = ("وقت", "مشغول", "لاحق", "time", "busy", "later")
    if any(k in t for k in timing_kw):
        return ObjectionCategory.TIMING
    auth_kw = ("مديري", "القرار", "boss", "manager", "decision", "authority")
    if any(k in t for k in auth_kw):
        return ObjectionCategory.AUTHORITY
    need_kw = ("مو محتاج", "عندنا", "don't need", "already have", "no need")
    if any(k in t for k in need_kw):
        return ObjectionCategory.NEED
    trust_kw = ("ثقة", "خايف", "trust", "risk", "guarantee", "proof")
    if any(k in t for k in trust_kw):
        return ObjectionCategory.TRUST
    comp_kw = ("بديل", "منافس", "competitor", "alternative", "other")
    if any(k in t for k in comp_kw):
        return ObjectionCategory.COMPETITOR
    complex_kw = ("معقد", "صعب", "complex", "difficult", "complicated")
    if any(k in t for k in complex_kw):
        return ObjectionCategory.COMPLEXITY
    return ObjectionCategory.CUSTOM


def _closing_probability(
    stage: DealStage,
    signals: tuple[ClosingSignal, ...],
    raised: tuple[ObjectionCategory, ...],
    resolved: tuple[ObjectionCategory, ...],
    days_in_stage: int,
    total_replies: int,
) -> float:
    """Calculate closing probability 0-100."""
    stage_probs = {
        DealStage.PROSPECT: 5.0,
        DealStage.CONTACTED: 10.0,
        DealStage.INTERESTED: 20.0,
        DealStage.DISCOVERY: 30.0,
        DealStage.DIAGNOSTIC: 40.0,
        DealStage.PROPOSAL: 50.0,
        DealStage.NEGOTIATION: 65.0,
        DealStage.VERBAL_YES: 80.0,
        DealStage.CONTRACT: 90.0,
        DealStage.WON: 100.0,
        DealStage.LOST: 0.0,
        DealStage.DEFERRED: 10.0,
    }
    base = stage_probs.get(stage, 5.0)

    # Signal bonus
    signal_bonus = len(signals) * 3.0

    # Objection penalty (unresolved)
    unresolved = len(raised) - len(resolved)
    objection_penalty = max(0, unresolved) * 5.0

    # Staleness penalty
    staleness = 0.0
    if days_in_stage > 14:
        staleness = min((days_in_stage - 14) * 1.0, 20.0)

    # Engagement bonus
    engagement = min(total_replies * 2.0, 10.0)

    prob = base + signal_bonus + engagement - objection_penalty - staleness
    return max(0.0, min(100.0, prob))


def _next_action(
    stage: DealStage,
    signals: tuple[ClosingSignal, ...],
    raised: tuple[ObjectionCategory, ...],
    resolved: tuple[ObjectionCategory, ...],
    days_in_stage: int,
    prob: float,
) -> tuple[str, str]:
    """Determine the next best action."""
    if stage == DealStage.LOST:
        return "archive", "أرشف الصفقة"
    if stage == DealStage.WON:
        return "start_delivery", "ابدأ التسليم"

    unresolved = set(raised) - set(resolved)
    if unresolved:
        cat = next(iter(unresolved))
        return f"resolve_objection_{cat.value}", f"عالج اعتراض: {cat.value}"

    if ClosingSignal.VERBAL_AGREEMENT in signals and stage != DealStage.CONTRACT:
        return "send_contract", "أرسل العقد"
    if ClosingSignal.REQUESTED_PROPOSAL in signals and stage not in (DealStage.PROPOSAL, DealStage.NEGOTIATION):
        return "send_proposal", "أرسل العرض التجاري"
    if stage == DealStage.PROSPECT:
        return "initiate_contact", "ابدأ التواصل"
    if stage == DealStage.CONTACTED and days_in_stage > 3:
        return "follow_up", "تابع"
    if stage == DealStage.INTERESTED:
        return "schedule_discovery", "حدد موعد الاكتشاف"
    if stage == DealStage.DISCOVERY:
        return "deliver_diagnostic", "سلّم التشخيص"
    if stage == DealStage.DIAGNOSTIC:
        return "present_proposal", "قدّم العرض"
    if stage == DealStage.PROPOSAL:
        return "follow_up_proposal", "تابع العرض"
    if stage == DealStage.NEGOTIATION:
        return "negotiate_terms", "تفاوض على الشروط"

    if days_in_stage > 7:
        return "re_engage", "أعد التواصل"
    return "monitor", "راقب"


def _closing_steps(deal: DealProgression) -> tuple[list[str], list[str]]:
    """Generate closing steps based on deal state."""
    steps_en: list[str] = []
    steps_ar: list[str] = []

    stage_order = [
        DealStage.PROSPECT, DealStage.CONTACTED, DealStage.INTERESTED,
        DealStage.DISCOVERY, DealStage.DIAGNOSTIC, DealStage.PROPOSAL,
        DealStage.NEGOTIATION, DealStage.VERBAL_YES, DealStage.CONTRACT,
        DealStage.WON,
    ]

    current_idx = stage_order.index(deal.current_stage) if deal.current_stage in stage_order else 0

    step_map = {
        DealStage.CONTACTED: ("Initiate contact and introduce Dealix", "ابدأ التواصل وقدّم ديلكس"),
        DealStage.INTERESTED: ("Confirm interest and schedule discovery", "تأكد من الاهتمام وحدد موعد الاكتشاف"),
        DealStage.DISCOVERY: ("Conduct discovery call", "أجرِ جلسة الاكتشاف"),
        DealStage.DIAGNOSTIC: ("Deliver free diagnostic", "سلّم التشخيص المجاني"),
        DealStage.PROPOSAL: ("Present tailored proposal", "قدّم عرض مخصص"),
        DealStage.NEGOTIATION: ("Negotiate terms and pricing", "تفاوض على الشروط والتسعير"),
        DealStage.VERBAL_YES: ("Get verbal commitment", "احصل على موافقة شفهية"),
        DealStage.CONTRACT: ("Send and sign contract", "أرسل ووقّع العقد"),
        DealStage.WON: ("Begin onboarding and delivery", "ابدأ التأهيل والتسليم"),
    }

    for stage in stage_order[current_idx + 1:]:
        if stage in step_map:
            en, ar = step_map[stage]
            steps_en.append(en)
            steps_ar.append(ar)

    return steps_en, steps_ar


def _identify_blockers(deal: DealProgression) -> list[str]:
    """Identify blocking issues for a deal."""
    blockers: list[str] = []
    unresolved = set(deal.objections_raised) - set(deal.objections_resolved)
    for obj in unresolved:
        blockers.append(f"Unresolved objection: {obj.value}")
    if deal.days_in_stage > 14:
        blockers.append(f"Stalled for {deal.days_in_stage} days in {deal.current_stage.value}")
    if deal.total_replies == 0 and deal.total_touches > 3:
        blockers.append("No response after multiple touches")
    return blockers


def _required_approvals(deal: DealProgression) -> list[str]:
    """List approvals needed to proceed."""
    approvals: list[str] = []
    if deal.current_stage in (DealStage.PROPOSAL, DealStage.NEGOTIATION):
        approvals.append("Founder approval on pricing and terms")
    if deal.current_stage == DealStage.CONTRACT:
        approvals.append("Founder signature on contract")
    if deal.estimated_value > 10000:
        approvals.append("Founder approval for high-value deal")
    approvals.append("Founder approval for all external communications")
    return approvals


def _estimate_days(deal: DealProgression) -> int:
    """Estimate days to close."""
    stage_days = {
        DealStage.PROSPECT: 30,
        DealStage.CONTACTED: 25,
        DealStage.INTERESTED: 20,
        DealStage.DISCOVERY: 15,
        DealStage.DIAGNOSTIC: 12,
        DealStage.PROPOSAL: 10,
        DealStage.NEGOTIATION: 7,
        DealStage.VERBAL_YES: 5,
        DealStage.CONTRACT: 3,
    }
    return stage_days.get(deal.current_stage, 30)
