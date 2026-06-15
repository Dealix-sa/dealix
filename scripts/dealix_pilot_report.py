#!/usr/bin/env python3
"""
Dealix Pilot Results Reporter
================================
After the 7-day Revenue Intelligence Sprint (499 SAR pilot), this tool
generates a bilingual AR+EN results summary for the customer meeting.

Usage:
  python3 scripts/dealix_pilot_report.py \
    --company "شركة نجم اللوجستية" \
    --sector logistics \
    --leads-before 0 \
    --leads-after 47 \
    --response-time-before "24 hours" \
    --response-time-after "4 minutes" \
    --replied 3 \
    --meetings 1

  python3 scripts/dealix_pilot_report.py --dry-run (uses sample data)

Doctrine: reads inputs from founder, never pulls live data automatically.
Founder reviews before sharing with customer.
"""

from __future__ import annotations

import argparse
import json
import uuid
from datetime import date, timedelta
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
PITCHES_FILE = REPO_ROOT / "data/outreach/sector_pitches.json"
OUTPUT_DIR = REPO_ROOT / "reports/pilot_reports"

SECTOR_METRICS = {
    "real_estate": {
        "primary_metric_ar": "استفسارات العقارات المُتابعة خلال 5 دقائق",
        "primary_metric_en": "Property inquiries followed up within 5 minutes",
        "secondary_metric_ar": "معدل تحويل الاستفسار إلى معاينة",
        "secondary_metric_en": "Inquiry-to-visit conversion rate",
    },
    "clinic": {
        "primary_metric_ar": "استفسارات الحجوزات التي تمّ الرد عليها تلقائياً",
        "primary_metric_en": "Booking inquiries answered automatically",
        "secondary_metric_ar": "حجوزات مؤكدة عبر النظام",
        "secondary_metric_en": "Bookings confirmed through the system",
    },
    "logistics": {
        "primary_metric_ar": "إشعارات الشحنات التلقائية المُرسَلة للعملاء",
        "primary_metric_en": "Automated shipment notifications sent to customers",
        "secondary_metric_ar": "شكاوى حالة الشحنة التي انخفضت",
        "secondary_metric_en": "Shipment status complaints reduced",
    },
    "training": {
        "primary_metric_ar": "رسائل متابعة الدورات المُرسَلة تلقائياً",
        "primary_metric_en": "Automated course follow-up messages sent",
        "secondary_metric_ar": "معدل إعادة التسجيل في الدورات",
        "secondary_metric_en": "Course re-enrollment rate",
    },
    "marketing_agency": {
        "primary_metric_ar": "ليدز عملاء تم الرد عليهم خلال 5 دقائق",
        "primary_metric_en": "Client leads responded to within 5 minutes",
        "secondary_metric_ar": "تقارير أداء يومية مُولَّدة تلقائياً",
        "secondary_metric_en": "Daily performance reports auto-generated",
    },
    "b2b_services": {
        "primary_metric_ar": "فرص مبيعات تمّت متابعتها خلال الجدول الزمني",
        "primary_metric_en": "Sales opportunities followed up on schedule",
        "secondary_metric_ar": "متوسط دورة المبيعات (أيام)",
        "secondary_metric_en": "Average sales cycle (days)",
    },
}

REPORT_TEMPLATE = """\
# تقرير نتائج الـ Pilot — Dealix × {company_name}
# Pilot Results Report

---

**رقم التقرير / Report ID**: {report_id}
**التاريخ / Date**: {report_date}
**الشركة / Company**: {company_name}
**القطاع / Sector**: {sector_ar} / {sector_en}
**فترة الـ Pilot / Pilot Period**: {pilot_start} → {pilot_end} (7 أيام / 7 days)

---

## 🏆 النتائج الرئيسية | Key Results

### مؤشرات الأداء | KPIs

| المؤشر / KPI | قبل Dealix / Before | بعد Dealix / After | التحسن / Improvement |
|---|---|---|---|
| وقت الاستجابة / Response time | {response_time_before} | {response_time_after} | {response_improvement} |
| {primary_metric_ar} | {primary_before} | {primary_after} | {primary_improvement} |
| ردود واردة / Replies received | {replied_before} | {replied_after} | +{replied_delta} |
| اجتماعات محجوزة / Meetings booked | {meetings_before} | {meetings_after} | +{meetings_delta} |

---

## 📊 تحليل المرحلة | Phase Analysis

### ما تم إنجازه في 7 أيام | What Was Done in 7 Days

1. ✅ **التشخيص / Diagnosis**: 30-point business intelligence scan
2. ✅ **إعداد النظام / Setup**: WhatsApp/email automation configured
3. ✅ **التكامل / Integration**: Connected to existing {sector_en} workflow
4. ✅ **التدريب / Training**: Team briefed on new response protocols
5. ✅ **القياس / Measurement**: Baseline vs. post-pilot metrics captured
6. ✅ **التقرير / Report**: This results summary for your records

---

## 💡 الفرص المكتشفة | Discovered Opportunities

{opportunities}

---

## 🚀 الخطوة التالية | Recommended Next Step

بناءً على نتائج الـ Pilot، نوصي بـ:

**Based on the pilot results, we recommend:**

### الخيار الأمثل | Best Option

**{recommended_tier_ar} — {recommended_tier_price} ريال/شهر**
*{recommended_tier_en}*

{tier_rationale_ar}

*{tier_rationale_en}*

### مسار القيمة | Value Path

```
الـ Pilot (7 أيام) → {recommended_tier_en} (3 أشهر) → نظام راسخ
```

---

## 📋 قرار العميل | Customer Decision

- [ ] **نعم — أكمل بـ {recommended_tier_en}** → `make contract COMPANY="{company_name}" TIER=...`
- [ ] **أريد وقتاً للتفكير** → أتواصل معك الأسبوع القادم
- [ ] **أريد تعديل الباقة** → نناقش البدائل
- [ ] **لا يناسبنا الآن** → `make outreach-tracker update --company "{company_name}" --status lost`

---

## 📎 الوثائق المرفقة | Attached Documents

- [ ] Diagnostic PDF (30 نقطة)
- [ ] Integration summary
- [ ] Proposal for next tier → `make proposal COMPANY="{company_name}" SECTOR={sector}`

---

*Dealix — نظام التشغيل الذكي للشركات السعودية B2B*
*hello@dealix.me | dealix.me | الرياض*

---

> **⚠️ للمؤسس**: هذا التقرير للمراجعة الداخلية. شاركه مع العميل بعد مراجعتك الشخصية.
> أدخل الأرقام الفعلية قبل الإرسال — لا تشارك الأرقام الافتراضية.
"""


def _load_pitches() -> dict:
    if not PITCHES_FILE.exists():
        return {}
    with PITCHES_FILE.open(encoding="utf-8") as f:
        return json.load(f)


def _improvement_str(before: str, after: str) -> str:
    try:
        b = float(before.replace("%", "").replace(",", ""))
        a = float(after.replace("%", "").replace(",", ""))
        if b == 0:
            return "N/A"
        pct = (a - b) / b * 100
        sign = "+" if pct > 0 else ""
        return f"{sign}{pct:.0f}%"
    except ValueError:
        return "↑ improved"


def _recommend_tier(sector: str) -> tuple[str, str, str, int, str, str]:
    recs = {
        "real_estate": ("نظام تشغيل الإيرادات", "Revenue OS", "revenue_os", 5_000,
                        "العقارات تحتاج سرعة رد + تتبع ليدز + قمع مبيعات واضح.",
                        "Real estate needs fast response + lead tracking + clear sales funnel."),
        "clinic": ("نظام المراجعة والسمعة", "Review & Reputation OS", "review_os", 3_500,
                   "العيادات تستفيد أكثر من إدارة المراجعات + الحجوزات التلقائية.",
                   "Clinics benefit most from review management + automated bookings."),
        "logistics": ("نظام تشغيل الإيرادات", "Revenue OS", "revenue_os", 5_000,
                      "اللوجستية تحتاج تتبع شحنات + إشعارات عملاء + لوحة عمليات.",
                      "Logistics needs shipment tracking + customer notifications + ops dashboard."),
        "training": ("نظام تشغيل الإيرادات", "Revenue OS", "revenue_os", 5_000,
                     "التدريب يحتاج نظام متابعة + تجديد اشتراكات + قياس رضا.",
                     "Training needs follow-up system + subscription renewal + satisfaction tracking."),
        "marketing_agency": ("مركز القيادة الذكي", "Command Center OS", "command_center", 9_000,
                             "الوكالات تحتاج تقارير عملاء + لوحة أداء موحدة + SLA واضح.",
                             "Agencies need client reports + unified performance dashboard + clear SLA."),
        "b2b_services": ("نظام تشغيل الإيرادات", "Revenue OS", "revenue_os", 5_000,
                         "B2B تحتاج دورة مبيعات منظمة + متابعة منتظمة + تقارير pipeline.",
                         "B2B needs organized sales cycle + regular follow-up + pipeline reports."),
    }
    return recs.get(sector, ("Revenue OS", "Revenue OS", "revenue_os", 5_000,
                             "نظام شامل لتشغيل الإيرادات.",
                             "Comprehensive revenue operations system."))


def generate_report(
    company: str,
    sector: str,
    response_time_before: str = "24 ساعة / 24 hours",
    response_time_after: str = "4 دقائق / 4 minutes",
    leads_before: int = 0,
    leads_after: int = 0,
    replied_before: int = 0,
    replied_after: int = 0,
    meetings_before: int = 0,
    meetings_after: int = 0,
    dry_run: bool = False,
) -> Path | None:
    pitches = _load_pitches()
    sectors = pitches.get("sectors", {})
    if sector not in sectors:
        print(f"[ERROR] Unknown sector: {sector}")
        return None

    sector_data = sectors[sector]
    metrics = SECTOR_METRICS.get(sector, {
        "primary_metric_ar": "ليدز مُعالَجة / Leads processed",
        "primary_metric_en": "Leads processed",
        "secondary_metric_ar": "ردود / Replies",
        "secondary_metric_en": "Replies",
    })

    rec_ar, rec_en, rec_key, rec_price, rat_ar, rat_en = _recommend_tier(sector)

    today = date.today()
    pilot_end = today
    pilot_start = today - timedelta(days=7)

    report_id = f"PLT-{today.strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"

    opportunities_list = [
        f"  - {sector_data.get('pain_ar', 'فرصة تحسين العمليات')}",
        "  - أتمتة ردود WhatsApp / Email خارج أوقات الدوام",
        "  - لوحة قيادة موحدة لجميع القنوات",
        "  - تقارير أسبوعية تلقائية",
    ]

    report = REPORT_TEMPLATE.format(
        report_id=report_id,
        report_date=today.isoformat(),
        company_name=company,
        sector_ar=sector_data["label_ar"],
        sector_en=sector_data["label_en"],
        pilot_start=pilot_start.isoformat(),
        pilot_end=pilot_end.isoformat(),
        response_time_before=response_time_before,
        response_time_after=response_time_after,
        response_improvement=_improvement_str(
            response_time_before.split("/")[0].strip().split()[0],
            response_time_after.split("/")[0].strip().split()[0],
        ) if "/" in response_time_before else "↑ improved",
        primary_metric_ar=metrics["primary_metric_ar"],
        primary_before=str(leads_before),
        primary_after=str(leads_after),
        primary_improvement=_improvement_str(str(leads_before), str(leads_after)),
        replied_before=str(replied_before),
        replied_after=str(replied_after),
        replied_delta=replied_after - replied_before,
        meetings_before=str(meetings_before),
        meetings_after=str(meetings_after),
        meetings_delta=meetings_after - meetings_before,
        opportunities="\n".join(opportunities_list),
        recommended_tier_ar=rec_ar,
        recommended_tier_en=rec_en,
        recommended_tier_price=f"{rec_price:,}",
        tier_rationale_ar=rat_ar,
        tier_rationale_en=rat_en,
        sector=sector,
    )

    if dry_run:
        print(report[:3000] + ("\n...[truncated]" if len(report) > 3000 else ""))
        return None

    out_dir = OUTPUT_DIR / today.strftime("%Y-%m-%d")
    out_dir.mkdir(parents=True, exist_ok=True)
    safe_name = "".join(c if c.isalnum() or c in "-_" else "_" for c in company)
    out_file = out_dir / f"pilot_report_{safe_name}_{report_id}.md"
    out_file.write_text(report, encoding="utf-8")

    print()
    print("━" * 65)
    print("📊 PILOT RESULTS REPORT GENERATED — FOUNDER REVIEW")
    print("━" * 65)
    print(f"  Report ID  : {report_id}")
    print(f"  Company    : {company}")
    print(f"  Sector     : {sector_data['label_ar']} ({sector_data['label_en']})")
    print(f"  Period     : {pilot_start} → {pilot_end}")
    print(f"  File       : {out_file}")
    print()
    print("  NEXT STEPS:")
    print(f"  [ ] Review metrics — enter actual numbers before sharing")
    print(f"  [ ] Present to {company} in 30-min debrief call")
    print(f"  [ ] Recommended next step: {rec_en}")
    print(f"  [ ] If yes: make contract COMPANY='{company}' SECTOR={sector} TIER={rec_key}")
    print(f"  [ ] If no:  make outreach-tracker update --company '{company}' --status lost")
    print("━" * 65)
    print()

    return out_file


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate bilingual pilot results report (founder review required)"
    )
    parser.add_argument("--company", help="Company name")
    parser.add_argument("--sector", help="Sector key")
    parser.add_argument("--response-time-before", default="24 ساعة / 24 hours")
    parser.add_argument("--response-time-after", default="4 دقائق / 4 minutes")
    parser.add_argument("--leads-before", type=int, default=0)
    parser.add_argument("--leads-after", type=int, default=0)
    parser.add_argument("--replied-before", type=int, default=0)
    parser.add_argument("--replied-after", type=int, default=0)
    parser.add_argument("--meetings-before", type=int, default=0)
    parser.add_argument("--meetings-after", type=int, default=0)
    parser.add_argument("--dry-run", action="store_true", help="Preview with sample data")
    args = parser.parse_args()

    if args.dry_run and not args.company:
        args.company = "شركة نموذج"
        args.sector = "logistics"

    if not args.company or not args.sector:
        parser.error("--company and --sector are required (or use --dry-run)")

    generate_report(
        company=args.company,
        sector=args.sector,
        response_time_before=args.response_time_before,
        response_time_after=args.response_time_after,
        leads_before=args.leads_before,
        leads_after=args.leads_after,
        replied_before=args.replied_before,
        replied_after=args.replied_after,
        meetings_before=args.meetings_before,
        meetings_after=args.meetings_after,
        dry_run=args.dry_run,
    )


if __name__ == "__main__":
    main()
