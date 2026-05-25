from __future__ import annotations

"""`python -m dealix_cli` entry point."""

import argparse
import sys
from pathlib import Path

# Make the repo root importable when invoked as a module from anywhere.
_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from dealix_cli import commands  # noqa: E402

_DEFAULT_PRIVATE_OPS = Path("../dealix-ops-private")

_SUBCOMMANDS = {
    "sprint": commands.cmd_sprint,
    "kit": commands.cmd_kit,
    "stage": commands.cmd_stage,
    "daily": commands.cmd_daily,
    "advance": commands.cmd_advance,
    "close-day": commands.cmd_close_day,
    "weekly": commands.cmd_weekly,
    "dashboard": commands.cmd_dashboard,
    "verify": commands.cmd_verify,
}


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="dealix",
        description="Dealix Company OS CLI",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    for name in _SUBCOMMANDS:
        sub = subparsers.add_parser(name, help=f"Run the '{name}' command")
        sub.add_argument(
            "--private-ops",
            type=Path,
            default=_DEFAULT_PRIVATE_OPS,
            help="Path to private ops directory (default: ../dealix-ops-private)",
        )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    handler = _SUBCOMMANDS[args.command]
    return handler(args.private_ops)


if __name__ == "__main__":
    raise SystemExit(main())
