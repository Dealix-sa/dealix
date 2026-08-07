#!/usr/bin/env python3
"""
Content factory dry-run — generates sample content assets for different channels.

Run: python scripts/launch/content_factory_dry_run.py

No external calls. No mutations. Safe any time.
"""
from __future__ import annotations

import sys
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))


LINKEDIN_TEMPLATES = [
    {
        "day": 1,
        "topic_ar": "لماذا يخسر 60% من مشاريع العقارات عملاءهم قبل أول اجتماع",
        "hook_ar": "سؤال لكل مدير مبيعات عقارات:",
        "body_ar": (
            "آخر 10 استفسارات وصلتك — كم واحد منهم تحولوا لاجتماع حقيقي؟\n\n"
            "الأرقام تقول 4 من كل 10 فقط.\n\n"
            "السبب ليس المنتج. وليس السعر.\n\n"
            "السبب: الاستفسار يصل في وقت المشغول، وما ترد بسرعة، والعميل يذهب لمنافسك اللي رد أسرع.\n\n"
            "الحل ليس توظيف موظف جديد.\n"
            "الحل: نظام يتابع بدلاً عنك حتى لو كنت في اجتماع."
        ),
        "cta_ar": "هل تعاني من نفس المشكلة؟ اكتب 'نعم' في التعليقات.",
        "char_estimate": 520,
    },
    {
        "day": 2,
        "topic_ar": "3 أخطاء تجعل كل ريال تنفقه على التسويق يضيع",
        "hook_ar": "تنفق على الإعلانات وما ترى نتيجة؟",
        "body_ar": (
            "الخطأ الأول: الاستفسار يأتي — ما أحد يرد في أقل من ساعة.\n"
            "الخطأ الثاني: العميل يرد مرة ثم ينسى — وأنت ما تتابع.\n"
            "الخطأ الثالث: ما عندك طريقة تعرف من قريب من الشراء ومن ليس جاهزاً.\n\n"
            "هذه الأخطاء الثلاثة تكلف الشركات المتوسطة في السعودية ما بين 200,000 و 500,000 ريال سنوياً.\n\n"
            "ليس بالضرورة — ممكن تصلحها بنظام بسيط خلال 30 يوم."
        ),
        "cta_ar": "أي خطأ يؤثر عليك أكثر؟ شاركني.",
        "char_estimate": 580,
    },
]

VIDEO_TEMPLATES = [
    {
        "title_ar": "لماذا متابعة العملاء مهمة أكثر من إيجادهم",
        "hook_ar": "عندي سؤال يصدمك: كم عميل محتمل تركت بدون متابعة آخر أسبوع؟",
        "body_ar": (
            "الحقيقة: 80% من الصفقات تحتاج 5-8 نقاط تواصل قبل الإغلاق.\n"
            "لكن أغلب الشركات تتوقف بعد نقطة أو نقطتين.\n"
            "النتيجة: المنافس اللي يتابع أكثر يأخذ صفقتك."
        ),
        "cta_ar": "في ثواني قليلة سأريك الحل البسيط.",
        "duration_seconds": 45,
    },
]

EMAIL_TEMPLATES = [
    {
        "persona_ar": "مدير مبيعات عقارات",
        "subject_ar": "كيف تستعيد العملاء الضائعين قبل نهاية هذا الأسبوع",
        "body_ar": (
            "أحمد،\n\n"
            "لاحظت أن شركتك في قطاع العقارات — وهذا القطاع يعاني من مشكلة واحدة بشكل شبه موحد:\n\n"
            "الاستفسار يأتي → يُرد عليه مرة أو مرتين → ثم يُنسى.\n\n"
            "الشركات التي حلّت هذه المشكلة رأت نتائج واضحة خلال 30 يوماً من تطبيق نظام متابعة منهجي.\n\n"
            "أنا لا أعد بأرقام محددة — لكن يمكنني أن أريك كيف يبدو النظام قبل أن تلتزم بأي شيء.\n\n"
            "هل تناسبك 15 دقيقة هذا الأسبوع؟"
        ),
        "signature_ar": "سامي العسيري\nDealix — نظام تشغيل الإيرادات",
    },
]


def render_linkedin(post: dict) -> str:
    return (
        f"{'─' * 50}\n"
        f"📅 اليوم {post['day']}: {post['topic_ar']}\n"
        f"{'─' * 50}\n\n"
        f"{post['hook_ar']}\n\n"
        f"{post['body_ar']}\n\n"
        f"— {post['cta_ar']}\n\n"
        f"[~{post['char_estimate']} حرف]\n"
    )


def render_video(script: dict) -> str:
    return (
        f"{'─' * 50}\n"
        f"🎬 {script['title_ar']}\n"
        f"{'─' * 50}\n\n"
        f"[HOOK — 5 ثوانٍ]\n{script['hook_ar']}\n\n"
        f"[BODY — {script['duration_seconds']} ثانية]\n{script['body_ar']}\n\n"
        f"[CTA — 5 ثوانٍ]\n{script['cta_ar']}\n"
    )


def render_email(email: dict) -> str:
    return (
        f"{'─' * 50}\n"
        f"📧 للـ: {email['persona_ar']}\n"
        f"الموضوع: {email['subject_ar']}\n"
        f"{'─' * 50}\n\n"
        f"{email['body_ar']}\n\n"
        f"{email['signature_ar']}\n"
    )


def main() -> None:
    today = date.today()
    print("=" * 60)
    print(f"DEALIX CONTENT FACTORY — DRY RUN — {today}")
    print("=" * 60)

    print("\n📣 LinkedIn Posts:\n")
    for post in LINKEDIN_TEMPLATES:
        print(render_linkedin(post))

    print("\n🎬 Video Scripts:\n")
    for script in VIDEO_TEMPLATES:
        print(render_video(script))

    print("\n📧 Email Templates:\n")
    for email in EMAIL_TEMPLATES:
        print(render_email(email))

    print("=" * 60)
    print(f"✅ {len(LINKEDIN_TEMPLATES)} LinkedIn posts | {len(VIDEO_TEMPLATES)} video scripts | {len(EMAIL_TEMPLATES)} emails generated")
    print("   Review docs/content/30_DAY_LINKEDIN_CONTENT_CALENDAR_AR.md for full calendar")


if __name__ == "__main__":
    main()
