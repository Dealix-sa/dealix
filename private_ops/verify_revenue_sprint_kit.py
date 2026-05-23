"""Verify that the private Revenue Sprint Kit templates are present and non-trivial."""

from __future__ import annotations

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
    base = Path(__file__).resolve().parent
    failures: list[str] = []

    for relative in REQUIRED:
        path = base / relative
        if not path.exists():
            failures.append(f"Missing: {relative}")
            continue
        if path.stat().st_size < MIN_BYTES:
            failures.append(f"Too short: {relative}")

    if failures:
        print("Revenue Sprint Kit verification failed:")
        for failure in failures:
            print("-", failure)
        return 1

    print("PASS: private Revenue Sprint Kit is ready.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
