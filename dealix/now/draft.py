"""Outreach draft writer for the Dealix Now engine (Draft Writer Agent).

Produces an Arabic, approval-first outreach draft per ``os/01_CLAUDE.md``
"Outreach Writing Rules":
  - <= 150 words
  - mentions the company name at least once
  - exactly ONE specific pain
  - exactly ONE CTA (a single question)
  - NO pricing (no digits, no SAR/ريال/price words)
  - no "نحن شركة رائدة" / overclaim, no service list

Drafts are only generated for high + medium tiers (``next_action == "draft"``).
nurture / disqualified rows get ``None``.

``status`` is the literal string ``"draft — awaiting founder approval"``.

Pure and deterministic: no network, no API keys, no LLM. Dealix never sends.
"""

from __future__ import annotations

DRAFT_STATUS = "draft — awaiting founder approval"

_CONTACT_NOTE_AR = "أضف بريد جهة الاتصال المعتمد قبل الإرسال — Dealix لا يرسل تلقائيًا."

# Tiers that receive a draft (next_action == "draft").
_DRAFTABLE_TIERS = frozenset({"high", "medium"})

# Per-offer Arabic templates. Each yields (subject, body). Templates state a
# single pain and end with exactly one question (the only "?" in the body).
# No digits, no price words, no service lists, no "رائدة"/overclaim.
#
# Placeholders:
#   {company}      -> company name (mentioned >= 1)
#   {contact}      -> "[اسم جهة الاتصال]" placeholder the founder fills in
_CONTACT_PLACEHOLDER = "[اسم جهة الاتصال]"


def _tmpl_ret(company: str) -> tuple[str, str]:
    subject = f"متابعة قرار التشغيل المستمر — {company}"
    body = (
        f"أهلاً {_CONTACT_PLACEHOLDER}،\n\n"
        f"بعد التشخيص السابق مع {company}، لاحظنا أن متابعة تقارير العمليات يدويًا "
        "لا تزال تأخذ وقتًا من فريقكم كل أسبوع.\n\n"
        "نقترح تحويل ذلك إلى تشغيل شهري يحدّث التقارير ويتابع الـ SLA للشحنات "
        "تلقائيًا — أنتم تراجعون، والنظام يجهّز. لا إرسال آلي لأي شيء.\n\n"
        "هل يناسبكم وقت قصير هذا الأسبوع لمراجعة خطة التشغيل المستمر؟"
    )
    return subject, body


def _tmpl_pcos(company: str) -> tuple[str, str]:
    subject = f"تسرّب فوترة أوامر التغيير — {company}"
    body = (
        f"السلام عليكم {_CONTACT_PLACEHOLDER}،\n\n"
        f"في مكاتب هندسية بحجم {company}، يتسرّب جزء من الإيراد عند عدم ربط "
        "أوامر التغيير بالفوترة في وقتها.\n\n"
        "نبني نظامًا يتتبع كل change order من الطلب حتى الفوترة، وينبّه قبل أن "
        "يضيع. تبقى الموافقة النهائية على كل خطوة لفريقكم.\n\n"
        "هل نأخذ workflow واحدًا كمثال في مكالمة قصيرة ونريكم أين يظهر التسرّب؟"
    )
    return subject, body


def _tmpl_agp(company: str) -> tuple[str, str]:
    subject = f"جاهزية ZATCA Wave 24 قبل الموعد — {company}"
    body = (
        f"السلام عليكم {_CONTACT_PLACEHOLDER}،\n\n"
        "مع اقتراب موعد ZATCA المقبل والتزامات PDPL على البيانات الحساسة، "
        f"تحتاج {company} إطار حوكمة واضحًا لأي أتمتة تمسّ بيانات العملاء.\n\n"
        "نجهّز سياسة استخدام، مصفوفة صلاحيات، وبوابات موافقة بشرية — بحيث "
        "تتحركون بأمان قبل الموعد.\n\n"
        "هل نحجز وقتًا قصيرًا لمراجعة وضعكم الحالي؟"
    )
    return subject, body


def _tmpl_raos(company: str) -> tuple[str, str]:
    subject = f"تسرّب الفرص بعد الديمو — {company}"
    body = (
        f"السلام عليكم {_CONTACT_PLACEHOLDER}،\n\n"
        f"تخسر {company} جزءًا من الفرص بعد الديمو بسبب ضعف المتابعة المنظّمة.\n\n"
        "نجهّز تسلسل متابعة ومسودات تواصل مخصّصة لكل فرصة — أنتم تراجعون "
        "وترسلون، بدون أي إرسال آلي.\n\n"
        "هل نراجع معكم تسلسل المتابعة الحالي في مكالمة قصيرة؟"
    )
    return subject, body


def _tmpl_mios(company: str) -> tuple[str, str]:
    subject = f"متابعة بلاغات الصيانة والـ SLA — {company}"
    body = (
        f"السلام عليكم {_CONTACT_PLACEHOLDER}،\n\n"
        f"في عمليات الصيانة الميدانية بحجم {company}، تأخّر إشعارات تجاوز "
        "الـ SLA يكلّف وقتًا ورضا عملاء.\n\n"
        "نبني نظامًا يستقبل البلاغات ويتابع الـ SLA ويولّد تقارير الإغلاق "
        "تلقائيًا، مع إبقاء القرار التشغيلي لفريقكم.\n\n"
        "هل نأخذ مسار بلاغ واحدًا كمثال في مكالمة قصيرة؟"
    )
    return subject, body


def _tmpl_ecc(company: str) -> tuple[str, str]:
    subject = f"رؤية تنفيذية موحّدة عبر الأقسام — {company}"
    body = (
        f"السلام عليكم {_CONTACT_PLACEHOLDER}،\n\n"
        f"في مجموعة بحجم {company}، يتأخّر وصول صورة الأداء والمخاطر كاملةً "
        "إلى الإدارة بسبب تجميع التقارير يدويًا.\n\n"
        "نبني لوحة تنفيذية تجمع تقارير الأقسام والمخاطر وتحدّث نفسها، مع "
        "إبقاء القرار للإدارة.\n\n"
        "هل نراجع معكم أهم قسمين تريدون توحيد رؤيتهما أولًا؟"
    )
    return subject, body


def _tmpl_wfa(company: str) -> tuple[str, str]:
    subject = f"تدقيق workflow واحد منخفض المخاطر — {company}"
    body = (
        f"السلام عليكم {_CONTACT_PLACEHOLDER}،\n\n"
        f"تعتمد عمليات {company} على خطوات يدوية متكررة تستهلك وقت الفريق "
        "أسبوعيًا.\n\n"
        "نقترح البدء بتدقيق workflow واحد فقط: نحلل الخطوات ونطلع خريطة فرص "
        "عملية خلال أيام، قبل أي التزام أكبر.\n\n"
        "هل تحدّدون لنا أكثر workflow يدوي يرهق الفريق لنبدأ منه؟"
    )
    return subject, body


_TEMPLATES = {
    "RET": _tmpl_ret,
    "PCOS": _tmpl_pcos,
    "AGP": _tmpl_agp,
    "RAOS": _tmpl_raos,
    "MIOS": _tmpl_mios,
    "ECC": _tmpl_ecc,
    "WFA": _tmpl_wfa,
}


def _word_count(text: str) -> int:
    return len(text.split())


def write_outreach_draft(target: dict, score: dict, offer: dict) -> dict | None:
    """Build an Arabic approval-first outreach draft, or ``None``.

    Returns ``None`` for nurture / disqualified tiers (no draft). Otherwise
    returns the draft dict with ``status == DRAFT_STATUS``, a single-question
    body, no pricing, and a contact stub the founder fills before sending.
    """
    tier = (score.get("tier") or "").strip().lower()
    if tier not in _DRAFTABLE_TIERS:
        return None

    company = (target.get("company_name") or "").strip()
    offer_id = str(offer.get("id") or "WFA")
    builder = _TEMPLATES.get(offer_id, _TEMPLATES["WFA"])
    subject, body = builder(company)

    lead_id = str(target.get("id") or "")
    draft_id = (
        lead_id.replace("lead_", "draft_", 1) if lead_id.startswith("lead_") else f"draft_{lead_id}"
    )

    return {
        "id": draft_id,
        "lead_id": lead_id,
        "company_name": company,
        "channel": "email",
        "lang": "ar",
        "offer_id": offer_id,
        "subject": subject,
        "body": body,
        "word_count": _word_count(body),
        "status": DRAFT_STATUS,
        "contact": {"to": "", "note_ar": _CONTACT_NOTE_AR},
    }


__all__ = ["DRAFT_STATUS", "write_outreach_draft"]
