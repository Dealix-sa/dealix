#!/usr/bin/env python3
"""Verify the Security, Reliability, and Supply Chain OS is in place."""
from __future__ import annotations

from pathlib import Path
import sys

REQUIRED = [
    "SECURITY.md",
    "docs/security/SECURITY_BASELINE.md",
    "docs/security/SECURITY_RELIABILITY_SUPPLY_CHAIN_OS.md",
    "docs/security/DEPENDENCY_POLICY.md",
    "docs/security/INCIDENT_RESPONSE_SYSTEM.md",
    ".gitignore",
    ".env.example",
]

MIN_BYTES = 50


def main() -> int:
    failures: list[str] = []
    for rel in REQUIRED:
        path = Path(rel)
        if not path.exists():
            failures.append(f"Missing: {rel}")
            continue
        if path.is_file() and path.stat().st_size < MIN_BYTES:
            failures.append(f"Too short: {rel}")

    gitignore = Path(".gitignore")
    if gitignore.exists():
        text = gitignore.read_text(encoding="utf-8", errors="ignore")
        for marker in (".env", "secrets/"):
            if marker not in text:
                failures.append(f".gitignore missing pattern: {marker}")

    if failures:
        print("Security/Reliability/Supply-Chain OS verification FAILED:")
        for f in failures:
            print(" -", f)
        return 1
    print("PASS: Security/Reliability/Supply-Chain OS in place.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
