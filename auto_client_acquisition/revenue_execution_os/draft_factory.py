"""Draft factory — approval-first outreach / message drafts.

Every draft is created with ``status=pending_approval`` and
``approval_required=True``. Content is routed through the existing
``governance_os`` gate so a ``governance_decision`` and any issues travel with
the draft. Nothing here sends anything; it only prepares copy for the founder
to approve and copy/send manually.
"""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterable
from uuid import uuid4

from auto_client_acquisition.compliance_trust_os.approval_engine import GovernanceDecision
from auto_client_acquisition.governance_os import policy_check_draft
from auto_client_acquisition.revenue_execution_os import stores
from auto_client_acquisition.revenue_execution_os.models import (
    Channel,
    Draft,
    DraftStatus,
    DraftType,
    Prospect,
    now_iso,
)
from auto_client_acquisition.revenue_execution_os.offers import next_offer, offer_by_key

_DISCLAIMER = "القيمة التقديرية ليست قيمة مُتحقَّقة — Estimated value is not Verified value."


def assess_draft_text(text: str) -> tuple[GovernanceDecision, list[str]]:
    """Map draft copy to a governance decision + issue list (single gate call).

    - A forbidden *claim* (guarantee / fake proof) -> BLOCK.
    - Any other forbidden term / channel language -> DRAFT_ONLY.
    - Clean copy -> REQUIRE_APPROVAL (content is fine, sending still needs a human).
    """
    result = policy_check_draft(text)
    issues = list(result.issues)
    if any(i.startswith("forbidden_claim:") for i in issues):
        return GovernanceDecision.BLOCK, issues
    if issues:
        return GovernanceDecision.DRAFT_ONLY, issues
    return GovernanceDecision.REQUIRE_APPROVAL, issues


# template key -> spec. Bodies are deliberately claim-free and channel-safe.
_TEMPLATES: dict[str, dict] = {
    DraftType.OUTREACH_FIRST: {
        "channel": Channel.EMAIL,
        "evidence_level": 0,
        "value_claim": False,
        "subject": "{company} — فكرة سريعة لتقليل تسرّب الإيراد",
        "body_ar": (
            "مرحبًا {contact}،\n\n"
            "أتابع شركات في قطاع {sector} وألاحظ نمطًا متكررًا: فرص تضيع بين "
            "الاستفسار والمتابعة. أقدّم تشخيصًا مجانيًا قصيرًا يوضّح أين قد يتسرّب "
            "الإيراد لديكم وكيف يمكن معالجته.\n\n"
            "هل يناسبكم اتصال ١٥ دقيقة هذا الأسبوع؟"
        ),
        "body_en": (
            "Hi {contact},\n\n"
            "I work with {sector} teams and keep seeing the same pattern: "
            "opportunities lost between inquiry and follow-up. I offer a short, "
            "free diagnostic that shows where revenue may be leaking and how to "
            "address it.\n\n"
            "Would a 15-minute call this week work?"
        ),
    },
    DraftType.OUTREACH_FOLLOWUP_1: {
        "channel": Channel.EMAIL,
        "evidence_level": 0,
        "value_claim": False,
        "subject": "متابعة — تشخيص {company}",
        "body_ar": (
            "مرحبًا {contact}،\n\n"
            "أتابع رسالتي السابقة. التشخيص المجاني يستغرق دقائق ويعطيكم صورة واضحة "
            "عن نقاط التسرّب. أسعد بترتيب موعد قصير متى ما ناسبكم."
        ),
        "body_en": (
            "Hi {contact},\n\n"
            "Following up on my earlier note. The free diagnostic takes minutes "
            "and gives a clear picture of leak points. Happy to book a short slot "
            "whenever suits you."
        ),
    },
    DraftType.OUTREACH_FOLLOWUP_2: {
        "channel": Channel.EMAIL,
        "evidence_level": 0,
        "value_claim": False,
        "subject": "آخر متابعة — {company}",
        "body_ar": (
            "مرحبًا {contact}،\n\n"
            "لا أريد أن أزعجكم. إن كان التوقيت غير مناسب الآن، أخبروني وسأعاود "
            "التواصل لاحقًا. وإن كان هناك اهتمام، يكفي ردّ من سطر واحد."
        ),
        "body_en": (
            "Hi {contact},\n\n"
            "I don't want to crowd your inbox. If now isn't the right time, let "
            "me know and I'll circle back later. If there's interest, a one-line "
            "reply is enough."
        ),
    },
    DraftType.BREAKUP: {
        "channel": Channel.EMAIL,
        "evidence_level": 0,
        "value_claim": False,
        "subject": "أغلق الحلقة — {company}",
        "body_ar": (
            "مرحبًا {contact}،\n\n"
            "سأغلق هذه المحادثة حتى لا أكرّر التواصل. الباب مفتوح متى احتجتم "
            "مراجعة عمليات الإيراد لديكم. أتمنى لكم التوفيق."
        ),
        "body_en": (
            "Hi {contact},\n\n"
            "I'll close this thread so I'm not repeating myself. The door is open "
            "whenever you'd like to review your revenue operations. Wishing you "
            "the best."
        ),
    },
    DraftType.DISCOVERY_INVITE: {
        "channel": Channel.EMAIL,
        "evidence_level": 0,
        "value_claim": False,
        "subject": "موعد اكتشاف — {company}",
        "body_ar": (
            "شكرًا لردّكم {contact}.\n\n"
            "أقترح مكالمة اكتشاف قصيرة نفهم فيها وضعكم الحالي ونحدّد أولوية واحدة "
            "نبدأ بها. ما أنسب وقت لكم؟"
        ),
        "body_en": (
            "Thanks for replying, {contact}.\n\n"
            "Let's do a short discovery call to understand your current setup and "
            "pick one priority to start with. What time works for you?"
        ),
    },
    DraftType.DIAGNOSTIC_SUMMARY: {
        "channel": Channel.EMAIL,
        "evidence_level": 1,
        "value_claim": True,
        "subject": "ملخص التشخيص — {company}",
        "body_ar": (
            "مرحبًا {contact}،\n\n"
            "إليكم ملخص التشخيص الأولي لعمليات الإيراد. النقاط أدناه تقديرية وتعتمد "
            "على ما تمت مشاركته، وتحتاج تأكيدًا من بياناتكم قبل أي قرار:\n"
            "• أبرز نقاط التسرّب المحتملة.\n"
            "• خطوة سريعة مقترحة (Quick Win).\n"
            "• كيف نقيس الأثر لاحقًا.\n\n"
            "الخطوة التالية المقترحة: {offer_ar}."
        ),
        "body_en": (
            "Hi {contact},\n\n"
            "Here is the initial diagnostic summary for your revenue operations. "
            "The points below are estimates based on what was shared and need "
            "confirmation from your data before any decision:\n"
            "• Most likely leak points.\n"
            "• A suggested quick win.\n"
            "• How we measure impact afterwards.\n\n"
            "Suggested next step: {offer_en}."
        ),
    },
    DraftType.PROOF_PACK_INTRO: {
        "channel": Channel.EMAIL,
        "evidence_level": 2,
        "value_claim": True,
        "subject": "حزمة الإثبات — {company}",
        "body_ar": (
            "مرحبًا {contact}،\n\n"
            "أرفقت حزمة إثبات توضّح الوضع الحالي، نقاط التسرّب، والخطوة السريعة "
            "المقترحة مع طريقة القياس. الأرقام تقديرية حتى نتحقق منها معًا."
        ),
        "body_en": (
            "Hi {contact},\n\n"
            "I've attached a proof pack covering the current state, leak points, "
            "and a suggested quick win with how we'd measure it. Figures are "
            "estimates until we verify them together."
        ),
    },
    DraftType.PAYMENT_FOLLOWUP: {
        "channel": Channel.EMAIL,
        "evidence_level": 0,
        "value_claim": False,
        "subject": "تأكيد الخطوة التالية — {company}",
        "body_ar": (
            "مرحبًا {contact}،\n\n"
            "للمتابعة على ما اتفقنا عليه: بمجرد تأكيدكم نرسل رابط الدفع الرسمي "
            "ونبدأ التنفيذ. هل تودّون المضي قدمًا؟"
        ),
        "body_en": (
            "Hi {contact},\n\n"
            "Following up on what we discussed: once you confirm, we'll send the "
            "official payment link and begin. Would you like to proceed?"
        ),
    },
    DraftType.ONBOARDING_MESSAGE: {
        "channel": Channel.EMAIL,
        "evidence_level": 0,
        "value_claim": False,
        "subject": "أهلًا بكم — بدء التنفيذ {company}",
        "body_ar": (
            "مرحبًا {contact}،\n\n"
            "سعداء ببدء العمل معكم. سأشارك خطة الأسبوع الأول والوصول المطلوب، "
            "وسأرسل تقرير قيمة أسبوعيًا حتى تكون الصورة واضحة دائمًا."
        ),
        "body_en": (
            "Hi {contact},\n\n"
            "Glad to get started. I'll share the first-week plan and the access "
            "needed, and send a weekly value report so the picture stays clear."
        ),
    },
    DraftType.RENEWAL_UPSELL: {
        "channel": Channel.EMAIL,
        "evidence_level": 1,
        "value_claim": True,
        "subject": "الخطوة التالية معكم — {company}",
        "body_ar": (
            "مرحبًا {contact}،\n\n"
            "بناءً على ما أنجزناه، أرى فرصة للبناء عليه عبر {offer_ar}. "
            "الأثر المذكور تقديري ويُراجع ببياناتكم. هل نحدّد موعدًا لمناقشته؟"
        ),
        "body_en": (
            "Hi {contact},\n\n"
            "Building on what we've done, I see an opportunity to go further with "
            "{offer_en}. The impact noted is an estimate and is reviewed against "
            "your data. Shall we set a time to discuss?"
        ),
    },
}

DRAFT_TYPES: tuple[str, ...] = tuple(_TEMPLATES.keys())
# The standard cold-to-warm outreach sequence.
OUTREACH_SEQUENCE: tuple[str, ...] = (
    DraftType.OUTREACH_FIRST,
    DraftType.OUTREACH_FOLLOWUP_1,
    DraftType.OUTREACH_FOLLOWUP_2,
    DraftType.BREAKUP,
)


def _fmt(template: str, values: dict[str, str]) -> str:
    return template.format_map(defaultdict(str, values))


def _offer_for(draft_type: str, prospect: Prospect, offer_key: str | None) -> tuple[str, str]:
    if offer_key:
        try:
            o = offer_by_key(offer_key)
            return o.name_ar, o.name_en
        except KeyError:
            pass
    if draft_type == DraftType.RENEWAL_UPSELL:
        nxt = next_offer("managed_revenue_ops")
        if nxt:
            return nxt.name_ar, nxt.name_en
    entry = offer_by_key("free_diagnostic")
    return entry.name_ar, entry.name_en


def render_draft(
    prospect: Prospect,
    draft_type: str,
    *,
    channel: str | None = None,
    offer_key: str | None = None,
) -> Draft:
    """Render a single draft (pure — does not persist)."""
    spec = _TEMPLATES.get(draft_type)
    if spec is None:
        raise ValueError(f"unknown draft_type: {draft_type}")
    offer_ar, offer_en = _offer_for(draft_type, prospect, offer_key)
    values = {
        "company": prospect.company or "—",
        "contact": prospect.contact_name or "—",
        "sector": prospect.sector or "—",
        "offer_ar": offer_ar,
        "offer_en": offer_en,
    }
    subject = _fmt(str(spec["subject"]), values)
    body_ar = _fmt(str(spec["body_ar"]), values)
    body_en = _fmt(str(spec["body_en"]), values)
    if spec.get("value_claim"):
        body_ar = f"{body_ar}\n\n{_DISCLAIMER}"
        body_en = f"{body_en}\n\n{_DISCLAIMER}"
    decision, issues = assess_draft_text(f"{subject}\n{body_ar}\n{body_en}")
    ts = now_iso()
    return Draft(
        draft_id=f"drf_{uuid4().hex[:18]}",
        prospect_id=prospect.prospect_id,
        draft_type=draft_type,
        channel=channel or str(spec["channel"]),
        status=DraftStatus.PENDING_APPROVAL,
        approval_required=True,
        subject=subject,
        body_ar=body_ar,
        body_en=body_en,
        evidence_level=int(spec["evidence_level"]),
        governance_decision=str(decision),
        issues=issues,
        created_at=ts,
        updated_at=ts,
    )


def generate_draft(
    prospect: Prospect,
    draft_type: str,
    *,
    channel: str | None = None,
    offer_key: str | None = None,
) -> Draft:
    """Render + persist a single draft."""
    draft = render_draft(prospect, draft_type, channel=channel, offer_key=offer_key)
    return stores.DRAFTS.add(draft)


def generate_drafts(
    prospect: Prospect,
    draft_types: Iterable[str] | None = None,
    *,
    offer_key: str | None = None,
) -> list[Draft]:
    """Render + persist a batch of drafts for one prospect (defaults to outreach)."""
    types = tuple(draft_types) if draft_types is not None else OUTREACH_SEQUENCE
    return [generate_draft(prospect, t, offer_key=offer_key) for t in types]


__all__ = [
    "DRAFT_TYPES",
    "OUTREACH_SEQUENCE",
    "assess_draft_text",
    "generate_draft",
    "generate_drafts",
    "render_draft",
]
