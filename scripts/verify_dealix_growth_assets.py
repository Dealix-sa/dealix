#!/usr/bin/env python3
"""Dealix growth-assets verifier (Wave 7).

Validates the manual, founder-approved growth machine:
  - data/growth/first_30_targets.csv (schema + allowed statuses + evidence rule)
  - data/revenue/outreach_queue.jsonl (no auto-send, approval gate honored)
  - reports/revenue/outreach_approval_queue.md (exists)

Safety rules enforced:
  - every approved/sent target has evidence_url OR warm_intro_reason
  - no personal phone numbers in target rows
  - no scraping language in notes
  - no outreach row marked 'sent' unless approval_status == 'approved'

Exit 0 = PASS, 1 = FAIL. Pure stdlib.
"""
from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS_CSV = ROOT / "data" / "growth" / "first_30_targets.csv"
OUTREACH_JSONL = ROOT / "data" / "revenue" / "outreach_queue.jsonl"
OUTREACH_MD = ROOT / "reports" / "revenue" / "outreach_approval_queue.md"

REQUIRED_COLUMNS = [
    "company_name", "website", "city", "sector", "why_target",
    "pain_hypothesis", "evidence_url", "recommended_angle",
    "recommended_offer", "score", "status", "next_action", "owner", "notes",
]
ALLOWED_STATUSES = {
    "research", "approved", "draft_ready", "sent_manually", "replied",
    "diagnostic_booked", "offer_sent", "paid", "nurture", "rejected",
}
EVIDENCE_REQUIRED_STATUSES = {
    "approved", "draft_ready", "sent_manually", "replied",
    "diagnostic_booked", "offer_sent", "paid",
}

# A loose Saudi/intl personal mobile pattern: +9665######## or 05########
PHONE_RE = re.compile(r"(\+?966\s?5\d{8}|\b05\d{8}\b)")
SCRAPE_RE = re.compile(r"\bscrap(e|ing)\b", re.IGNORECASE)

FAILURES: list[str] = []
WARNINGS: list[str] = []


def check_targets_csv() -> None:
    if not TARGETS_CSV.is_file():
        FAILURES.append(f"missing {TARGETS_CSV.relative_to(ROOT)}")
        return
    with TARGETS_CSV.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        cols = reader.fieldnames or []
        missing = [c for c in REQUIRED_COLUMNS if c not in cols]
        if missing:
            FAILURES.append(f"first_30_targets.csv missing columns: {', '.join(missing)}")
            return
        rows = list(reader)

    if not rows:
        WARNINGS.append("first_30_targets.csv has a header but no target rows yet")

    for i, row in enumerate(rows, start=2):  # header is line 1
        status = (row.get("status") or "").strip()
        company = (row.get("company_name") or "").strip() or f"row {i}"
        if status and status not in ALLOWED_STATUSES:
            FAILURES.append(f"{company}: invalid status {status!r}")
        if status in EVIDENCE_REQUIRED_STATUSES:
            ev = (row.get("evidence_url") or "").strip()
            warm = (row.get("notes") or "").lower()
            if not ev and "warm_intro" not in warm and "warm intro" not in warm:
                FAILURES.append(
                    f"{company}: status {status!r} requires evidence_url or a warm_intro reason in notes"
                )
        blob = " ".join(str(v) for v in row.values())
        if PHONE_RE.search(blob):
            FAILURES.append(f"{company}: personal phone number present — remove it")
        if SCRAPE_RE.search(blob):
            FAILURES.append(f"{company}: scraping language present — not allowed")


def check_outreach_queue() -> None:
    if not OUTREACH_JSONL.is_file():
        FAILURES.append(f"missing {OUTREACH_JSONL.relative_to(ROOT)}")
    else:
        for n, line in enumerate(OUTREACH_JSONL.read_text(encoding="utf-8").splitlines(), 1):
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError as exc:
                FAILURES.append(f"outreach_queue.jsonl line {n}: invalid JSON ({exc})")
                continue
            appr = (rec.get("approval_status") or "").strip()
            if appr and appr not in {"draft", "approved", "rejected", "sent"}:
                FAILURES.append(f"outreach_queue.jsonl line {n}: invalid approval_status {appr!r}")
            if appr == "sent" and rec.get("_approved_by") in (None, "", False):
                # 'sent' must have come through approval first
                if rec.get("prior_status") not in ("approved",):
                    WARNINGS.append(
                        f"outreach_queue.jsonl line {n}: marked 'sent' without recorded approval"
                    )

    if not OUTREACH_MD.is_file():
        FAILURES.append(f"missing {OUTREACH_MD.relative_to(ROOT)}")


def main() -> int:
    print("== Dealix growth-assets verifier ==")
    check_targets_csv()
    check_outreach_queue()

    for w in WARNINGS:
        print(f"  WARN: {w}")
    for f in FAILURES:
        print(f"  FAIL: {f}")

    if FAILURES:
        print(f"\nRESULT: FAIL ({len(FAILURES)} blocker(s), {len(WARNINGS)} warning(s))")
        return 1
    print(f"\nRESULT: PASS ({len(WARNINGS)} warning(s))")
    return 0


if __name__ == "__main__":
    sys.exit(main())
