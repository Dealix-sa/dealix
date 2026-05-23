"""Verify the public Revenue Sprint Kit documents are present and well-formed."""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

REQUIRED = [
    "docs/offers/revenue_sprint/REVENUE_SPRINT_KIT.md",
    "docs/offers/revenue_sprint/OFFER.md",
    "docs/offers/revenue_sprint/PRICING.md",
    "docs/offers/revenue_sprint/SCOPE.md",
    "docs/delivery/revenue_sprint/QA_CHECKLIST.md",
    "docs/trust/NO_OVERCLAIM_POLICY.md",
]

KIT_TERMS = [
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

    for relative in REQUIRED:
        path = REPO_ROOT / relative
        if not path.exists():
            failures.append(f"Missing: {relative}")
            continue
        if path.stat().st_size < MIN_BYTES:
            failures.append(f"Too short: {relative}")

    kit_path = REPO_ROOT / "docs/offers/revenue_sprint/REVENUE_SPRINT_KIT.md"
    if kit_path.exists():
        text = kit_path.read_text(encoding="utf-8", errors="ignore")
        for term in KIT_TERMS:
            if term not in text:
                failures.append(f"Revenue Sprint Kit missing term: {term}")

    if failures:
        print("Public Revenue Sprint Kit verification failed:")
        for failure in failures:
            print("-", failure)
        return 1

    print("PASS: public Revenue Sprint Kit is ready.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
