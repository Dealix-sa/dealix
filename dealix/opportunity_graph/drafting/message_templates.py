"""Segment-based outreach templates (AR + EN). Draft-only, no fake claims.

Every template uses hypothesis language ("we expect" / "نتوقع"), never
guarantees, and never pretends a prior relationship. Email variants include an
opt-out line. Templates are plain ``str.format`` strings keyed by segment.
"""

from __future__ import annotations

from dealix.opportunity_graph.schemas import Channel, Language, Segment

# Default per-segment channel + recommended language.
SEGMENT_DEFAULTS: dict[Segment, tuple[Channel, Language]] = {
    "foreign_saas_ai_entering_saudi": ("linkedin", "en"),
    "foreign_supplier_needing_distributor": ("email", "en"),
    "saudi_clinic_revenue_leak": ("whatsapp_manual", "ar"),
    "saudi_training_or_b2b_service_growth": ("whatsapp_manual", "ar"),
    "b2g_readiness_candidate": ("email", "en"),
    "rhq_vendor_or_partner_candidate": ("linkedin", "en"),
    "event_expo_tourism_supplier": ("email", "en"),
    "not_fit": ("linkedin", "ar"),
}

_OPT_OUT_EN = "\n\nIf this isn't relevant, reply 'stop' and I won't follow up."
_OPT_OUT_AR = "\n\nإذا لم يكن هذا مناسبًا، ردّوا بكلمة «إيقاف» ولن نتابع."

# {company}, {persona}, {signal}, {pain} are filled per company.
_TEMPLATES: dict[Segment, dict[Language, str]] = {
    "foreign_saas_ai_entering_saudi": {
        "en": (
            "Hi {persona} — I noticed {company}'s signal around Saudi/MENA ({signal}). "
            "Before heavy setup or hiring, we run a 14-day Saudi Opportunity Command Room: "
            "target accounts, partner candidates, fit scoring, and a decision memo. "
            "We expect it to de-risk your entry. Open to a 15-min look?"
        ),
        "ar": (
            "مرحبًا {persona} — لاحظت اهتمام {company} بالسوق السعودي ({signal}). "
            "قبل الإنفاق على التأسيس والتوظيف، نجهّز غرفة قيادة فرص لمدة ١٤ يومًا: "
            "حسابات مستهدفة، شركاء محتملون، تقييم ملاءمة، ومذكرة قرار. "
            "نتوقع أن تقلّل مخاطر دخولكم. هل يناسبكم اطلاع ١٥ دقيقة؟"
        ),
    },
    "foreign_supplier_needing_distributor": {
        "en": (
            "Hi {persona} — for {company}, entering Saudi usually needs the right distributor/partner. "
            "We map partner candidates and readiness in a 14-day sprint, drafts included for your approval. "
            "We expect a shortlist you can act on. Worth a short call?"
        ),
        "ar": (
            "مرحبًا {persona} — دخول {company} للسعودية يحتاج غالبًا الموزّع/الشريك المناسب. "
            "نرسم مرشحي الشراكة والجاهزية في ١٤ يومًا مع مسودات للاعتماد. "
            "نتوقع قائمة قابلة للتنفيذ. هل نرتّب مكالمة قصيرة؟"
        ),
    },
    "saudi_clinic_revenue_leak": {
        "ar": (
            "مرحبًا {persona} — في {company}، كثير من العيادات تفقد مواعيد ومتابعات "
            "بسبب تشتت الواتساب والردود المتأخرة ({pain}). "
            "نجهّز Revenue Leak Scanner: أين تضيع الفرص وكيف نستعيدها — بمسودات متابعة تعتمدونها. "
            "نتوقع صورة أوضح خلال أيام. هل نبدأ بتشخيص؟"
        ),
        "en": (
            "Hi {persona} — clinics like {company} often lose bookings and follow-ups to scattered WhatsApp ({pain}). "
            "Our Revenue Leak Scanner shows where opportunities leak and how to recover them, with approval-ready drafts. "
            "We expect a clearer picture in days. Start with a diagnostic?"
        ),
    },
    "saudi_training_or_b2b_service_growth": {
        "ar": (
            "مرحبًا {persona} — في {company}، الاستفسارات والعروض تحتاج انضباط متابعة ({pain}). "
            "نبني غرفة قيادة إيراد يومية: تقرير للفرص، مسودات متابعة معتمدة، وProof Pack أسبوعي. "
            "نتوقع استعادة فرص متأخرة. هل نرتّب ١٠ دقائق؟"
        ),
        "en": (
            "Hi {persona} — {company}'s inquiries and proposals need follow-up discipline ({pain}). "
            "We build a daily revenue command room: opportunity report, approved drafts, weekly proof pack. "
            "We expect to recover stalled deals. 10 minutes?"
        ),
    },
    "b2g_readiness_candidate": {
        "en": (
            "Hi {persona} — for {company}, Saudi B2G opportunities reward readiness ({signal}). "
            "We prepare a readiness checklist, target map, and decision memo in a 14-day sprint. "
            "We expect a clearer path to qualification. Open to a short call?"
        ),
        "ar": (
            "مرحبًا {persona} — فرص القطاع الحكومي في السعودية تكافئ الجاهزية ({signal}). "
            "نجهّز قائمة جاهزية وخريطة استهداف ومذكرة قرار في ١٤ يومًا. "
            "نتوقع مسارًا أوضح للتأهل. هل نرتّب مكالمة قصيرة؟"
        ),
    },
    "rhq_vendor_or_partner_candidate": {
        "en": (
            "Hi {persona} — {company} looks like a strong partner/vendor candidate for our Saudi clients ({signal}). "
            "We run one pilot per client, drafts approved before anything is sent. "
            "We expect a clean pilot fit. Worth 15 minutes?"
        ),
        "ar": (
            "مرحبًا {persona} — {company} تبدو مرشحًا قويًا للشراكة مع عملائنا في السعودية ({signal}). "
            "نبدأ بتجربة واحدة لكل عميل، والمسودات تُعتمد قبل أي إرسال. "
            "نتوقع ملاءمة جيدة. هل ١٥ دقيقة تناسبكم؟"
        ),
    },
    "event_expo_tourism_supplier": {
        "en": (
            "Hi {persona} — with {company}'s event/expo activity in Saudi ({signal}), timing matters. "
            "We prepare a target map and approval-ready outreach so your team acts before the event. "
            "We expect faster qualified conversations. Short call?"
        ),
        "ar": (
            "مرحبًا {persona} — مع نشاط {company} في الفعاليات بالسعودية ({signal})، التوقيت مهم. "
            "نجهّز خريطة استهداف ومسودات جاهزة للاعتماد قبل الحدث. "
            "نتوقع محادثات مؤهلة أسرع. مكالمة قصيرة؟"
        ),
    },
    "not_fit": {
        "ar": (
            "مرحبًا {persona} — نساعد شركات B2B على تحويل المتابعة المشتّتة إلى غرفة قيادة يومية. "
            "إذا كان هناك اهتمام مستقبلي بالسوق السعودي، يسعدنا التواصل."
        ),
        "en": (
            "Hi {persona} — we help B2B companies turn scattered follow-up into a daily command room. "
            "If Saudi market interest comes up later, happy to connect."
        ),
    },
}

# Optional follow-up + phone-script scaffolds (approval-gated like all drafts).
_FOLLOWUP: dict[Language, str] = {
    "ar": (
        "متابعة قصيرة — لا أريد أن أزعجكم. إن كان التوقيت غير مناسب الآن، "
        "أخبروني بالوقت الأفضل وسأعاود لاحقًا."
    ),
    "en": (
        "Quick follow-up — I don't want to crowd your inbox. If now isn't right, "
        "tell me a better time and I'll circle back."
    ),
}

_PHONE_SCRIPT: dict[Language, str] = {
    "ar": (
        "افتتاحية: عرّف نفسك وسبب المكالمة في جملة.\n"
        "السؤال: «كيف تتابعون العملاء الجدد اليوم؟»\n"
        "الجسر: اربط الألم بـ Revenue Command Room.\n"
        "الطلب: اقترح تشخيصًا قصيرًا — لا التزام."
    ),
    "en": (
        "Open: one-line intro + reason for the call.\n"
        "Ask: 'How do you follow up with new leads today?'\n"
        "Bridge: connect the pain to the Revenue Command Room.\n"
        "Ask: propose a short diagnostic — no commitment."
    ),
}


def render_message(
    *,
    segment: Segment,
    language: Language,
    channel: Channel,
    company: str,
    persona: str,
    signal: str,
    pain: str,
) -> str:
    seg_templates = _TEMPLATES.get(segment, _TEMPLATES["not_fit"])
    template = seg_templates.get(language) or next(iter(seg_templates.values()))
    body = template.format(
        company=company or ("الشركة" if language == "ar" else "your team"),
        persona=persona or ("فريقكم" if language == "ar" else "there"),
        signal=signal or ("إشارة السوق" if language == "ar" else "your market signal"),
        pain=pain or ("متابعة مشتّتة" if language == "ar" else "scattered follow-up"),
    )
    if channel == "email":
        body += _OPT_OUT_AR if language == "ar" else _OPT_OUT_EN
    return body.strip()


def render_followup(language: Language) -> str:
    return _FOLLOWUP.get(language, _FOLLOWUP["en"])


def render_phone_script(language: Language) -> str:
    return _PHONE_SCRIPT.get(language, _PHONE_SCRIPT["en"])
