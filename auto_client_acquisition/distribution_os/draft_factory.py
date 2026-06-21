"""Draft Factory — deterministic, bilingual, approval-first outreach drafts.

Every draft is generated through the quality gate and carries a
``governance_status``. The factory has NO capability to send: drafts only ever
move between ``generated`` / ``pending_approval`` / ``needs_edit`` /
``approved`` / ``rejected`` / ``copied_manually`` / ``replied`` / ``archived``.
External sending stays a manual, founder-controlled action (doctrine: no
external sends in v1; all drafts pending approval).
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import StrEnum
from typing import Any
from uuid import uuid4

from auto_client_acquisition.distribution_os import catalog
from auto_client_acquisition.distribution_os._store import JsonlStore, now_iso
from auto_client_acquisition.distribution_os.draft_quality import check_draft
from auto_client_acquisition.distribution_os.prospect import Prospect


class DraftType(StrEnum):
    OUTREACH_FIRST = "outreach_first"
    OUTREACH_FOLLOWUP_1 = "outreach_followup_1"
    OUTREACH_FOLLOWUP_2 = "outreach_followup_2"
    BREAKUP = "breakup"
    DISCOVERY_INVITE = "discovery_invite"
    DIAGNOSTIC_SUMMARY = "diagnostic_summary"
    PROPOSAL_INTRO = "proposal_intro"
    PROOF_PACK_INTRO = "proof_pack_intro"
    PAYMENT_FOLLOWUP = "payment_followup"
    ONBOARDING_MESSAGE = "onboarding_message"
    RENEWAL_UPSELL = "renewal_upsell"


class DraftStatus(StrEnum):
    GENERATED = "generated"
    PENDING_APPROVAL = "pending_approval"
    APPROVED = "approved"
    REJECTED = "rejected"
    NEEDS_EDIT = "needs_edit"
    COPIED_MANUALLY = "copied_manually"
    SENT_VIA_INTEGRATION = "sent_via_integration"  # reserved; never set by AI in v1
    REPLIED = "replied"
    ARCHIVED = "archived"


_VALID_CHANNELS: frozenset[str] = frozenset({"email", "whatsapp", "linkedin", "phone", "proposal"})

# Deterministic, safe templates. {company} {pain} {offer} {dm} placeholders.
# No guaranteed-outcome language; framed as a respectful founder note.
_TEMPLATES_AR: dict[str, tuple[str, str]] = {
    DraftType.OUTREACH_FIRST.value: (
        "{company} — فكرة سريعة حول {pain}",
        "مرحباً {dm}،\n\nلاحظت أن {company} قد تواجه {pain}. نساعد شركات مشابهة عبر "
        "{offer} لترتيب البيانات وتوضيح الفرص دون أي التزام مبكر.\n\nهل يناسبك نقاش "
        "قصير 15 دقيقة هذا الأسبوع؟",
    ),
    DraftType.OUTREACH_FOLLOWUP_1.value: (
        "متابعة — {company}",
        "مرحباً {dm}،\n\nأتابع رسالتي السابقة حول {pain}. أرسل لك ملخصاً موجزاً عن "
        "{offer} إن رغبت — بدون أي إلزام.",
    ),
    DraftType.OUTREACH_FOLLOWUP_2.value: (
        "خطوة بسيطة — {company}",
        "مرحباً {dm}،\n\nإن كان التوقيت غير مناسب الآن، يمكننا البدء بخطوة صغيرة عبر "
        "{offer} لقياس الأثر أولاً.",
    ),
    DraftType.BREAKUP.value: (
        "أغلق الملف؟ — {company}",
        "مرحباً {dm}،\n\nلم يصلني رد، وهذا مفهوم تماماً. سأغلق المتابعة الآن وأبقى متاحاً "
        "متى ما رغبت بالعودة لموضوع {pain}.",
    ),
    DraftType.DISCOVERY_INVITE.value: (
        "دعوة لجلسة اكتشاف — {company}",
        "مرحباً {dm}،\n\nشكراً لردك. أقترح جلسة اكتشاف قصيرة لفهم {pain} بشكل أدق قبل "
        "اقتراح أي نطاق عمل.",
    ),
    DraftType.DIAGNOSTIC_SUMMARY.value: (
        "ملخص التشخيص — {company}",
        "مرحباً {dm}،\n\nهذا ملخص أولي لما رصدناه حول {pain}، مع الخطوة المقترحة التالية "
        "عبر {offer}. الأرقام تقديرية حتى نتحقق من بياناتكم.",
    ),
    DraftType.PROPOSAL_INTRO.value: (
        "مقترح مبدئي — {company}",
        "مرحباً {dm}،\n\nأرفق مقترحاً مبدئياً يغطي {pain} عبر {offer}، مع النطاق والمدة "
        "والسعر المرجعي. النطاق قابل للنقاش قبل أي التزام.",
    ),
    DraftType.PROOF_PACK_INTRO.value: (
        "حزمة إثبات — {company}",
        "مرحباً {dm}،\n\nأشارك معك حزمة إثبات توضح العملية الحالية ونقاط التسرّب وفرصة "
        "مكسب سريع، مع طريقة القياس المقترحة.",
    ),
    DraftType.PAYMENT_FOLLOWUP.value: (
        "متابعة الإجراء — {company}",
        "مرحباً {dm}،\n\nأتابع بخصوص الخطوة التالية بعد الموافقة على المقترح. أنا جاهز "
        "لأي توضيح يخص النطاق أو الجدول.",
    ),
    DraftType.ONBOARDING_MESSAGE.value: (
        "بداية التشغيل — {company}",
        "مرحباً {dm}،\n\nأهلاً بكم. سنبدأ بترتيب الوصول للبيانات وتحديد أول workflow "
        "ومؤشر النجاح للأسبوع الأول.",
    ),
    DraftType.RENEWAL_UPSELL.value: (
        "الخطوة التالية — {company}",
        "مرحباً {dm}،\n\nبعد نتائج المرحلة الحالية، أقترح مناقشة {offer} كخطوة تالية "
        "لتوسيع الأثر — فقط بعد مراجعة الأرقام معكم.",
    ),
}

_TEMPLATES_EN: dict[str, tuple[str, str]] = {
    DraftType.OUTREACH_FIRST.value: (
        "{company} — a quick idea on {pain}",
        "Hi {dm},\n\nI noticed {company} may be dealing with {pain}. We help similar "
        "companies through {offer} to organise data and surface opportunities, with no "
        "early commitment.\n\nWould a short 15-minute chat this week work?",
    ),
    DraftType.OUTREACH_FOLLOWUP_1.value: (
        "Following up — {company}",
        "Hi {dm},\n\nFollowing up on my note about {pain}. Happy to send a brief summary "
        "of {offer} if useful — no obligation.",
    ),
    DraftType.OUTREACH_FOLLOWUP_2.value: (
        "A simple first step — {company}",
        "Hi {dm},\n\nIf now isn't the right time, we can start small with {offer} to "
        "measure impact first.",
    ),
    DraftType.BREAKUP.value: (
        "Close the loop? — {company}",
        "Hi {dm},\n\nI haven't heard back, which is completely fine. I'll close the "
        "follow-up for now and stay available whenever {pain} is worth revisiting.",
    ),
    DraftType.DISCOVERY_INVITE.value: (
        "Discovery session invite — {company}",
        "Hi {dm},\n\nThanks for replying. I'd suggest a short discovery session to "
        "understand {pain} before proposing any scope.",
    ),
    DraftType.DIAGNOSTIC_SUMMARY.value: (
        "Diagnostic summary — {company}",
        "Hi {dm},\n\nHere is an initial summary of what we observed about {pain}, with a "
        "suggested next step via {offer}. Figures are estimates until we verify your data.",
    ),
    DraftType.PROPOSAL_INTRO.value: (
        "Draft proposal — {company}",
        "Hi {dm},\n\nAttached is a draft proposal covering {pain} via {offer}, with scope, "
        "timeline, and a reference price. Scope is open to discussion before any commitment.",
    ),
    DraftType.PROOF_PACK_INTRO.value: (
        "Proof pack — {company}",
        "Hi {dm},\n\nSharing a proof pack outlining the current process, leakage points, "
        "and a quick win, with the proposed measurement method.",
    ),
    DraftType.PAYMENT_FOLLOWUP.value: (
        "Next-step follow-up — {company}",
        "Hi {dm},\n\nFollowing up on the next step after proposal approval. Happy to "
        "clarify anything on scope or timeline.",
    ),
    DraftType.ONBOARDING_MESSAGE.value: (
        "Kickoff — {company}",
        "Hi {dm},\n\nWelcome aboard. We'll start by arranging data access and defining the "
        "first workflow and a week-one success metric.",
    ),
    DraftType.RENEWAL_UPSELL.value: (
        "The next step — {company}",
        "Hi {dm},\n\nAfter this phase's results, I'd suggest discussing {offer} as a next "
        "step to expand impact — only after we review the numbers together.",
    ),
}


@dataclass
class Draft:
    id: str = field(default_factory=lambda: f"draft_{uuid4().hex[:12]}")
    prospect_id: str = ""
    draft_type: str = DraftType.OUTREACH_FIRST.value
    channel: str = "email"
    locale: str = "ar"
    subject: str = ""
    body: str = ""
    status: str = DraftStatus.GENERATED.value
    governance_status: str = "pending_approval"
    quality_issues: list[str] = field(default_factory=list)
    evidence_level: int = 0
    product_id: str = ""
    created_at: str = field(default_factory=now_iso)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


_store = JsonlStore(env_var="DEALIX_DRAFTS_PATH", default_rel="var/drafts.jsonl", id_field="id")


def _resolve_offer_label(prospect: Prospect, locale: str) -> tuple[str, str]:
    """Return ``(offer_label, product_id)`` from the prospect's offer angle."""
    product = catalog.product_by_id(prospect.offer_angle)
    if product is None:
        # offer_angle may be free text; keep label, no product link
        return (prospect.offer_angle or ("خدماتنا" if locale == "ar" else "our service"), "")
    label = product.name_ar if locale == "ar" else product.name_en
    return (label, product.id)


def generate_draft(
    *,
    prospect: Prospect,
    draft_type: str | DraftType,
    channel: str | None = None,
    locale: str = "ar",
) -> Draft:
    """Generate one draft, run it through the quality gate, and persist it."""
    dtype = draft_type.value if isinstance(draft_type, DraftType) else str(draft_type)
    if dtype not in {d.value for d in DraftType}:
        raise ValueError(f"invalid_draft_type:{dtype}")
    chan = channel or prospect.preferred_channel
    if chan not in _VALID_CHANNELS:
        raise ValueError(f"invalid_channel:{chan}")
    locale = "en" if locale == "en" else "ar"

    templates = _TEMPLATES_EN if locale == "en" else _TEMPLATES_AR
    subject_tpl, body_tpl = templates[dtype]
    offer_label, product_id = _resolve_offer_label(prospect, locale)
    fields = {
        "company": prospect.company or ("شركتكم" if locale == "ar" else "your company"),
        "pain": prospect.pain_hypothesis
        or ("التحدي الحالي" if locale == "ar" else "the current challenge"),
        "offer": offer_label,
        "dm": prospect.decision_maker or ("there" if locale == "en" else "فريقكم الكريم"),
    }
    subject = subject_tpl.format(**fields)
    body = body_tpl.format(**fields)

    quality = check_draft(text=body, channel=chan)
    draft = Draft(
        prospect_id=prospect.id,
        draft_type=dtype,
        channel=chan,
        locale=locale,
        subject=subject,
        body=body,
        status=quality.governance_status,
        governance_status=quality.governance_status,
        quality_issues=list(quality.issues),
        evidence_level=prospect.evidence_level,
        product_id=product_id,
    )
    _store.append(draft.to_dict())
    return draft


def get_draft(draft_id: str) -> Draft | None:
    rec = _store.get(draft_id)
    return Draft(**rec) if rec else None


def list_drafts(*, status: str | None = None, prospect_id: str | None = None) -> list[Draft]:
    latest: dict[str, dict[str, Any]] = {}
    for rec in _store.list():
        latest[str(rec.get("id"))] = rec
    drafts = [Draft(**rec) for rec in latest.values()]
    if status is not None:
        drafts = [d for d in drafts if d.status == status]
    if prospect_id is not None:
        drafts = [d for d in drafts if d.prospect_id == prospect_id]
    return drafts


def approve_draft(draft_id: str) -> Draft | None:
    """Approve a draft for manual sending. Refuses blocked / needs-edit drafts."""
    draft = get_draft(draft_id)
    if draft is None:
        return None
    if (
        draft.governance_status != "pending_approval"
        or draft.status != DraftStatus.PENDING_APPROVAL.value
    ):
        raise ValueError(f"cannot_approve_draft_in_status:{draft.status}/{draft.governance_status}")
    rec = _store.patch(draft_id, {"status": DraftStatus.APPROVED.value})
    return Draft(**rec) if rec else None


def reject_draft(draft_id: str, reason: str = "") -> Draft | None:
    rec = _store.patch(
        draft_id,
        {
            "status": DraftStatus.REJECTED.value,
            "quality_issues": [f"rejected:{reason}"] if reason else [],
        },
    )
    return Draft(**rec) if rec else None


def request_edit(draft_id: str, note: str = "") -> Draft | None:
    rec = _store.patch(
        draft_id,
        {"status": DraftStatus.NEEDS_EDIT.value, "governance_status": "needs_edit"},
    )
    return Draft(**rec) if rec else None


def mark_copied(draft_id: str) -> Draft | None:
    """Founder copied the approved draft to send it manually."""
    draft = get_draft(draft_id)
    if draft is None:
        return None
    if draft.status not in {DraftStatus.APPROVED.value, DraftStatus.PENDING_APPROVAL.value}:
        raise ValueError(f"cannot_mark_copied_in_status:{draft.status}")
    rec = _store.patch(draft_id, {"status": DraftStatus.COPIED_MANUALLY.value})
    return Draft(**rec) if rec else None


def clear_for_test() -> None:
    _store.clear_for_test()


__all__ = [
    "Draft",
    "DraftStatus",
    "DraftType",
    "approve_draft",
    "clear_for_test",
    "generate_draft",
    "get_draft",
    "list_drafts",
    "mark_copied",
    "reject_draft",
    "request_edit",
]
