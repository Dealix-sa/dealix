"""
Warm Intro Generator — Draft first-touch messages for human approval.
مولّد الرسائل الترحيبية — يُعدّ مسودات الرسائل الأولى للموافقة البشرية.

CONSTITUTIONAL: NO_LIVE_SEND enforced.
All drafts queued for founder review — NOTHING is sent automatically.
The founder approves and sends manually via their channel of choice.
"""

from __future__ import annotations

import json
import logging
import os
import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any, Literal

log = logging.getLogger(__name__)

Channel = Literal["whatsapp", "email", "linkedin"]

# ── Constitutional gate ───────────────────────────────────────────
_NO_LIVE_SEND = True  # Immutable — never set False


@dataclass
class ProspectContext:
    company_name: str
    contact_name: str = ""
    sector: str = "other"
    pain_point: str = ""
    signal: str = ""  # why_now signal (e.g. "hiring", "funding", "new office")
    channel: Channel = "whatsapp"
    locale: str = "ar"
    account_id: str = field(default_factory=lambda: str(uuid.uuid4()))


@dataclass
class WarmIntroDraft:
    draft_id: str
    account_id: str
    channel: Channel
    subject: str | None  # for email only
    body: str
    locale: str
    variant: int  # 1-5
    status: str = "pending_approval"  # pending_approval | approved | rejected
    generated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def to_dict(self) -> dict[str, Any]:
        return {
            "draft_id": self.draft_id,
            "account_id": self.account_id,
            "channel": self.channel,
            "subject": self.subject,
            "body": self.body,
            "locale": self.locale,
            "variant": self.variant,
            "status": self.status,
            "generated_at": self.generated_at.isoformat(),
        }


@dataclass
class WarmIntroDraftBundle:
    bundle_id: str
    account_id: str
    company_name: str
    drafts: list[WarmIntroDraft]
    constitutional_note: str = "NO_LIVE_SEND: جميع المسودات تتطلب موافقة الفاوندر قبل الإرسال"
    generated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def to_dict(self) -> dict[str, Any]:
        return {
            "bundle_id": self.bundle_id,
            "account_id": self.account_id,
            "company_name": self.company_name,
            "drafts": [d.to_dict() for d in self.drafts],
            "constitutional_note": self.constitutional_note,
            "generated_at": self.generated_at.isoformat(),
            "pending_approval_count": sum(1 for d in self.drafts if d.status == "pending_approval"),
        }


# ── Hardcoded WhatsApp variant templates (Arabic-first, compact) ──
_WHATSAPP_TEMPLATES: list[dict[str, str]] = [
    {
        "variant": 1,
        "label": "المشكلة المحددة",
        "template_ar": "أهلاً {name}، أنا سامي من Dealix.\n\nلاحظت أن {company} في قطاع {sector_ar} — كثير من الشركات في قطاعكم تخسر صفقات بسبب تأخر الرد على العملاء.\n\nعندنا برنامج تجريبي 7 أيام يثبت نتيجة قابلة للقياس.\n\nهل يناسبك 15 دقيقة هذا الأسبوع؟",
        "template_en": "Hi {name}, I'm Sami from Dealix.\n\nI noticed {company} is in the {sector_en} space — many companies there lose deals from slow follow-up.\n\nWe have a 7-day pilot that proves measurable results.\n\nCan we find 15 minutes this week?",
    },
    {
        "variant": 2,
        "label": "الفرصة التنافسية",
        "template_ar": "مرحباً {name}،\n\nرأيت {company} في السوق — الشركات التي تحل مشكلة الرد السريع الآن ستكون في موقع تنافسي أقوى خلال 6 أشهر.\n\nDealix يساعد شركات {sector_ar} السعودية على هذا بالضبط.\n\nهل تريد أرى كيف؟",
        "template_en": "Hi {name},\n\nSaw {company} in the market — companies solving fast-response now will have a competitive edge in 6 months.\n\nDealix helps Saudi {sector_en} companies do exactly this.\n\nWant to see how?",
    },
    {
        "variant": 3,
        "label": "الإشارة التوقيتية",
        "template_ar": "أهلاً {name}،\n\n{signal_text}\n\nهذا الوقت المناسب لوضع نظام يتابع العملاء المحتملين تلقائياً مع الحفاظ على اللمسة الشخصية.\n\nDealix جرّبناه مع شركات {sector_ar} — هل نكلم؟",
        "template_en": "Hi {name},\n\n{signal_text}\n\nThis is the right time to put a system that follows up leads automatically while keeping the personal touch.\n\nDealix — proven with {sector_en} companies. Want to talk?",
    },
    {
        "variant": 4,
        "label": "قصة Dealix نفسها",
        "template_ar": "مرحباً {name}،\n\nنحن في Dealix نستخدم نظامنا لتنمية أعمالنا — هذه الرسالة نفسها جُهّزت بمساعدة الذكاء الاصطناعي وراجعتها أنا شخصياً قبل الإرسال.\n\nنُثبت له تأثيراً على {company} في 7 أيام.\n\nهل نجرّب؟",
        "template_en": "Hi {name},\n\nAt Dealix we use our own system to grow — this very message was drafted with AI and I reviewed it personally before sending.\n\nWe can prove its impact on {company} in 7 days.\n\nShall we try?",
    },
    {
        "variant": 5,
        "label": "السؤال المباشر",
        "template_ar": "أهلاً {name}، سؤال مباشر:\n\nما هي أكبر مشكلة في متابعة العملاء المحتملين في {company} الآن؟\n\nأسأل لأن Dealix بنيناه خصيصاً لحل هذه المشاكل في السوق السعودي.",
        "template_en": "Hi {name}, direct question:\n\nWhat's the biggest challenge with lead follow-up at {company} right now?\n\nI ask because Dealix was built specifically to solve these for the Saudi market.",
    },
]

_EMAIL_TEMPLATES: list[dict[str, str]] = [
    {
        "variant": 1,
        "subject_ar": "فكرة لـ {company} — 5 دقائق",
        "subject_en": "An idea for {company} — 5 minutes",
        "template_ar": "أهلاً {name}،\n\nأتواصل معك لأن {company} في قطاع {sector_ar} وهذا بالضبط المجال الذي يُحقق فيه عملاؤنا أفضل النتائج.\n\nمشكلة المتابعة اليدوية للعملاء المحتملين تكلّف شركات مثل شركتك صفقات كل شهر.\n\nبرنامج التجربة لدينا (7 أيام، 499 ريال) يُثبت نتيجة قابلة للقياس أو نُكرر مجاناً.\n\nهل تتاح لك 15 دقيقة هذا الأسبوع؟\n\nبالتوفيق،\nسامي\nDealix",
        "template_en": "Hi {name},\n\nI'm reaching out because {company} is in the {sector_en} space — exactly where our clients see the best results.\n\nManual lead follow-up costs companies like yours deals every month.\n\nOur 7-day proof sprint (499 SAR) delivers a measurable result or we repeat for free.\n\nAre you available for 15 minutes this week?\n\nBest,\nSami\nDealix",
    },
    {
        "variant": 2,
        "subject_ar": "سؤال سريع عن {company}",
        "subject_en": "Quick question about {company}",
        "template_ar": "أهلاً {name}،\n\nسؤال مباشر: كم صفقة تقديرياً تخسرون شهرياً بسبب تأخر الرد على العملاء؟\n\nDealix حل هذه المشكلة لشركات {sector_ar} في السوق السعودي بنتائج قابلة للقياس.\n\nهل نكلم 15 دقيقة؟",
        "template_en": "Hi {name},\n\nDirect question: how many deals do you estimate you lose monthly from slow lead response?\n\nDealix solved this for Saudi {sector_en} companies with measurable results.\n\nCan we speak for 15 minutes?",
    },
    {
        "variant": 3,
        "subject_ar": "Dealix × {company} — فرصة للتجربة",
        "subject_en": "Dealix × {company} — pilot opportunity",
        "template_ar": "أهلاً {name}،\n\nنُقدم لشركات {sector_ar} السعودية برنامج تجربة 7 أيام (499 ريال) يُثبت:\n• تسريع الرد على العملاء المحتملين\n• متابعة منتظمة دون جهد يدوي\n• نتيجة قابلة للقياس في أسبوع\n\nهل {company} مهتمة بالتجربة؟",
        "template_en": "Hi {name},\n\nWe offer Saudi {sector_en} companies a 7-day pilot (499 SAR) that proves:\n• Faster lead response\n• Consistent follow-up with no manual effort\n• Measurable result in one week\n\nIs {company} interested in a pilot?",
    },
]


def _signal_text(signal: str, locale: str) -> str:
    signals = {
        "hiring": {
            "ar": "لاحظت أن {company} يبدو أنها تتوسع (توظيف جديد)",
            "en": "{company} appears to be expanding (new hires)",
        },
        "funding": {
            "ar": "تهانينا على التمويل الجديد لـ {company}",
            "en": "Congrats on the recent funding for {company}",
        },
        "new_office": {
            "ar": "لاحظت افتتاح {company} فرع جديد",
            "en": "Noticed {company} opened a new office",
        },
        "event": {
            "ar": "رأيت {company} في الفعالية مؤخراً",
            "en": "Saw {company} at the recent event",
        },
    }
    key = locale if locale in ("ar", "en") else "ar"
    template = signals.get(signal, {}).get(key, "")
    return template


async def generate_warm_intros(ctx: ProspectContext, num_variants: int = 5) -> WarmIntroDraftBundle:
    """
    Generate warm intro drafts for human approval.
    Returns a bundle of drafts — ALL pending_approval, NOTHING sent.

    Constitutional: NO_LIVE_SEND = True (cannot be changed here)
    """
    assert _NO_LIVE_SEND, "NO_LIVE_SEND gate violated — this should never happen"

    from auto_client_acquisition.revenue_memory.events import EVENT_TYPES

    sector_info_map = {
        "marketing_agency": ("وكالة تسويق", "Marketing Agency"),
        "consulting": ("استشارات", "Consulting"),
        "real_estate": ("عقارات", "Real Estate"),
        "logistics": ("لوجستيات", "Logistics"),
        "events": ("فعاليات", "Events"),
        "training": ("تدريب", "Training"),
        "other": ("خدمات B2B", "B2B Services"),
    }
    sector_ar, sector_en = sector_info_map.get(ctx.sector, ("خدمات B2B", "B2B Services"))
    name = ctx.contact_name or "مدير {company}".format(company=ctx.company_name) if ctx.locale == "ar" else ctx.contact_name or ctx.company_name
    signal_text = _signal_text(ctx.signal, ctx.locale).format(company=ctx.company_name) if ctx.signal else ""

    drafts: list[WarmIntroDraft] = []

    if ctx.channel == "whatsapp":
        templates = _WHATSAPP_TEMPLATES[:num_variants]
        for tpl in templates:
            key = "template_ar" if ctx.locale == "ar" else "template_en"
            body = tpl[key].format(
                name=name,
                company=ctx.company_name,
                sector_ar=sector_ar,
                sector_en=sector_en,
                signal_text=signal_text or f"أهلاً بك في {ctx.company_name}",
            )
            drafts.append(WarmIntroDraft(
                draft_id=str(uuid.uuid4()),
                account_id=ctx.account_id,
                channel="whatsapp",
                subject=None,
                body=body,
                locale=ctx.locale,
                variant=tpl["variant"],
                status="pending_approval",
            ))
    else:  # email
        templates = _EMAIL_TEMPLATES[:min(num_variants, 3)]
        for tpl in templates:
            key_subj = "subject_ar" if ctx.locale == "ar" else "subject_en"
            key_body = "template_ar" if ctx.locale == "ar" else "template_en"
            subject = tpl[key_subj].format(company=ctx.company_name)
            body = tpl[key_body].format(
                name=name,
                company=ctx.company_name,
                sector_ar=sector_ar,
                sector_en=sector_en,
            )
            drafts.append(WarmIntroDraft(
                draft_id=str(uuid.uuid4()),
                account_id=ctx.account_id,
                channel="email",
                subject=subject,
                body=body,
                locale=ctx.locale,
                variant=tpl["variant"],
                status="pending_approval",
            ))

    bundle = WarmIntroDraftBundle(
        bundle_id=str(uuid.uuid4()),
        account_id=ctx.account_id,
        company_name=ctx.company_name,
        drafts=drafts,
    )

    # Persist drafts to JSONL (message.drafted events)
    _save_drafts(bundle)

    log.info(
        "Warm intro bundle generated: bundle_id=%s company=%s channel=%s variants=%d",
        bundle.bundle_id,
        ctx.company_name,
        ctx.channel,
        len(drafts),
    )
    return bundle


def _save_drafts(bundle: WarmIntroDraftBundle) -> None:
    try:
        outbox_dir = os.path.join(os.path.dirname(__file__), "..", "..", "data", "outbox")
        os.makedirs(outbox_dir, exist_ok=True)
        path = os.path.join(outbox_dir, "warm_intros.jsonl")
        with open(path, "a", encoding="utf-8") as f:
            f.write(json.dumps(bundle.to_dict(), ensure_ascii=False) + "\n")
    except Exception as exc:
        log.warning("Could not save warm intro bundle: %s", exc)
