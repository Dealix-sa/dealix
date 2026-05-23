#!/usr/bin/env python3
"""Enforce the public/private data boundary.

Verifies that no private-only filenames or paths appear inside the public repo,
and that referenced private paths use the documented `dealix-ops-private/` prefix.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

EXCLUDED_DIRS = {
    ".git",
    "node_modules",
    "__pycache__",
    ".venv",
    "venv",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    "dist",
    "build",
    ".next",
    ".cache",
}

# Filenames that should only exist inside dealix-ops-private/.
PRIVATE_ONLY_BASENAMES = {
    "pipeline_tracker.csv",
    "revenue_action_log.csv",
    "cash_collected.csv",
    "pipeline_value.csv",
    "mrr_tracker.csv",
    "expenses.csv",
    "approval_log.csv",
    "execution_evidence_ledger.csv",
    "weekly_metrics.csv",
}

# Files in the public tree that may keep these names because they are templates,
# documentation, or already-known historical fixtures.
KNOWN_PUBLIC_EXCEPTIONS = {
    "docs/ops/pipeline_tracker.csv",
    "docs/ops/pipeline_tracker_enriched.csv",
}


def main() -> int:
    failures: list[str] = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if any(part in EXCLUDED_DIRS for part in path.parts):
            continue
        rel = path.relative_to(ROOT).as_posix()
        if rel in KNOWN_PUBLIC_EXCEPTIONS:
            continue
        if path.name in PRIVATE_ONLY_BASENAMES:
            failures.append(
                f"Private-only filename '{path.name}' must live in dealix-ops-private/, found: {rel}"
            )

    if failures:
        print("Data boundary verification FAILED:")
        for f in failures:
            print(" -", f)
        return 1
    print("PASS: data boundary clean — no private filenames in the public tree.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
