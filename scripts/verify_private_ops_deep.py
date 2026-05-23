"""Dealix private ops deep verifier.

This script is intended to run inside the *private* `dealix-ops-private`
repo. It is kept here in the public repo as a canonical reference so the
public verifier chain knows what the private side must contain. Drop a
copy of this file into the private repo to enforce the same checks there.

When invoked from the public repo, the script will exit 0 if no private
ops folder is found (it is not the public repo's job to host that data).

Run inside the private repo:
    python verify_private_ops_deep.py
"""
from pathlib import Path
import csv

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


def main() -> int:
    # If we are accidentally running this from the public repo, exit cleanly.
    private_marker = Path("PRIVATE_OPS.md")
    if not private_marker.exists() and not Path("founder").exists():
        print("verify_private_ops_deep.py: no private ops detected in CWD, skipping.")
        return 0

    failures: list[str] = []

    for file in REQUIRED_FILES:
        path = Path(file)
        if not path.exists():
            failures.append(f"Missing: {file}")
        elif path.stat().st_size == 0:
            failures.append(f"Empty: {file}")

    pipeline = Path("pipeline/pipeline_tracker.csv")
    if pipeline.exists():
        with pipeline.open(newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            headers = reader.fieldnames or []
            required_headers = [
                "company",
                "sector",
                "contact",
                "stage",
                "priority",
                "next_action",
                "last_touch",
                "notes",
            ]
            for header in required_headers:
                if header not in headers:
                    failures.append(f"pipeline missing header: {header}")

    approval = Path("trust/approval_log.csv")
    if approval.exists():
        with approval.open(newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            headers = reader.fieldnames or []
            required_headers = [
                "date",
                "item",
                "type",
                "risk_level",
                "decision",
                "approved_by",
                "evidence",
            ]
            for header in required_headers:
                if header not in headers:
                    failures.append(f"approval_log missing header: {header}")

    if failures:
        print("Private ops deep verification failed:")
        for failure in failures:
            print("-", failure)
        return 1

    print("PASS: private ops deep verification passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
