#!/usr/bin/env python3
"""
Classify a reply received from a prospect and log it to ledgers/reply_log.csv.
Also updates the prospect's verification_status in prospects.csv.

Reply classifications:
  interested       → move to approved_to_send or schedule call
  not_interested   → mark not_fit
  do_not_contact   → mark do_not_contact in both logs and prospects
  need_more_info   → send info pack, keep in pipeline
  meeting_request  → book meeting, high priority
  no_reply_needed  → neutral, log only

Usage:
    python scripts/founder/classify_replies.py \\
        --company "العيادة الطبية المتقدمة" \\
        --classification interested \\
        --notes "طلب جدول اجتماع هذا الأسبوع"
"""
from __future__ import annotations

import argparse
import csv
import sys
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REPLY_LOG = ROOT / "ledgers" / "reply_log.csv"
PROSPECTS = ROOT / "ledgers" / "prospects.csv"

REPLY_SCHEMA = [
    "date", "company_name", "classification", "reply_channel",
    "reply_summary", "next_action", "next_action_date", "notes",
]

PROSPECT_SCHEMA = [
    "company_name", "sector", "city", "website", "source_url",
    "contact_page_url", "public_email", "phone", "linkedin_url",
    "verification_status", "confidence", "pain_hypothesis",
    "dealix_angle", "recommended_product", "message_stage",
    "next_action", "owner_decision",
]

CLASSIFICATIONS = {
    "interested": ("approved_to_send", "book_discovery_call", 1),
    "not_interested": ("not_fit", "archive", 30),
    "do_not_contact": ("do_not_contact", "do_not_contact", 999),
    "need_more_info": ("ready_for_review", "send_info_pack", 2),
    "meeting_request": ("approved_to_send", "confirm_meeting", 0),
    "no_reply_needed": (None, "monitor", 7),
}


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, str]], schema: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=schema, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser(description="Classify a prospect reply")
    parser.add_argument("--company", required=True)
    parser.add_argument("--classification", required=True, choices=list(CLASSIFICATIONS))
    parser.add_argument("--channel", default="whatsapp", help="Channel reply came through")
    parser.add_argument("--summary", default="", help="Brief summary of reply")
    parser.add_argument("--notes", default="")
    args = parser.parse_args()

    new_status, next_action, days = CLASSIFICATIONS[args.classification]
    next_date = (date.today() + timedelta(days=days)).isoformat() if days < 999 else "never"

    # Log reply
    reply_row = {
        "date": date.today().isoformat(),
        "company_name": args.company,
        "classification": args.classification,
        "reply_channel": args.channel,
        "reply_summary": args.summary,
        "next_action": next_action,
        "next_action_date": next_date,
        "notes": args.notes,
    }
    reply_rows = read_csv(REPLY_LOG)
    reply_rows.append(reply_row)
    write_csv(REPLY_LOG, reply_rows, REPLY_SCHEMA)

    # Update prospect
    if new_status is not None:
        prospect_rows = read_csv(PROSPECTS)
        name_lower = args.company.strip().lower()
        updated = False
        for row in prospect_rows:
            if (row.get("company_name") or "").strip().lower() == name_lower:
                row["verification_status"] = new_status
                row["next_action"] = next_action
                row["message_stage"] = f"reply_{args.classification}"
                updated = True
        write_csv(PROSPECTS, prospect_rows, PROSPECT_SCHEMA)
        status_msg = f"Prospect status → {new_status}" if updated else "Prospect not found in ledger (reply logged)"
    else:
        status_msg = "No status change"

    print(f"REPLY_LOGGED: {args.company} — {args.classification}")
    print(f"  {status_msg}")
    print(f"  Next action: {next_action} by {next_date}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
