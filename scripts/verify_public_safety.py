"""Verify the public repo is safe to publish.

Scans the public-facing operating tree for content that should never appear in
a public repository: real customer names, private pipeline data, payment IDs,
API tokens, or other operating signals that belong only in the private ops
repo. Pattern-based, conservative, and intentionally noisy.
"""

from __future__ import annotations

import re
from pathlib import Path

FORBIDDEN_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("private API token", re.compile(r"sk-[a-zA-Z0-9]{20,}")),
    ("AWS access key", re.compile(r"AKIA[0-9A-Z]{16}")),
    ("Stripe secret", re.compile(r"sk_live_[0-9a-zA-Z]{16,}")),
    ("Moyasar secret", re.compile(r"sk_(live|test)_[0-9a-zA-Z]{16,}")),
    ("private slack token", re.compile(r"xox[baprs]-[0-9a-zA-Z\-]{10,}")),
    ("private repo path leak", re.compile(r"dealix-ops-private/[a-zA-Z0-9_\-/]+\.csv")),
]

SCAN_FOLDERS = [
    "docs",
    "DEALIX_OPERATING_DOCTRINE.md",
    "DEALIX_COMPANY_OS_SCORECARD.md",
]

SKIP_PARTS = {
    ".git",
    "node_modules",
    "__pycache__",
    "archive",
}


def iter_files() -> list[Path]:
    files: list[Path] = []
    for entry in SCAN_FOLDERS:
        path = Path(entry)
        if not path.exists():
            continue
        if path.is_file():
            files.append(path)
            continue
        for child in path.rglob("*"):
            if not child.is_file():
                continue
            if any(part in SKIP_PARTS for part in child.parts):
                continue
            if child.suffix.lower() in {".md", ".txt", ".yml", ".yaml", ".json", ".csv"}:
                files.append(child)
    return files


def main() -> int:
    failures: list[str] = []

    for path in iter_files():
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for label, pattern in FORBIDDEN_PATTERNS:
            for match in pattern.finditer(text):
                failures.append(f"{path}: forbidden pattern ({label}): {match.group(0)[:24]}...")

    if failures:
        print("Public safety verification failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("PASS: public surface contains no forbidden private patterns.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
