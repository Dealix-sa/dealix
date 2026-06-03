#!/usr/bin/env python3
"""Scan content draft files for high-risk claim patterns.

Run with a target directory (default: `dealix-ops-private/content`).
Flags lines that look like quantified claims without an obvious source.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


HIGH_RISK_PATTERNS = [
    re.compile(r"\b\d{1,3}\s*%\b"),
    re.compile(r"\b\d+\s*x\b", re.IGNORECASE),
    re.compile(r"\b(best|world-class|leading|revolutionary)\b", re.IGNORECASE),
    re.compile(r"\btrusted by\b", re.IGNORECASE),
]

SOURCE_HINTS = [
    "source:",
    "ref:",
    "from:",
    "based on",
    "according to",
]


def line_has_source(line: str) -> bool:
    lower = line.lower()
    return any(h in lower for h in SOURCE_HINTS)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default="../dealix-ops-private/content")
    parser.add_argument("--strict", action="store_true", help="Exit non-zero on findings")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    if not root.exists():
        print(f"WARN: content root missing: {root}")
        return 0

    findings: list[str] = []
    for path in root.rglob("*.md"):
        try:
            for i, line in enumerate(path.read_text(encoding="utf-8", errors="ignore").splitlines(), start=1):
                if line_has_source(line):
                    continue
                for pattern in HIGH_RISK_PATTERNS:
                    if pattern.search(line):
                        findings.append(f"{path}:{i}: {line.strip()}")
                        break
        except OSError:
            continue

    if findings:
        print("Content claim review found high-risk lines (verify source or downgrade claim):")
        for f in findings:
            print(" -", f)
        return 1 if args.strict else 0
    print("PASS: no high-risk claim patterns detected without a source.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
