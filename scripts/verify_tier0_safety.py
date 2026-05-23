"""Verify Tier-0 (Trust) safety contract.

Tier 0 is the smallest, hardest contract Dealix makes about what it can do
without a human in the loop. This verifier enforces it on the public repo.
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

TRUST_DOC = REPO_ROOT / "docs" / "trust" / "TRUST_COMMAND_CENTER.md"

REQUIRED_SECTION_HEADERS = (
    "## Green list",
    "## Red list",
    "## Approval log",
    "## Trust boundary terms",
)

# Patterns that must NEVER appear in the production codebase as enabled,
# unguarded behaviour. Each entry is checked across the modules below.
FORBIDDEN_PATTERNS = (
    "auto_send=True",
    "automated_send=True",
    "send_now()",
    "post_to_linkedin(",
    "send_whatsapp(",
)

SCAN_TARGETS = (
    REPO_ROOT / "dealix_cli",
    REPO_ROOT / "execution_engine",
)


def _check_trust_doc() -> list[str]:
    if not TRUST_DOC.exists():
        return [f"Missing trust doc: {TRUST_DOC.relative_to(REPO_ROOT)}"]
    body = TRUST_DOC.read_text(encoding="utf-8")
    missing = [h for h in REQUIRED_SECTION_HEADERS if h not in body]
    return [f"Trust doc missing section: {m}" for m in missing]


def _scan_for_forbidden() -> list[str]:
    failures: list[str] = []
    for target in SCAN_TARGETS:
        if not target.exists():
            continue
        for py in target.rglob("*.py"):
            text = py.read_text(encoding="utf-8", errors="replace")
            for pattern in FORBIDDEN_PATTERNS:
                if pattern in text:
                    failures.append(
                        f"Forbidden pattern `{pattern}` in {py.relative_to(REPO_ROOT)}"
                    )
    return failures


def main() -> None:
    print("== Tier 0 — Trust / Safety ==")
    failures = _check_trust_doc() + _scan_for_forbidden()
    if failures:
        print("FAIL:")
        for f in failures:
            print(f"- {f}")
        sys.exit(1)
    print("PASS: Tier 0 safety contract verified.")


if __name__ == "__main__":
    main()
