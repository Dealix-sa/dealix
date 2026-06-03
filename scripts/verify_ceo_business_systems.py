"""Verify the broader CEO business systems are present in the repo.

This is a wider check than `verify_ceo_business_score.py`: it covers
docs, runtime, generator script, score verifier, and workflow file so
that the CI surface always asserts the full system is wired.
"""

from __future__ import annotations

from pathlib import Path


REQUIRED = [
    "docs/founder/CEO_BUSINESS_AUDIT.md",
    "ops_runtime/__init__.py",
    "ops_runtime/business_audit.py",
    "scripts/generate_ceo_business_score.py",
    "scripts/verify_ceo_business_score.py",
    ".github/workflows/dealix-business-systems.yml",
]


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    failures: list[str] = []
    for rel in REQUIRED:
        path = repo_root / rel
        if not path.exists():
            failures.append(f"Missing: {rel}")
        elif path.is_file() and path.stat().st_size == 0 and not rel.endswith("__init__.py"):
            failures.append(f"Empty: {rel}")

    if failures:
        print("CEO business systems verification failed:")
        for failure in failures:
            print("-", failure)
        return 1

    print("PASS: CEO business systems are present.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
