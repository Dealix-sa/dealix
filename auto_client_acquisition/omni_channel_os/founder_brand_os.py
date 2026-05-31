"""Founder Brand OS — generates daily personal brand content for the Dealix founder."""
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

FOUNDER_NAME = "Sami"
FOUNDER_POSITIONING_AR = (
    "فاوندر يبني Agentic AI workflows للشركات الخليجية، "
    "خصوصًا operations-heavy وprofessional services"
)
FOUNDER_POSITIONING_EN = (
    "Founder building controlled Agentic AI workflows for GCC operations-heavy companies"
)

DAILY_POST_TEMPLATES: dict[str, list[str]] = {
    "ar": [
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
            "لاحظت في العمل مع شركات الخليج:\n"
            "أكثر مشكلة تكررت هي مشكلة البيانات المتفرقة.\n"
            "الفريق يعرف الإجابة — لكن يقضي وقته يبحث عنها في أنظمة مختلفة.\n"
            "الـ AI الحقيقي لا يخترع بيانات — يجمعها ويرتبها ويرفع القرار."
        ),
        (
            "كيف تحدد أفضل workflow تبدأ به AI في شركتك؟\n"
            "الإطار البسيط:\n"
            "• الأكثر تكراراً\n"
            "• الأوضح في خطواته\n"
            "• الأسرع في التحقق من النتيجة\n"
            "هذا المسار هو نقطة البداية الصحيحة."
        ),
        (
            "خرافة شائعة عن AI في الشركات:\n"
            "«AI يستبدل الموظفين.»\n"
            "الحقيقة: AI يستبدل المهام المتكررة التي تمنع الموظف من العمل الفعلي.\n"
            "الفريق يعمل أكثر على القرارات — وأقل على التقارير."
        ),
    ],
    "en": [
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
            "Working with GCC companies, I've noticed:\n"
            "The most common problem is scattered data.\n"
            "The team knows the answer — but spends time finding it across different systems.\n"
            "Real AI does not invent data — it aggregates, organizes, and escalates the decision."
        ),
        (
            "How to identify the first AI workflow for your company:\n"
            "• Most repetitive\n"
            "• Clearest in steps\n"
            "• Fastest to verify output\n"
            "That workflow is the right starting point."
        ),
    ],
}

_ar_pool = cycle(DAILY_POST_TEMPLATES["ar"])
_en_pool = cycle(DAILY_POST_TEMPLATES["en"])

_INSIGHT_POSTS: dict[str, dict[str, str]] = {
    "legal": {
        "ar": (
            "مكاتب المحاماة والـ AI:\n"
            "السؤال الصحيح ليس «هل نستخدم AI؟»\n"
            "بل «أي مهمة متكررة نبدأ بها؟»\n"
            "البداية دائماً من مسار واحد — لا من تحول كامل."
        ),
        "en": (
            "Law firms and AI:\n"
            "The right question is not 'do we use AI?'\n"
            "It is 'which repetitive task do we start with?'\n"
            "Always start with one workflow — not a full transformation."
        ),
    },
    "facilities_management": {
        "ar": (
            "شركات FM وتقارير SLA:\n"
            "الوقت الضائع في إعداد التقارير يدوياً هو نفسه الوقت الذي تحتاجونه لحل المشكلة.\n"
            "الـ workflow الذكي لا يلغي قرار المسؤول — يعطيه الوقت ليتخذه."
        ),
        "en": (
            "FM companies and SLA reports:\n"
            "Time lost on manual report preparation is exactly the time you need to solve the problem.\n"
            "The intelligent workflow does not eliminate the manager's decision — it gives them time to make it."
        ),
    },
    "default": {
        "ar": (
            "ملاحظة من العمل مع شركات الخليج:\n"
            "أنجح مشاريع AI تبدأ بسؤال بسيط: ما الـ workflow الذي يأخذ أكثر وقت من الفريق؟\n"
            "الإجابة تحدد المسار."
        ),
        "en": (
            "Observation from working with GCC companies:\n"
            "The most successful AI projects start with a simple question: which workflow takes the most team time?\n"
            "The answer points to the path."
        ),
    },
}

_MYTH_BUSTS: dict[str, str] = {
    "ar": (
        "خرافة: AI يحتاج بيانات ضخمة للعمل.\n"
        "الحقيقة: معظم AI workflows الناجحة تعمل على بيانات موجودة بالفعل في أنظمة الشركة.\n"
        "المشكلة ليست كمية البيانات — بل كيفية ربطها وتنظيمها."
    ),
    "en": (
        "Myth: AI needs massive amounts of data to work.\n"
        "Reality: Most successful AI workflows run on data that already exists in company systems.\n"
        "The problem is not data volume — it is how to connect and organize it."
    ),
}

_FRAMEWORKS: dict[str, dict[str, str]] = {
    "workflow_readiness": {
        "ar": (
            "إطار جاهزية الـ Workflow للـ AI:\n\n"
            "اسأل هذه الأسئلة قبل أي pilot:\n"
            "1. هل الخطوات موثقة؟ (نعم/لا)\n"
            "2. هل النتيجة قابلة للتحقق؟ (نعم/لا)\n"
            "3. هل البيانات المطلوبة متاحة؟ (نعم/لا)\n"
            "4. هل هناك قرار بشري واضح في المسار؟ (نعم/لا)\n\n"
            "4 من 4: ابدأ الـ pilot الآن.\n"
            "3 من 4: أصلح النقطة الناقصة أولاً.\n"
            "أقل من 3: ابنِ الأساس قبل الـ AI."
        ),
        "en": (
            "AI Workflow Readiness Framework:\n\n"
            "Ask these questions before any pilot:\n"
            "1. Are the steps documented? (yes/no)\n"
            "2. Is the output verifiable? (yes/no)\n"
            "3. Is the required data available? (yes/no)\n"
            "4. Is there a clear human decision point in the workflow? (yes/no)\n\n"
            "4 of 4: Start the pilot now.\n"
            "3 of 4: Fix the missing point first.\n"
            "Less than 3: Build the foundation before the AI."
        ),
    },
}


class FounderBrandOS:
    """Generates daily personal brand content for the founder."""

    _NO_AUTO_SEND = True
    _REQUIRES_REVIEW = True

    def daily_package(self) -> dict[str, ChannelAsset]:
        """Generate daily content package: 2 AR posts + 2 EN posts + 1 thread."""
        assert _NO_AUTO_SEND, "_NO_AUTO_SEND gate violated"
        return {
            "ar_post_1": self._next_ar_post(),
            "ar_post_2": self.insight_post(sector=None, language=Language.arabic),
            "en_post_1": self._next_en_post(),
            "en_post_2": self.myth_bust_post(
                myth="AI needs massive data to work",
                language=Language.english,
            ),
            "thread": self.framework_post(
                framework_name="workflow_readiness",
                language=Language.english,
            ),
        }

    def insight_post(self, sector: str | None, language: Language) -> ChannelAsset:
        """Insight post about AI workflows, optionally sector-specific."""
        assert _NO_AUTO_SEND, "_NO_AUTO_SEND gate violated"
        key = sector if sector in _INSIGHT_POSTS else "default"
        lang_key = "ar" if language == Language.arabic else "en"
        body = _INSIGHT_POSTS[key][lang_key]
        hook = "ملاحظة من الميدان" if language == Language.arabic else "Field observation"
        cta = "ما رأيكم؟" if language == Language.arabic else "What do you think?"
        return self._make_asset(
            asset_type=AssetType.linkedin_post_ar
            if language == Language.arabic
            else AssetType.linkedin_post_en,
            language=language,
            subject_or_hook=hook,
            body=body,
            cta=cta,
        )

    def myth_bust_post(self, myth: str, language: Language) -> ChannelAsset:
        """Post that busts a common AI myth."""
        assert _NO_AUTO_SEND, "_NO_AUTO_SEND gate violated"
        lang_key = "ar" if language == Language.arabic else "en"
        body = _MYTH_BUSTS[lang_key]
        hook = "خرافة شائعة" if language == Language.arabic else "Common myth"
        cta = "ما رأيكم؟" if language == Language.arabic else "Thoughts?"
        return self._make_asset(
            asset_type=AssetType.linkedin_post_ar
            if language == Language.arabic
            else AssetType.linkedin_post_en,
            language=language,
            subject_or_hook=hook,
            body=body,
            cta=cta,
        )

    def framework_post(self, framework_name: str, language: Language) -> ChannelAsset:
        """Short framework/checklist post."""
        assert _NO_AUTO_SEND, "_NO_AUTO_SEND gate violated"
        fw = _FRAMEWORKS.get(framework_name, _FRAMEWORKS["workflow_readiness"])
        lang_key = "ar" if language == Language.arabic else "en"
        body = fw[lang_key]
        hook = "إطار عمل" if language == Language.arabic else "Framework"
        cta = "احفظ الإطار" if language == Language.arabic else "Save the framework"
        return self._make_asset(
            asset_type=AssetType.linkedin_post_ar
            if language == Language.arabic
            else AssetType.linkedin_post_en,
            language=language,
            subject_or_hook=hook,
            body=body,
            cta=cta,
        )

    def case_observation(self, sector: str, language: Language) -> ChannelAsset:
        """Observation from working with a specific sector."""
        assert _NO_AUTO_SEND, "_NO_AUTO_SEND gate violated"
        key = sector if sector in _INSIGHT_POSTS else "default"
        lang_key = "ar" if language == Language.arabic else "en"
        body = _INSIGHT_POSTS[key][lang_key]
        hook = (
            f"ملاحظة من قطاع {sector}"
            if language == Language.arabic
            else f"Observation from the {sector} sector"
        )
        cta = "ما تجربتكم؟" if language == Language.arabic else "What is your experience?"
        return self._make_asset(
            asset_type=AssetType.linkedin_post_ar
            if language == Language.arabic
            else AssetType.linkedin_post_en,
            language=language,
            subject_or_hook=hook,
            body=body,
            cta=cta,
        )

    def comment_for_post(self, post_topic: str, language: Language) -> ChannelAsset:
        """Smart comment to post on a decision-maker's LinkedIn post."""
        assert _NO_AUTO_SEND, "_NO_AUTO_SEND gate violated"
        if language == Language.arabic:
            body = (
                f"نقطة مثيرة للاهتمام حول {post_topic}.\n"
                "في تجربتي مع شركات الخليج، هذا الموضوع عادةً يرتبط بسؤال عملي:\n"
                "ما الـ workflow الذي يتأثر أكثر وكيف يمكن تحسينه؟\n"
                "هل مررتم بتجارب مشابهة؟"
            )
            hook = f"تعليق ذكي — {post_topic}"
            cta = ""
        else:
            body = (
                f"Interesting point about {post_topic}.\n"
                "In my experience working with GCC companies, this topic usually connects to a practical question:\n"
                "Which workflow is most affected and how can it be improved?\n"
                "Have you encountered similar situations?"
            )
            hook = f"Smart comment — {post_topic}"
            cta = ""

        return self._make_asset(
            asset_type=AssetType.linkedin_comment_idea,
            language=language,
            subject_or_hook=hook,
            body=body,
            cta=cta,
        )

    def _next_ar_post(self) -> ChannelAsset:
        body = next(_ar_pool)
        return self._make_asset(
            asset_type=AssetType.linkedin_post_ar,
            language=Language.arabic,
            subject_or_hook="منشور يومي — عربي",
            body=body,
            cta="ما رأيكم؟",
        )

    def _next_en_post(self) -> ChannelAsset:
        body = next(_en_pool)
        return self._make_asset(
            asset_type=AssetType.linkedin_post_en,
            language=Language.english,
            subject_or_hook="Daily post — English",
            body=body,
            cta="What do you think?",
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
            company_id="founder",
            asset_type=asset_type,
            channel=ChannelType.founder_brand,
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


__all__ = ["FOUNDER_NAME", "FOUNDER_POSITIONING_AR", "FOUNDER_POSITIONING_EN", "FounderBrandOS"]
