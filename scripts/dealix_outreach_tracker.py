#!/usr/bin/env python3
"""
Dealix Outreach Tracker
========================
CLI to log and update outreach activity in outreach_log.csv without
opening a spreadsheet. The founder runs this after each outreach action.

Usage:
  # Log a new outreach event:
  python3 scripts/dealix_outreach_tracker.py log \
    --company "شركة نجم اللوجستية" \
    --sector logistics \
    --status sent

  # Update a company's status:
  python3 scripts/dealix_outreach_tracker.py update \
    --company "شركة نجم اللوجستية" \
    --status reply \
    --note "مهتمين بالتشخيص المجاني"

  # Show current pipeline summary:
  python3 scripts/dealix_outreach_tracker.py summary

  # List all companies in a given status:
  python3 scripts/dealix_outreach_tracker.py list --status sent

Doctrine: local file only. Nothing leaves this machine without founder action.
"""

from __future__ import annotations

import argparse
import csv
import os
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
LOG_FILE = REPO_ROOT / "data/outreach/outreach_log.csv"
FIELDNAMES = ["date", "company", "sector", "status", "replied", "note"]
VALID_STATUSES = ["drafted", "sent", "reply", "meeting", "won", "lost"]
STATUS_AR = {
    "drafted": "مسودة",
    "sent": "تم الإرسال",
    "reply": "جاء رد",
    "meeting": "اجتماع",
    "won": "إغلاق",
    "lost": "خسارة",
}


def _load_log() -> list[dict]:
    if not LOG_FILE.exists():
        return []
    with LOG_FILE.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        return [dict(r) for r in reader]


def _save_log(rows: list[dict]) -> None:
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with LOG_FILE.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


def _normalize(name: str) -> str:
    return name.strip().lower().replace(" ", "")


def cmd_log(args: argparse.Namespace) -> None:
    if args.status not in VALID_STATUSES:
        print(f"[ERROR] Invalid status: {args.status}. Choose from: {', '.join(VALID_STATUSES)}")
        return

    rows = _load_log()
    existing = [r for r in rows if _normalize(r.get("company", "")) == _normalize(args.company)]
    if existing:
        print(f"[WARN] {args.company} already exists. Use 'update' to change status.")
        print(f"       Current status: {existing[-1].get('status')}")
        return

    new_row = {
        "date": date.today().isoformat(),
        "company": args.company,
        "sector": args.sector or "",
        "status": args.status,
        "replied": "yes" if args.status in ("reply", "meeting", "won") else "no",
        "note": args.note or "",
    }
    rows.append(new_row)
    _save_log(rows)
    print(f"✅ Logged: {args.company} → {args.status} ({STATUS_AR.get(args.status, '')})")


def cmd_update(args: argparse.Namespace) -> None:
    if args.status and args.status not in VALID_STATUSES:
        print(f"[ERROR] Invalid status: {args.status}. Choose from: {', '.join(VALID_STATUSES)}")
        return

    rows = _load_log()
    updated = False
    for row in rows:
        if _normalize(row.get("company", "")) == _normalize(args.company):
            old_status = row.get("status")
            if args.status:
                row["status"] = args.status
                if args.status in ("reply", "meeting", "won"):
                    row["replied"] = "yes"
            if args.note:
                row["note"] = args.note
            row["date"] = date.today().isoformat()
            updated = True
            new_status = row["status"]
            print(f"✅ Updated: {args.company}")
            print(f"   {old_status} → {new_status} ({STATUS_AR.get(new_status, '')})")
            if args.note:
                print(f"   Note: {args.note}")

    if not updated:
        print(f"[NOT FOUND] '{args.company}' not in outreach_log.csv. Use 'log' to add it.")
        return

    _save_log(rows)


def cmd_list(args: argparse.Namespace) -> None:
    rows = _load_log()
    if args.status:
        rows = [r for r in rows if r.get("status") == args.status]

    if not rows:
        if args.status:
            print(f"No companies with status '{args.status}'.")
        else:
            print("outreach_log.csv is empty.")
        return

    # Group by status
    by_status: dict[str, list[dict]] = {}
    for r in rows:
        s = r.get("status", "—")
        by_status.setdefault(s, []).append(r)

    print()
    for status in VALID_STATUSES:
        entries = by_status.get(status, [])
        if not entries:
            continue
        print(f"── {STATUS_AR.get(status, status)} ({status}) ── {len(entries)} شركة")
        for r in entries:
            note = f" — {r['note']}" if r.get("note") else ""
            print(f"  • {r['company']} [{r.get('sector', '—')}]{note}")
        print()


def cmd_summary(args: argparse.Namespace) -> None:
    rows = _load_log()
    if not rows:
        print("\n⚠️  outreach_log.csv فارغ. استخدم 'log' لإضافة شركات.\n")
        return

    from collections import Counter
    status_counts = Counter(r.get("status", "drafted") for r in rows)
    total = len(rows)
    sent = sum(1 for r in rows if r.get("status") in ("sent", "reply", "meeting", "won"))
    replied = sum(1 for r in rows if r.get("status") in ("reply", "meeting", "won"))
    won = sum(1 for r in rows if r.get("status") == "won")
    reply_rate = f"{replied / sent * 100:.1f}%" if sent else "—"

    print()
    print("━" * 55)
    print(" 📊 ملخص Pipeline — Dealix Outreach Tracker")
    print("━" * 55)
    print(f"  الإجمالي / Total      : {total}")
    print(f"  تم الإرسال / Sent     : {sent}")
    print(f"  جاء رد / Replied      : {replied}")
    print(f"  معدل الرد / Reply rate: {reply_rate}")
    print(f"  اجتماعات / Meetings   : {status_counts.get('meeting', 0)}")
    print(f"  إغلاق / Won           : {won}")
    print()
    print("  Pipeline:")
    for status in VALID_STATUSES:
        count = status_counts.get(status, 0)
        if count:
            bar = "█" * min(count, 20)
            print(f"  {STATUS_AR.get(status, status):<12} / {status:<8}: {bar} ({count})")
    print()
    print("  Quick actions:")
    if status_counts.get("drafted", 0):
        print(f"  → {status_counts['drafted']} مسودة جاهزة → راجعها وأرسلها: make outreach")
    if status_counts.get("sent", 0):
        print(f"  → {status_counts['sent']} تم الإرسال → تابع: make outreach-f3")
    if status_counts.get("reply", 0):
        print(f"  → {status_counts['reply']} جاء رد → رد وحجز موعد: python scripts/dealix_reply_classifier.py")
    if status_counts.get("meeting", 0):
        print(f"  → {status_counts['meeting']} اجتماع → جهّز agenda: make meeting COMPANY='...' SECTOR='...'")
    print("━" * 55)
    print()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Track outreach activity in outreach_log.csv from the terminal"
    )
    sub = parser.add_subparsers(dest="command")

    # log
    p_log = sub.add_parser("log", help="Log a new outreach event")
    p_log.add_argument("--company", required=True, help="Company name")
    p_log.add_argument("--sector", help="Sector key")
    p_log.add_argument("--status", required=True, choices=VALID_STATUSES)
    p_log.add_argument("--note", help="Optional note")

    # update
    p_upd = sub.add_parser("update", help="Update an existing company's status")
    p_upd.add_argument("--company", required=True)
    p_upd.add_argument("--status", choices=VALID_STATUSES)
    p_upd.add_argument("--note", help="Optional note to add")

    # list
    p_list = sub.add_parser("list", help="List companies (optionally filtered by status)")
    p_list.add_argument("--status", choices=VALID_STATUSES, help="Filter by status")

    # summary
    sub.add_parser("summary", help="Show pipeline summary")

    args = parser.parse_args()

    if args.command == "log":
        cmd_log(args)
    elif args.command == "update":
        cmd_update(args)
    elif args.command == "list":
        cmd_list(args)
    elif args.command == "summary":
        cmd_summary(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
