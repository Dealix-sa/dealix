#!/usr/bin/env python3
"""Verify Dealix marketing OS docs are present."""
from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

REQUIRED = [
    "docs/marketing/DEALIX_MARKETING_OS.md",
    "docs/marketing/CONTENT_CALENDAR_SYSTEM.md",
    "docs/marketing/FOUNDER_LED_CONTENT_SYSTEM.md",
    "docs/marketing/LANDING_PAGE_CONVERSION_SYSTEM.md",
    "docs/marketing/COPYWRITING_RULES.md",
    "docs/marketing/BRAND_VOICE_EXAMPLES.md",
    "docs/marketing/EMAIL_OUTREACH_GUIDE.md",
    "docs/marketing/LINKEDIN_OUTREACH_GUIDE.md",
    "docs/marketing/PARTNER_OUTREACH_GUIDE.md",
    "docs/marketing/SECTOR_REPORT_SYSTEM.md",
    "docs/marketing/NEWSLETTER_SYSTEM.md",
    "docs/marketing/CASE_STUDY_SYSTEM.md",
    "docs/marketing/SOCIAL_PROOF_SYSTEM.md",
    "docs/marketing/SEO_CLUSTER_SYSTEM.md",
]


def main() -> int:
    missing = [f for f in REQUIRED if not (REPO / f).exists()]
    print("[marketing-system]")
    print(f"  missing files: {len(missing)}")
    for m in missing:
        print(f"    - {m}")
    print("RESULT:", "FAIL" if missing else "PASS")
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
