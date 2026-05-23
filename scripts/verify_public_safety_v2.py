#!/usr/bin/env python3
"""Scan the public tree for content that must not be public.

Blocks PR merges when any private-only marker is found in the working tree.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

EXCLUDED_DIRS = {
    ".git",
    "node_modules",
    "__pycache__",
    ".venv",
    "venv",
    "dist",
    "build",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".next",
    ".cache",
}

# Filename patterns that must never appear in the public tree.
FORBIDDEN_FILENAMES = (
    "client_real_secrets.json",
    "real_dashboard.json",
    "live_customers.csv",
    "live_pipeline_real.csv",
    "founder_personal_kpi_export.csv",
)

# Substrings that indicate live data made it into a committed file.
FORBIDDEN_CONTENT_MARKERS = (
    "BEGIN PRIVATE KEY",
    "BEGIN RSA PRIVATE KEY",
    "BEGIN OPENSSH PRIVATE KEY",
    "BEGIN CERTIFICATE",
    "Bearer eyJ",  # JWTs leaking into docs
)

# Files allowed to mention secret-like markers (examples, policy docs, test fixtures).
ALLOWLIST = {
    ".gitleaks.toml",
    ".secrets.baseline",
    ".env.example",
    ".env.staging.example",
    "scripts/verify_public_safety_v2.py",
    "scripts/verify_data_boundary.py",
    "tests/test_agent_observability_integration.py",
    "evals/personal_operator_cases.jsonl",
    "docs/security/SECURITY_BASELINE.md",
    "docs/security/SECURITY_RELIABILITY_SUPPLY_CHAIN_OS.md",
    "docs/security/DEPENDENCY_POLICY.md",
    "docs/security/INCIDENT_RESPONSE_SYSTEM.md",
    "docs/security/INCIDENT_RESPONSE_QUICKCARD.md",
    "docs/data/REDACTION_SYSTEM.md",
}

# Personal data heuristics — high-confidence patterns only.
PERSONAL_DATA_PATTERNS = [
    re.compile(r"\b\d{10}\b"),  # Saudi 10-digit ID candidates
]


def iter_files() -> list[Path]:
    files: list[Path] = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if any(part in EXCLUDED_DIRS for part in path.parts):
            continue
        files.append(path)
    return files


def main() -> int:
    failures: list[str] = []
    for path in iter_files():
        rel = path.relative_to(ROOT).as_posix()
        if path.name in FORBIDDEN_FILENAMES:
            failures.append(f"Forbidden filename: {rel}")
            continue
        if rel in ALLOWLIST:
            continue
        if path.suffix in {".png", ".jpg", ".jpeg", ".pdf", ".ico", ".gif", ".webp", ".woff", ".woff2", ".ttf"}:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        for marker in FORBIDDEN_CONTENT_MARKERS:
            if marker in text:
                failures.append(f"Forbidden marker '{marker}' found in {rel}")

    if failures:
        print("Public safety scan FAILED:")
        for f in failures:
            print(" -", f)
        return 1
    print("PASS: Public safety scan v2 found no forbidden content.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
