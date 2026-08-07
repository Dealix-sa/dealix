#!/usr/bin/env python3
"""
Dealix Daily Ops Command
=========================
Single command the founder runs every morning to know exactly what to do today.
Reads from outreach_log.csv, contract_log.csv, and proposals/ directory.
Prints a bilingual AR+EN prioritized action checklist.

Usage:
  python3 scripts/dealix_daily_ops.py
  make daily-ops

Doctrine: read-only. No auto-send. No AI calls. Pure local data aggregation.
"""

from __future__ import annotations

import csv
from collections import Counter
from datetime import date, datetime, timedelta
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
OUTREACH_LOG = REPO_ROOT / "data/outreach/outreach_log.csv"
OUTREACH_TEMPLATE = REPO_ROOT / "data/outreach/outreach_log.template.csv"
CONTRACT_LOG = REPO_ROOT / "data/contracts/contract_log.csv"
PROPOSALS_DIR = REPO_ROOT / "reports/proposals"
MEETINGS_DIR = REPO_ROOT / "reports/meetings"


def _read_csv(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as f:
        return [dict(r) for r in csv.DictReader(f)]


def _days_until(date_str: str) -> int | None:
    try:
        d = datetime.strptime(date_str.strip(), "%Y-%m-%d").date()
        return (d - date.today()).days
    except (ValueError, AttributeError):
        return None


def _count_proposals_last_days(days: int = 7) -> int:
    if not PROPOSALS_DIR.exists():
        return 0
    cutoff = date.today() - timedelta(days=days)
    count = 0
    for day_dir in PROPOSALS_DIR.iterdir():
        if not day_dir.is_dir():
            continue
        try:
            d = datetime.strptime(day_dir.name, "%Y-%m-%d").date()
            if d >= cutoff:
                count += len(list(day_dir.glob("*.md")))
        except ValueError:
            continue
    return count


def _urgent_actions(outreach: list[dict], contracts: list[dict]) -> list[tuple[str, str, str]]:
    """Returns list of (priority, action_ar, action_en) tuples."""
    actions = []

    # Contracts expiring in next 14 days
    for row in contracts:
        if row.get("status", "") not in ("active", "paused"):
            continue
        days = _days_until(row.get("end_date", ""))
        if days is not None and 0 <= days <= 14:
            company = row.get("company", "?")
            actions.append((
                "🔴 URGENT",
                f"عقد {company} ينتهي خلال {days} يوم — جدد الآن",
                f"Contract for {company} expires in {days} days — renew now",
            ))

    # Replies that need response (reply status with recent date)
    reply_rows = [r for r in outreach if r.get("status") == "reply"]
    for row in reply_rows:
        days = _days_until(row.get("date", ""))
        if days is not None and days >= -3:
            company = row.get("company", "?")
            actions.append((
                "🔴 URGENT",
                f"رد من {company} بحاجة لمتابعة — حجز موعد",
                f"Reply from {company} needs follow-up — book meeting",
            ))

    # Meetings booked (follow up after)
    meeting_rows = [r for r in outreach if r.get("status") == "meeting"]
    if meeting_rows:
        actions.append((
            "🟠 HIGH",
            f"عندك {len(meeting_rows)} اجتماع مجدول — جهّز agenda",
            f"You have {len(meeting_rows)} scheduled meeting(s) — prep agenda",
        ))

    # Day-3 follow-ups
    f3_candidates = [
        r for r in outreach
        if r.get("status") == "sent"
        and r.get("replied", "") != "yes"
        and _days_until(r.get("date", "")) is not None
        and -7 <= (_days_until(r.get("date", "")) or 0) <= -3
    ]
    if f3_candidates:
        actions.append((
            "🟠 HIGH",
            f"{len(f3_candidates)} شركة تستحق متابعة يوم 3 — make outreach-f3",
            f"{len(f3_candidates)} companies need day-3 follow-up — make outreach-f3",
        ))

    # Day-7 follow-ups
    f7_candidates = [
        r for r in outreach
        if r.get("status") == "sent"
        and _days_until(r.get("date", "")) is not None
        and -14 <= (_days_until(r.get("date", "")) or 0) <= -7
    ]
    if f7_candidates:
        actions.append((
            "🟡 MEDIUM",
            f"{len(f7_candidates)} شركة تستحق متابعة يوم 7 — make outreach-f7",
            f"{len(f7_candidates)} companies need day-7 follow-up — make outreach-f7",
        ))

    # Weekly content
    actions.append((
        "🟡 MEDIUM",
        "منشور LinkedIn الأسبوعي — make content",
        "Weekly LinkedIn post — make content",
    ))

    # New outreach
    drafted_count = sum(1 for r in outreach if r.get("status") == "drafted")
    if drafted_count > 0:
        actions.append((
            "🟡 MEDIUM",
            f"{drafted_count} مسودة جاهزة — راجع وأرسل: make outreach",
            f"{drafted_count} drafts ready — review and send: make outreach",
        ))
    else:
        actions.append((
            "🟢 LOW",
            "جهّز رسائل الأسبوع الجديد — make outreach",
            "Prepare new week's outreach — make outreach",
        ))

    return actions


def run() -> None:
    outreach = _read_csv(OUTREACH_LOG)
    if not outreach:
        outreach = _read_csv(OUTREACH_TEMPLATE)
    contracts = _read_csv(CONTRACT_LOG)

    today = date.today()
    status_counts = Counter(r.get("status", "drafted") for r in outreach)
    active_contracts = [r for r in contracts if r.get("status") == "active"]
    mrr = sum(int(r.get("monthly_sar", 0)) for r in active_contracts)
    proposals_this_week = _count_proposals_last_days(7)

    actions = _urgent_actions(outreach, contracts)
    # Sort by priority: 🔴 first, then 🟠, then 🟡, then 🟢
    priority_order = {"🔴": 0, "🟠": 1, "🟡": 2, "🟢": 3}
    actions.sort(key=lambda x: priority_order.get(x[0][0], 9))

    print()
    print("━" * 65)
    print(f"🌅 Dealix Daily Ops — {today.strftime('%A, %Y-%m-%d')}")
    print("━" * 65)
    print()
    print("  📊 الوضع الحالي | Current Status")
    print(f"     Pipeline     : {len(outreach)} شركة")
    print(f"     Sent         : {status_counts.get('sent', 0)}")
    print(f"     Replies      : {status_counts.get('reply', 0)}")
    print(f"     Meetings     : {status_counts.get('meeting', 0)}")
    print(f"     Won          : {status_counts.get('won', 0)}")
    print(f"     Active MRR   : {mrr:,} SAR/mo ({len(active_contracts)} customers)")
    print(f"     Proposals    : {proposals_this_week} this week")
    print()
    print("  ✅ قائمة أعمال اليوم | Today's Action List")
    print()

    if not actions:
        print("     ✨ لا شيء عاجل اليوم. استمر في الاتجاه الصحيح!")
        print("     ✨ Nothing urgent today. Keep up the momentum!")
    else:
        for i, (priority, action_ar, action_en) in enumerate(actions[:8], 1):
            print(f"  [{i}] {priority}")
            print(f"      AR: {action_ar}")
            print(f"      EN: {action_en}")
            print()

    print()
    print("  🔧 أوامر سريعة | Quick Commands")
    print("     make outreach-tracker-summary   # pipeline overview")
    print("     make weekly-review-print        # full GTM report")
    print("     make renewal-check              # contracts expiring soon")
    print("     make command-room               # visual dashboard")
    print()
    print("━" * 65)
    print()


if __name__ == "__main__":
    run()
