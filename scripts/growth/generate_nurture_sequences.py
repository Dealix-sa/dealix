#!/usr/bin/env python3
"""Generate the 7-day and 30-day Dealix nurture sequences."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.growth._common import (  # noqa: E402
    DATA_DIR,
    assert_single_cta,
    ensure_dirs,
    write_json,
)

_OUT = DATA_DIR / "nurture_sequences.json"

# 7-day onboarding nurture (Day 0..7). One CTA per message.
_SEVEN_DAY: list[dict[str, Any]] = [
    {
        "day": 0,
        "subject_ar": "نتيجتك جاهزة: أين تتسرب القيمة؟",
        "body_skeleton_ar": (
            "شكر على إكمال الأداة. تلخيص أعلى فجوتين تشغيليتين بصيغة محايدة "
            "بلا أي وعد بنتيجة. دعوة لخطوة واحدة."
        ),
        "cta": "Business OS Score",
    },
    {
        "day": 1,
        "subject_ar": "لماذا تفشل الأدوات التقليدية في إثبات القيمة",
        "body_skeleton_ar": (
            "إطار قصير: الفرق بين إنجاز المهمة وإثبات القيمة. مثال تشغيلي مجهّل "
            "المصدر. دعوة واحدة."
        ),
        "cta": "Free Diagnostic",
    },
    {
        "day": 2,
        "subject_ar": "سجل الإثبات: كيف يبدأ بصف واحد",
        "body_skeleton_ar": (
            "شرح فكرة سجل الإثبات بصف واحد لكل ارتباط. لا أسماء عملاء. دعوة واحدة."
        ),
        "cta": "Command Sprint",
    },
    {
        "day": 3,
        "subject_ar": "خريطة الإيراد من العميل المحتمل حتى الدفعة",
        "body_skeleton_ar": (
            "توضيح مراحل المسار ونقاط التسرب الشائعة بصيغة تقديرية تشغيلية. دعوة واحدة."
        ),
        "cta": "Free Diagnostic",
    },
    {
        "day": 4,
        "subject_ar": "المتابعة المنضبطة: موافقة أولاً وقوائم اختيارية",
        "body_skeleton_ar": (
            "مبدأ الموافقة أولاً قبل أي تواصل خارجي، والاعتماد على قوائم اختيارية "
            "فقط. لا أتمتة بريد بارد. دعوة واحدة."
        ),
        "cta": "Business OS Score",
    },
    {
        "day": 5,
        "subject_ar": "الموجز القيادي الأسبوعي: قرار واحد وإجراء تالٍ",
        "body_skeleton_ar": (
            "شرح الموجز التنفيذي بصفحة واحدة: إشارة، قرار، إجراء تالٍ، مالك. دعوة واحدة."
        ),
        "cta": "Command Sprint",
    },
    {
        "day": 6,
        "subject_ar": "حوكمة الذكاء الاصطناعي ووعي حماية البيانات",
        "body_skeleton_ar": (
            "تذكير بوعي نظام حماية البيانات الشخصية ومتطلب تصريح المصدر قبل أي "
            "إخراج بالذكاء الاصطناعي. دعوة واحدة."
        ),
        "cta": "Free Diagnostic",
    },
    {
        "day": 7,
        "subject_ar": "خطوتك التالية: سبرنت القيادة في سبعة أيام",
        "body_skeleton_ar": (
            "تلخيص الرحلة وعرض سبرنت القيادة كخطوة واحدة واضحة بلا وعد بإيراد مضمون. "
            "دعوة واحدة."
        ),
        "cta": "Command Sprint",
    },
]

# 30-day (4-week) nurture. One CTA per weekly message.
_THIRTY_DAY: list[dict[str, Any]] = [
    {
        "week": 1,
        "subject_ar": "الأسبوع الأول: رؤية واضحة لمسار الإيراد",
        "body_skeleton_ar": (
            "تعميق فكرة خريطة الإيراد ونقاط التسرب. نمط تشغيلي مجهّل المصدر. دعوة واحدة."
        ),
        "cta": "Free Diagnostic",
    },
    {
        "week": 2,
        "subject_ar": "الأسبوع الثاني: بناء سجل إثبات يثق به العميل",
        "body_skeleton_ar": (
            "كيف ينمو سجل الإثبات أسبوعياً دون ادعاءات مضمونة. دعوة واحدة."
        ),
        "cta": "Command Sprint",
    },
    {
        "week": 3,
        "subject_ar": "الأسبوع الثالث: وضوح التسليم وذاكرة العميل",
        "body_skeleton_ar": (
            "ربط وضوح التسليم بذاكرة العميل المشتركة وأثرها على البقاء. دعوة واحدة."
        ),
        "cta": "Business OS Score",
    },
    {
        "week": 4,
        "subject_ar": "الأسبوع الرابع: من التشخيص إلى التشغيل المُدار",
        "body_skeleton_ar": (
            "تلخيص الرحلة وعرض الخطوة التالية نحو التشغيل المُدار بلا وعد بإيراد. دعوة واحدة."
        ),
        "cta": "Command Sprint",
    },
]


def build_sequences() -> dict[str, Any]:
    """Return validated nurture sequences with a single CTA per message."""
    for msg in _SEVEN_DAY + _THIRTY_DAY:
        assert_single_cta(msg["cta"])
    return {
        "seven_day": sorted(_SEVEN_DAY, key=lambda m: m["day"]),
        "thirty_day": sorted(_THIRTY_DAY, key=lambda m: m["week"]),
    }


def main() -> int:
    """Write the nurture sequences and print a summary line."""
    ensure_dirs()
    sequences = build_sequences()
    size = write_json(_OUT, sequences)
    print(
        "nurture_sequences: wrote "
        f"{len(sequences['seven_day'])} day-messages + "
        f"{len(sequences['thirty_day'])} week-messages to {_OUT} ({size} bytes)",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
