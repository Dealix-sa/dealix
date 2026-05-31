"""Call Script OS — generates call briefs, opening lines, objection handlers, and outcome templates."""
from __future__ import annotations

import logging

from auto_client_acquisition.omni_channel_os.schemas import (
    AssetType,
    BuyerPersona,
    ChannelAsset,
    ChannelType,
    Company,
    Language,
    RiskLevel,
)

log = logging.getLogger(__name__)

_NO_AUTO_SEND = True

_OPENING_LINES: dict[str, str] = {
    "ar": (
        "السلام عليكم، معك Sami من Dealix.\n"
        "أشتغل على أنظمة AI Workflow للشركات، خصوصًا للعمليات التي فيها تقارير ومتابعة يدوية.\n"
        "أردت فقط أعرف من الشخص المناسب عندكم لموضوع تحسين workflows أو التحول الرقمي؟"
    ),
    "en": (
        "Hi, this is Sami from Dealix.\n"
        "I work with GCC companies on AI workflow automation — specifically operations with "
        "repetitive reporting or manual follow-up.\n"
        "I wanted to find out who would be the right person to speak with about "
        "workflow improvement or digital transformation?"
    ),
}

_OBJECTION_HANDLERS: dict[str, dict[str, str]] = {
    "ar": {
        "لسنا مستعدين": (
            "أفهم تماماً. في الواقع كثير من الشركات التي عملنا معها قالت نفس الشيء في البداية. "
            "المرحلة الأولى ليست تطبيق كامل — بل تشخيص مجاني على مسار واحد لتحديد إذا كان "
            "AI مناسباً أصلاً. لا التزام، ولا تغيير في الأنظمة الحالية."
        ),
        "ليس وقت مناسب": (
            "أفهم — الجدول مشغول دائماً. لهذا السبب نبدأ بـ 20 دقيقة فقط لتحديد إذا كان "
            "هناك فرصة تستحق الوقت. إذا لم يكن مناسباً بعد ذلك — لا مشكلة. "
            "هل يناسبك نهاية هذا الأسبوع أو بداية الأسبوع القادم؟"
        ),
        "عندنا نظام": (
            "ممتاز — هذا يسهل الأمور. Dealix لا يستبدل الأنظمة الحالية، بل يضيف طبقة "
            "AI Workflow فوقها لأتمتة المهام المتكررة التي يتركها النظام الحالي بدون حل. "
            "هل يمكنني أسأل أي نظام تستخدمون الآن؟"
        ),
        "ما نحتاج AI": (
            "سؤال وجيه. في الواقع ليس كل شركة تحتاج AI الآن. لهذا نبدأ بتشخيص — "
            "إذا لم نجد مساراً يستحق الأتمتة، سنقول ذلك بصراحة. "
            "هل يمكنني أسألك عن أصعب مهمة متكررة في فريقكم الآن؟"
        ),
        "غالي": (
            "أتفهم القلق من التكلفة. نبدأ بـ pilot مجاني على مسار واحد — "
            "بدون تكلفة مسبقة. إذا رأيتم قيمة واضحة، نناقش التوسع. "
            "إذا لم تروا قيمة — لا يوجد التزام. هل يناسبكم هذا النهج؟"
        ),
    },
    "en": {
        "not_ready": (
            "I completely understand. Many companies we work with said the same thing initially. "
            "The first step is not a full implementation — it is a free diagnostic on one workflow "
            "to determine if AI is even appropriate. No commitment, no changes to existing systems."
        ),
        "bad_timing": (
            "I understand — schedules are always busy. That is why we start with just 20 minutes "
            "to determine if there is an opportunity worth your time. If not — no problem. "
            "Would end of this week or early next week work?"
        ),
        "have_a_system": (
            "Great — that actually makes things easier. Dealix does not replace existing systems. "
            "It adds an AI workflow layer on top to automate repetitive tasks the current system "
            "leaves unsolved. May I ask which system you are using?"
        ),
        "dont_need_ai": (
            "Fair question. Not every company needs AI right now. That is why we start with a "
            "diagnostic — if we do not find a workflow worth automating, we will say so honestly. "
            "May I ask what the most repetitive task in your team is right now?"
        ),
        "too_expensive": (
            "I understand the cost concern. We start with a free pilot on one workflow — "
            "no upfront cost. If you see clear value, we discuss scaling. "
            "If not — no commitment. Does that approach work for you?"
        ),
    },
}

_OUTCOME_TEMPLATE = (
    "Call Outcome Log\n"
    "================\n"
    "Date: [DATE]\n"
    "Company: [COMPANY]\n"
    "Contact: [CONTACT_NAME] | [CONTACT_TITLE]\n"
    "Call Duration: [DURATION] min\n\n"
    "Outcome: [ ] Interested — next step: [NEXT_STEP]\n"
    "         [ ] Not interested — reason: [REASON]\n"
    "         [ ] Callback requested — date: [CALLBACK_DATE]\n"
    "         [ ] Wrong person — referred to: [REFERRAL_NAME]\n\n"
    "Notes:\n[NOTES]\n\n"
    "Follow-up action: [ACTION]\n"
    "Deadline: [DEADLINE]\n"
)


class CallScriptOS:
    """Generates call scripts with briefs, openers, objection handlers, and outcome logs."""

    _NO_AUTO_SEND = True

    def generate_script(
        self,
        company: Company,
        persona: BuyerPersona,
        offer: object,
    ) -> ChannelAsset:
        """Generates full call script."""
        assert _NO_AUTO_SEND, "_NO_AUTO_SEND gate violated"

        lang = company.language
        sector = company.sector.value
        opener = self.opening_line(company, lang)
        handlers = self.objection_handlers(sector, lang)
        outcome = self.outcome_template()

        if lang == Language.arabic:
            handlers_text = "\n".join(
                f"الاعتراض: {obj}\nالرد: {handler}\n"
                for obj, handler in handlers.items()
            )
            body = (
                f"مختصر المكالمة:\n"
                f"الشركة: {company.name}\n"
                f"القطاع: {sector}\n"
                f"المسمى الوظيفي المستهدف: {persona.typical_titles[0] if persona.typical_titles else 'المدير'}\n\n"
                f"جملة الافتتاح:\n{opener}\n\n"
                f"معالجة الاعتراضات:\n{handlers_text}\n"
                f"نموذج نتيجة المكالمة:\n{outcome}"
            )
            cta = "جدولة المكالمة"
            hook = f"سكريبت مكالمة — {company.name}"
        else:
            handlers_text = "\n".join(
                f"Objection: {obj}\nResponse: {handler}\n"
                for obj, handler in handlers.items()
            )
            body = (
                f"Call Brief:\n"
                f"Company: {company.name}\n"
                f"Sector: {sector}\n"
                f"Target Title: {persona.typical_titles[0] if persona.typical_titles else 'Manager'}\n\n"
                f"Opening Line:\n{opener}\n\n"
                f"Objection Handlers:\n{handlers_text}\n"
                f"Outcome Template:\n{outcome}"
            )
            cta = "Schedule call"
            hook = f"Call script — {company.name}"

        log.debug(
            "call_script_os.generate_script company_id=%s lang=%s",
            company.id,
            lang.value,
        )

        return ChannelAsset(
            company_id=company.id,
            asset_type=AssetType.call_script,
            channel=ChannelType.phone_call,
            language=lang,
            subject_or_hook=hook,
            body=body,
            cta=cta,
            is_auto_sendable=False,
            requires_founder_approval=True,
            risk_level=RiskLevel.medium,
            approval_status="approval_required",
            sector=company.sector.value,
            country=company.country.value,
        )

    def call_brief(self, company: Company, persona: BuyerPersona) -> dict:
        """One-page call brief: company context, decision maker, likely objections."""
        return {
            "company_name": company.name,
            "sector": company.sector.value,
            "country": company.country.value,
            "decision_maker_title": persona.typical_titles[0] if persona.typical_titles else "",
            "pain_points": persona.pain_points[:3],
            "decision_style": persona.decision_style,
            "likely_objections": list(
                _OBJECTION_HANDLERS.get(
                    "ar" if company.language == Language.arabic else "en", {}
                ).keys()
            )[:3],
            "language": company.language.value,
        }

    def opening_line(self, company: Company, language: Language) -> str:
        """Returns the opening line for a cold call."""
        key = "ar" if language == Language.arabic else "en"
        return _OPENING_LINES[key]

    def objection_handlers(self, sector: str, language: Language) -> dict[str, str]:
        """Returns objection-handler dict for the given language."""
        key = "ar" if language == Language.arabic else "en"
        return dict(_OBJECTION_HANDLERS[key])

    def outcome_template(self) -> str:
        """Returns the blank call outcome log template."""
        return _OUTCOME_TEMPLATE


__all__ = ["CallScriptOS"]
