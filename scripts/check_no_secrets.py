#!/usr/bin/env python3
"""Fail if exposed secrets (API keys, tokens, private keys) are committed.

This is the scanner referenced by CI ("V3 — No secrets check"), the security
docs (docs/security/*), and the NO_SPAM_POLICY. It scans git-tracked files for
high-confidence secret patterns and exits non-zero if any real secret is found.

Scope and false-positive control:
  * Only git-tracked files are scanned (gitignored .env / credentials never get
    here in the first place).
  * Test fixtures, example templates, docs, and generated reports are skipped —
    they legitimately contain *fake* secrets to exercise detection logic.
  * Obvious placeholders (``xxxx``, ``change-me``, ``your-...``, ``example``,
    sequential ``abcdef…`` / ``123456…``) are treated as safe.

Exit codes: 0 = clean, 1 = secrets found.
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Paths that legitimately carry fake/sample secrets — never flagged.
SKIP_DIR_PARTS = {
    "tests", "test", "docs", "reports", "examples", "fixtures",
    "node_modules", ".git", "__pycache__",
}
SKIP_NAME_RE = re.compile(
    r"(^|/)(test_[^/]*\.py|[^/]*_verify\.py|conftest\.py)$"
    r"|\.example($|\.)|\.md$|\.lock$",
)
SKIP_EXT = {
    ".png", ".jpg", ".jpeg", ".gif", ".ico", ".svg", ".woff", ".woff2",
    ".ttf", ".eot", ".pdf", ".zip", ".gz", ".map",
}

# High-confidence secret signatures.
PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("AWS access key id", re.compile(r"AKIA[0-9A-Z]{16}")),
    ("Private key block", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA |PGP )?PRIVATE KEY-----")),
    ("GitHub token", re.compile(r"gh[pousr]_[A-Za-z0-9]{36,}")),
    ("Slack token", re.compile(r"xox[baprs]-[A-Za-z0-9-]{10,}")),
    ("Google API key", re.compile(r"AIza[0-9A-Za-z_\-]{35}")),
    ("Generic sk/pk key", re.compile(r"\b(?:sk|pk)-[A-Za-z0-9]{20,}\b")),
]

# Placeholder / obviously-fake markers — if a matched line contains any of
# these, it is not a real secret.
PLACEHOLDER_RE = re.compile(
    r"xxxx|XXXX|example|placeholder|your[-_]|change[-_]?me|dummy|sample|"
    r"redacted|<[^>]+>|abcdefghijklmnopqrstuvwxyz|0123456789|123456789012",
    re.IGNORECASE,
)


def _tracked_files() -> list[str]:
    out = subprocess.run(
        ["git", "ls-files"], cwd=str(ROOT), capture_output=True, text=True, check=True
    ).stdout
    return [line for line in out.splitlines() if line.strip()]


def _skip(rel: str) -> bool:
    p = Path(rel)
    if p.suffix.lower() in SKIP_EXT:
        return True
    if SKIP_NAME_RE.search(rel):
        return True
    return any(part in SKIP_DIR_PARTS for part in p.parts)


def scan() -> list[str]:
    findings: list[str] = []
    for rel in _tracked_files():
        if _skip(rel):
            continue
        fpath = ROOT / rel
        try:
            text = fpath.read_text(encoding="utf-8", errors="ignore")
        except (OSError, UnicodeError):
            continue
        for lineno, line in enumerate(text.splitlines(), start=1):
            if PLACEHOLDER_RE.search(line):
                continue
            for label, pat in PATTERNS:
                if pat.search(line):
                    findings.append(f"{rel}:{lineno}: possible {label}")
                    break
    return findings


def main() -> int:
    findings = scan()
    if findings:
        print("Exposed secrets detected — do NOT commit these:")
        for f in findings:
            print(f"  - {f}")
        print(
            "\nIf a match is a placeholder or test fixture, move it under a "
            "tests/ or *.example path, or replace with an obvious placeholder."
        )
        return 1
    print("No exposed secrets found in tracked files.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
