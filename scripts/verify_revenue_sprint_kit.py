"""Verify that the public Revenue Sprint Kit is present and complete.

Runs in CI and locally via `make kit`. Fails (exit 1) when a required
file is missing, too short to be meaningful, or when the main kit doc
is missing one of its required sections.
"""

from pathlib import Path


REQUIRED_FILES = [
    "docs/offers/revenue_sprint/REVENUE_SPRINT_KIT.md",
    "docs/offers/revenue_sprint/OFFER.md",
    "docs/offers/revenue_sprint/PRICING.md",
    "docs/offers/revenue_sprint/SCOPE.md",
    "docs/delivery/revenue_sprint/QA_CHECKLIST.md",
    "docs/trust/NO_OVERCLAIM_POLICY.md",
]

REQUIRED_KIT_SECTIONS = [
    "Founder DM Pack",
    "Sample Pack",
    "Proposal",
    "QA",
    "Feedback",
    "Retainer",
]

MIN_BYTES = 120


def main() -> int:
    failures: list[str] = []

    for file in REQUIRED_FILES:
        path = Path(file)
        if not path.exists():
            failures.append(f"Missing: {file}")
        elif path.stat().st_size < MIN_BYTES:
            failures.append(f"Too short: {file}")

    kit = Path("docs/offers/revenue_sprint/REVENUE_SPRINT_KIT.md")
    if kit.exists():
        text = kit.read_text(encoding="utf-8", errors="ignore")
        for term in REQUIRED_KIT_SECTIONS:
            if term not in text:
                failures.append(f"Revenue Sprint Kit missing: {term}")

    if failures:
        print("Public Revenue Sprint Kit verification failed:")
        for failure in failures:
            print("-", failure)
        return 1

    print("PASS: public Revenue Sprint Kit is ready.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
