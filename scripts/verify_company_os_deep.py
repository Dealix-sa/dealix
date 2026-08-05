"""Deep verifier for the Dealix Company OS.

Goes beyond ``verify_document_quality.py`` (which only checks for
section headings). This script asserts that the 12 core operating
documents contain the specific operating terms that make them useful:
the five loops in the doctrine, the rungs in the offer ladder, the
seven pipeline stages, the autonomy levels, the approval levels, and
the five questions of the weekly intelligence review.
"""

from __future__ import annotations

from pathlib import Path
import sys

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
    "docs/founder/WEEKLY_CEO_REVIEW.md": [
        "What happened",
        "What worked",
        "What failed",
        "What bottleneck",
        "What will change",
    ],
    "docs/revenue/OFFER_LADDER.md": [
        "Signal Sample",
        "Revenue Sprint",
        "Managed Pilot",
        "Revenue Desk",
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
    "docs/delivery/revenue_sprint/DELIVERY_PLAYBOOK.md": [
        "Day 0",
        "Day 1",
        "Day 7",
        "QA",
        "founder approval",
    ],
    "docs/delivery/revenue_sprint/QA_CHECKLIST.md": [
        "Scope",
        "Evidence",
        "Clarity",
        "Trust",
        "Customer Voice",
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
    "docs/learning/WEEKLY_INTELLIGENCE_REVIEW.md": [
        "What happened",
        "What worked",
        "What failed",
        "What bottleneck",
        "What will change",
    ],
    "docs/ops/OPERATING_LOOPS.md": [
        "Revenue Loop",
        "Delivery Loop",
        "Trust Loop",
        "Learning Loop",
        "CEO Loop",
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
            if term.lower() not in text.lower():
                failures.append(f"{file} missing required term: {term}")

    if failures:
        print("Company OS deep verification failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("PASS: Dealix Company OS deep verification passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
