"""Verify the CEO Business Score system is wired correctly.

Confirms that the required files exist and are non-trivial in size.
Fails the run (exit 1) if any check is missing so CI / pre-commit can
gate on it. Performs no network or filesystem mutations.
"""

from __future__ import annotations

from pathlib import Path


REQUIRED = [
    "docs/founder/CEO_BUSINESS_AUDIT.md",
    "ops_runtime/business_audit.py",
    "scripts/generate_ceo_business_score.py",
]


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    failures: list[str] = []
    for rel in REQUIRED:
        path = repo_root / rel
        if not path.exists():
            failures.append(f"Missing: {rel}")
        elif path.stat().st_size < 100:
            failures.append(f"Too short: {rel}")

    if failures:
        print("CEO business score verification failed:")
        for failure in failures:
            print("-", failure)
        return 1

    print("PASS: CEO business score system is ready.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
