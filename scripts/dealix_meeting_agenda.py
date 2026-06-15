#!/usr/bin/env python3
"""
Dealix Discovery Call Agenda Generator
========================================
Generates a structured bilingual AR+EN agenda for the first discovery call
with a prospect. Tailored to sector pain points from sector_pitches.json.

Usage:
  python3 scripts/dealix_meeting_agenda.py \
    --company "شركة نجم اللوجستية" \
    --contact "أحمد العتيبي" \
    --sector logistics \
    --duration 45   # minutes

  python3 scripts/dealix_meeting_agenda.py --list-sectors

Doctrine: generates prep docs only. Founder conducts call. Nothing auto-sends.
"""

from __future__ import annotations

import argparse
import json
from datetime import date, timedelta
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
PITCHES_FILE = REPO_ROOT / "data/outreach/sector_pitches.json"
OUTPUT_DIR = REPO_ROOT / "reports/meetings"

DISCOVERY_QUESTIONS = {
    "real_estate": [
        ("pain_ar", "كم طلب عقاري بتوصلكم في الأسبوع، وكم منهم يرد عليه خلال ساعة؟"),
        ("pain_en", "How many property inquiries do you receive weekly, and how many get a response within an hour?"),
        ("process_ar", "كيف يتم توزيع الليدز على الفريق الحالي؟"),
        ("process_en", "How do you currently distribute leads across your team?"),
        ("metric_ar", "ما هو معدل التحويل من استفسار إلى معاينة؟"),
        ("metric_en", "What's your current conversion rate from inquiry to property visit?"),
        ("tool_ar", "ما الأدوات اللي تستخدمونها الحين لتتبع الليدز؟"),
        ("tool_en", "What tools do you currently use to track leads?"),
    ],
    "clinic": [
        ("pain_ar", "كم استفسار يوصل يومياً عبر القنوات المختلفة؟"),
        ("pain_en", "How many inquiries arrive daily across all channels?"),
        ("process_ar", "من يرد على استفسارات الواتساب خارج أوقات الدوام؟"),
        ("process_en", "Who responds to WhatsApp inquiries outside office hours?"),
        ("metric_ar", "كم نسبة الحجوزات التي تُلغى أو تُنسى؟"),
        ("metric_en", "What percentage of bookings get cancelled or forgotten?"),
        ("tool_ar", "هل عندكم نظام لمتابعة تقييمات Google؟"),
        ("tool_en", "Do you have a system to follow up on Google reviews?"),
    ],
    "logistics": [
        ("pain_ar", "كم عدد شحنات يومية، وكم منها تواجه تأخير أو شكوى من العميل؟"),
        ("pain_en", "How many daily shipments, and how many face delays or customer complaints?"),
        ("process_ar", "كيف يعرف العميل وضع شحنته الحالي؟"),
        ("process_en", "How does the customer currently know the status of their shipment?"),
        ("metric_ar", "ما هو معدل التسليم في الوقت المحدد مقارنة بالوعد؟"),
        ("metric_en", "What's your on-time delivery rate vs. promise?"),
        ("tool_ar", "هل فيه لوحة موحدة للفريق تبيّن حالة كل شحنة؟"),
        ("tool_en", "Is there a single board showing the status of every shipment for your team?"),
    ],
    "training": [
        ("pain_ar", "كم متدرب أنجزتم في آخر دورة، وكم منهم تواصلتم معهم بعد الانتهاء؟"),
        ("pain_en", "How many trainees completed your last cohort, and how many did you follow up with after?"),
        ("process_ar", "كيف تتابعون تجديد الاشتراك أو الدورة التالية؟"),
        ("process_en", "How do you handle renewal follow-ups or next course upsells?"),
        ("metric_ar", "ما هو معدل الاحتفاظ بالمتدربين (يعيدون التسجيل)؟"),
        ("metric_en", "What's your trainee retention rate (they re-enroll)?"),
        ("tool_ar", "هل فيه نظام لقياس رضا المتدربين بعد الدورة؟"),
        ("tool_en", "Do you have a system to measure trainee satisfaction post-course?"),
    ],
    "marketing_agency": [
        ("pain_ar", "ما هي أسرع استجابة تقدرون عليها لليدز الوارد لعملائكم؟"),
        ("pain_en", "What's the fastest response time you can guarantee for inbound leads for your clients?"),
        ("process_ar", "كيف تثبتون لعملائكم أن الليدز تم الرد عليها؟"),
        ("process_en", "How do you prove to clients that inbound leads are being responded to?"),
        ("metric_ar", "ما هو معدل التحويل الذي يتوقعه عملاؤكم مقارنة بما تحققونه؟"),
        ("metric_en", "What conversion rate do your clients expect vs. what you achieve?"),
        ("tool_ar", "هل فيه لوحة تقرير للعميل تبيّن أداء الحملة مع الرد على الليدز؟"),
        ("tool_en", "Is there a client-facing report showing campaign performance alongside lead response?"),
    ],
    "b2b_services": [
        ("pain_ar", "كيف يبدو إيقاع المتابعة الأسبوعي الحالي مع الفرص المفتوحة؟"),
        ("pain_en", "What does your current weekly follow-up cadence look like for open opportunities?"),
        ("process_ar", "من يتابع مع الليدز إذا المسؤول الأساسي كان مشغولاً؟"),
        ("process_en", "Who follows up with a lead if the primary owner is busy?"),
        ("metric_ar", "ما هو متوسط دورة المبيعات من أول تواصل لين الإغلاق؟"),
        ("metric_en", "What's your average sales cycle from first contact to close?"),
        ("tool_ar", "هل فيه نظام يُنبّه الفريق متى يراجعون فرصة معينة؟"),
        ("tool_en", "Is there a system that alerts the team when to revisit a specific opportunity?"),
    ],
}

AGENDA_TEMPLATE = """# أجندة مكالمة الاستكشاف | Discovery Call Agenda
# {company_name} × Dealix
# يتطلب مراجعة الفاوندر قبل المكالمة

---

**التاريخ / Date**: {date}
**الشركة / Company**: {company_name}
**المسؤول / Contact**: {contact_name}
**القطاع / Sector**: {sector_ar} / {sector_en}
**المدة / Duration**: {duration} دقيقة / {duration} minutes

---

## 🎯 هدف المكالمة | Call Objective

تشخيص التحدي الأساسي في {company_name} وتحديد ما إذا كان Dealix مناسباً لهم —
**لا هدف للبيع في هذه المكالمة. الهدف هو الاستماع.**

*Diagnose the primary challenge at {company_name} and assess Dealix fit —
**No sales pressure. Goal is to listen.***

---

## ⏱️ الأجندة | Agenda ({duration} min)

| الوقت | العنصر | الهدف |
|-------|--------|-------|
| 0-3 دقائق | ترحيب وتقديم | كسر الجليد ✅ |
| 3-8 دقائق | سؤال عام عن العمل | فهم السياق |
| 8-25 دقيقة | أسئلة الاستكشاف (انظر الأسفل) | تحديد الألم |
| 25-35 دقيقة | عرض التشخيص المجاني | نقل القيمة |
| 35-{duration} دقيقة | الخطوة التالية | تحديد الإجراء |

---

## 🔍 أسئلة الاستكشاف | Discovery Questions

*اطرح 2-3 أسئلة فقط، استمع أكثر مما تتكلم.*
*Ask only 2-3 questions. Listen more than you speak.*

{questions_ar}

---

### By Sector: {sector_en}

{questions_en}

---

## 💡 فرضية الألم | Pain Hypothesis

> **بالعربي**: {pain_ar}

> **English**: {pain_en}

**ملاحظة**: هذه فرضية مبنية على القطاع، وليست حقيقة عن {company_name}.
راجعها مع ما تسمعه في المكالمة.

---

## 🚀 الخطوة التالية | Next Step

اختر واحدة من الخيارات التالية بناءً على المكالمة:

- [ ] **إيجابي**: "أرسل لك التشخيص المجاني (30 نقطة) — بدون أي التزام" → `make outreach --stage diagnostic`
- [ ] **محتاج وقت**: "أفهمك — أتواصل معك خلال أسبوع" → سجّل في `outreach_log.csv` كـ `reply`
- [ ] **مهتم بالعرض**: اقترح tier مناسب → `make proposal COMPANY="{company_name}" SECTOR={sector}`
- [ ] **غير مناسب**: سجّل سبب في `outreach_log.csv` كـ `lost`

---

## 📋 قواعد المكالمة | Call Rules

- ✅ استمع أكثر مما تتكلم (70% استماع / 30% كلام)
- ✅ اطرح سؤالاً واحداً في كل مرة
- ✅ لا تعرض الأسعار في أول مكالمة
- ✅ ابدأ دائماً بالتشخيص المجاني
- ❌ لا تعد بنتائج محددة قبل التشخيص
- ❌ لا تضغط على القرار — أهمك أن تفهم مشكلتهم

---

*Dealix — نظام التشغيل الذكي للشركات السعودية B2B*
*hello@dealix.me | dealix.me*

---

> **للمؤسس**: هذه الأجندة للتحضير فقط. لا ترسلها للعميل. بعد المكالمة، حدّث `outreach_log.csv` بالنتيجة.
"""


def _load_pitches() -> dict:
    if not PITCHES_FILE.exists():
        return {}
    with PITCHES_FILE.open(encoding="utf-8") as f:
        return json.load(f)


def generate_agenda(
    company: str,
    contact: str,
    sector: str,
    duration: int = 45,
    dry_run: bool = False,
) -> Path | None:
    pitches = _load_pitches()
    sectors = pitches.get("sectors", {})

    if sector not in sectors:
        print(f"[ERROR] Unknown sector: {sector}")
        return None

    sector_data = sectors[sector]
    questions = DISCOVERY_QUESTIONS.get(sector, [])

    q_ar = "\n".join(
        f"- **{i+1}. (AR)** {q}" for i, (_, q) in enumerate(questions) if _[0] != "q"
        if _.endswith("_ar")
        for _, q in [(_, q)]
    )

    questions_ar_lines = [
        f"**{i+1}.** {q}"
        for i, (key, q) in enumerate((kv for kv in questions if kv[0].endswith("_ar")))
    ]
    questions_en_lines = [
        f"**{i+1}.** {q}"
        for i, (key, q) in enumerate((kv for kv in questions if kv[0].endswith("_en")))
    ]

    agenda = AGENDA_TEMPLATE.format(
        company_name=company,
        contact_name=contact,
        date=date.today().strftime("%Y-%m-%d"),
        sector_ar=sector_data["label_ar"],
        sector_en=sector_data["label_en"],
        duration=duration,
        sector=sector,
        pain_ar=sector_data["pain_ar"],
        pain_en=sector_data["pain_en"],
        questions_ar="\n".join(questions_ar_lines) or "_لا توجد أسئلة محددة لهذا القطاع بعد._",
        questions_en="\n".join(questions_en_lines) or "_No sector-specific questions yet._",
    )

    if dry_run:
        print(agenda[:3000] + ("\n...[truncated]" if len(agenda) > 3000 else ""))
        return None

    out_dir = OUTPUT_DIR / date.today().strftime("%Y-%m-%d")
    out_dir.mkdir(parents=True, exist_ok=True)
    safe_name = "".join(c if c.isalnum() or c in "-_" else "_" for c in company)
    out_file = out_dir / f"agenda_{safe_name}_{sector}.md"
    out_file.write_text(agenda, encoding="utf-8")

    print()
    print("━" * 65)
    print("📞 DISCOVERY CALL AGENDA GENERATED — FOUNDER ONLY")
    print("━" * 65)
    print(f"  Company  : {company}")
    print(f"  Contact  : {contact}")
    print(f"  Sector   : {sector_data['label_ar']} ({sector_data['label_en']})")
    print(f"  Duration : {duration} min")
    print(f"  File     : {out_file}")
    print()
    print("  PREP CHECKLIST:")
    print("  [ ] Read pain hypothesis and customize to your signal about this lead")
    print("  [ ] Pick 2-3 questions max from the discovery questions")
    print("  [ ] Have outreach_log.csv open to update during/after call")
    print("  [ ] Don't offer price in the first call")
    print("━" * 65)
    print()

    return out_file


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate bilingual discovery call agenda (founder prep only)"
    )
    parser.add_argument("--company", help="Company name")
    parser.add_argument("--contact", help="Contact name", default="المسؤول")
    parser.add_argument("--sector", help="Sector key")
    parser.add_argument("--duration", type=int, default=45, help="Meeting duration in minutes (default: 45)")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing file")
    parser.add_argument("--list-sectors", action="store_true")
    args = parser.parse_args()

    pitches = _load_pitches()

    if args.list_sectors:
        print("\nAvailable sectors:")
        for key in pitches.get("sectors", {}):
            data = pitches["sectors"][key]
            print(f"  {key:<20} {data['label_ar']} / {data['label_en']}")
        print()
        return

    if not args.company or not args.sector:
        parser.error("--company and --sector are required")

    generate_agenda(
        company=args.company,
        contact=args.contact,
        sector=args.sector,
        duration=args.duration,
        dry_run=args.dry_run,
    )


if __name__ == "__main__":
    main()
