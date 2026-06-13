"""Outreach draft factory for the Dealix launch OS.

Generates bilingual (Arabic + English) outreach drafts per channel and
runs trust preflight before returning the draft.  Drafts that fail a
hard-block rule raise :class:`TrustPreflightError` so callers never
accidentally dispatch non-compliant content.

Supported channels:
    email               Standard cold/warm email
    linkedin_manual     Manual LinkedIn DM (no automation)
    phone               Phone call script / talk-track
    whatsapp_after_consent  WhatsApp — only after explicit consent
"""
from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

from dealix.launch_os.trust_preflight import TrustViolation, run_preflight


class TrustPreflightError(ValueError):
    """Raised when a draft fails one or more block-severity trust rules."""

    def __init__(self, violations: list[TrustViolation]) -> None:
        codes = ", ".join(v.rule_id for v in violations if v.severity == "block")
        super().__init__(f"Draft blocked by trust preflight rules: {codes}")
        self.violations = violations


@dataclass
class OutreachDraft:
    """Bilingual outreach draft ready for review and dispatch.

    Attributes:
        id:               UUID string assigned at creation.
        channel:          One of email/linkedin_manual/phone/whatsapp_after_consent.
        persona_id:       Target persona slug (e.g. ``"owner_operator"``).
        subject_ar:       Arabic email/message subject.
        subject_en:       English email/message subject.
        body_ar:          Arabic message body.
        body_en:          English message body.
        cta_ar:           Arabic call-to-action line.
        cta_en:           English call-to-action line.
        requires_approval: Whether founder approval is needed before send.
        trust_score:      Count of warnings (0 = clean, warnings are not blocks).
        offer_id:         Offer identifier this draft promotes.
        account_id:       Target account identifier.
        drafted_by:       Owner/author of the draft.
        evidence_level:   Claim evidence tier (L0–L5).
        pricing_status:   Pricing approval state.
        created_at_iso:   ISO timestamp of draft creation.

    Examples:
        >>> d = OutreachDraft(
        ...     id="draft_001",
        ...     channel="email",
        ...     persona_id="owner_operator",
        ...     subject_ar="موضوع",
        ...     subject_en="Subject",
        ...     body_ar="جسم الرسالة",
        ...     body_en="Body",
        ...     cta_ar="احجز مكالمة",
        ...     cta_en="Book a call",
        ...     requires_approval=False,
        ...     trust_score=0,
        ... )
        >>> d.channel
        'email'
    """

    id: str
    channel: str
    persona_id: str
    subject_ar: str
    subject_en: str
    body_ar: str
    body_en: str
    cta_ar: str
    cta_en: str
    requires_approval: bool
    trust_score: int
    offer_id: str = ""
    account_id: str = ""
    drafted_by: str = "founder"
    evidence_level: str = "L2"
    pricing_status: str = "approved_range_required"
    created_at_iso: str = field(default_factory=lambda: datetime.now(UTC).isoformat())


# ---------------------------------------------------------------------------
# Channel templates
# ---------------------------------------------------------------------------

CHANNEL_TEMPLATES: dict[str, dict[str, str]] = {
    "email": {
        "subject_ar": "تحسين منظومة المبيعات لـ {account_name}",
        "subject_en": "Sales system improvement for {account_name}",
        "body_ar": (
            "مرحباً {contact_name},\n\n"
            "لاحظنا أن شركات في قطاع {sector} تواجه تحديات في متابعة العملاء المحتملين "
            "وتحويلهم إلى عقود فعلية.\n\n"
            "نعمل مع {offer_name} على تقليل هذه الفجوة خلال أسابيع قليلة.\n\n"
            "هل لديك 20 دقيقة هذا الأسبوع لنستعرض كيف يمكن أن ينطبق هذا على {account_name}؟"
        ),
        "body_en": (
            "Hi {contact_name},\n\n"
            "We've seen companies in the {sector} sector struggle with lead follow-up "
            "and converting opportunities into signed contracts.\n\n"
            "We work with {offer_name} to close this gap within a few weeks.\n\n"
            "Do you have 20 minutes this week to explore what this could look like for {account_name}?"
        ),
        "cta_ar": "احجز مكالمة سريعة: {cta_link}",
        "cta_en": "Book a quick call: {cta_link}",
    },
    "linkedin_manual": {
        "subject_ar": "",
        "subject_en": "",
        "body_ar": (
            "أهلاً {contact_name},\n\n"
            "أتابع عمل {account_name} في قطاع {sector} واهتم بما تحققونه.\n\n"
            "نساعد شركات مثلكم على تحسين منظومة المبيعات وتقليل تسرب الإيرادات.\n\n"
            "هل يناسبك تبادل أفكار سريع؟"
        ),
        "body_en": (
            "Hi {contact_name},\n\n"
            "I've been following {account_name}'s work in the {sector} sector — impressive trajectory.\n\n"
            "We help companies like yours improve their sales system and reduce revenue leakage.\n\n"
            "Would a quick exchange of ideas work for you?"
        ),
        "cta_ar": "يسعدني الرد على رسالتك هنا.",
        "cta_en": "Happy to continue the conversation here.",
    },
    "phone": {
        "subject_ar": "سكريبت مكالمة هاتفية",
        "subject_en": "Phone call script",
        "body_ar": (
            "مرحباً، معك {drafted_by} من Dealix.\n\n"
            "أتصل لأنني أعمل مع شركات في قطاع {sector} لتحسين منظومة متابعة العملاء.\n\n"
            "هل لديك دقيقتان لأشرح لك الفكرة؟\n\n"
            "[إذا نعم]\n"
            "نقدم {offer_name} — نبدأ بتشخيص سريع ومجاني لمنظومة المبيعات الحالية.\n\n"
            "[الهدف: حجز اجتماع اكتشافي]"
        ),
        "body_en": (
            "Hi, this is {drafted_by} from Dealix.\n\n"
            "I'm calling because we work with {sector} companies on improving lead follow-up systems.\n\n"
            "Do you have two minutes for me to explain the concept?\n\n"
            "[If yes]\n"
            "We offer {offer_name} — starting with a free quick diagnostic of the current sales setup.\n\n"
            "[Goal: book a discovery meeting]"
        ),
        "cta_ar": "هل يمكنني إرسال ملخص على البريد الإلكتروني؟",
        "cta_en": "Can I send you a short summary by email?",
    },
    "whatsapp_after_consent": {
        "subject_ar": "",
        "subject_en": "",
        "body_ar": (
            "السلام عليكم {contact_name},\n\n"
            "هذا {drafted_by} من Dealix — تواصلت معك سابقاً بخصوص {offer_name}.\n\n"
            "أردت فقط أن أتأكد أن رسالتي وصلت. هل الموضوع لا يزال يهمك؟"
        ),
        "body_en": (
            "Hello {contact_name},\n\n"
            "This is {drafted_by} from Dealix — we connected previously about {offer_name}.\n\n"
            "Just wanted to make sure my message reached you. Is this still relevant for you?"
        ),
        "cta_ar": "أخبرني وقتك المناسب.",
        "cta_en": "Let me know a convenient time.",
    },
}

_OFFER_NAMES: dict[str, dict[str, str]] = {
    "REVENUE_LEAK_AUDIT": {
        "ar": "تشخيص تسرب الإيرادات",
        "en": "Revenue Leak Audit",
    },
    "WHATSAPP_FOLLOWUP_OS": {
        "ar": "منظومة متابعة واتساب",
        "en": "WhatsApp Follow-Up OS",
    },
    "SALES_COMMAND_CENTER": {
        "ar": "مركز قيادة المبيعات",
        "en": "Sales Command Center",
    },
    "PROPOSAL_PROOF_PACK_OS": {
        "ar": "منظومة العروض والإثبات",
        "en": "Proposal & Proof Pack OS",
    },
    "AI_OPERATING_SYSTEM_FOR_SMB": {
        "ar": "نظام التشغيل بالذكاء الاصطناعي للشركات الصغيرة",
        "en": "AI Operating System for SMB",
    },
    "CUSTOM_ENTERPRISE_OS": {
        "ar": "نظام تشغيل مؤسسي مخصص",
        "en": "Custom Enterprise OS",
    },
}


def _fill(template: str, context: dict[str, str]) -> str:
    for key, value in context.items():
        template = template.replace(f"{{{key}}}", value)
    return template


def build_draft(
    account: dict[str, Any],
    offer_id: str,
    channel: str,
    *,
    drafted_by: str = "founder",
    evidence_level: str = "L2",
    pricing_status: str = "approved_range_required",
    consent_record_ref: str = "",
    persona_id: str = "owner_operator",
) -> OutreachDraft:
    """Build a bilingual outreach draft and gate it through trust preflight.

    Args:
        account:            Account dict with at least ``account_id``, optional
                            ``account_name``, ``contact_name``, ``sector``.
        offer_id:           One of the canonical offer IDs.
        channel:            One of ``email``, ``linkedin_manual``, ``phone``,
                            ``whatsapp_after_consent``.
        drafted_by:         Author identifier (default ``"founder"``).
        evidence_level:     Evidence level string L0–L5 (default ``"L2"``).
        pricing_status:     Pricing approval status.
        consent_record_ref: Required for WhatsApp channel.
        persona_id:         Target persona slug.

    Returns:
        :class:`OutreachDraft` that has passed preflight.

    Raises:
        ValueError:             If ``channel`` is not in ``CHANNEL_TEMPLATES``.
        TrustPreflightError:    If any block-severity rule fires.

    Examples:
        >>> draft = build_draft(
        ...     {"account_id": "acme_001", "account_name": "Acme Motors",
        ...      "contact_name": "Ahmed", "sector": "automotive"},
        ...     "REVENUE_LEAK_AUDIT", "email",
        ... )
        >>> draft.channel
        'email'
        >>> draft.requires_approval
        False
    """
    if channel not in CHANNEL_TEMPLATES:
        raise ValueError(f"Unknown channel: {channel!r}. Must be one of {list(CHANNEL_TEMPLATES)}")

    tmpl = CHANNEL_TEMPLATES[channel]
    offer_names = _OFFER_NAMES.get(offer_id, {"ar": offer_id, "en": offer_id})

    ctx: dict[str, str] = {
        "account_name": str(account.get("account_name", account.get("account_id", ""))),
        "contact_name": str(account.get("contact_name", "")),
        "sector": str(account.get("sector", "")),
        "offer_name": offer_names["ar"],
        "drafted_by": drafted_by,
        "cta_link": "https://dealix.sa/book",
    }
    ctx_en = dict(ctx)
    ctx_en["offer_name"] = offer_names["en"]

    subject_ar = _fill(tmpl["subject_ar"], ctx)
    subject_en = _fill(tmpl["subject_en"], ctx_en)
    body_ar = _fill(tmpl["body_ar"], ctx)
    body_en = _fill(tmpl["body_en"], ctx_en)
    cta_ar = _fill(tmpl["cta_ar"], ctx)
    cta_en = _fill(tmpl["cta_en"], ctx_en)

    requires_approval = pricing_status == "founder_approval_required"

    # Build the preflight dict using schema-compatible fields.
    preflight_dict: dict[str, Any] = {
        "channel": channel,
        "subject": subject_en,
        "body": body_en,
        "body_ar": body_ar,
        "body_en": body_en,
        "subject_ar": subject_ar,
        "subject_en": subject_en,
        "evidence_level": evidence_level,
        "drafted_by": drafted_by,
        "pricing_status": pricing_status,
        "approval_required": requires_approval,
        "consent_record_ref": consent_record_ref,
    }

    passed, violations = run_preflight(preflight_dict)
    if not passed:
        raise TrustPreflightError(violations)

    warn_count = sum(1 for v in violations if v.severity == "warn")

    return OutreachDraft(
        id=f"draft_{uuid.uuid4().hex[:12]}",
        channel=channel,
        persona_id=persona_id,
        subject_ar=subject_ar,
        subject_en=subject_en,
        body_ar=body_ar,
        body_en=body_en,
        cta_ar=cta_ar,
        cta_en=cta_en,
        requires_approval=requires_approval,
        trust_score=warn_count,
        offer_id=offer_id,
        account_id=str(account.get("account_id", "")),
        drafted_by=drafted_by,
        evidence_level=evidence_level,
        pricing_status=pricing_status,
        created_at_iso=datetime.now(UTC).isoformat(),
    )


if __name__ == "__main__":
    import doctest
    results = doctest.testmod(verbose=False)
    print(f"Outreach factory doctests: {results.attempted} run, {results.failed} failed")

    account = {
        "account_id": "smoke_motors",
        "account_name": "Smoke Motors",
        "contact_name": "Khalid",
        "sector": "automotive",
    }
    draft = build_draft(account, "REVENUE_LEAK_AUDIT", "email")
    print(f"Draft id={draft.id} channel={draft.channel} warns={draft.trust_score}")
    print(f"Subject (AR): {draft.subject_ar}")
