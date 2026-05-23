"""Private Revenue Sprint Kit verifier.

This script is meant to run from the root of the **private** operations
repository (`dealix-ops-private`). It checks that every operational
template the Revenue Sprint Kit needs is present and non-trivial.

Copy this file to `dealix-ops-private/verify_revenue_sprint_kit.py`
and run:

    python verify_revenue_sprint_kit.py

It is kept in the public repo only as a reference copy so the kit
structure can be reviewed in one place.
"""

from pathlib import Path


REQUIRED = [
    "offers/revenue_sprint/founder_dm_pack.md",
    "offers/revenue_sprint/sample_pack_template.md",
    "offers/revenue_sprint/proposal_fast_template.md",
    "offers/revenue_sprint/payment_followup_templates.md",
    "offers/revenue_sprint/client_intake.md",
    "offers/revenue_sprint/delivery_report_template.md",
    "offers/revenue_sprint/qa_checklist.md",
    "offers/revenue_sprint/handoff_template.md",
    "offers/revenue_sprint/feedback_request.md",
    "offers/revenue_sprint/retainer_ask.md",
]

MIN_BYTES = 120


def main() -> int:
    failures: list[str] = []

    for file in REQUIRED:
        path = Path(file)
        if not path.exists():
            failures.append(f"Missing: {file}")
        elif path.stat().st_size < MIN_BYTES:
            failures.append(f"Too short: {file}")

    if failures:
        print("Revenue Sprint Kit verification failed:")
        for failure in failures:
            print("-", failure)
        return 1

    print("PASS: private Revenue Sprint Kit is ready.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
