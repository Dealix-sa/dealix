"""Enforce that the trust-boundary phrasing in TRUST_COMMAND_CENTER.md is not
silently weakened or deleted.

Each REQUIRED_PHRASE must appear verbatim. The trust doc itself lists the
same set under `## Trust boundary terms — never weaken these`.
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
TRUST_DOC = REPO_ROOT / "docs" / "trust" / "TRUST_COMMAND_CENTER.md"

REQUIRED_PHRASES = (
    "No external send is automated.",
    "Every red-list action that *did* happen is appended to",
    "approval_evidence must be a path",
    "force-push, hard-reset, branch deletion on shared branches",
)


def main() -> None:
    print("== Trust Boundary Terms ==")
    if not TRUST_DOC.exists():
        print(f"FAIL: Missing {TRUST_DOC.relative_to(REPO_ROOT)}")
        sys.exit(1)
    body = TRUST_DOC.read_text(encoding="utf-8")
    failures = [f"Missing trust phrase: {p!r}" for p in REQUIRED_PHRASES if p not in body]
    if failures:
        print("FAIL:")
        for f in failures:
            print(f"- {f}")
        sys.exit(1)
    print(f"PASS: {len(REQUIRED_PHRASES)} trust-boundary phrases intact.")


if __name__ == "__main__":
    main()
