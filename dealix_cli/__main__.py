"""Entry point for `python -m dealix_cli`."""

from __future__ import annotations

import argparse
import sys


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="dealix_cli",
        description=(
            "Dealix founder CLI. Boring on purpose. Never sends external "
            "messages, never charges customers."
        ),
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    daily_parser = subparsers.add_parser(
        "daily",
        help="Print the daily founder brief and write daily_brief.md.",
    )
    daily_parser.add_argument("--private-ops", required=True)

    stage_parser = subparsers.add_parser(
        "stage",
        help="Show the current stage, its exit criteria, and what is missing.",
    )
    stage_parser.add_argument("--private-ops", required=True)

    advance_parser = subparsers.add_parser(
        "advance",
        help="Advance to the next stage if and only if exit criteria are met.",
    )
    advance_parser.add_argument("--private-ops", required=True)

    subparsers.add_parser(
        "kit",
        help="Verify the Revenue Sprint Kit is complete.",
    )

    weekly_close_parser = subparsers.add_parser(
        "weekly-close",
        help="Write this week's weekly review template into the private repo.",
    )
    weekly_close_parser.add_argument("--private-ops", required=True)

    audit_parser = subparsers.add_parser(
        "audit",
        help="Run full public and private implementation audit.",
    )
    audit_parser.add_argument("--private-ops", required=True)

    init_parser = subparsers.add_parser(
        "init",
        help="Bootstrap a private-ops directory with the minimum file layout.",
    )
    init_parser.add_argument("--private-ops", required=True)

    return parser


def main(argv: list[str] | None = None) -> None:
    from dealix_cli import commands

    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.command == "daily":
        commands.daily(args.private_ops)
    elif args.command == "stage":
        commands.stage(args.private_ops)
    elif args.command == "advance":
        commands.advance(args.private_ops)
    elif args.command == "kit":
        commands.kit()
    elif args.command == "weekly-close":
        commands.weekly_close(args.private_ops)
    elif args.command == "audit":
        commands.audit(args.private_ops)
    elif args.command == "init":
        commands.init(args.private_ops)
    else:
        parser.print_help()
        sys.exit(2)


if __name__ == "__main__":
    main()
