#!/usr/bin/env python3
"""
Dealix Weekly GTM Review
========================
Weekly bilingual founder review: outreach pipeline → proposals sent →
meetings booked → deals won. Reads from outreach_log.csv + reports/proposals/.

Usage:
  python3 scripts/dealix_weekly_gtm_review.py
  python3 scripts/dealix_weekly_gtm_review.py --weeks 2    # last 2 weeks
  python3 scripts/dealix_weekly_gtm_review.py --output report.md

Doctrine: read-only. Never sends anything. Founder reviews before any action.
"""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from datetime import date, datetime, timedelta
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
OUTREACH_LOG = REPO_ROOT / "data/outreach/outreach_log.csv"
OUTREACH_LOG_TEMPLATE = REPO_ROOT / "data/outreach/outreach_log.template.csv"
PROPOSALS_DIR = REPO_ROOT / "reports/proposals"
OUTPUT_DIR = REPO_ROOT / "reports/command_room"

STAGE_ORDER = ["drafted", "sent", "reply", "meeting", "won", "lost"]
STAGE_AR = {
    "drafted": "مسودة جاهزة",
    "sent": "تم الإرسال",
    "reply": "جاء رد",
    "meeting": "اجتماع محجوز",
    "won": "تم الإغلاق",
    "lost": "غير مناسب",
}


def _load_log(path: Path) -> list[dict]:
    if not path.exists():
        return []
    rows = []
    with path.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(dict(row))
    return rows


def _week_range(weeks_back: int = 0) -> tuple[date, date]:
    today = date.today()
    start_of_week = today - timedelta(days=today.weekday())  # Monday
    start = start_of_week - timedelta(weeks=weeks_back)
    end = start + timedelta(days=6)
    return start, end


def _filter_this_period(rows: list[dict], start: date, end: date) -> list[dict]:
    result = []
    for row in rows:
        raw = row.get("date", "").strip()
        if not raw:
            result.append(row)  # include undated rows
            continue
        try:
            d = datetime.strptime(raw, "%Y-%m-%d").date()
            if start <= d <= end:
                result.append(row)
        except ValueError:
            result.append(row)
    return result


def _count_proposals(start: date, end: date) -> int:
    count = 0
    if not PROPOSALS_DIR.exists():
        return count
    for day_dir in PROPOSALS_DIR.iterdir():
        if not day_dir.is_dir():
            continue
        try:
            day = datetime.strptime(day_dir.name, "%Y-%m-%d").date()
        except ValueError:
            continue
        if start <= day <= end:
            count += len(list(day_dir.glob("*.md")))
    return count


def _generate_report(rows: list[dict], start: date, end: date, weeks: int) -> str:
    period_rows = _filter_this_period(rows, start, end)
    proposals = _count_proposals(start, end)

    stage_counts: dict[str, int] = defaultdict(int)
    sector_counts: dict[str, int] = defaultdict(int)
    for row in period_rows:
        s = (row.get("status") or "drafted").strip() or "drafted"
        stage_counts[s] += 1
        sec = (row.get("sector") or "—").strip() or "—"
        sector_counts[sec] += 1

    total = len(period_rows) if period_rows else len(rows)
    all_rows = rows if not period_rows and rows else period_rows
    sent = sum(1 for r in all_rows if r.get("status", "") in ("sent", "reply", "meeting", "won"))
    replied = sum(1 for r in all_rows if r.get("status", "") in ("reply", "meeting", "won"))
    meetings = sum(1 for r in all_rows if r.get("status", "") == "meeting")
    won = sum(1 for r in all_rows if r.get("status", "") == "won")
    reply_rate = f"{replied / sent * 100:.1f}%" if sent else "—"

    period_label = f"{start} → {end}" if weeks <= 1 else f"آخر {weeks} أسابيع"
    week_num = start.isocalendar()[1]

    lines = []

    lines += [
        f"# تقرير GTM الأسبوعي — Dealix",
        f"# Weekly GTM Review — Dealix",
        f"",
        f"**الفترة / Period**: {period_label} · الأسبوع {week_num}",
        f"**تاريخ التقرير / Report Date**: {date.today()}",
        f"",
        "---",
        "",
        "## 📊 ملخص الأسبوع | Week Summary",
        "",
        "| المؤشر | القيمة | KPI | Value |",
        "|--------|--------|-----|-------|",
        f"| رسائل في هذه الفترة | **{total}** | Outreach this period | **{total}** |",
        f"| تم الإرسال فعلياً | **{sent}** | Actually sent | **{sent}** |",
        f"| جاء رد | **{replied}** | Replies received | **{replied}** |",
        f"| معدل الرد | **{reply_rate}** | Reply rate | **{reply_rate}** |",
        f"| اجتماعات محجوزة | **{meetings}** | Meetings booked | **{meetings}** |",
        f"| عروض أسعار أُرسلت | **{proposals}** | Proposals generated | **{proposals}** |",
        f"| صفقات مُغلقة | **{won}** | Deals won | **{won}** |",
        "",
    ]

    # Pipeline funnel
    lines += [
        "## 🔄 قمع المبيعات | Pipeline Funnel",
        "",
    ]
    if period_rows:
        for stage in STAGE_ORDER:
            count = stage_counts.get(stage, 0)
            bar = "█" * min(count, 30) + f" ({count})"
            lines.append(f"- **{STAGE_AR.get(stage, stage)}** / {stage}: {bar}")
    else:
        lines.append("_لم يُسجَّل أي نشاط بعد في outreach_log.csv_")
        lines.append("_No activity logged yet in outreach_log.csv_")
    lines.append("")

    # By sector
    if sector_counts and any(k != "—" for k in sector_counts):
        lines += [
            "## 🏢 بالقطاع | By Sector",
            "",
        ]
        for sec, count in sorted(sector_counts.items(), key=lambda x: -x[1]):
            if sec == "—":
                continue
            lines.append(f"- **{sec}**: {count}")
        lines.append("")

    # Next week actions
    lines += [
        "## ✅ أولويات الأسبوع القادم | Next Week Actions",
        "",
        "### متابعات عاجلة | Urgent Follow-ups",
    ]
    if rows:
        f3_candidates = [
            r for r in rows
            if r.get("status", "") == "sent" and not r.get("replied", "")
        ]
        f7_candidates = [
            r for r in rows
            if r.get("status", "") == "sent"
        ]
        if f3_candidates:
            lines.append(f"- [ ] يوم 3 متابعة: {len(f3_candidates)} شركة تستحق `make outreach-f3`")
        if len(f7_candidates) > len(f3_candidates):
            lines.append(f"- [ ] يوم 7 متابعة: {len(f7_candidates)} شركة تستحق `make outreach-f7`")
    lines += [
        "- [ ] راجع غرفة القيادة: `make command-room`",
        "- [ ] جهّز رسائل الأسبوع الجديد: `make outreach`",
        "- [ ] منشور LinkedIn الأسبوعي: `make content`",
        "",
        "### الهدف الأسبوعي | Weekly Target",
        "",
        "| الهدف | المستهدف | الحالي |",
        "|-------|----------|--------|",
        f"| رسائل ترسل | 25 | {sent} |",
        f"| ردود | 3 | {replied} |",
        f"| اجتماعات | 1 | {meetings} |",
        f"| عروض أسعار | 1 | {proposals} |",
        "",
        "---",
        "",
        "_Dealix — نظام التشغيل الذكي للشركات السعودية B2B_",
        "_hello@dealix.me | dealix.me | الرياض_",
        "",
        f"_تقرير تلقائي — للمراجعة فقط. لا يُرسل أي شيء تلقائياً._",
        f"_Auto-generated for review only. Nothing sends automatically._",
    ]

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate weekly bilingual GTM pipeline review (founder review only)"
    )
    parser.add_argument("--weeks", type=int, default=1, help="Number of weeks to cover (default: 1)")
    parser.add_argument("--output", help="Output markdown file (default: auto-named in reports/command_room/)")
    parser.add_argument("--print", action="store_true", help="Print report to stdout instead of writing file")
    args = parser.parse_args()

    rows = _load_log(OUTREACH_LOG)
    if not rows:
        rows = _load_log(OUTREACH_LOG_TEMPLATE)

    start, end = _week_range(weeks_back=0)
    if args.weeks > 1:
        start, _ = _week_range(weeks_back=args.weeks - 1)

    report = _generate_report(rows, start, end, args.weeks)

    if getattr(args, "print", False):
        print(report)
        return

    if args.output:
        out_path = Path(args.output)
    else:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        out_path = OUTPUT_DIR / f"weekly_gtm_{date.today().strftime('%Y-W%V')}.md"

    out_path.write_text(report, encoding="utf-8")

    print()
    print("━" * 65)
    print("📈 WEEKLY GTM REVIEW GENERATED — FOUNDER REVIEW")
    print("━" * 65)
    print(f"  Period  : {start} → {end}")
    print(f"  File    : {out_path}")
    print(f"  Log     : {OUTREACH_LOG} {'✅' if OUTREACH_LOG.exists() else '⚠️  (not found — update outreach_log.csv)'}")
    print()
    print("  Run: make weekly-review")
    print("━" * 65)
    print()


if __name__ == "__main__":
    main()
