#!/usr/bin/env python3
"""
Log a manual outreach send to ledgers/outreach_log.csv.

Every message sent by the founder must be logged here.
This is the audit trail for controlled outbound compliance.

Usage:
    python scripts/founder/log_manual_send.py \\
        --company "العيادة الطبية المتقدمة" \\
        --channel whatsapp \\
        --product "WhatsApp / Inbox Follow-up OS" \\
        --draft-file outbox/2026-06-21/01_clinic_draft.txt
"""
from __future__ import annotations

import argparse
import csv
import sys
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUTREACH_LOG = ROOT / "ledgers" / "outreach_log.csv"

SCHEMA = [
    "date", "time", "company_name", "channel", "phone_or_email",
    "product", "draft_file", "sent_by", "message_preview",
    "follow_up_date", "notes",
]

VALID_CHANNELS = {"whatsapp", "email", "linkedin", "sms", "phone"}


def read_log() -> list[dict[str, str]]:
    if not OUTREACH_LOG.exists():
        return []
    with OUTREACH_LOG.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_log(rows: list[dict[str, str]]) -> None:
    OUTREACH_LOG.parent.mkdir(parents=True, exist_ok=True)
    with OUTREACH_LOG.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=SCHEMA, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser(description="Log a manual outreach send")
    parser.add_argument("--company", required=True, help="Company name")
    parser.add_argument("--channel", required=True, choices=list(VALID_CHANNELS), help="Channel used")
    parser.add_argument("--product", default="", help="Product recommended")
    parser.add_argument("--phone-or-email", dest="contact", default="", help="Contact info used")
    parser.add_argument("--draft-file", default="", help="Path to draft file sent")
    parser.add_argument("--follow-up-days", type=int, default=3, help="Days until follow-up")
    parser.add_argument("--notes", default="", help="Any notes")
    args = parser.parse_args()

    preview = ""
    if args.draft_file:
        p = Path(args.draft_file)
        if p.exists():
            preview = p.read_text(encoding="utf-8")[:200].replace("\n", " ")

    from datetime import timedelta
    now = datetime.now()
    follow_up_date = (date.today() + timedelta(days=args.follow_up_days)).isoformat()

    row = {
        "date": date.today().isoformat(),
        "time": now.strftime("%H:%M"),
        "company_name": args.company,
        "channel": args.channel,
        "phone_or_email": args.contact,
        "product": args.product,
        "draft_file": args.draft_file,
        "sent_by": "founder",
        "message_preview": preview,
        "follow_up_date": follow_up_date,
        "notes": args.notes,
    }

    rows = read_log()
    rows.append(row)
    write_log(rows)

    print(f"LOG_OK: Send logged to {OUTREACH_LOG}")
    print(f"  Company:    {args.company}")
    print(f"  Channel:    {args.channel}")
    print(f"  Follow-up:  {follow_up_date}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
