"""Outreach Sequencer — multi-touch bilingual outreach sequences.

Builds deterministic, policy-compliant outreach sequences by motion.
All messages require founder approval before send (governance gate).
Hard rules: no cold WhatsApp, no automation, manual execution only.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class OutreachChannel(StrEnum):
    EMAIL = "email_warm"
    LINKEDIN = "linkedin_manual"
    WHATSAPP_WARM = "whatsapp_warm"
    PARTNER_INTRO = "partner_intro"
    IN_PERSON = "in_person"


class MotionKey(StrEnum):
    A_AGENCY = "motion_a_agency"
    B_DIRECT = "motion_b_direct"
    C_DIAGNOSTIC = "motion_c_diagnostic"
    D_EXECUTIVE = "motion_d_executive"
    E_PARTNER = "motion_e_partner"


@dataclass(frozen=True, slots=True)
class OutreachMessage:
    """A single outreach touchpoint in a sequence."""

    step_number: int
    channel: OutreachChannel
    wait_days_after_previous: int
    subject_ar: str
    subject_en: str
    body_ar: str
    body_en: str
    call_to_action_ar: str
    call_to_action_en: str
    requires_approval: bool = True  # Always True — governance gate


@dataclass(frozen=True, slots=True)
class OutreachSequence:
    """Complete multi-touch outreach sequence."""

    motion: MotionKey
    icp_tier: str
    pain_signal: str
    messages: tuple[OutreachMessage, ...]
    total_touchpoints: int
    estimated_duration_days: int
    governance_note_ar: str
    governance_note_en: str


# ─────────────────────────────────────────────────────────────────────────────
# Motion A — Agency Wedge (proof-gap pain)
# ─────────────────────────────────────────────────────────────────────────────

_MOTION_A: tuple[OutreachMessage, ...] = (
    OutreachMessage(
        step_number=1,
        channel=OutreachChannel.LINKEDIN,
        wait_days_after_previous=0,
        subject_ar="تواصل أولي — إثبات ما بعد الحملة",
        subject_en="Initial connect — post-campaign proof",
        body_ar=(
            "أهلاً {name}،\n\n"
            "لاحظت أن وكالتكم تدير حملات لعملاء متعددين — عمل مميز.\n\n"
            "سؤال مباشر: كيف تثبتون لعميلكم ماذا حدث بعد انتهاء الحملة؟ "
            "نعمل مع وكالات تحتاج هذا الدليل — وأثره مباشر على الاحتفاظ بالعميل.\n\n"
            "هل يستحق 15 دقيقة؟"
        ),
        body_en=(
            "Hello {name},\n\n"
            "I noticed your agency manages campaigns for multiple clients — impressive work.\n\n"
            "Direct question: how do you prove to your client what happened after the campaign ended? "
            "We work with agencies that need this proof — it directly impacts client retention.\n\n"
            "Worth 15 minutes?"
        ),
        call_to_action_ar="هل يمكن نتكلم 15 دقيقة هذا الأسبوع؟",
        call_to_action_en="Can we talk for 15 minutes this week?",
    ),
    OutreachMessage(
        step_number=2,
        channel=OutreachChannel.LINKEDIN,
        wait_days_after_previous=3,
        subject_ar="متابعة — ملاحظة واحدة",
        subject_en="Follow-up — one observation",
        body_ar=(
            "أهلاً {name}،\n\n"
            "متابعة لرسالتي السابقة — ملاحظة واحدة:\n\n"
            "الوكالات التي لديها دليل موثّق بعد الحملة تحتفظ بعملائها بمعدل أعلى بكثير. "
            "الفرق الوحيد: نظام تتبع ومتابعة leads.\n\n"
            "لدينا تشخيص 7 أيام يكشف هذا الرقم لوكالتكم — بـ 499 ر.س فقط.\n\n"
            "هل هذا يهمكم؟"
        ),
        body_en=(
            "Hello {name},\n\n"
            "Following up — one observation:\n\n"
            "Agencies with documented post-campaign proof retain clients at significantly higher rates. "
            "The only difference: a lead tracking and follow-up system.\n\n"
            "We have a 7-day diagnostic that reveals this number for your agency — for just 499 SAR.\n\n"
            "Does this interest you?"
        ),
        call_to_action_ar="هل تريدون أن نحسب هذا الرقم لوكالتكم؟",
        call_to_action_en="Do you want us to calculate this number for your agency?",
    ),
    OutreachMessage(
        step_number=3,
        channel=OutreachChannel.EMAIL,
        wait_days_after_previous=7,
        subject_ar="مثال Proof Pack — {company}",
        subject_en="Proof Pack example — {company}",
        body_ar=(
            "أهلاً {name}،\n\n"
            "أُشارككم مثالاً على Proof Pack كاملة بنيناها لوكالة في {city}.\n\n"
            "ماذا تحتوي:\n"
            "• تتبع كل lead بعد الحملة مع المالك والخطوة التالية\n"
            "• تقرير قيمة شهري ثنائي اللغة للعميل النهائي\n"
            "• دليل مرئي للقرارات — من وافق وماذا تغيّر\n\n"
            "التشخيص 7 أيام يبني هذا لوكالتكم.\n\n"
            "هل نتكلم هذا الأسبوع؟"
        ),
        body_en=(
            "Hello {name},\n\n"
            "Sharing a sample of a complete Proof Pack we built for an agency in {city}.\n\n"
            "What it contains:\n"
            "• Tracking every lead post-campaign with owner and next step\n"
            "• Bilingual monthly value report for the end client\n"
            "• Visual decision proof — who approved and what changed\n\n"
            "The 7-day diagnostic builds this for your agency.\n\n"
            "Shall we talk this week?"
        ),
        call_to_action_ar="احجز 30 دقيقة عرض مباشر",
        call_to_action_en="Book a 30-minute live demo",
    ),
    OutreachMessage(
        step_number=4,
        channel=OutreachChannel.LINKEDIN,
        wait_days_after_previous=7,
        subject_ar="رسالة أخيرة — القرار لكم",
        subject_en="Final message — your call",
        body_ar=(
            "أهلاً {name}،\n\n"
            "رسالة أخيرة — لا أريد أن أضيع وقتكم.\n\n"
            "إذا إثبات ما بعد الحملة لعملاؤكم لم يكن تحدياً — لا مشكلة على الإطلاق.\n"
            "إذا كان — نحن هنا.\n\n"
            "التشخيص: 499 ر.س، 7 أيام، بدون التزام."
        ),
        body_en=(
            "Hello {name},\n\n"
            "Final message — I don't want to waste your time.\n\n"
            "If post-campaign proof for your clients isn't a challenge — no problem at all.\n"
            "If it is — we're here.\n\n"
            "Diagnostic: 499 SAR, 7 days, no commitment."
        ),
        call_to_action_ar="ردّ بـ 'نعم' إذا تريدون التشخيص",
        call_to_action_en="Reply 'yes' if you want the diagnostic",
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
# Motion B — Direct B2B (pipeline-leak pain)
# ─────────────────────────────────────────────────────────────────────────────

_MOTION_B: tuple[OutreachMessage, ...] = (
    OutreachMessage(
        step_number=1,
        channel=OutreachChannel.EMAIL,
        wait_days_after_previous=0,
        subject_ar="سؤال حول pipeline {company}",
        subject_en="Question about {company}'s pipeline",
        body_ar=(
            "أهلاً {name}،\n\n"
            "سؤال مباشر من تجربتنا مع {sector} في السعودية:\n\n"
            "كم نسبة leads تدخل pipeline ولا تُتابع بشكل موثّق؟\n\n"
            "معظم الشركات في حجمكم تخسر 30-40% من leads بسبب غياب المالك الواضح والخطوة التالية.\n\n"
            "لدينا تشخيص 7 أيام يكشف هذا الرقم بدقة.\n\n"
            "هل هذا سؤال يهمكم؟"
        ),
        body_en=(
            "Hello {name},\n\n"
            "Direct question from our experience with {sector} in Saudi Arabia:\n\n"
            "What percentage of leads enter your pipeline without documented follow-up?\n\n"
            "Most companies your size lose 30-40% of leads due to unclear ownership and next steps.\n\n"
            "We have a 7-day diagnostic that reveals this number accurately.\n\n"
            "Is this a question that matters to you?"
        ),
        call_to_action_ar="رد بنعم إذا تريدون معرفة الرقم الحقيقي",
        call_to_action_en="Reply yes if you want to know the real number",
    ),
    OutreachMessage(
        step_number=2,
        channel=OutreachChannel.EMAIL,
        wait_days_after_previous=4,
        subject_ar="حساب سريع — تكلفة التسرب في {company}",
        subject_en="Quick calculation — the leak cost in {company}",
        body_ar=(
            "أهلاً {name}،\n\n"
            "حساب تقديري سريع بناءً على ما نراه في {sector}:\n\n"
            "إذا كان عندكم 50 lead شهري × متوسط صفقة 10,000 ر.س:\n"
            "• 30% تضيع بلا متابعة = 15 lead × 10,000 = 150,000 ر.س/شهر تقديراً\n"
            "• هذا ما يقارب 1.8 مليون ر.س سنوياً من الفرص غير المحوّلة\n\n"
            "التشخيص 499 ر.س يثبت (أو ينفي) هذا الرقم لفريقكم.\n\n"
            "هل هذا الحساب قريب من واقعكم؟"
        ),
        body_en=(
            "Hello {name},\n\n"
            "A quick indicative calculation based on what we see in {sector}:\n\n"
            "If you have 50 leads/month × average deal SAR 10,000:\n"
            "• 30% lost without follow-up = 15 leads × 10,000 = SAR 150,000/month estimated\n"
            "• That's approximately SAR 1.8M annually in unconverted opportunities\n\n"
            "The 499 SAR diagnostic proves (or disproves) this number for your team.\n\n"
            "Is this calculation close to your reality?"
        ),
        call_to_action_ar="شارك أرقامكم ونحسب معاً",
        call_to_action_en="Share your numbers and we calculate together",
    ),
    OutreachMessage(
        step_number=3,
        channel=OutreachChannel.LINKEDIN,
        wait_days_after_previous=7,
        subject_ar="15 دقيقة — بدون التزام",
        subject_en="15 minutes — no commitment",
        body_ar=(
            "أهلاً {name}،\n\n"
            "أقترح 15 دقيقة فقط:\n"
            "• نشاركم حساباً دقيقاً لحجم التسرب في {sector}\n"
            "• نشرح كيف يعمل التشخيص بدون تعطيل عملياتكم\n"
            "• تقررون أنتم الخطوة التالية\n\n"
            "بدون ضغط — نحن هنا لنثبت القيمة أولاً."
        ),
        body_en=(
            "Hello {name},\n\n"
            "I suggest just 15 minutes:\n"
            "• We share an accurate calculation of the leak size in {sector}\n"
            "• We explain how the diagnostic works without disrupting your operations\n"
            "• You decide the next step\n\n"
            "No pressure — we're here to prove value first."
        ),
        call_to_action_ar="احجز 15 دقيقة هذا الأسبوع",
        call_to_action_en="Book 15 minutes this week",
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
# Motion D — Executive Governance
# ─────────────────────────────────────────────────────────────────────────────

_MOTION_D: tuple[OutreachMessage, ...] = (
    OutreachMessage(
        step_number=1,
        channel=OutreachChannel.EMAIL,
        wait_days_after_previous=0,
        subject_ar="حوكمة القرار في {company}",
        subject_en="Decision governance at {company}",
        body_ar=(
            "أهلاً {name}،\n\n"
            "سؤال للقيادة التنفيذية:\n\n"
            "هل لديكم نظام يُثبت كل قرار — من اتخذه، متى، وما النتيجة؟\n\n"
            "المؤسسات التي تعمل بدون trail قرار واضح تواجه مخاطر تدقيق وبطءًا في الموافقات.\n\n"
            "لدينا تشخيص حوكمة تنفيذية — أسبوع واحد، يخرج بخريطة قرار واضحة.\n\n"
            "هل هذا يستحق 20 دقيقة؟"
        ),
        body_en=(
            "Hello {name},\n\n"
            "A question for executive leadership:\n\n"
            "Do you have a system that proves every decision — who made it, when, and what resulted?\n\n"
            "Organizations without clear decision trails face audit risk and approval bottlenecks.\n\n"
            "We offer an executive governance diagnostic — one week, exits with a clear decision map.\n\n"
            "Is this worth 20 minutes?"
        ),
        call_to_action_ar="هل تتاح 20 دقيقة هذا الأسبوع؟",
        call_to_action_en="Is 20 minutes available this week?",
    ),
    OutreachMessage(
        step_number=2,
        channel=OutreachChannel.EMAIL,
        wait_days_after_previous=5,
        subject_ar="متابعة — تكلفة غياب trail القرار",
        subject_en="Follow-up — cost of missing decision trail",
        body_ar=(
            "أهلاً {name}،\n\n"
            "متابعة — نقطة واحدة:\n\n"
            "غياب trail القرار الواضح يكلّف المؤسسات ساعات من إعادة النقاش وتأخّر القرارات.\n"
            "في الشركات التي تعمل معها — هذا يُترجَم مباشرة إلى تأخّر إيرادي.\n\n"
            "تشخيص أسبوع واحد يقيس هذا بدقة ويعطيكم خطة إصلاح.\n\n"
            "هل نحجز 20 دقيقة؟"
        ),
        body_en=(
            "Hello {name},\n\n"
            "One follow-up point:\n\n"
            "Absent decision trails cost organizations hours of re-discussion and delayed approvals.\n"
            "In the companies we work with — this translates directly into revenue delay.\n\n"
            "A one-week diagnostic measures this accurately and gives you a remediation plan.\n\n"
            "Shall we book 20 minutes?"
        ),
        call_to_action_ar="احجز جلسة 20 دقيقة",
        call_to_action_en="Book a 20-minute session",
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
# Sequence registry
# ─────────────────────────────────────────────────────────────────────────────

_SEQUENCES: dict[MotionKey, tuple[OutreachMessage, ...]] = {
    MotionKey.A_AGENCY: _MOTION_A,
    MotionKey.B_DIRECT: _MOTION_B,
    MotionKey.C_DIAGNOSTIC: _MOTION_B,
    MotionKey.D_EXECUTIVE: _MOTION_D,
    MotionKey.E_PARTNER: _MOTION_A,
}

_GOVERNANCE_NOTE_AR = (
    "كل رسالة تحتاج موافقة المؤسس قبل الإرسال — لا إرسال تلقائي. "
    "مسودة فقط حتى تُمنح الموافقة الصريحة."
)
_GOVERNANCE_NOTE_EN = (
    "Every message requires founder approval before sending — no automatic sending. "
    "Draft only until explicit approval is granted."
)


def build_sequence(
    motion: MotionKey,
    icp_tier: str = "",
    pain_signal: str = "",
) -> OutreachSequence:
    """Build a complete multi-touch outreach sequence.

    Args:
        motion: GTM motion key.
        icp_tier: ICP segment label for metadata.
        pain_signal: Primary pain signal for context.

    Returns:
        OutreachSequence with all touchpoints and governance metadata.
    """
    messages = _SEQUENCES.get(motion, _MOTION_B)
    total_days = sum(m.wait_days_after_previous for m in messages)

    return OutreachSequence(
        motion=motion,
        icp_tier=icp_tier,
        pain_signal=pain_signal,
        messages=messages,
        total_touchpoints=len(messages),
        estimated_duration_days=total_days,
        governance_note_ar=_GOVERNANCE_NOTE_AR,
        governance_note_en=_GOVERNANCE_NOTE_EN,
    )


def list_available_motions() -> list[MotionKey]:
    return list(MotionKey)


__all__ = [
    "MotionKey",
    "OutreachChannel",
    "OutreachMessage",
    "OutreachSequence",
    "build_sequence",
    "list_available_motions",
]
