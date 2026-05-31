"""Content Engine — generates SEO articles, LinkedIn posts, and case study drafts."""
from __future__ import annotations

import logging
from itertools import cycle

from auto_client_acquisition.omni_channel_os.schemas import (
    AssetType,
    ChannelAsset,
    ChannelType,
    Language,
    RiskLevel,
)

log = logging.getLogger(__name__)

_NO_AUTO_SEND = True
_REQUIRES_REVIEW = True

CONTENT_TOPICS: dict[str, list[str]] = {
    "ar": [
        "كيف تستخدم الشركات الخليجية AI بدون تعريض بياناتها للخطر؟",
        "ما الفرق بين chatbot و agentic workflow؟",
        "كيف تقلل شركات الصيانة تقارير SLA اليدوية؟",
        "كيف تستفيد مكاتب المحاماة من AI بدون المساس بسرية العميل؟",
        "كيف تبدأ AI Workflow Audit خلال 7 أيام؟",
        "5 workflows تستحق الأتمتة في شركات الخليج",
        "لماذا فشلت كثير من مشاريع AI في المنطقة؟",
        "الفرق بين RPA وAI Agent — أيهما يناسب شركتك؟",
    ],
    "en": [
        "How GCC Companies Use AI Without Exposing Their Data",
        "Chatbot vs. Agentic Workflow: What's the Difference?",
        "How FM Companies Can Eliminate Manual SLA Reports with AI",
        "AI for Legal Document Workflows in Saudi Arabia",
        "5 Workflows Worth Automating in GCC Operations",
        "Why Most GCC AI Projects Fail (and How to Avoid It)",
        "From Pilot to Production: Scaling AI Workflows in the GCC",
    ],
}

_AR_POST_TEMPLATES: list[str] = [
    (
        "أغلب الشركات لا تحتاج chatbot.\n"
        "تحتاج workflow ذكي:\n"
        "• يفهم الطلب\n"
        "• يجمع البيانات الناقصة\n"
        "• يصنف الحالة\n"
        "• يجهز التقرير\n"
        "• ويرفع القرار للمسؤول\n"
        "هذا الفرق بين استخدام AI كشات، واستخدامه كنظام تشغيل."
    ),
    (
        "كيف تعرف إذا كان AI مناسباً لعملياتكم؟\n"
        "ثلاثة أسئلة:\n"
        "1. هل تكررون نفس المهمة أكثر من 10 مرات أسبوعياً؟\n"
        "2. هل النتيجة قابلة للتحقق من إنسان؟\n"
        "3. هل البيانات المطلوبة موجودة بالفعل في أنظمتكم؟\n"
        "إذا كانت إجاباتكم نعم على الثلاثة — لديكم workflow جاهز للأتمتة."
    ),
    (
        "أكثر خطأ شائع في مشاريع AI في الشركات:\n"
        "البدء بالتقنية بدلاً من المشكلة.\n\n"
        "الترتيب الصحيح:\n"
        "1. حدد المشكلة التشغيلية أولاً\n"
        "2. ارسم الـ workflow الحالي\n"
        "3. حدد أين تحتاج قراراً بشرياً\n"
        "4. ثم اختر التقنية\n\n"
        "التقنية تخدم العملية — وليس العكس."
    ),
]

_EN_POST_TEMPLATES: list[str] = [
    (
        "Most companies do not need another chatbot.\n"
        "They need controlled AI workflows:\n"
        "• intake to classification\n"
        "• missing data request\n"
        "• report generation\n"
        "• human approval\n"
        "That is where agentic AI becomes operational, not experimental."
    ),
    (
        "Three questions to know if AI fits your operations:\n"
        "1. Do you repeat the same task more than 10 times a week?\n"
        "2. Can a human verify the output?\n"
        "3. Is the required data already in your systems?\n"
        "If yes to all three — you have a workflow ready to automate."
    ),
    (
        "The most common mistake in corporate AI projects:\n"
        "Starting with the technology instead of the problem.\n\n"
        "The correct order:\n"
        "1. Define the operational problem first\n"
        "2. Map the current workflow\n"
        "3. Identify where a human decision is needed\n"
        "4. Then choose the technology\n\n"
        "Technology serves the process — not the other way around."
    ),
]

_CASE_STUDY_TEMPLATES: dict[str, dict[str, str]] = {
    "legal": {
        "ar": (
            "دراسة حالة — مكتب محاماة (مجهول الهوية)\n\n"
            "التحدي:\n"
            "كان الفريق يقضي ساعات يومياً في البحث في ملفات القضايا وتتبع المراسلات مع العملاء.\n\n"
            "الحل:\n"
            "تطبيق AI Workflow يصنف المستندات، يبحث فيها، ويجهز ملخصاً لكل قضية للمراجعة البشرية.\n\n"
            "النتيجة المتوقعة:\n"
            "تقليل وقت البحث في الملفات، وتحسين متابعة العملاء — مع موافقة بشرية كاملة.\n\n"
            "ملاحظة: هذه دراسة حالة توضيحية — أرقام الأداء الفعلية تعتمد على حالة كل شركة."
        ),
        "en": (
            "Case Study — Law Firm (Anonymized)\n\n"
            "Challenge:\n"
            "The team spent hours daily searching case files and tracking client correspondence.\n\n"
            "Solution:\n"
            "An AI Workflow that classifies documents, searches them, and prepares a case summary for human review.\n\n"
            "Expected outcome:\n"
            "Reduced file search time and improved client follow-up — with full human oversight.\n\n"
            "Note: This is an illustrative case study — actual performance figures depend on each company's situation."
        ),
    },
    "facilities_management": {
        "ar": (
            "دراسة حالة — شركة FM (مجهولة الهوية)\n\n"
            "التحدي:\n"
            "فريق العمليات يعمل على إعداد تقارير SLA يدوياً من بيانات متفرقة في أنظمة مختلفة.\n\n"
            "الحل:\n"
            "AI Workflow يجمع البيانات، يصنف البلاغات، ويجهز تقرير SLA للمراجعة.\n\n"
            "النتيجة المتوقعة:\n"
            "تقليل الوقت المستغرق في إعداد التقارير وتحسين الاستجابة لتجاوزات الـ SLA.\n\n"
            "ملاحظة: هذه دراسة حالة توضيحية."
        ),
        "en": (
            "Case Study — FM Company (Anonymized)\n\n"
            "Challenge:\n"
            "Operations team manually compiling SLA reports from scattered data across multiple systems.\n\n"
            "Solution:\n"
            "AI Workflow that aggregates data, classifies tickets, and prepares the SLA report for review.\n\n"
            "Expected outcome:\n"
            "Reduced report preparation time and faster response to SLA breaches.\n\n"
            "Note: This is an illustrative case study."
        ),
    },
    "default": {
        "ar": (
            "دراسة حالة — شركة خليجية (مجهولة الهوية)\n\n"
            "التحدي:\n"
            "عمليات تشغيلية متكررة تستهلك وقتاً كبيراً من الفريق.\n\n"
            "الحل:\n"
            "AI Workflow يأتمت المهام المتكررة مع موافقة بشرية في النقاط الحرجة.\n\n"
            "النتيجة المتوقعة:\n"
            "تحرير وقت الفريق للعمل على المهام عالية القيمة.\n\n"
            "ملاحظة: هذه دراسة حالة توضيحية."
        ),
        "en": (
            "Case Study — GCC Company (Anonymized)\n\n"
            "Challenge:\n"
            "Repetitive operational processes consuming significant team time.\n\n"
            "Solution:\n"
            "AI Workflow automating repetitive tasks with human approval at critical decision points.\n\n"
            "Expected outcome:\n"
            "Freeing team time for high-value work.\n\n"
            "Note: This is an illustrative case study."
        ),
    },
}

_MINI_FRAMEWORK_TEMPLATES: dict[str, dict[str, str]] = {
    "ar": {
        "hook": "إطار عمل: كيف تقيّم أي workflow لـ AI في 5 دقائق؟",
        "body": (
            "إطار 3-2-1:\n"
            "• 3 مرات يُكرر في الأسبوع على الأقل\n"
            "• 2 خطوة قابلة للتوثيق بشكل واضح\n"
            "• 1 نقطة قرار بشري واضحة\n\n"
            "إذا توفر الثلاثة — الـ workflow مناسب للـ AI pilot."
        ),
    },
    "en": {
        "hook": "Framework: How to evaluate any workflow for AI in 5 minutes",
        "body": (
            "The 3-2-1 framework:\n"
            "• Repeats at least 3 times per week\n"
            "• Has 2 clearly documentable steps\n"
            "• Has 1 clear human decision point\n\n"
            "If all three apply — the workflow is ready for an AI pilot."
        ),
    },
}

_NEWSLETTER_SEGMENTS: dict[str, dict[str, str]] = {
    "legal": {
        "ar": (
            "للقانونيين هذا الشهر:\n"
            "أكثر سؤال يطرحه مكاتب المحاماة: كيف نستخدم AI بدون المساس بسرية العميل؟\n\n"
            "الجواب في ثلاث نقاط:\n"
            "1. البيانات لا تغادر بيئتكم المحلية\n"
            "2. كل قرار يمر عبر مراجعة بشرية\n"
            "3. النظام يساعد — لا يستبدل الحكم القانوني\n\n"
            "إذا أردتم مزيداً من التفاصيل — نبذة مخصصة متاحة."
        ),
        "en": (
            "For legal professionals this month:\n"
            "The most common question from law firms: how do we use AI without risking client confidentiality?\n\n"
            "The answer in three points:\n"
            "1. Data stays within your local environment\n"
            "2. Every decision passes through human review\n"
            "3. The system assists — it does not replace legal judgment\n\n"
            "A customized overview is available on request."
        ),
    },
    "default": {
        "ar": (
            "هذا الشهر في Dealix:\n"
            "نعمل مع شركات خليجية على تحويل أصعب workflows إلى مسارات ذكية.\n"
            "إذا كان عندكم workflow يستهلك وقتاً — يسعدني التشخيص معكم مجاناً."
        ),
        "en": (
            "This month at Dealix:\n"
            "We are working with GCC companies on turning their most time-consuming workflows into intelligent processes.\n"
            "If you have a workflow that is consuming team time — happy to run a free diagnostic."
        ),
    },
}

_ar_topic_cycle = cycle(CONTENT_TOPICS["ar"])
_en_topic_cycle = cycle(CONTENT_TOPICS["en"])


class ContentEngine:
    """Generates daily posts, article outlines, case studies, and newsletter segments."""

    _NO_AUTO_SEND = True
    _REQUIRES_REVIEW = True

    def daily_posts(self, n_ar: int = 3, n_en: int = 2) -> list[ChannelAsset]:
        """Generate n_ar Arabic + n_en English LinkedIn posts for the day."""
        assert _NO_AUTO_SEND, "_NO_AUTO_SEND gate violated"
        assets: list[ChannelAsset] = []
        ar_pool = cycle(_AR_POST_TEMPLATES)
        en_pool = cycle(_EN_POST_TEMPLATES)

        for _ in range(n_ar):
            body = next(ar_pool)
            assets.append(
                self._make_asset(
                    asset_type=AssetType.content_post_ar,
                    language=Language.arabic,
                    subject_or_hook="منشور يومي — عربي",
                    body=body,
                    cta="ما رأيكم؟",
                )
            )
        for _ in range(n_en):
            body = next(en_pool)
            assets.append(
                self._make_asset(
                    asset_type=AssetType.content_post_en,
                    language=Language.english,
                    subject_or_hook="Daily post — English",
                    body=body,
                    cta="What do you think?",
                )
            )
        log.debug("content_engine.daily_posts n_ar=%d n_en=%d", n_ar, n_en)
        return assets

    def article_outline(self, topic: str, language: Language) -> ChannelAsset:
        """Generate article outline with H2s and key points."""
        assert _NO_AUTO_SEND, "_NO_AUTO_SEND gate violated"
        if language == Language.arabic:
            body = (
                f"مسودة مقال: {topic}\n\n"
                "H1: [العنوان الرئيسي]\n\n"
                "مقدمة:\n"
                "• سياق المشكلة\n"
                "• سبب أهمية الموضوع لشركات الخليج\n\n"
                "H2: المشكلة الرئيسية\n"
                "• التفاصيل\n"
                "• أمثلة عملية\n\n"
                "H2: الحل المقترح\n"
                "• الخطوات\n"
                "• المتطلبات\n\n"
                "H2: كيفية التطبيق\n"
                "• خطوات عملية\n"
                "• نقاط الاعتبار\n\n"
                "خاتمة وCTA:\n"
                "• ملخص\n"
                "• الخطوة التالية"
            )
            cta = "كتابة المقال الكامل"
            hook = f"هيكل مقال — {topic}"
        else:
            body = (
                f"Article outline: {topic}\n\n"
                "H1: [Main title]\n\n"
                "Introduction:\n"
                "• Problem context\n"
                "• Why this matters for GCC companies\n\n"
                "H2: The core challenge\n"
                "• Details\n"
                "• Practical examples\n\n"
                "H2: The proposed solution\n"
                "• Steps\n"
                "• Requirements\n\n"
                "H2: How to implement\n"
                "• Practical steps\n"
                "• Considerations\n\n"
                "Conclusion and CTA:\n"
                "• Summary\n"
                "• Next step"
            )
            cta = "Write full article"
            hook = f"Article outline — {topic}"

        return self._make_asset(
            asset_type=AssetType.content_post_en
            if language == Language.english
            else AssetType.content_post_ar,
            language=language,
            subject_or_hook=hook,
            body=body,
            cta=cta,
        )

    def case_study_draft(self, sector: str, language: Language) -> ChannelAsset:
        """Generate anonymized case study draft."""
        assert _NO_AUTO_SEND, "_NO_AUTO_SEND gate violated"
        templates = _CASE_STUDY_TEMPLATES.get(sector, _CASE_STUDY_TEMPLATES["default"])
        key = "ar" if language == Language.arabic else "en"
        body = templates[key]

        if language == Language.arabic:
            hook = f"دراسة حالة — {sector}"
            cta = "مراجعة وتفصيل"
        else:
            hook = f"Case study — {sector}"
            cta = "Review and expand"

        return self._make_asset(
            asset_type=AssetType.content_post_ar
            if language == Language.arabic
            else AssetType.content_post_en,
            language=language,
            subject_or_hook=hook,
            body=body,
            cta=cta,
        )

    def mini_framework_post(self, topic: str, language: Language) -> ChannelAsset:
        """Short framework/checklist post for communities."""
        assert _NO_AUTO_SEND, "_NO_AUTO_SEND gate violated"
        key = "ar" if language == Language.arabic else "en"
        tmpl = _MINI_FRAMEWORK_TEMPLATES.get(key, _MINI_FRAMEWORK_TEMPLATES["en"])
        hook = tmpl["hook"]
        body = f"{hook}\n\n{tmpl['body']}\n\nالموضوع: {topic}" if language == Language.arabic else f"{hook}\n\n{tmpl['body']}\n\nTopic: {topic}"

        return self._make_asset(
            asset_type=AssetType.content_post_ar
            if language == Language.arabic
            else AssetType.content_post_en,
            language=language,
            subject_or_hook=hook,
            body=body,
            cta="شارك الإطار" if language == Language.arabic else "Share the framework",
        )

    def newsletter_segment(self, sector: str, language: Language) -> ChannelAsset:
        """Newsletter content block for a specific sector."""
        assert _NO_AUTO_SEND, "_NO_AUTO_SEND gate violated"
        segments = _NEWSLETTER_SEGMENTS.get(sector, _NEWSLETTER_SEGMENTS["default"])
        key = "ar" if language == Language.arabic else "en"
        body = segments[key]

        if language == Language.arabic:
            hook = f"مقطع النشرة البريدية — {sector}"
            cta = "اشترك في النشرة"
        else:
            hook = f"Newsletter segment — {sector}"
            cta = "Subscribe to newsletter"

        return self._make_asset(
            asset_type=AssetType.content_post_ar
            if language == Language.arabic
            else AssetType.content_post_en,
            language=language,
            subject_or_hook=hook,
            body=body,
            cta=cta,
        )

    def _make_asset(
        self,
        asset_type: AssetType,
        language: Language,
        subject_or_hook: str,
        body: str,
        cta: str,
    ) -> ChannelAsset:
        assert _REQUIRES_REVIEW, "_REQUIRES_REVIEW gate violated"
        return ChannelAsset(
            company_id="content",
            asset_type=asset_type,
            channel=ChannelType.seo_content,
            language=language,
            subject_or_hook=subject_or_hook,
            body=body,
            cta=cta,
            is_auto_sendable=False,
            requires_founder_approval=True,
            risk_level=RiskLevel.low,
            approval_status="approval_required",
            sector="",
            country="",
        )


__all__ = ["CONTENT_TOPICS", "ContentEngine"]
