"""Verify the dealix_cli package is importable and exposes the expected commands."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

EXPECTED_SUBCOMMANDS = (
    "daily",
    "stage",
    "advance",
    "kit",
    "weekly-close",
    "audit",
    "init",
)


def main() -> None:
    print("== Dealix CLI ==")
    failures: list[str] = []

    sys.path.insert(0, str(REPO_ROOT))
    try:
        import dealix_cli  # noqa: F401
        from dealix_cli import commands  # noqa: F401
        from dealix_cli.__main__ import _build_parser
    except Exception as exc:
        print(f"FAIL: import error: {exc}")
        sys.exit(1)

    parser = _build_parser()
    actions = {a.dest for a in parser._actions}  # noqa: SLF001
    if "command" not in actions:
        failures.append("CLI parser missing `command` subparser")

    result = subprocess.run(
        [sys.executable, "-m", "dealix_cli", "--help"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        failures.append(f"`python -m dealix_cli --help` failed: {result.stderr.strip()}")
    else:
        for sub in EXPECTED_SUBCOMMANDS:
            if sub not in result.stdout:
                failures.append(f"Subcommand `{sub}` not listed in help")

    for fn in EXPECTED_SUBCOMMANDS:
        attr_name = fn.replace("-", "_")
        if not hasattr(commands, attr_name):
            failures.append(f"commands.{attr_name} not implemented")

    if failures:
        print("FAIL:")
        for f in failures:
            print(f"- {f}")
        sys.exit(1)
    print(f"PASS: dealix_cli exposes {len(EXPECTED_SUBCOMMANDS)} commands.")


if __name__ == "__main__":
    main()
