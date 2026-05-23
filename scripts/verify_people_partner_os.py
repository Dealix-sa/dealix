"""Verify the People, Delegation & Partner Operating System artifacts.

Checks every required doc exists and is non-trivial. Run via:

    python scripts/verify_people_partner_os.py

Exit code 0 = PASS; exit code 1 = FAIL with itemized list of failures.
"""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

REQUIRED_FILES = [
    "docs/people/PEOPLE_DELEGATION_PARTNER_OS.md",
    "docs/people/FOUNDER_BOTTLENECK_SYSTEM.md",
    "docs/people/DELEGATION_LADDER.md",
    "docs/people/ROLE_ARCHITECTURE.md",
    "docs/people/HIRING_TRIGGER_SYSTEM.md",
    "docs/people/SDR_SCORECARD.md",
    "docs/people/DELIVERY_ANALYST_SCORECARD.md",
    "docs/people/OPS_MANAGER_SCORECARD.md",
    "docs/people/CONTRACTOR_ONBOARDING_SYSTEM.md",
    "docs/people/ACCESS_CONTROL_SYSTEM.md",
    "docs/people/PEOPLE_OPERATING_ROUTINE.md",
    "docs/partners/PARTNER_OPERATING_SYSTEM.md",
    "docs/partners/REFERRAL_TERMS_SYSTEM.md",
    "docs/partners/WHITE_LABEL_GUARDRAILS.md",
    "docs/partners/PARTNER_OPERATING_ROUTINE.md",
]

MIN_BYTES = 120


def main() -> int:
    failures: list[str] = []
    for rel in REQUIRED_FILES:
        path = REPO_ROOT / rel
        if not path.exists():
            failures.append(f"Missing: {rel}")
            continue
        if path.stat().st_size < MIN_BYTES:
            failures.append(f"Too short (<{MIN_BYTES} bytes): {rel}")

    if failures:
        print("People & Partner OS verification failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print(f"PASS: People & Partner OS is ready ({len(REQUIRED_FILES)} docs).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
