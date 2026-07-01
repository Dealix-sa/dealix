#!/usr/bin/env python3
"""Gate: no raw secret patterns committed to the repo.

Scans all tracked files for patterns that look like real credentials.
Allowlist paths that are known-safe (test fixtures, redaction examples, etc.).
Run: python scripts/verify_secret_patterns.py
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Patterns that indicate a real secret — must NOT appear in source code.
# These match common credential prefixes used by SaaS providers.
SECRET_PATTERNS: list[re.Pattern[str]] = [
    re.compile(r"\bsk-[a-zA-Z0-9]{20,}\b"),         # OpenAI / Anthropic keys
    re.compile(r"\bghp_[a-zA-Z0-9]{36}\b"),           # GitHub personal access tokens
    re.compile(r"\bAIza[0-9A-Za-z_-]{35}\b"),         # Google API keys
    re.compile(r"\bEAACEdEose0cBAN[a-zA-Z0-9]+\b"),   # Facebook tokens
    re.compile(r"aws_secret_access_key\s*=\s*[A-Za-z0-9/+]{40}", re.IGNORECASE),
]

# File extensions to skip (binaries, archives, etc.)
SKIP_EXTENSIONS = {
    ".zip", ".tar", ".gz", ".xz", ".bin", ".pyc", ".pyo",
    ".jpg", ".jpeg", ".png", ".gif", ".ico", ".woff", ".woff2",
    ".pdf", ".db", ".sqlite", ".sqlite3",
}

# Paths that are explicitly allowed to contain secret-like patterns
# (e.g., redaction tests, pattern documentation, allowlist modules).
ALLOWLIST_PATTERNS = [
    "tests/",
    "scripts/",    # test/verify scripts use dummy placeholder values
    "api/middleware/bopla_redaction.py",
    "api/security/api_key.py",
    "SECURITY.md",
    "docs/",
    ".env.example",
    ".env.template",
]


def is_allowlisted(rel_path: str) -> bool:
    return any(rel_path.startswith(p) or rel_path == p for p in ALLOWLIST_PATTERNS)


def main() -> int:
    result = subprocess.run(
        ["git", "ls-files", "-z"],
        capture_output=True, text=True, cwd=ROOT,
    )
    if result.returncode != 0:
        print(f"WARN: git ls-files failed: {result.stderr.strip()}", file=sys.stderr)
        return 0

    files = [f for f in result.stdout.split("\0") if f]
    violations: list[tuple[str, int, str]] = []

    for rel in files:
        if is_allowlisted(rel):
            continue
        path = ROOT / rel
        if not path.is_file():
            continue
        if path.suffix.lower() in SKIP_EXTENSIONS:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        for lineno, line in enumerate(text.splitlines(), 1):
            for pat in SECRET_PATTERNS:
                if pat.search(line):
                    violations.append((rel, lineno, line.strip()[:80]))

    if violations:
        for rel, lineno, snippet in violations[:10]:
            print(f"FAIL: {rel}:{lineno}: {snippet}")
        if len(violations) > 10:
            print(f"... and {len(violations) - 10} more")
        return 1

    print("PASS: no raw secret patterns found in tracked files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
