"""Scan content drafts for banned claims and sensitive hints before publishing.

Part of the Dealix Brand, Proof & Content Operating System v1.
See docs/content/BRAND_PROOF_CONTENT_OS.md.
"""

from __future__ import annotations

import argparse
from pathlib import Path

BANNED = [
    "guaranteed revenue",
    "guaranteed sales",
    "guaranteed meetings",
    "guaranteed replies",
    "fully compliant",
    "100% automated",
    "no-risk",
]

SENSITIVE_HINTS = [
    "@",
    "+966",
    "client secret",
    "api key",
    "private key",
]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True)
    args = parser.parse_args()
    path = Path(args.file)
    if not path.exists():
        print(f"Missing file: {path}")
        raise SystemExit(1)
    text = path.read_text(encoding="utf-8", errors="ignore")
    lower = text.lower()
    failures = []
    for term in BANNED:
        if term in lower:
            failures.append(f"Banned claim found: {term}")
    for hint in SENSITIVE_HINTS:
        if hint.lower() in lower:
            failures.append(f"Potential sensitive hint found: {hint}")
    if failures:
        print("Content claim review failed:")
        for failure in failures:
            print("-", failure)
        raise SystemExit(1)
    print("PASS: content claim review passed.")


if __name__ == "__main__":
    main()
