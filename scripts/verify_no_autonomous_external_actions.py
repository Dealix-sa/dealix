"""Block code that takes autonomous external action without an approval gate.

This is a coarse, repo-wide grep for high-risk patterns. False positives are
expected — the verifier supports an ALLOWLIST below for documented exceptions.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# Files we scan. Limit to the new audit-system modules to keep this signal
# meaningful — the legacy codebase has its own checks.
SCAN_TARGETS = (
    REPO_ROOT / "dealix_cli",
    REPO_ROOT / "execution_engine",
    REPO_ROOT / "scripts" / "audit_dealix_implementation.py",
)

# Patterns that imply external action without a clear human gate.
RISKY_PATTERNS = (
    re.compile(r"\brequests\.post\("),
    re.compile(r"\brequests\.put\("),
    re.compile(r"\bhttpx\.post\("),
    re.compile(r"\bhttpx\.put\("),
    re.compile(r"\bsmtplib\."),
    re.compile(r"\btwilio\."),
    re.compile(r"\bsendgrid\."),
    re.compile(r"send_email\s*\("),
    re.compile(r"send_dm\s*\("),
)

# Lines/files exempted (only when they document an approval gate above the call).
ALLOWLIST_PATHS: tuple[str, ...] = ()


def _iter_py(target: Path):
    if target.is_file() and target.suffix == ".py":
        yield target
    elif target.is_dir():
        yield from target.rglob("*.py")


def main() -> None:
    print("== No Autonomous External Actions ==")
    failures: list[str] = []
    for target in SCAN_TARGETS:
        for py in _iter_py(target):
            rel = py.relative_to(REPO_ROOT).as_posix()
            if rel in ALLOWLIST_PATHS:
                continue
            text = py.read_text(encoding="utf-8", errors="replace")
            for pattern in RISKY_PATTERNS:
                for match in pattern.finditer(text):
                    line_no = text[: match.start()].count("\n") + 1
                    failures.append(
                        f"{rel}:{line_no}: risky external pattern `{match.group()}`"
                    )
    if failures:
        print("FAIL:")
        for f in failures:
            print(f"- {f}")
        sys.exit(1)
    print("PASS: no autonomous external-action calls found in audit modules.")


if __name__ == "__main__":
    main()
