#!/usr/bin/env python3
"""
Verify the Dealix Marketing Operating System.

Checks:
- Required marketing docs exist.
- Marketing seed CSVs exist with required columns.
- No row carries banned claims.
"""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_DOCS = [
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
    "data/seeds/marketing/content_calendar.csv": [
        "slot_id", "date", "surface", "theme",
        "language", "status", "proof_required", "owner", "source",
    ],
    "data/seeds/marketing/campaigns.csv": [
        "campaign_id", "name", "theme", "start_date",
        "end_date", "owner", "kpi", "status", "source",
    ],
    "data/seeds/marketing/content_ideas.csv": [
        "idea_id", "topic", "theme", "format",
        "proof_required", "owner", "score", "status", "source",
    ],
}

BANNED = [
    "guaranteed revenue",
    "guaranteed sales",
    "guaranteed leads",
    "guaranteed results",
    "auto-pilot growth",
    "10x your pipeline",
]


def main() -> int:
    failures: list[str] = []
    passes: list[str] = []

    voice_examples = ROOT / "docs/marketing/BRAND_VOICE_EXAMPLES.md"

    for doc in REQUIRED_DOCS:
        if (ROOT / doc).exists():
            passes.append(f"doc exists: {doc}")
        else:
            failures.append(f"MISSING doc: {doc}")

    for csv_path, required_cols in REQUIRED_CSVS.items():
        path = ROOT / csv_path
        if not path.exists():
            failures.append(f"MISSING CSV: {csv_path}")
            continue
        with path.open("r", encoding="utf-8") as fh:
            reader = csv.reader(fh)
            try:
                header = next(reader)
            except StopIteration:
                failures.append(f"empty CSV: {csv_path}")
                continue
            missing_cols = [c for c in required_cols if c not in header]
            if missing_cols:
                failures.append(f"CSV {csv_path} missing columns: {missing_cols}")
            else:
                passes.append(f"CSV columns OK: {csv_path}")
            for row in reader:
                joined = " ".join(row).lower()
                for banned in BANNED:
                    if re.search(rf"\b{re.escape(banned.lower())}\b", joined):
                        failures.append(f"banned claim '{banned}' in row of {csv_path}")

    # Banned claims scan over marketing docs (except voice examples which document them).
    for doc_path in (ROOT / "docs/marketing").glob("*.md"):
        if doc_path.resolve() == voice_examples.resolve():
            continue
        if doc_path.name in {"COPYWRITING_RULES.md", "DEALIX_MARKETING_OS.md"}:
            continue  # these files document the bans themselves
        text = doc_path.read_text(encoding="utf-8").lower()
        for banned in BANNED:
            if re.search(rf"\b{re.escape(banned.lower())}\b", text):
                failures.append(f"banned claim '{banned}' in {doc_path.relative_to(ROOT)}")

    print(f"PASSED: {len(passes)}")
    for p in passes:
        print(f"  - {p}")
    print()
    print(f"FAILED: {len(failures)}")
    for f in failures:
        print(f"  - {f}")
    if failures:
        import os
        if os.environ.get("GITHUB_ACTIONS") == "true":
            for f in failures[:10]:
                msg = f.replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")
                print(f"::error title=Marketing verifier failure::{msg}")
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
