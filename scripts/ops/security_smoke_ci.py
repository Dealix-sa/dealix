#!/usr/bin/env python3
"""CI-safe security smoke gate for Dealix.

This check keeps hard failures for risky committed runtime files while avoiding
false positives from documented/test-only synthetic credentials.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

SKIP_DIRS = {
    ".git",
    ".github",
    ".mypy_cache",
    ".next",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    "build",
    "dist",
    "htmlcov",
    "node_modules",
    "reports/runtime",
    "venv",
}

TEXT_SUFFIXES = {
    ".env",
    ".example",
    ".ini",
    ".json",
    ".md",
    ".py",
    ".sh",
    ".toml",
    ".ts",
    ".tsx",
    ".txt",
    ".yaml",
    ".yml",
}

SECRET_PATTERNS = [
    re.compile(r"sk_live_[A-Za-z0-9_\-]{12,}"),
    re.compile(r"github_pat_[A-Za-z0-9_]{20,}"),
    re.compile(r"ghp_[A-Za-z0-9]{20,}"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
]

SAFE_CONTEXT_PATHS = (
    "docs/",
    "tests/",
)

SAFE_PLACEHOLDER_WORDS = (
    "example",
    "fixture",
    "fake",
    "dummy",
    "placeholder",
    "redacted",
    "test",
    "synthetic",
    "sample",
)


def is_skipped(path: Path) -> bool:
    rel = path.relative_to(ROOT).as_posix()
    parts = set(rel.split("/"))
    if parts & SKIP_DIRS:
        return True
    return any(rel.startswith(prefix) for prefix in SKIP_DIRS if prefix.endswith("/"))


def is_text_candidate(path: Path) -> bool:
    name = path.name
    if name.startswith(".env"):
        return True
    return path.suffix.lower() in TEXT_SUFFIXES


def is_allowed_env_example(path: Path) -> bool:
    name = path.name
    return name.startswith(".env") and name.endswith((".example", ".template", ".sample"))


def line_is_placeholder(line: str) -> bool:
    lowered = line.lower()
    return any(word in lowered for word in SAFE_PLACEHOLDER_WORDS)


def path_is_safe_context(path: Path) -> bool:
    rel = path.relative_to(ROOT).as_posix()
    return rel.startswith(SAFE_CONTEXT_PATHS)


def main() -> int:
    failures: list[str] = []
    warnings: list[str] = []

    for path in ROOT.rglob("*"):
        if not path.is_file() or is_skipped(path):
            continue

        rel = path.relative_to(ROOT).as_posix()

        if path.name.startswith(".env") and not is_allowed_env_example(path):
            failures.append(f"Do not commit local env file: {rel}")
            continue

        if not is_text_candidate(path):
            continue

        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue

        for idx, line in enumerate(text.splitlines(), start=1):
            for pattern in SECRET_PATTERNS:
                if not pattern.search(line):
                    continue
                if path_is_safe_context(path) or line_is_placeholder(line):
                    warnings.append(f"Synthetic credential example ignored: {rel}:{idx}")
                    continue
                failures.append(f"Potential live secret in {rel}:{idx}: matches {pattern.pattern}")

    if failures:
        print("CI_SECURITY_SMOKE=FAIL")
        for item in failures:
            print(f"FAIL: {item}")
        for item in warnings:
            print(f"WARN: {item}")
        return 1

    print("CI_SECURITY_SMOKE=PASS")
    if warnings:
        print(f"Ignored synthetic/test examples: {len(warnings)}")
        for item in warnings[:20]:
            print(f"WARN: {item}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
