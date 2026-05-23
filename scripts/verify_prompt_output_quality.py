#!/usr/bin/env python3
"""C4 — Static scan of prompts/ and outputs/ for unsafe content.

Looks for banned commercial claims, leaked secret patterns, and auto-send
phrases used without the word "approval". Runs in both CI and local
modes (no private-ops dependency).
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from dealix.commercial_ops.stdio_utf8 import ensure_stdout_utf8  # noqa: E402

FAILURES: list[str] = []
WARNINGS: list[str] = []

BANNED_CLAIMS = (
    "guaranteed revenue",
    "guaranteed sales",
    "guaranteed roi",
    "نضمن",
    "مضمون",
)

SECRET_PATTERNS = (
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----"),
    re.compile(r"sk-[A-Za-z0-9]{20,}"),
    re.compile(r"xox[baprs]-[A-Za-z0-9-]{10,}"),
)

AUTO_SEND_PHRASES = (
    "sent automatically",
    "auto-sent",
    "تم الإرسال",
)

SCAN_DIRS = ("prompts", "outputs")
SCAN_EXTS = (".txt", ".md", ".json", ".yaml", ".yml")


def ok(msg: str) -> None:
    print(f"  ok: {msg}")


def fail(msg: str) -> None:
    FAILURES.append(msg)
    print(f"  FAIL: {msg}")


def warn(msg: str) -> None:
    WARNINGS.append(msg)
    print(f"  warn: {msg}")


def scan_file(path: Path) -> None:
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except Exception as e:
        warn(f"cannot read {path}: {e}")
        return
    lower = text.lower()
    rel = path.relative_to(REPO)
    for phrase in BANNED_CLAIMS:
        if phrase in lower:
            fail(f"{rel}: banned claim present: {phrase!r}")
    for pat in SECRET_PATTERNS:
        if pat.search(text):
            fail(f"{rel}: looks like a leaked secret ({pat.pattern})")
    for phrase in AUTO_SEND_PHRASES:
        if phrase in lower and "approval" not in lower:
            fail(f"{rel}: auto-send phrase {phrase!r} without 'approval'")


def main() -> int:
    ensure_stdout_utf8()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--private-ops", required=False, type=Path, default=None)
    parser.parse_args()

    print("# C4 — Prompt & Output Quality")

    files_scanned = 0
    for d in SCAN_DIRS:
        root = REPO / d
        if not root.exists():
            warn(f"{d}/ does not exist; nothing to scan")
            continue
        for path in root.rglob("*"):
            if path.is_file() and path.suffix.lower() in SCAN_EXTS:
                scan_file(path)
                files_scanned += 1
    ok(f"files scanned: {files_scanned}")

    ok_status = not FAILURES
    print(f"\nWARNINGS={len(WARNINGS)} FAILURES={len(FAILURES)}")
    print(f"VERIFY_PROMPT_OUTPUT_QUALITY_READY={'true' if ok_status else 'false'}")
    return 0 if ok_status else 1


if __name__ == "__main__":
    raise SystemExit(main())
