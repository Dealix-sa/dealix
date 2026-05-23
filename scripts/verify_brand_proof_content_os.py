#!/usr/bin/env python3
"""Verify the Brand, Proof, Content OS artifacts are in place."""
from __future__ import annotations

import sys
from pathlib import Path


REQUIRED = [
    "docs/content/BRAND_PROOF_CONTENT_OS.md",
    "docs/content/BRAND_POSITIONING_SYSTEM.md",
    "docs/content/FOUNDER_VOICE_SYSTEM.md",
    "docs/content/PROOF_LEVEL_POLICY.md",
    "docs/content/PROOF_APPROVAL_SYSTEM.md",
    "docs/content/CONTENT_PRODUCTION_SYSTEM.md",
    "docs/content/LINKEDIN_SYSTEM.md",
    "docs/content/CASE_STUDY_SYSTEM.md",
    "docs/content/SECTOR_REPORT_SYSTEM.md",
    "docs/content/CONTENT_TO_PIPELINE_SYSTEM.md",
    "scripts/review_content_claims.py",
]


def main() -> int:
    failures: list[str] = []
    for rel in REQUIRED:
        p = Path(rel)
        if not p.exists():
            failures.append(f"Missing: {rel}")
        elif p.stat().st_size < 30:
            failures.append(f"Too short: {rel}")
    if failures:
        print("Brand/Proof/Content OS verification FAILED:")
        for f in failures:
            print(" -", f)
        return 1
    print("PASS: Brand/Proof/Content OS is in place.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
