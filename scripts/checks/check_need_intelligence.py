"""
check_need_intelligence.py — verify sprint library and business needs docs.

Run from repo root:
    python scripts/checks/check_need_intelligence.py
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.parent

SPRINT_LIBRARY_PATH = (
    REPO_ROOT / "docs/business_need_intelligence/SPECIALIZED_SPRINT_LIBRARY_50_AR.md"
)
BUSINESS_NEEDS_PATH = (
    REPO_ROOT / "docs/business_need_intelligence/BUSINESS_NEEDS_25_AR.md"
)

MIN_SPRINT_H2 = 20
MIN_NEEDS_H2 = 10


def _count_h2_headers(path: Path) -> int:
    """Return the number of level-2 markdown headers (## ) in a file."""
    content = path.read_text(encoding="utf-8", errors="replace")
    return sum(1 for line in content.splitlines() if line.startswith("## "))


def run_checks() -> int:
    """Run all need-intelligence checks. Returns count of failures."""
    print("=" * 60)
    print("CHECK: need intelligence")
    print("=" * 60)

    failures = 0
    total = 0

    # Sprint library — existence + header count
    total += 1
    if not SPRINT_LIBRARY_PATH.exists():
        print(
            f"  FAIL  SPRINT_LIBRARY: file not found at "
            f"{SPRINT_LIBRARY_PATH.relative_to(REPO_ROOT)}"
        )
        failures += 1
    else:
        total += 1  # second sub-check
        count = _count_h2_headers(SPRINT_LIBRARY_PATH)
        print(f"  PASS  SPRINT_LIBRARY: file found")
        if count >= MIN_SPRINT_H2:
            print(f"  PASS  SPRINT_LIBRARY: {count} sprint entries (>= {MIN_SPRINT_H2})")
        else:
            print(
                f"  FAIL  SPRINT_LIBRARY: only {count} '## ' entries "
                f"(need >= {MIN_SPRINT_H2})"
            )
            failures += 1

    # Business needs — existence (header count optional)
    total += 1
    if not BUSINESS_NEEDS_PATH.exists():
        print(
            f"  FAIL  BUSINESS_NEEDS: file not found at "
            f"{BUSINESS_NEEDS_PATH.relative_to(REPO_ROOT)}"
        )
        failures += 1
    else:
        total += 1  # second sub-check
        count = _count_h2_headers(BUSINESS_NEEDS_PATH)
        print(f"  PASS  BUSINESS_NEEDS: file found")
        if count >= MIN_NEEDS_H2:
            print(f"  PASS  BUSINESS_NEEDS: {count} entries (>= {MIN_NEEDS_H2})")
        else:
            print(
                f"  FAIL  BUSINESS_NEEDS: only {count} '## ' entries "
                f"(need >= {MIN_NEEDS_H2})"
            )
            failures += 1

    passed = total - failures
    print("-" * 60)
    print(f"Summary: {passed}/{total} passed, {failures} failed")
    return failures


def main() -> None:
    failures = run_checks()
    sys.exit(0 if failures == 0 else 1)


if __name__ == "__main__":
    main()
