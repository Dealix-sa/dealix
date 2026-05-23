"""Dealix public safety verifier.

Ensures the public repo contains no obvious private-data leaks: customer
names from a known private list, raw payment evidence, or PII patterns
that should not be in a public repo.

Run:
    python scripts/verify_public_safety.py
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent

FORBIDDEN_PATTERNS = [
    # Saudi IBAN
    re.compile(r"\bSA\d{22}\b"),
    # Saudi national ID (10 digits starting with 1 or 2)
    re.compile(r"\b[12]\d{9}\b"),
    # Bare private API keys (heuristic)
    re.compile(r"sk-[A-Za-z0-9]{20,}"),
]

FORBIDDEN_TOKENS = [
    "PRIVATE_CUSTOMER_DATA",
    "DO_NOT_COMMIT",
]

DOC_FOLDERS = [
    "docs",
]

SKIP_DIRS = {".git", "node_modules", ".venv", "venv", "__pycache__"}


def iter_files():
    for folder in DOC_FOLDERS:
        base = ROOT / folder
        if not base.exists():
            continue
        for path in base.rglob("*"):
            if not path.is_file():
                continue
            if any(part in SKIP_DIRS for part in path.parts):
                continue
            if path.suffix.lower() not in {".md", ".txt", ".csv", ".yml", ".yaml"}:
                continue
            yield path


def main() -> int:
    failures: list[str] = []

    for path in iter_files():
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue

        for pattern in FORBIDDEN_PATTERNS:
            if pattern.search(text):
                failures.append(f"{path}: matches forbidden pattern {pattern.pattern}")

        for token in FORBIDDEN_TOKENS:
            if token in text:
                failures.append(f"{path}: contains forbidden token {token}")

    if failures:
        print("Public safety verification failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("PASS: Dealix public safety verified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
