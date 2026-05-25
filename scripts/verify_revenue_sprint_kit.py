"""Verify the Revenue Sprint Kit.

Checks:
- docs/offers/revenue_sprint/ has 8 required files.
- PRICING.md mentions 499 SAR.
- SCOPE.md has in-scope and out-of-scope sections.
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

REQUIRED_KIT_FILES = [
    "SCOPE.md",
    "PRICING.md",
    "DELIVERABLES.md",
    "TIMELINE.md",
    "PROPOSAL_TEMPLATE.md",
    "REFUND_POLICY.md",
    "CASE_STUDY_TEMPLATE.md",
    "README.md",
]


def check_files() -> tuple[bool, list[str]]:
    base = REPO_ROOT / "docs" / "offers" / "revenue_sprint"
    missing = [f for f in REQUIRED_KIT_FILES if not (base / f).exists()]
    return (not missing, missing)


def check_pricing_499() -> bool:
    p = REPO_ROOT / "docs" / "offers" / "revenue_sprint" / "PRICING.md"
    if not p.exists():
        return False
    text = p.read_text(encoding="utf-8")
    return "499" in text and "SAR" in text


def check_scope_sections() -> tuple[bool, list[str]]:
    p = REPO_ROOT / "docs" / "offers" / "revenue_sprint" / "SCOPE.md"
    if not p.exists():
        return False, ["In scope", "Out of scope"]
    text = p.read_text(encoding="utf-8").lower()
    missing: list[str] = []
    if "in scope" not in text and "in-scope" not in text:
        missing.append("In scope")
    if "out of scope" not in text and "out-of-scope" not in text:
        missing.append("Out of scope")
    return (not missing, missing)


def main() -> int:
    failures: list[str] = []

    ok, missing = check_files()
    if ok:
        print(f"PASS docs/offers/revenue_sprint/ — all {len(REQUIRED_KIT_FILES)} files present")
    else:
        print(f"FAIL docs/offers/revenue_sprint/ — missing: {missing}")
        failures.append("kit_files")

    if check_pricing_499():
        print("PASS PRICING.md — 499 SAR present")
    else:
        print("FAIL PRICING.md — 499 SAR not found")
        failures.append("pricing_499")

    ok, missing_sections = check_scope_sections()
    if ok:
        print("PASS SCOPE.md — in/out scope sections present")
    else:
        print(f"FAIL SCOPE.md — missing sections: {missing_sections}")
        failures.append("scope_sections")

    if failures:
        print(f"\nverify_revenue_sprint_kit: FAIL ({len(failures)} checks)")
        return 1
    print("\nverify_revenue_sprint_kit: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
