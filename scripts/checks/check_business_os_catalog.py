"""
check_business_os_catalog.py — verify business OS catalog and market entry docs.

Run from repo root:
    python scripts/checks/check_business_os_catalog.py
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.parent

TOP_40_PATH = REPO_ROOT / "docs/business_os_catalog/TOP_40_BUSINESS_SYSTEMS_AR.md"
FOCUS_5_PATH = REPO_ROOT / "docs/commercial/FOCUS_5_SYSTEMS_MARKET_ENTRY_AR.md"

MIN_H2_HEADERS = 5


def _count_h2_headers(path: Path) -> int:
    """Return the number of level-2 markdown headers (## ) in a file."""
    content = path.read_text(encoding="utf-8", errors="replace")
    return sum(1 for line in content.splitlines() if line.startswith("## "))


def _check_catalog_file(path: Path, label: str) -> int:
    """Check file exists and has at least MIN_H2_HEADERS ## sections. Returns failure count."""
    rel = path.relative_to(REPO_ROOT)
    if not path.exists():
        print(f"  FAIL  {label}: file not found at {rel}")
        return 1

    count = _count_h2_headers(path)
    if count >= MIN_H2_HEADERS:
        print(f"  PASS  {label}: found {count} '## ' entries (>= {MIN_H2_HEADERS})")
        return 0

    print(
        f"  FAIL  {label}: only {count} '## ' entries found (need >= {MIN_H2_HEADERS})"
    )
    return 1


def run_checks() -> int:
    """Run all catalog checks. Returns count of failures."""
    print("=" * 60)
    print("CHECK: business OS catalog")
    print("=" * 60)

    failures = 0
    failures += _check_catalog_file(TOP_40_PATH, "TOP_40_BUSINESS_SYSTEMS")
    failures += _check_catalog_file(FOCUS_5_PATH, "FOCUS_5_SYSTEMS_MARKET_ENTRY")

    total = 2
    passed = total - failures
    print("-" * 60)
    print(f"Summary: {passed}/{total} passed, {failures} failed")
    return failures


def main() -> None:
    failures = run_checks()
    sys.exit(0 if failures == 0 else 1)


if __name__ == "__main__":
    main()
