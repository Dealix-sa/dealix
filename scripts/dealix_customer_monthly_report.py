#!/usr/bin/env python3
"""
Dealix Monthly Customer Success Report
=======================================
Generates a bilingual AR+EN monthly performance report for retained customers.
The founder fills in actual numbers; the script formats a professional report
ready for sharing after personal review.

Usage:
  python3 scripts/dealix_customer_monthly_report.py \
    --company "شركة نجم اللوجستية" \
    --sector logistics \
    --month 2026-06 \
    --leads-handled 120 \
    --avg-response-min 3 \
    --replied-pct 68 \
    --meetings-booked 4 \
    --deals-won 1 \
    --revenue-influenced 15000

  python3 scripts/dealix_customer_monthly_report.py --dry-run

Doctrine: founder fills real metrics. Nothing is pulled live. No auto-send.
"""

from __future__ import annotations

import argparse
import json
import uuid
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
PITCHES_FILE = REPO_ROOT / "data/outreach/sector_pitches.json"
OUTPUT_DIR = REPO_ROOT / "reports/customer_reports"

HEALTH_THRESHOLDS = {
    "avg_response_min": {"green": 10, "yellow": 30},
    "replied_pct": {"green": 40, "yellow": 20},
    "meetings_booked": {"green": 2, "yellow": 1},
}


def _health_emoji(metric: str, value: float) -> str:
    th = HEALTH_THRESHOLDS.get(metric, {})
    green = th.get("green", 0)
    yellow = th.get("yellow", 0)
    if metric == "avg_response_min":
        if value <= green:
            return "🟢"
        if value <= yellow:
            return "🟡"
        return "🔴"
    else:
        if value >= green:
            return "🟢"
        if value >= yellow:
            return "🟡"
        return "🔴"


def _load_pitches() -> dict:
    if not PITCHES_FILE.exists():
        return {}
    with PITCHES_FILE.open(encoding="utf-8") as f:
        return json.load(f)


REPORT_TEMPLATE = """\
# تقرير الأداء الشهري | Monthly Performance Report
# Dealix × {company_name} — {month}

---

**رقم التقرير / Report ID**: {report_id}
**الشهر / Month**: {month}
**الشركة / Company**: {company_name}
**القطاع / Sector**: {sector_ar} / {sector_en}
**تاريخ الإصدار / Issue Date**: {issue_date}

---

## 📊 مؤشرات الأداء الشهري | Monthly KPIs

| المؤشر / KPI | القيمة / Value | الحالة / Status |
|---|---|---|
| ليدز مُعالجة / Leads handled | **{leads_handled}** | {leads_status} |
| متوسط وقت الرد (دقائق) / Avg response (min) | **{avg_response_min}** | {response_status} |
| معدل الرد / Reply rate | **{replied_pct}%** | {reply_status} |
| اجتماعات محجوزة / Meetings booked | **{meetings_booked}** | {meetings_status} |
| صفقات مُغلقة / Deals won | **{deals_won}** | — |
| إيرادات متأثرة (ريال) / Revenue influenced (SAR) | **{revenue_influenced:,}** | — |

---

## 🏆 إنجازات الشهر | Month Highlights

{highlights}

---

## ⚠️ نقاط تحتاج متابعة | Areas to Watch

{watch_points}

---

## 📈 مقارنة بالشهر السابق | vs. Previous Month

| المؤشر | الشهر الحالي | الشهر السابق | التغيير |
|---|---|---|---|
| ليدز مُعالجة | {leads_handled} | (أدخل يدوياً) | — |
| معدل الرد | {replied_pct}% | (أدخل يدوياً) | — |
| اجتماعات | {meetings_booked} | (أدخل يدوياً) | — |

> **ملاحظة**: أرقام الشهر السابق تُدخَل يدوياً من التقرير الشهري الماضي.
> *Note: Previous month figures are entered manually from last month's report.*

---

## 🎯 أهداف الشهر القادم | Next Month Targets

| الهدف / Target | المستهدف / Goal | ملاحظة / Note |
|---|---|---|
| ليدز مُعالجة | {target_leads} | +10% من الشهر الحالي |
| متوسط الرد | < {target_response} دقيقة | الحفاظ على الأداء الحالي |
| معدل الرد | > {target_reply_pct}% | تحسين بـ 5 نقاط |
| اجتماعات | {target_meetings} | +1 على الأقل |

---

## 🔔 قرارات مطلوبة | Decisions Required

- [ ] مراجعة جودة الردود في قنوات WhatsApp/Email
- [ ] تحديد 3 فرص بارزة من pipeline للمتابعة المكثفة
- [ ] تجديد العقد / Renewal: {renewal_status}

*Review reply quality across WhatsApp/Email channels, identify 3 top pipeline opportunities, confirm renewal status.*

---

*Dealix — نظام التشغيل الذكي للشركات السعودية B2B*
*hello@dealix.me | dealix.me | الرياض*

---

> **⚠️ للمؤسس**: راجع الأرقام قبل إرسال التقرير للعميل.
> هذا مسودة داخلية — أضف أي سياق إضافي قبل المشاركة.
"""


def generate_report(
    company: str,
    sector: str,
    month: str,
    leads_handled: int = 0,
    avg_response_min: float = 0,
    replied_pct: float = 0,
    meetings_booked: int = 0,
    deals_won: int = 0,
    revenue_influenced: int = 0,
    dry_run: bool = False,
) -> Path | None:
    pitches = _load_pitches()
    sectors = pitches.get("sectors", {})
    if sector not in sectors:
        print(f"[ERROR] Unknown sector: {sector}")
        return None

    sector_data = sectors[sector]
    report_id = f"MSR-{date.today().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"
    issue_date = date.today().isoformat()

    response_status = _health_emoji("avg_response_min", avg_response_min)
    reply_status = _health_emoji("replied_pct", replied_pct)
    meetings_status = _health_emoji("meetings_booked", meetings_booked)
    leads_status = "🟢" if leads_handled >= 50 else ("🟡" if leads_handled >= 20 else "🔴")

    highlights = []
    if avg_response_min <= 10:
        highlights.append(f"  - ✅ وقت الرد ممتاز: {avg_response_min:.0f} دقائق / Excellent response time: {avg_response_min:.0f} min")
    if replied_pct >= 40:
        highlights.append(f"  - ✅ معدل رد قوي: {replied_pct:.0f}% / Strong reply rate: {replied_pct:.0f}%")
    if meetings_booked >= 2:
        highlights.append(f"  - ✅ اجتماعات: {meetings_booked} حُجزت هذا الشهر / {meetings_booked} meetings booked this month")
    if deals_won >= 1:
        highlights.append(f"  - 🏆 صفقات مُغلقة: {deals_won} / Deals won: {deals_won}")
    if not highlights:
        highlights.append("  - (أدخل إنجازات الشهر يدوياً / Enter month highlights manually)")

    watch_points = []
    if avg_response_min > 30:
        watch_points.append(f"  - ⚠️ وقت الرد عالي: {avg_response_min:.0f} دقيقة — راجع إعدادات التوجيه")
    if replied_pct < 20:
        watch_points.append(f"  - ⚠️ معدل الرد منخفض: {replied_pct:.0f}% — راجع جودة الرسائل")
    if meetings_booked == 0:
        watch_points.append("  - ⚠️ لم يُحجز أي اجتماع — راجع خطوة المتابعة")
    if not watch_points:
        watch_points.append("  - ✅ لا توجد نقاط تحتاج تدخلاً فورياً هذا الشهر")

    target_leads = int(leads_handled * 1.1) + 1
    target_response = max(5, int(avg_response_min * 0.9))
    target_reply_pct = min(80, int(replied_pct + 5))
    target_meetings = meetings_booked + 1
    renewal_status = "قيد المراجعة / Under review — تواصل مع العميل قبل نهاية الشهر"

    report = REPORT_TEMPLATE.format(
        report_id=report_id,
        month=month,
        company_name=company,
        sector_ar=sector_data["label_ar"],
        sector_en=sector_data["label_en"],
        issue_date=issue_date,
        leads_handled=leads_handled,
        leads_status=leads_status,
        avg_response_min=avg_response_min,
        response_status=response_status,
        replied_pct=replied_pct,
        reply_status=reply_status,
        meetings_booked=meetings_booked,
        meetings_status=meetings_status,
        deals_won=deals_won,
        revenue_influenced=revenue_influenced,
        highlights="\n".join(highlights),
        watch_points="\n".join(watch_points),
        target_leads=target_leads,
        target_response=target_response,
        target_reply_pct=target_reply_pct,
        target_meetings=target_meetings,
        renewal_status=renewal_status,
    )

    if dry_run:
        print(report[:3000] + ("\n...[truncated]" if len(report) > 3000 else ""))
        return None

    out_dir = OUTPUT_DIR / month
    out_dir.mkdir(parents=True, exist_ok=True)
    safe_name = "".join(c if c.isalnum() or c in "-_" else "_" for c in company)
    out_file = out_dir / f"monthly_report_{safe_name}_{report_id}.md"
    out_file.write_text(report, encoding="utf-8")

    print()
    print("━" * 65)
    print("📋 MONTHLY CUSTOMER REPORT GENERATED — FOUNDER REVIEW")
    print("━" * 65)
    print(f"  Report ID  : {report_id}")
    print(f"  Company    : {company}")
    print(f"  Sector     : {sector_data['label_ar']} ({sector_data['label_en']})")
    print(f"  Month      : {month}")
    print(f"  File       : {out_file}")
    print()
    print("  Health Summary:")
    print(f"    Response time  : {response_status} {avg_response_min:.0f} min")
    print(f"    Reply rate     : {reply_status} {replied_pct:.0f}%")
    print(f"    Meetings       : {meetings_status} {meetings_booked}")
    print()
    print("  NEXT STEPS:")
    print("  [ ] Review and add any missing context")
    print("  [ ] Share with customer in monthly check-in call")
    print("  [ ] Confirm renewal / upsell opportunity")
    print("━" * 65)
    print()

    return out_file


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate monthly customer success report (founder review required)"
    )
    parser.add_argument("--company", help="Company name")
    parser.add_argument("--sector", help="Sector key")
    parser.add_argument("--month", help="Month (YYYY-MM)", default=date.today().strftime("%Y-%m"))
    parser.add_argument("--leads-handled", type=int, default=0)
    parser.add_argument("--avg-response-min", type=float, default=0.0)
    parser.add_argument("--replied-pct", type=float, default=0.0)
    parser.add_argument("--meetings-booked", type=int, default=0)
    parser.add_argument("--deals-won", type=int, default=0)
    parser.add_argument("--revenue-influenced", type=int, default=0)
    parser.add_argument("--dry-run", action="store_true", help="Preview with sample data")
    args = parser.parse_args()

    if args.dry_run and not args.company:
        args.company = "شركة نموذج"
        args.sector = "real_estate"
        args.leads_handled = 87
        args.avg_response_min = 4.5
        args.replied_pct = 52.0
        args.meetings_booked = 3
        args.deals_won = 1
        args.revenue_influenced = 22_000

    if not args.company or not args.sector:
        parser.error("--company and --sector are required (or use --dry-run)")

    generate_report(
        company=args.company,
        sector=args.sector,
        month=args.month,
        leads_handled=args.leads_handled,
        avg_response_min=args.avg_response_min,
        replied_pct=args.replied_pct,
        meetings_booked=args.meetings_booked,
        deals_won=args.deals_won,
        revenue_influenced=args.revenue_influenced,
        dry_run=args.dry_run,
    )


if __name__ == "__main__":
    main()
