"""Draft Factory — turn prospects into governed, approval-first drafts.

Deterministic Arabic templates (Saudi-first). Every generated draft:
  * is ``pending_approval`` with ``approval_required=True``
  * is routed through ``governance_os.policy_check_draft`` before queueing
  * never auto-sends — sending is always a manual human step after approval

If a generated body somehow trips the governance gate it is downgraded to
``needs_edit`` with the issues recorded in ``next_action`` (defence in depth).
"""

from __future__ import annotations

from collections.abc import Callable

from auto_client_acquisition.distribution_os.models import (
    Channel,
    Draft,
    DraftStatus,
    DraftType,
    Language,
    Prospect,
    ProspectStatus,
    RiskLevel,
    now_iso,
)
from auto_client_acquisition.governance_os import policy_check_draft

# ── prospect stage → the single "next best" draft to generate ──────────────
_STAGE_PLAN: dict[str, DraftType] = {
    ProspectStatus.NEW.value: DraftType.OUTREACH_FIRST,
    ProspectStatus.QUALIFIED.value: DraftType.OUTREACH_FIRST,
    ProspectStatus.DRAFTED.value: DraftType.OUTREACH_FIRST,
    ProspectStatus.CONTACTED.value: DraftType.OUTREACH_FOLLOWUP_1,
    ProspectStatus.REPLIED.value: DraftType.DISCOVERY_INVITE,
    ProspectStatus.DISCOVERY_BOOKED.value: DraftType.DIAGNOSTIC_SUMMARY,
    ProspectStatus.PROPOSAL_SENT.value: DraftType.PAYMENT_FOLLOWUP,
    ProspectStatus.WON.value: DraftType.ONBOARDING_MESSAGE,
    ProspectStatus.NURTURE.value: DraftType.OUTREACH_FOLLOWUP_2,
    ProspectStatus.LOST.value: DraftType.BREAKUP,
}

_EVIDENCE_BY_TYPE: dict[DraftType, str] = {
    DraftType.DIAGNOSTIC_SUMMARY: "L2",
    DraftType.PROOF_PACK_INTRO: "L2",
    DraftType.ONBOARDING_MESSAGE: "L2",
    DraftType.RENEWAL_UPSELL: "L3",
}

_RISK_BY_TYPE: dict[DraftType, str] = {
    DraftType.PAYMENT_FOLLOWUP: RiskLevel.MEDIUM.value,
    DraftType.RENEWAL_UPSELL: RiskLevel.MEDIUM.value,
}


def _greeting(p: Prospect) -> str:
    return p.decision_maker.strip() or f"فريق {p.company}"


def _offer(p: Prospect, fallback: str) -> str:
    return p.offer_angle.strip() or fallback


def _pain(p: Prospect, fallback: str) -> str:
    return p.pain_hypothesis.strip() or fallback


def _outreach_first(p: Prospect) -> tuple[str, str]:
    subject = f"تشخيص مجاني لتنظيم عمليات الإيرادات — {p.company}"
    body = (
        f"مرحباً {_greeting(p)},\n\n"
        f"نساعد شركات قطاع {p.sector} في السعودية على تنظيم عمليات الإيرادات "
        "(العملاء المحتملون، المتابعات، التقارير) عبر نظام محكوم تكون فيه الموافقة البشرية أولاً.\n\n"
        f"الفرضية التي نراها: {_pain(p, 'فرص تضيع بسبب ضعف المتابعة المنظمة')}.\n"
        f"{_offer(p, 'نقترح تشخيصاً مجانياً قصيراً يوضح أين تتسرّب الفرص وكيف نعالجها خطوة بخطوة.')}\n\n"
        "هل يناسبكم لقاء عشر دقائق هذا الأسبوع، أو نرسل لكم عيّنة Proof أولاً؟\n\n"
        "تحياتي،\nفريق Dealix"
    )
    return subject, body


def _outreach_followup_1(p: Prospect) -> tuple[str, str]:
    subject = f"متابعة سريعة — {p.company}"
    body = (
        f"مرحباً {_greeting(p)},\n\n"
        "متابعة لطيفة لرسالتي السابقة. أعرف أن الجدول مزدحم، فاختصرت الفكرة:\n"
        f"- المشكلة المحتملة: {_pain(p, 'متابعات غير منظمة تؤخّر القرارات')}\n"
        f"- ما نقدّمه: {_offer(p, 'تشخيص مجاني + خطة تنفيذ أول أسبوع')}\n\n"
        "إن كان التوقيت غير مناسب الآن، أخبروني بالشهر المناسب وأعاود التواصل باحترام.\n\n"
        "تحياتي،\nفريق Dealix"
    )
    return subject, body


def _outreach_followup_2(p: Prospect) -> tuple[str, str]:
    subject = f"قيمة سريعة قبل أن نغلق الملف — {p.company}"
    body = (
        f"مرحباً {_greeting(p)},\n\n"
        "حتى لو لم يكن التوقيت مناسباً، إليكم ملاحظة قد تفيد فريقكم اليوم:\n"
        f"{_offer(p, 'نقطة واحدة عملية لتقليل تسرّب المتابعات هذا الأسبوع.')}\n\n"
        "إن رغبتم، نرسل عيّنة Proof مختصرة بدون أي التزام.\n\n"
        "تحياتي،\nفريق Dealix"
    )
    return subject, body


def _breakup(p: Prospect) -> tuple[str, str]:
    subject = f"نغلق الحلقة باحترام — {p.company}"
    body = (
        f"مرحباً {_greeting(p)},\n\n"
        "لم يصلني رد، وهذا طبيعي تماماً. سأغلق هذا الملف حالياً حتى لا أزعجكم.\n"
        "الباب مفتوح متى ما أردتم تشخيصاً مجانياً أو عيّنة Proof مستقبلاً.\n\n"
        "تحياتي،\nفريق Dealix"
    )
    return subject, body


def _discovery_invite(p: Prospect) -> tuple[str, str]:
    subject = f"شكراً لردّكم — نحجز لقاء التشخيص؟ — {p.company}"
    body = (
        f"مرحباً {_greeting(p)},\n\n"
        "سعدت بردّكم. الخطوة التالية لقاء قصير (10–15 دقيقة) نفهم فيه وضع العمليات الحالي "
        "ونحدّد أكبر فرصة سريعة.\n\n"
        f"التركيز المبدئي: {_pain(p, 'تنظيم المتابعات ورؤية الإيراد اليومية')}.\n"
        "ما هو اليوم والوقت المناسب لكم؟ أرسل لكم رابط الحجز فور تأكيدكم.\n\n"
        "تحياتي،\nفريق Dealix"
    )
    return subject, body


def _diagnostic_summary(p: Prospect) -> tuple[str, str]:
    subject = f"ملخص التشخيص والخطوات التالية — {p.company}"
    body = (
        f"مرحباً {_greeting(p)},\n\n"
        "شكراً على وقتكم في جلسة التشخيص. هذا ملخص مبدئي للمراجعة (مسودة قابلة للتعديل):\n"
        f"- أبرز نقطة تسرّب: {_pain(p, 'متابعات يدوية غير منظمة')}\n"
        f"- الفرصة السريعة: {_offer(p, 'workflow متابعة محكوم خلال 7–14 يوماً')}\n"
        "- طريقة القياس المقترحة: قبل/بعد على عدد المتابعات في الوقت.\n\n"
        "أرسل لكم Proof Pack وعرضاً مختصراً بعد موافقتكم على هذا الملخص.\n\n"
        "تحياتي،\nفريق Dealix"
    )
    return subject, body


def _proof_pack_intro(p: Prospect) -> tuple[str, str]:
    subject = f"Proof Pack مختصر — {p.company}"
    body = (
        f"مرحباً {_greeting(p)},\n\n"
        "أرفقت لكم Proof Pack مختصراً يوضح خريطة العملية الحالية، نقاط التسرّب، "
        "والفرصة المقترحة مع طريقة القياس.\n"
        "كل رقم في الحزمة مرتبط بمستوى دليل واضح (L0–L5) بدون مبالغة.\n\n"
        "بعد اطّلاعكم، نحدّد خطوة واحدة تالية فقط.\n\n"
        "تحياتي،\nفريق Dealix"
    )
    return subject, body


def _payment_followup(p: Prospect) -> tuple[str, str]:
    subject = f"متابعة العرض والخطوة التالية — {p.company}"
    body = (
        f"مرحباً {_greeting(p)},\n\n"
        "متابعة للعرض الذي شاركناه. هل لديكم أي سؤال قبل اعتماد البدء؟\n"
        "عند الموافقة، نرسل رابط الدفع الرسمي ونبدأ تنفيذ أول أسبوع مباشرة.\n\n"
        "سعدنا بالعمل معكم، وننتظر توجيهكم.\n\n"
        "تحياتي،\nفريق Dealix"
    )
    return subject, body


def _onboarding_message(p: Prospect) -> tuple[str, str]:
    subject = f"أهلاً بكم — خطة الانطلاق — {p.company}"
    body = (
        f"مرحباً {_greeting(p)},\n\n"
        "أهلاً بكم في Dealix. هذه خطة الانطلاق المختصرة:\n"
        "- الأسبوع الأول: تجهيز مصادر العملاء وتنظيم المتابعات.\n"
        "- تقرير أسبوعي واضح يوضّح التقدّم والقيمة.\n\n"
        "نحتاج فقط صلاحية الاطّلاع على مصادر العملاء الحالية للبدء.\n\n"
        "تحياتي،\nفريق Dealix"
    )
    return subject, body


def _renewal_upsell(p: Prospect) -> tuple[str, str]:
    subject = f"مراجعة القيمة والخطوة القادمة — {p.company}"
    body = (
        f"مرحباً {_greeting(p)},\n\n"
        "مرّت فترة جيدة من العمل المشترك. أقترح مراجعة سريعة للقيمة المتحققة "
        "(مبنية على أدلة فعلية) ثم نناقش الخطوة القادمة المناسبة لكم.\n\n"
        "متى يناسبكم لقاء قصير لمراجعة النتائج؟\n\n"
        "تحياتي،\nفريق Dealix"
    )
    return subject, body


_BUILDERS: dict[DraftType, Callable[[Prospect], tuple[str, str]]] = {
    DraftType.OUTREACH_FIRST: _outreach_first,
    DraftType.OUTREACH_FOLLOWUP_1: _outreach_followup_1,
    DraftType.OUTREACH_FOLLOWUP_2: _outreach_followup_2,
    DraftType.BREAKUP: _breakup,
    DraftType.DISCOVERY_INVITE: _discovery_invite,
    DraftType.DIAGNOSTIC_SUMMARY: _diagnostic_summary,
    DraftType.PROOF_PACK_INTRO: _proof_pack_intro,
    DraftType.PAYMENT_FOLLOWUP: _payment_followup,
    DraftType.ONBOARDING_MESSAGE: _onboarding_message,
    DraftType.RENEWAL_UPSELL: _renewal_upsell,
}


def build_draft(
    prospect: Prospect, draft_type: DraftType, *, created_at: str | None = None
) -> Draft:
    """Build one governed draft of ``draft_type`` for ``prospect``."""
    builder = _BUILDERS[draft_type]
    subject, body = builder(prospect)
    channel = prospect.preferred_channel or Channel.EMAIL.value
    draft = Draft(
        id=f"drf-{prospect.id}-{draft_type.value}",
        prospect_id=prospect.id,
        company=prospect.company,
        sector=prospect.sector,
        channel=channel,
        draft_type=draft_type.value,
        language=Language.AR.value,
        body=body,
        subject=subject,
        offer_angle=prospect.offer_angle,
        evidence_level=_EVIDENCE_BY_TYPE.get(draft_type, "L1"),
        risk_level=_RISK_BY_TYPE.get(draft_type, RiskLevel.LOW.value),
        approval_required=True,
        status=DraftStatus.PENDING_APPROVAL.value,
        created_at=created_at or now_iso(),
    )
    # Defence in depth: never queue a body that fails the governance gate.
    verdict = policy_check_draft(body)
    if not verdict.allowed:
        draft.status = DraftStatus.NEEDS_EDIT.value
        draft.next_action = "fix_governance_issues:" + ",".join(verdict.issues)
    return draft


def generate_drafts(prospects: list[Prospect], *, created_at: str | None = None) -> list[Draft]:
    """Generate the next-best governed draft for each prospect (deterministic)."""
    drafts: list[Draft] = []
    for p in prospects:
        draft_type = _STAGE_PLAN.get(p.status)
        if draft_type is None:
            continue
        drafts.append(build_draft(p, draft_type, created_at=created_at))
    return drafts


__all__ = ["build_draft", "generate_drafts"]
