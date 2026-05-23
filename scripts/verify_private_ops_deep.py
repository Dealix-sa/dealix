"""Deep verifier intended to run inside the private ops repo (dealix-ops-private).

It is kept in the public repo as the canonical reference implementation so the
private repo can pull it in or vendor it. Run it from the private repo root.

Checks:
- Required private operating files exist and are non-empty.
- The pipeline tracker CSV has the required headers.
- The approval log CSV has the required headers.
"""

from __future__ import annotations

import csv
from pathlib import Path

REQUIRED_FILES = [
    "founder/daily_brief.md",
    "founder/ceo_dashboard.md",
    "founder/decision_queue.md",
    "founder/decision_log.md",
    "founder/approvals_waiting.md",
    "founder/risk_log.md",
    "pipeline/pipeline_tracker.csv",
    "revenue/mrr_tracker.csv",
    "trust/approval_log.csv",
    "trust/suppression_list.csv",
    "learning/experiment_log.md",
    "learning/weekly_intelligence_review.md",
    "weekly_reviews/template.md",
]

PIPELINE_HEADERS = [
    "company",
    "sector",
    "contact",
    "stage",
    "priority",
    "next_action",
    "last_touch",
    "notes",
]

APPROVAL_HEADERS = [
    "date",
    "item",
    "type",
    "risk_level",
    "decision",
    "approved_by",
    "evidence",
]


def check_csv_headers(path: Path, required: list[str], failures: list[str]) -> None:
    if not path.exists():
        return
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames or []
        for header in required:
            if header not in headers:
                failures.append(f"{path} missing header: {header}")


def main() -> int:
    failures: list[str] = []

    for file in REQUIRED_FILES:
        path = Path(file)
        if not path.exists():
            failures.append(f"Missing: {file}")
        elif path.stat().st_size == 0:
            failures.append(f"Empty: {file}")

    check_csv_headers(Path("pipeline/pipeline_tracker.csv"), PIPELINE_HEADERS, failures)
    check_csv_headers(Path("trust/approval_log.csv"), APPROVAL_HEADERS, failures)

    if failures:
        print("Private ops deep verification failed:")
        for failure in failures:
            print("-", failure)
        return 1

    print("PASS: private ops deep verification passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
