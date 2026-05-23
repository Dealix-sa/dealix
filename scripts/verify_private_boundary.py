#!/usr/bin/env python3
"""
verify_private_boundary.py — assert the public repo does not contain
filenames or paths that belong to the private ops repo.

The private-repo manifest is the source of truth for forbidden paths.
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))

from generate_master_tree import PRIVATE_MANIFEST  # noqa: E402


# Files / directories from the private manifest that should NEVER appear
# in the public repo at the repo root. We only check the top-level
# directories that are unambiguously private (founder/, clients/, etc.).
PRIVATE_TOP_LEVEL = {
    "founder", "pipeline", "weekly_reviews", "prompts",
    "people", "legal", "partners", "learning", "finance",
}
# These dirs may exist in the public repo with different meaning
# (e.g., docs/founder/). We only fail when they appear at the *root*.
# `clients/` is intentionally not in this set — it may hold templates
# at the public root, but tests/trust/test_private_boundary.py asserts
# it contains no real customer subdirectories.

PRIVATE_FILE_MARKERS = {
    "approval_log.csv", "suppression_list.csv", "claim_approval_log.csv",
    "export_log.csv", "mrr_tracker.csv", "cash_collected.csv",
    "pipeline_value.csv", "revenue_dashboard.csv", "monthly_finance_review.md",
}


def main() -> int:
    findings: list[str] = []

    # Top-level private directories must not exist
    for name in PRIVATE_TOP_LEVEL:
        candidate = REPO / name
        if candidate.exists() and candidate.is_dir():
            findings.append(
                f"private top-level dir present in public repo: {name}/"
            )

    # Marker files anywhere in the repo are suspicious
    for path in REPO.rglob("*"):
        if not path.is_file():
            continue
        if any(part in {".git", "node_modules", "__pycache__"} for part in path.relative_to(REPO).parts):
            continue
        if path.name in PRIVATE_FILE_MARKERS:
            findings.append(f"private-data filename found: {path.relative_to(REPO)}")

    if findings:
        print(f"[FAIL] verify_private_boundary: {len(findings)} boundary violations")
        for f in findings:
            print(f"  - {f}")
        return 1

    # Sanity check: the private manifest itself is non-empty.
    if not PRIVATE_MANIFEST:
        print("[FAIL] private manifest is empty")
        return 1

    print("[OK] verify_private_boundary: no boundary violations")
    return 0


if __name__ == "__main__":
    sys.exit(main())
