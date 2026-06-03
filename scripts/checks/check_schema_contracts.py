"""
check_schema_contracts.py — validate DATA_OS.md and SOURCE_PASSPORT.md schema sections.

Run from repo root:
    python scripts/checks/check_schema_contracts.py
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.parent

DATA_OS_PATH = REPO_ROOT / "docs/04_data_os/DATA_OS.md"
SOURCE_PASSPORT_PATH = REPO_ROOT / "docs/04_data_os/SOURCE_PASSPORT.md"

DATA_OS_REQUIRED_SECTIONS = ["Schema", "Contract", "Quality"]
SOURCE_PASSPORT_FIELD_MARKERS = ["required_fields", "fields"]


def _check_file_sections(path: Path, required_sections: list[str], label: str) -> int:
    """Check that a markdown file contains required section keywords. Returns failure count."""
    if not path.exists():
        print(f"  FAIL  {label}: file not found at {path.relative_to(REPO_ROOT)}")
        return 1

    content = path.read_text(encoding="utf-8", errors="replace")
    failures = 0
    for section in required_sections:
        if section.lower() in content.lower():
            print(f"  PASS  {label}: section '{section}' found")
        else:
            print(f"  FAIL  {label}: section '{section}' not found")
            failures += 1
    return failures


def _check_source_passport() -> int:
    """Check SOURCE_PASSPORT.md exists and has a fields section. Returns failure count."""
    if not SOURCE_PASSPORT_PATH.exists():
        print(
            f"  FAIL  SOURCE_PASSPORT: file not found at "
            f"{SOURCE_PASSPORT_PATH.relative_to(REPO_ROOT)}"
        )
        return 1

    content = SOURCE_PASSPORT_PATH.read_text(encoding="utf-8", errors="replace")
    for marker in SOURCE_PASSPORT_FIELD_MARKERS:
        if marker.lower() in content.lower():
            print(f"  PASS  SOURCE_PASSPORT: '{marker}' section found")
            return 0

    print(
        f"  FAIL  SOURCE_PASSPORT: none of {SOURCE_PASSPORT_FIELD_MARKERS!r} found in file"
    )
    return 1


def run_checks() -> int:
    """Run all schema contract checks. Returns count of failures."""
    print("=" * 60)
    print("CHECK: schema contracts")
    print("=" * 60)

    failures = 0
    failures += _check_file_sections(DATA_OS_PATH, DATA_OS_REQUIRED_SECTIONS, "DATA_OS")
    failures += _check_source_passport()

    total_checks = len(DATA_OS_REQUIRED_SECTIONS) + 1
    passed = total_checks - failures
    print("-" * 60)
    print(f"Summary: {passed}/{total_checks} passed, {failures} failed")
    return failures


def main() -> None:
    failures = run_checks()
    sys.exit(0 if failures == 0 else 1)


if __name__ == "__main__":
    main()
