#!/usr/bin/env python3
"""Verify Dealix positioning assets exist and carry no unsafe claims.

Checks that the core positioning + offer + start-path documents are present
and that none of them contain guaranteed-outcome language or auto-send wording.

Terminal markers:
    POSITIONING_FILES_PASS=true|false
    POSITIONING_CLAIMS_PASS=true|false
    DEALIX_POSITIONING_OK=true|false
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from scripts._wave8_scan import scan_files  # noqa: E402

POSITIONING_FILES = (
    "docs/company/POSITIONING.md",
    "docs/commercial/POSITIONING_WHY_NOW_SAUDI_ONEPAGER_AR.md",
    "docs/commercial/sales/P1_REVENUE_INTELLIGENCE_SPRINT_OFFER_AR.md",
    "docs/sales/ONE_PAGER.md",
    "docs/sales-kit/START_HERE.md",
)

# Unsafe claim patterns (guaranteed revenue / outcome) — English + Arabic.
UNSAFE_CLAIM_PATTERNS = (
    r"guaranteed\s+(revenue|results?|roi|return|income)",
    r"guarantee\s+(you|your)\s+(revenue|results?|sales)",
    r"\bنضمن\s+(لك\s+)?(زيادة|أرباح|إيراد|نتائج|مبيعات)",
    r"عائد\s+مضمون",
    r"أرباح\s+مضمونة",
)

# Auto-send / automation patterns that must not appear in positioning copy.
AUTO_SEND_PATTERNS = (
    r"auto[-\s]?send",
    r"automatically\s+send",
    r"cold\s+whatsapp\s+automation",
    r"linkedin\s+automation",
    r"إرسال\s+تلقائي",
)


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, OSError):
        # UTF-8 reconfigure is best-effort; the default stream is fine if unavailable.
        pass

    missing = [f for f in POSITIONING_FILES if not (REPO / f).is_file()]
    files_ok = not missing
    for m in missing:
        print(f"MISSING: {m}")

    claim_hits = scan_files(REPO, POSITIONING_FILES, UNSAFE_CLAIM_PATTERNS)
    autosend_hits = scan_files(REPO, POSITIONING_FILES, AUTO_SEND_PATTERNS)
    claims_ok = not claim_hits and not autosend_hits
    for h in claim_hits + autosend_hits:
        print(f"UNSAFE: {h}")

    print(f"POSITIONING_FILES_PASS={'true' if files_ok else 'false'}")
    print(f"POSITIONING_CLAIMS_PASS={'true' if claims_ok else 'false'}")
    ok = files_ok and claims_ok
    print(f"DEALIX_POSITIONING_OK={'true' if ok else 'false'}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
