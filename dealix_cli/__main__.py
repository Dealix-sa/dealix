"""``python -m dealix_cli`` entry-point.

Supports two subcommands today:

    python -m dealix_cli people   --private-ops <path>
    python -m dealix_cli partners --private-ops <path>

Both commands are read-only and stdlib-only.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from . import commands


def _default_private_ops() -> str:
    """Use the repo working directory if no ``--private-ops`` flag is passed.

    The founder typically runs the CLI from the Dealix repo root, where the
    private-ops folders (``founder/``, ``people/``, ``partners/``) already live.
    """

    return str(Path.cwd())


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="dealix_cli",
        description="Dealix founder CLI — people & partner OS commands.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    for name, help_text in (
        ("people", "Review the people & delegation private-ops files."),
        ("partners", "Review the partner pipeline private-ops files."),
    ):
        sp = sub.add_parser(name, help=help_text)
        sp.add_argument(
            "--private-ops",
            default=_default_private_ops(),
            help="Path to the private-ops root (default: current working directory).",
        )

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "people":
        commands.people(args.private_ops)
    elif args.command == "partners":
        commands.partners(args.private_ops)
    else:  # pragma: no cover — argparse already enforces this
        parser.error(f"unknown command: {args.command}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
