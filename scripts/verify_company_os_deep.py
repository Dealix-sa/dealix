"""Deep verification of Dealix Company OS.

For each of the 9 heart-of-system files, check that the required operating
terms are present in the document. This is the next level beyond
verify_document_quality.py: it does not just check structure, it checks that
the right things are written about.
"""

from pathlib import Path

CHECKS: dict[str, list[str]] = {
    "DEALIX_OPERATING_DOCTRINE.md": [
        "Revenue Loop",
        "Delivery Loop",
        "Trust Loop",
        "Learning Loop",
        "CEO Loop",
        "AI prepares",
        "Founder approves",
    ],
    "DEALIX_COMPANY_OS_SCORECARD.md": [
        "Founder OS",
        "Strategy OS",
        "Revenue OS",
        "Delivery OS",
        "Trust OS",
        "Learning OS",
    ],
    "docs/founder/DAILY_COMMAND_BRIEF.md": [
        "Money",
        "Sales",
        "Delivery",
        "Trust",
        "Decisions Required",
    ],
    "docs/revenue/OFFER_LADDER.md": [
        "Signal Sample",
        "Revenue Sprint",
        "Managed",
        "Dealix OS",
    ],
    "docs/revenue/PIPELINE_STAGES.md": [
        "New",
        "Contacted",
        "Replied",
        "Proposal Sent",
        "Paid",
        "Delivered",
        "Retainer",
    ],
    "docs/trust/AUTONOMY_POLICY.md": [
        "L0 Manual",
        "L1 Assisted",
        "L2 Semi-Auto",
        "L3 Auto",
        "L4 Prohibited",
    ],
    "docs/trust/APPROVAL_MATRIX.md": [
        "A0",
        "A1",
        "A2",
        "A3",
        "Never",
    ],
    "docs/ops/OPERATING_LOOPS.md": [
        "Revenue Loop",
        "Delivery Loop",
        "Trust Loop",
        "Learning Loop",
        "CEO Loop",
    ],
    "docs/learning/WEEKLY_INTELLIGENCE_REVIEW.md": [
        "What happened",
        "What worked",
        "What failed",
        "What bottleneck",
        "What will change",
    ],
}


def main() -> int:
    failures: list[str] = []

    for file, required_terms in CHECKS.items():
        path = Path(file)
        if not path.exists():
            failures.append(f"Missing file: {file}")
            continue

        text = path.read_text(encoding="utf-8", errors="ignore")

        for term in required_terms:
            if term not in text:
                failures.append(f"{file} missing required term: {term}")

    if failures:
        print("Company OS deep verification failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("PASS: Dealix Company OS deep verification passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
