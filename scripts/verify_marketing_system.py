#!/usr/bin/env python3
"""Verify the Dealix Marketing OS.

Checks:
- Required marketing docs exist.
- Marketing runtime CSVs exist with the canonical headers.
- No banned phrases in marketing docs.
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

REQUIRED_MARKETING_DOCS = [
    "docs/marketing/DEALIX_MARKETING_OS.md",
    "docs/marketing/CONTENT_CALENDAR_SYSTEM.md",
    "docs/marketing/FOUNDER_LED_CONTENT_SYSTEM.md",
    "docs/marketing/LANDING_PAGE_CONVERSION_SYSTEM.md",
    "docs/marketing/COPYWRITING_RULES.md",
    "docs/marketing/BRAND_VOICE_EXAMPLES.md",
    "docs/marketing/EMAIL_OUTREACH_GUIDE.md",
    "docs/marketing/LINKEDIN_OUTREACH_GUIDE.md",
    "docs/marketing/PARTNER_OUTREACH_GUIDE.md",
]

REQUIRED_CSVS = {
    "data/marketing/content_calendar.csv": [
        "calendar_id",
        "week",
        "day",
        "channel",
        "format",
        "pillar",
        "persona",
        "language",
        "title",
        "evidence_cited",
        "approval_state",
    ],
    "data/marketing/content_ideas.csv": [
        "idea_id",
        "pillar",
        "persona",
        "language",
        "format",
        "channel",
        "title",
        "evidence",
        "approval_state",
    ],
    "data/marketing/campaigns.csv": [
        "campaign_id",
        "name",
        "quarter",
        "sector",
        "target_persona",
        "offer",
        "channel",
        "owner",
        "kpi",
        "status",
    ],
    "data/marketing/outreach_drafts.csv": [
        "draft_id",
        "account_id",
        "target_contact",
        "channel",
        "language",
        "subject",
        "body",
        "personalisation_evidence",
        "proof_attached",
        "recommended_offer",
        "approval_state",
    ],
    "data/marketing/outreach_replies.csv": [
        "reply_id",
        "draft_id",
        "received_at",
        "classification",
        "next_action",
    ],
}

BANNED_PHRASES = [
    "guaranteed revenue",
    "guaranteed sales",
    "guaranteed results",
    "guaranteed outcome",
    "fully autonomous",
    "ai that sells for you",
    "10x revenue",
    "100x",
    "revolutionise",
    "revolutionize",
]

BANNED_ALLOWLIST = {
    "docs/marketing/COPYWRITING_RULES.md",
    "docs/marketing/BRAND_VOICE_EXAMPLES.md",
    "docs/marketing/DEALIX_MARKETING_OS.md",
    "docs/marketing/CONTENT_CALENDAR_SYSTEM.md",
    "docs/marketing/LANDING_PAGE_CONVERSION_SYSTEM.md",
    "docs/marketing/EMAIL_OUTREACH_GUIDE.md",
    "docs/marketing/LINKEDIN_OUTREACH_GUIDE.md",
}


def check_files(failures: list[str]) -> None:
    for rel in REQUIRED_MARKETING_DOCS:
        if not (ROOT / rel).exists():
            failures.append(f"missing file: {rel}")
    for rel in REQUIRED_CSVS:
        if not (ROOT / rel).exists():
            failures.append(f"missing file: {rel}")


def check_csv_headers(failures: list[str]) -> None:
    for rel, required in REQUIRED_CSVS.items():
        p = ROOT / rel
        if not p.exists():
            continue
        with p.open(newline="", encoding="utf-8") as f:
            try:
                header = next(csv.reader(f))
            except StopIteration:
                failures.append(f"{rel}: empty CSV")
                continue
        for col in required:
            if col not in header:
                failures.append(f"{rel}: missing required column '{col}'")


def check_banned(failures: list[str]) -> None:
    marketing_dir = ROOT / "docs/marketing"
    if not marketing_dir.exists():
        return
    for path in marketing_dir.rglob("*.md"):
        rel = str(path.relative_to(ROOT)).replace("\\", "/")
        if rel in BANNED_ALLOWLIST:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore").lower()
        for phrase in BANNED_PHRASES:
            if phrase in text:
                failures.append(f"banned phrase '{phrase}' found in {rel}")


def main() -> int:
    failures: list[str] = []
    check_files(failures)
    check_csv_headers(failures)
    check_banned(failures)

    print("=" * 60)
    print("Dealix Marketing System Verifier")
    print("=" * 60)
    if not failures:
        print("[PASS] marketing system verified")
        return 0
    print(f"[FAIL] {len(failures)} issue(s):")
    for f in failures:
        print(f"  - {f}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
