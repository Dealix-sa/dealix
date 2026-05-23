"""Verify the weekly automation contract is documented and wired."""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
LEARNING_DOC = REPO_ROOT / "docs" / "learning" / "LEARNING_LOOP.md"

REQUIRED_SECTIONS = (
    "## Weekly review template",
    "## How it is enforced",
    "## Anti-patterns",
)

REQUIRED_TOKENS = (
    "weekly_reviews/<ISO_week>.md",
    "make weekly-close",
    "metrics_history/weekly_metrics.csv",
)


def main() -> None:
    print("== Weekly Automation ==")
    failures: list[str] = []
    if not LEARNING_DOC.exists():
        print(f"FAIL: Missing {LEARNING_DOC.relative_to(REPO_ROOT)}")
        sys.exit(1)
    body = LEARNING_DOC.read_text(encoding="utf-8")
    for section in REQUIRED_SECTIONS:
        if section not in body:
            failures.append(f"Section missing: {section}")
    for token in REQUIRED_TOKENS:
        if token not in body:
            failures.append(f"Token missing: {token}")

    # CLI wiring
    cli_main = REPO_ROOT / "dealix_cli" / "__main__.py"
    if cli_main.exists():
        text = cli_main.read_text(encoding="utf-8")
        if '"weekly-close"' not in text:
            failures.append("dealix_cli/__main__.py missing weekly-close subcommand")
    cli_cmds = REPO_ROOT / "dealix_cli" / "commands.py"
    if cli_cmds.exists():
        if "def weekly_close" not in cli_cmds.read_text(encoding="utf-8"):
            failures.append("dealix_cli/commands.py missing weekly_close()")

    if failures:
        print("FAIL:")
        for f in failures:
            print(f"- {f}")
        sys.exit(1)
    print("PASS: weekly automation documented and wired.")


if __name__ == "__main__":
    main()
