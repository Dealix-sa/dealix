"""Verify the public/private boundary in this repo.

This repo is the *public* Dealix repo. It must not contain the private ops
tree, customer files, or anything that belongs in `dealix-ops-private`.
"""

from __future__ import annotations

from pathlib import Path

FORBIDDEN_TOP_LEVEL = {
    "dealix-ops-private",
    "ops-private",
    "private",
}

FORBIDDEN_PATTERNS = [
    "pipeline_tracker_live.csv",
    "approval_log_live.csv",
    "cash_collected_live.csv",
    "client_real_data.csv",
]


def main() -> int:
    failures: list[str] = []

    root = Path(".")
    for child in root.iterdir():
        if child.name in FORBIDDEN_TOP_LEVEL:
            failures.append(f"Forbidden top-level entry present: {child}")

    for pattern in FORBIDDEN_PATTERNS:
        for match in root.rglob(pattern):
            if ".git" in match.parts:
                continue
            failures.append(f"Forbidden file present: {match}")

    if failures:
        print("Private boundary verification failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("PASS: public/private boundary intact.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
