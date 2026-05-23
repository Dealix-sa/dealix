"""Dealix private boundary verifier.

Ensures the public repo does not embed paths or filenames that belong in
the private `dealix-ops-private` repo. The public repo may *reference*
private paths in documentation, but must not contain the actual files.

Run:
    python scripts/verify_private_boundary.py
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Real private folders that must not exist as committed top-level dirs in the
# public repo. Documentation may name them; they must not be present.
FORBIDDEN_TOP_LEVEL_DIRS = [
    "dealix-ops-private",
    "private",
    "_private",
]

# Files that, if present, indicate accidental import from the private repo.
FORBIDDEN_FILES = [
    "founder/daily_brief.md",
    "founder/decision_log.md",
    "founder/approvals_waiting.md",
    "pipeline/pipeline_tracker.csv",
    "revenue/mrr_tracker.csv",
    "revenue/cash_collected.csv",
    "trust/approval_log.csv",
    "trust/suppression_list.csv",
    "weekly_reviews/template.md",
]


def main() -> int:
    failures: list[str] = []

    for name in FORBIDDEN_TOP_LEVEL_DIRS:
        if (ROOT / name).is_dir():
            failures.append(f"Forbidden private directory present in public repo: {name}")

    for relpath in FORBIDDEN_FILES:
        if (ROOT / relpath).is_file():
            failures.append(f"Forbidden private file present in public repo: {relpath}")

    if failures:
        print("Private boundary verification failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("PASS: Dealix private boundary verified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
