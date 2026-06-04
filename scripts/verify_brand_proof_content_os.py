"""Verify Dealix Brand, Proof & Content Operating System v1 files exist.

See docs/content/BRAND_PROOF_CONTENT_OS.md.
"""

from __future__ import annotations

from pathlib import Path

required = [
    "docs/content/BRAND_PROOF_CONTENT_OS.md",
    "docs/content/BRAND_POSITIONING_SYSTEM.md",
    "docs/content/FOUNDER_VOICE_SYSTEM.md",
    "docs/content/PROOF_LEVEL_POLICY.md",
    "docs/content/CONTENT_PRODUCTION_SYSTEM.md",
    "docs/content/LINKEDIN_SYSTEM.md",
    "docs/content/CASE_STUDY_SYSTEM.md",
    "docs/content/SECTOR_REPORT_SYSTEM.md",
    "scripts/review_content_claims.py",
]

failures = []
for file in required:
    path = Path(file)
    if not path.exists():
        failures.append(f"Missing: {file}")
    elif path.stat().st_size < 120:
        failures.append(f"Too short: {file}")
if failures:
    print("Brand Proof Content OS verification failed:")
    for failure in failures:
        print("-", failure)
    raise SystemExit(1)
print("PASS: Brand Proof Content OS is ready.")
