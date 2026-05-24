#!/usr/bin/env python3
"""verify_repo_completeness.py — top-level repo skeleton check.

Confirms the directories and root files that every Dealix layer expects.
Fast (< 1s) so it can run in pre-commit and CI.
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

REQUIRED_DIRS = (
    "api",
    "apps/web",
    "dealix",
    "docs",
    "docs/ops",
    "docs/governance",
    "docs/founder",
    "docs/ai_governance",
    "docs/trust",
    "evals",
    "policies",
    "registries",
    "scripts",
    "tests",
    ".github/workflows",
)

REQUIRED_FILES = (
    "dealix_manifest.yaml",
    "Makefile",
    "Dockerfile",
    "railway.toml",
    "railway.json",
    "README.md",
    "scripts/verify_everything.py",
    "scripts/railway_predeploy.sh",
)


def main() -> int:
    missing_dirs = [d for d in REQUIRED_DIRS if not (REPO / d).is_dir()]
    missing_files = [f for f in REQUIRED_FILES if not (REPO / f).is_file()]

    for d in missing_dirs:
        print(f"missing_dir:{d}", file=sys.stderr)
    for f in missing_files:
        print(f"missing_file:{f}", file=sys.stderr)

    ok = not missing_dirs and not missing_files
    print(f"REPO_COMPLETENESS_PASS={'true' if ok else 'false'}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
