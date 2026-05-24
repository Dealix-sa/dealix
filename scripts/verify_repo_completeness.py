#!/usr/bin/env python3
"""
verify_repo_completeness.py — top-level skeleton check.

Verifies the repo still has the canonical directories and entry files the
rest of the audit assumes exist. Independent of the manifest so it can run
even if the manifest is broken.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

REQUIRED_DIRS = [
    "api",
    "api/routers",
    "core",
    "dealix",
    "dealix/config",
    "dealix/governance",
    "docs",
    "docs/ops",
    "docs/company",
    "docs/governance",
    "evals",
    "scripts",
    ".github/workflows",
    "frontend",
]

REQUIRED_FILES = [
    "Dockerfile",
    "Makefile",
    "Procfile",
    "railway.toml",
    "railway.json",
    "pyproject.toml",
    "requirements.txt",
    "api/main.py",
    "api/routers/health.py",
    "scripts/railway_predeploy.sh",
    "dealix_manifest.yaml",
]


def main() -> int:
    failures: list[str] = []

    for d in REQUIRED_DIRS:
        p = ROOT / d
        if not p.exists():
            failures.append(f"missing directory: {d}")
        elif not p.is_dir():
            failures.append(f"path is not a directory: {d}")

    for f in REQUIRED_FILES:
        p = ROOT / f
        if not p.exists():
            failures.append(f"missing file: {f}")
        elif not p.is_file():
            failures.append(f"path is not a file: {f}")
        elif p.stat().st_size == 0:
            failures.append(f"file is empty: {f}")

    if failures:
        print("REPO COMPLETENESS: FAIL")
        for f in failures:
            print(f"  - {f}")
        return 1
    print(f"REPO COMPLETENESS: PASS ({len(REQUIRED_DIRS)} dirs + {len(REQUIRED_FILES)} files)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
